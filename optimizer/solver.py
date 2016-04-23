import sys
import json
import random
from collections import defaultdict
from gurobipy import Model, LinExpr, GRB, GurobiError

class Solver(object):
    """Encapsulation for the Gurobi solver."""

    def __init__(self, json_data):
        self.m = Model('mip1.log')
        self.solution_matrix = None
        
        # Load from JSON
        self.all_data = json_data
        self.student_ids = [int(k) for k in json_data['students'].keys()]
        self.course_ids = [int(k) for k in json_data['courses'].keys()]
        self.semester_ids = [int(k) for k in json_data['semesters'].keys()]
        self.dependencies = [(d['first_course'], d['second_course']) for d in json_data['course_dependencies']]

        self.student_demand = defaultdict(lambda: False)
        for sd in json_data['student_demand']:
            self.student_demand[sd['student_id'], sd['course_id'], sd['semester_id']] = True

        self.instructor_availability = defaultdict(lambda: False)
        for ia in json_data['instructor_pool']:
            self.instructor_availability[ia['instructor_id'], ia['course_id'], ia['semester_id']] = True

        self.instructor_ids = [s['instructor_id'] for s in json_data['instructor_pool']]

    def construct_model(self):
        self.m = Model('mip1.log')

        # Create model variables
        self.solution_matrix = {(st, c, se): self.m.addVar(vtype=GRB.BINARY, name='{}_{}_{}'.format(st, c, se))
                           for st in self.student_ids for c in self.course_ids for se in self.semester_ids}

        self.m.update()

        # Constraint #1: Class availability and size
        for course in self.course_ids:
            for semester in self.semester_ids:
                class_size_expr = LinExpr()

                for student in self.student_ids:
                    class_size_expr.add(self.solution_matrix[student, course, semester])

                if not self.is_course_offered(course, semester):
                    self.m.addConstr(class_size_expr, GRB.EQUAL, 0, 'max_size_{}_{}'.format(course, semester))
                else:
                    self.m.addConstr(class_size_expr, GRB.LESS_EQUAL, 300, 'max_size_{}_{}'.format(course, semester))

        # Constraint #2: No classes with pre-requisites in first semester
        for student in self.student_ids:
            for prereq in self.dependencies:
                first_semester_prereq_expr = LinExpr()
                first_semester_prereq_expr.add(self.solution_matrix[student, prereq[1], 1])
                self.m.addConstr(first_semester_prereq_expr, GRB.EQUAL, 0, 'fs_prereq_{}_{}'.format(student, prereq))

        # Constraint #3: Max course load per student per semester
        for student in self.student_ids:
            for semester in self.semester_ids:
                max_load_expr = LinExpr()

                for course in self.course_ids:
                    max_load_expr.add(self.solution_matrix[student, course, semester])

                self.m.addConstr(max_load_expr, GRB.LESS_EQUAL, 2, 'max_load_{}_{}'.format(student, semester))

        # Constraint #4: Course demand for student
        for student in self.student_ids:
            for course in self.course_ids:
                if any([self.student_demand[student, course, semester] for semester in self.semester_ids]):
                    demand_expr = LinExpr()
                    for semester in self.semester_ids:
                        demand_expr.add(self.solution_matrix[student, course, semester])

                    self.m.addConstr(demand_expr, GRB.EQUAL, 1, 'student_demand_{}_{}'.format(student, course))

        # Constraint #5: Prerequisite courses
        for student in self.student_ids:
            for prereq in self.dependencies:
                prereq_expr = LinExpr()

                for semester in sorted(self.semester_ids)[:-1]:
                    prereq_expr.add(self.solution_matrix[student, prereq[0], semester], 1.0)
                    prereq_expr.add(self.solution_matrix[student, prereq[1], semester + 1], -1.0)

                self.m.addConstr(prereq_expr, GRB.GREATER_EQUAL, 0, 'prereq_{}_{}_{}'.format(student, prereq[0], prereq[1]))

        # Create the objective
        objective_expr = LinExpr()
        for student in self.student_ids:
            for course in self.course_ids:
                for semester in self.semester_ids:
                    if self.student_demand[student, course, semester]:
                        objective_expr.add(1 - self.solution_matrix[student, course, semester])

        self.m.setObjective(objective_expr, GRB.MINIMIZE)

    def optimize_model(self):
        self.m.optimize()
        return self.m.objVal

    def print_debug_matrix(self):
        for course in self.course_ids:
            schedule = 'C{:2d}  '.format(course)
            for semester in self.semester_ids:
                schedule += '{:3d}  '.format(int(sum([self.solution_matrix[student, course, semester].x
                                            for student in self.student_ids])))

            print(schedule)

    def get_student_assignments(self):
        assignments = []
        for (student, course, semester) in self.solution_matrix.keys():
            if self.solution_matrix[student, course, semester].x == 1:
                assignments.append(dict(student=student, course=course, semester=semester))

        return assignments

    def get_instructor_assignment(self):
        instructors_list = {(c, s): [] for (i, c, s) in self.instructor_availability.keys()}
        for (i, c, s) in self.instructor_availability.keys():
            instructors_list[c, s].append(i)

        student_counts = {(c, s): 0 for (st, c, s) in self.solution_matrix.keys()}
        for (student, course, semester) in self.solution_matrix.keys():
            if self.solution_matrix[student, course, semester].x == 1:
                student_counts[course, semester] += 1

        instructor_assign = []
        for (c, s) in student_counts.keys():
            if student_counts[c, s] > 0:
                if (c, s) in instructors_list.keys():
                    instructor_assign.append(dict(instructor_id=random.choice(instructors_list[c, s]), course_id=c, semester_id=s))


        return instructor_assign

    def is_course_offered(self, course_id, semester_id):
        c = self.all_data['courses'][str(course_id)]
        s = self.all_data['semesters'][str(semester_id)]['semester_name'].lower()

        return ('fall' in s and c['is_fall']) or ('summer' in s and c['is_summer']) or ('spring' in s and c['is_spring'])


if __name__ == '__main__':
    with open(sys.argv[1], 'rU') as json_file:
        solver = Solver(json.load(json_file))
        solver.construct_model()
        print(solver.optimize_model())
        solver.print_debug_matrix()
        print(solver.get_instructor_assignment())
