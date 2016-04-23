import json
from api.models import db_session, engine, BaseModel, User, Semester, Course, CourseDependency, InstructorPool, StudentDemand, StudentRecord

user_roles = {
    '5': 'student',
    '1': 'TA',
    '3': 'professor',
    '4': 'administrator'
}

# Students
students = {}
for (student, record) in db_session.query(User, StudentRecord).join(StudentRecord).all():
    students[student.id] = {
        'seniority': record.seniority if record else 0,
        'current_gpa': record.current_gpa if record else 0
    }

# Semesters (should figure out better course timing approach)
semesters = {}
for semester in db_session.query(Semester).all():
    semesters[semester.id] = {
        'semester_name': semester.name
    }

# Courses
courses = {}
for course in db_session.query(Course).all():
    courses[course.id] = {
        'is_fall': course.is_fall,
        'is_spring': course.is_spring,
        'is_summer': course.is_summer
    }

# Prerequisites
course_dependencies = []
for cd in db_session.query(CourseDependency).all():
    course_dependencies.append({
        'first_course': cd.first_course,
        'second_course': cd.second_course
    })

# Student demand
student_demand = []
for sd in db_session.query(StudentDemand).all():
    student_demand.append({
        'student_id': sd.student_id,
        'course_id': sd.course_id,
        'semester_id': sd.semester_id
    })

# Instructor availability
instructor_availability = []
for ia in db_session.query(InstructorPool).all():
    instructor_availability.append({
        'instructor_id': ia.user_id,
        'course_id': ia.course_id,
        'semester_id': ia.semester_id,
        'instructor_role': ia.instructor_role
    })

with open('optimizer/test_data.json', 'w') as testfile:
    testfile.write(json.dumps({
        'students': students,
        'courses': courses,
        'semesters': semesters,
        'course_dependencies': course_dependencies,
        'student_demand': student_demand,
        'instructor_pool': instructor_availability
    }, indent=2))
