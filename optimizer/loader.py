import csv
from collections import defaultdict

class SolverData(object):
    """Quick class to encapsulate all data needed to solve a problem."""

    def __init__(self, static_path, student_path):
        self._load_courses(static_path + '/courses.csv')
        self._load_semesters(static_path + '/semesters.csv')
        self._load_dependencies(static_path + '/course_dependencies.csv')
        self._load_student_demand(student_path)

    def _load_dependencies(self, dependencies_path):
        dependencies = []
        with open(dependencies_path, 'rU') as dependencies_file:
            for r in csv.DictReader(dependencies_file):
                dependencies.append((int(r['prereq_course_ID']), int(r['dependent_course_ID'])))

        self.dependencies = dependencies

    def _load_courses(self, courses_path):
        courses = {}
        with open(courses_path, 'rU') as courses_file:
            for r in csv.DictReader(courses_file):
                courses[int(r['course_ID'])] = {
                    'course_name': r['course_name'],
                    'course_number': r['course_number'],
                    'is_fall':bool(int(r['fall_term'])),
                    'is_spring': bool(int(r['spring_term'])),
                    'is_summer': bool(int(r['summer_term'])),
                    'availability': r['availability']
                }

        self.course_ids = courses.keys()
        self.courses = courses

    def _load_semesters(self, semester_path):
        semesters = {}
        with open(semester_path, 'rU') as semester_file:
            for r in csv.DictReader(semester_file):
                semesters[int(r['semester_ID'])] = {
                    'semester_name': r['semester_name'],
                    'start_date':r['start_date'],
                    'end_date': r['end_date']
                }

        self.semester_ids = semesters.keys()
        self.semesters_data = semesters

    def _load_student_demand(self, student_path):
        max_student = 0
        student_demand = defaultdict(lambda: False)
        student_ids = []
        with open(student_path, 'rU') as student_file:
            for r in csv.DictReader(student_file):
                student_id = int(r['student_ID'])
                semester_id = int(r['semester_ID'])
                course_id = int(r['course_ID'])
                max_student = max(max_student, student_id)

                # Hack-y override for demand data
                if semester_id == 0:
                    semester_id = 1

                student_demand[student_id, course_id, semester_id] = True
                student_ids.append(student_id)

        self.student_demand = student_demand
        self.student_ids = list(set(student_ids))

    def is_course_offered(self, course, semester):
        c = self.courses[course]
        return [c['is_fall'], c['is_spring'], c['is_summer']][(semester - 1) % 3]