from gurobipy import Model, LinExpr, GRB, GurobiError

from loader import SolverData

s = SolverData('resources/static', 'resources/large/large10000.csv')

m = Model('mip1.log')

# Create model variables
max_class_size = m.addVar(lb=0.0, ub=GRB.INFINITY, vtype=GRB.INTEGER, name='max_class_size')
solution_matrix = {(st, c, se): m.addVar(vtype=GRB.BINARY, name='{}_{}_{}'.format(st, c, se))
                   for st in s.student_ids for c in s.course_ids for se in s.semester_ids}

m.update()

# Constraint #1: Class availability and size
for course in s.course_ids:
    for semester in s.semester_ids:
        class_size_expr = LinExpr()

        for student in s.student_ids:
            class_size_expr.add(solution_matrix[student, course, semester])

        if not s.is_course_offered(course, semester):
            m.addConstr(class_size_expr, GRB.EQUAL, 0, 'max_size_{}_{}'.format(course, semester))
        else:
            m.addConstr(class_size_expr, GRB.LESS_EQUAL, max_class_size, 'max_size_{}_{}'.format(course, semester))

# Constraint #2: No classes with pre-requisites in first semester
for student in s.student_ids:
    for prereq in s.dependencies:
        first_semester_prereq_expr = LinExpr()
        first_semester_prereq_expr.add(solution_matrix[student, prereq[1], 1])
        m.addConstr(first_semester_prereq_expr, GRB.EQUAL, 0, 'fs_prereq_{}_{}'.format(student, prereq))

# Constraint #3: Max course load per student per semester
for student in s.student_ids:
    for semester in s.semester_ids:
        max_load_expr = LinExpr()

        for course in s.course_ids:
            max_load_expr.add(solution_matrix[student, course, semester])

        m.addConstr(max_load_expr, GRB.LESS_EQUAL, 2, 'max_load_{}_{}'.format(student, semester))

# Constraint #4: Course demand for student
for student in s.student_ids:
    for course in s.course_ids:

        if any([s.student_demand[student, course, semester] for semester in s.semester_ids]):
            demand_expr = LinExpr()
            for semester in s.semester_ids:
                demand_expr.add(solution_matrix[student, course, semester])

            m.addConstr(demand_expr, GRB.EQUAL, 1, 'student_demand_{}_{}'.format(student, course))

# Constraint #5: Prerequisite courses
for student in s.student_ids:
    for prereq in s.dependencies:
        prereq_expr = LinExpr()

        for semester in s.semester_ids[:-1]:
            prereq_expr.add(solution_matrix[student, prereq[0], semester], 1.0)
            prereq_expr.add(solution_matrix[student, prereq[1], semester + 1], -1.0)

        m.addConstr(prereq_expr, GRB.GREATER_EQUAL, 0, 'prereq_{}_{}_{}'.format(student, prereq[0], prereq[1]))

# Create the objective
objective_expr = LinExpr()
objective_expr.add(max_class_size)
m.setObjective(objective_expr, GRB.MINIMIZE)

m.optimize()

# Print objective value
print(m.objVal)

# Print debug solution
course_semester_totals = {}
for course in s.course_ids:
    schedule = 'C{:2d}  '.format(course)
    for semester in s.semester_ids:
        schedule += '{:3d}  '.format(int(sum([solution_matrix[student, course, semester].x
                                    for student in s.student_ids])))

    print(schedule)
