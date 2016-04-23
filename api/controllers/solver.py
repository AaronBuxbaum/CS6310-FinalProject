import requests
from flask import Blueprint, request, jsonify, g
from sqlalchemy import desc

from api.utils import requires_authentication
from api.models import db_session, OptimizationRun, User, Semester, Course, CourseDependency, InstructorPool, InstructorAssignment, StudentDemand, StudentRecord, StudentAssignment

user_roles = {
    '5': 'student',
    '1': 'TA',
    '3': 'professor',
    '4': 'administrator'
}

solver_bp = Blueprint('solver', __name__, url_prefix='/api/solver')

def get_solver_context():
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
    for sd in db_session.query(StudentDemand).filter(StudentDemand.is_current == True).all():
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

    return {
            'students': students,
            'courses': courses,
            'semesters': semesters,
            'course_dependencies': course_dependencies,
            'student_demand': student_demand,
            'instructor_pool': instructor_availability
        }

@solver_bp.route('/', methods=['POST'])
@requires_authentication()
def solve():
    r = requests.post('http://ec2-54-86-66-135.compute-1.amazonaws.com:8080/solve', json=get_solver_context())
    if r.status_code != 200 or 'error' in r.json():
        return jsonify(error=True)

    # Create this run ID
    o = OptimizationRun(created_by=g.user_id)
    db_session.add(o)
    db_session.flush()

    # Configure everything
    data = r.json()
    for a in data['assignments']:
        s = StudentAssignment(student_id=a['student'],
                              semester_id=a['semester'],
                              course_id=a['course'],
                              run_id=o.id)

        db_session.add(s)

    for a in data['instructors']:
        s = InstructorAssignment(instructor_id=a['instructor_id'],
                              semester_id=a['semester_id'],
                              course_id=a['course_id'],
                              run_id=o.id)

        db_session.add(s)

    db_session.commit()

    return jsonify(updated=True, run_id=o.id)
