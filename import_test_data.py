import csv
import string
import hashlib
from api.models import db_session, engine, BaseModel, User, Semester, Course, CourseDependency, InstructorPool, StudentDemand, StudentRecord

user_roles = {
    '5': 'student',
    '1': 'TA',
    '3': 'professor',
    '4': 'administrator'
}

# Reset the database state (drop and create)
BaseModel.metadata.drop_all(bind=engine)
BaseModel.metadata.create_all(bind=engine)

# Create all users
with open('optimizer/resources/small/users_10.csv', 'rU') as user_file:
    user_reader = csv.DictReader(user_file)
    for u in user_reader:
        db_user = User(first_name=string.capitalize(u['first_name']),
                       last_name=string.capitalize(u['last_name']),
                       username=u['username'].lower(),
                       password_hash=hashlib.sha256(u['username'].lower().encode()).hexdigest(),
                       role=user_roles[u['role_ID']])

        db_session.add(db_user)

    db_session.commit()

# Create all semesters
with open('optimizer/resources/static/semesters.csv', 'rU') as semester_file:
    semester_reader = csv.DictReader(semester_file)
    for s in semester_reader:
        db_semester = Semester(name=s['semester_name'],
                               start_date=s['start_date'],
                               end_date=s['end_date'])

        db_session.add(db_semester)

    db_session.commit()

# Create courses
with open('optimizer/resources/static/courses.csv', 'rU') as course_file:
    course_reader = csv.DictReader(course_file)
    for c in course_reader:
        db_course = Course(course_name=c['course_name'],
                           course_number=c['course_number'],
                           is_fall=(c['fall_term'] is '1'),
                           is_spring=(c['spring_term'] is '1'),
                           is_summer=(c['summer_term'] is '1'),
                           availability_string=c['availability'])

        db_session.add(db_course)

    db_session.commit()

# Create prerequisites
with open('optimizer/resources/static/course_dependencies.csv', 'rU') as prereq_file:
    prereq_reader = csv.DictReader(prereq_file)
    for p in prereq_reader:
        db_prereq = CourseDependency(first_course=p['prereq_course_ID'],
                                     second_course=p['dependent_course_ID'])

        db_session.add(db_prereq)

    db_session.commit()

# Create instructor pool
with open('optimizer/resources/small/instructor_pool_10.csv', 'rU') as ipool_file:
    ipool_reader = csv.DictReader(ipool_file)
    for p in ipool_reader:
        db_ipool = InstructorPool(user_id=p['faculty_ID'],
                                  course_id=p['course_ID'],
                                  semester_id=p['semester_ID'],
                                  instructor_role=user_roles[p['role_ID']])

        db_session.add(db_ipool)

    db_session.commit()

# Create course demand
with open('optimizer/resources/small/student_demand_10.csv', 'rU') as demand_file:
    demand_reader = csv.DictReader(demand_file)
    for d in demand_reader:
        db_demand = StudentDemand(student_id=int(d['student_ID']),
                                  course_id=int(d['course_ID']),
                                  semester_id=int(d['semester_ID']),
                                  is_current=True)

        db_session.add(db_demand)

    db_session.commit()

# Create student records
with open('optimizer/resources/small/student_records_10.csv', 'rU') as record_file:
    record_reader = csv.DictReader(record_file)
    for r in record_reader:
        db_record = StudentRecord(user_id=int(r['user_ID']),
                                  seniority=int(r['seniority']),
                                  current_gpa=float(r['GPA']))

        db_session.add(db_record)

    db_session.commit()