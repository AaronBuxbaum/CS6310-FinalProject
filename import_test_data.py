import csv
import sys
import random
import hashlib
from api.models import db_session, engine, BaseModel, User, Semester, Course, CourseDependency, InstructorPool, StudentDemand, StudentRecord

user_roles = {
    '5': 'student',
    '1': 'TA',
    '3': 'professor',
    '4': 'administrator'
}

first_names = ['Denice', 'Sybil', 'Barb', 'Shelly', 'Odis', 'Niki', 'Lyndsay', 'Sharmaine', 'Fatima', 'Lane', 'Reanna', 'Myrtice', 'Shirly', 'Chanda', 'Earlean', 'Marica', 'Queenie', 'Edison', 'Cristopher', 'Normand', 'Victor', 'Myrtis', 'Stepanie', 'Arica', 'Freddie', 'Rolf', 'Barbie', 'Wilburn', 'Emerald', 'Irina', 'Dana', 'Genevieve', 'Kaila', 'Clarisa', 'Shayne', 'Doria', 'Shameka', 'Bridgett', 'Jerrie', 'Sylvie', 'Lola', 'Casimira', 'Pamella', 'Melvin', 'Ramona', 'Arianna', 'Mina', 'Lai', 'Ladonna', 'Georgianna']
last_names = ['Kush', 'Stier', 'Marguez', 'Knaub', 'Hasson', 'Gambrell', 'Speciale', 'Israel', 'Burgdorf', 'Prout', 'Heinze', 'Bruen', 'Luttrell', 'Colyer', 'Lafontaine', 'Franco', 'Ager', 'Abernathy', 'Kolman', 'Marshburn', 'Gabrielli', 'Nath', 'Santoyo', 'Helle', 'Phelan', 'Kunze', 'Mucha', 'Vaughan', 'Hurwitz', 'Livengood', 'Kline', 'Degraffenreid', 'Denniston', 'Kuebler', 'Rote', 'Volkmann', 'Shimizu', 'Skiles', 'Alberti', 'Dejulio', 'Derouen', 'Priester', 'Hedman', 'Osgood', 'Zermeno', 'Ansley', 'Taff', 'Valera', 'Geisel', 'Kottwitz']

# Reset the database state (drop and create)
def reset_database():
    BaseModel.metadata.drop_all(bind=engine)
    BaseModel.metadata.create_all(bind=engine)

class BaseData(object):
    def __init__(self):
        self.semesters = {}
        self.courses = {}
        self.prerequisites_reversed = {}

    def create_semesters(self):
        with open('optimizer/resources/static/semesters.csv', 'rU') as semester_file:
            semester_reader = csv.DictReader(semester_file)
            for s in semester_reader:
                db_semester = Semester(name=s['semester_name'],
                                       start_date=s['start_date'],
                                       end_date=s['end_date'])

                db_session.add(db_semester)
                db_session.flush()
                self.semesters[db_semester.id] = db_semester.name

            db_session.commit()

    def create_courses(self):
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
                db_session.flush()
                self.courses[db_course.id] = dict(is_fall=db_course.is_fall, is_spring=db_course.is_spring,
                                                    is_summer=db_course.is_summer)

            db_session.commit()

    def create_prerequisites(self):
        with open('optimizer/resources/static/course_dependencies.csv', 'rU') as prereq_file:
            prereq_reader = csv.DictReader(prereq_file)
            for p in prereq_reader:
                db_prereq = CourseDependency(first_course=p['prereq_course_ID'],
                                             second_course=p['dependent_course_ID'])

                db_session.add(db_prereq)
                db_session.flush()
                self.prerequisites_reversed[db_prereq.second_course] = db_prereq.first_course

            db_session.commit()

    def create_admin_user(self):
        admin_user = User(first_name='Awesome',
                          last_name='Administrator',
                          username='aadmin3',
                          password_hash=hashlib.sha256('aadmin3'.lower().encode()).hexdigest(),
                          role='administrator')

        db_session.add(admin_user)
        db_session.commit()

class SampleData(object):
    def create_users(self):
        with open('optimizer/resources/small/users_10.csv', 'rU') as user_file:
            user_reader = csv.DictReader(user_file)
            for u in user_reader:
                db_user = User(first_name=u['first_name'].capitalize(),
                               last_name=u['last_name'].capitalize(),
                               username=u['username'].lower(),
                               password_hash=hashlib.sha256(u['username'].lower().encode()).hexdigest(),
                               role=user_roles[u['role_ID']])

                db_session.add(db_user)

            db_session.commit()

    def create_instructor_pool(self):
        with open('optimizer/resources/small/instructor_pool_10.csv', 'rU') as ipool_file:
            ipool_reader = csv.DictReader(ipool_file)
            for p in ipool_reader:
                db_ipool = InstructorPool(user_id=p['faculty_ID'],
                                          course_id=p['course_ID'],
                                          semester_id=p['semester_ID'],
                                          instructor_role=user_roles[p['role_ID']])

                db_session.add(db_ipool)

            db_session.commit()

    def create_student_demand(self):
        with open('optimizer/resources/small/student_demand_10.csv', 'rU') as demand_file:
            demand_reader = csv.DictReader(demand_file)
            for d in demand_reader:
                db_demand = StudentDemand(student_id=int(d['student_ID']),
                                          course_id=int(d['course_ID']),
                                          semester_id=int(d['semester_ID']),
                                          is_current=True)

                db_session.add(db_demand)

            db_session.commit()

    def create_student_records(self):
        with open('optimizer/resources/small/student_records_10.csv', 'rU') as record_file:
            record_reader = csv.DictReader(record_file)
            for r in record_reader:
                db_record = StudentRecord(user_id=int(r['user_ID']),
                                          seniority=int(r['seniority']),
                                          current_gpa=float(r['GPA']))

                db_session.add(db_record)

            db_session.commit()

class RandomData(object):

    def __init__(self, semester_array, course_array, prereq_array, num_students, num_instructors):
        self.semesters = semester_array
        self.courses = course_array
        self.prereq_reversed = prereq_array
        self.num_students = num_students
        self.num_instructors = num_instructors

        self.student_ids = []
        self.instructor_ids = []

    def create_users(self):
        for u in range(self.num_students):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            username = '{}{}{:03d}'.format(first_name[0], last_name[1:], random.randint(1, 1000)).lower()

            db_user = User(first_name=first_name.capitalize(),
                           last_name=last_name.capitalize(),
                           username=username,
                           password_hash=hashlib.sha256(username.encode()).hexdigest(),
                           role='student')

            db_session.add(db_user)
            db_session.flush()
            self.student_ids.append(db_user.id)

        for u in range(self.num_instructors):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            username = '{}{}{:03d}'.format(first_name[0], last_name[1:], random.randint(1, 1000)).lower()

            db_user = User(first_name=first_name.capitalize(),
                           last_name=last_name.capitalize(),
                           username=username,
                           password_hash=hashlib.sha256(username.encode()).hexdigest(),
                           role='TA')

            db_session.add(db_user)
            db_session.flush()
            self.instructor_ids.append(db_user.id)

        db_session.commit()

    def create_instructor_pool(self):
        for _ in range(self.num_instructors * 2):
            db_ipool = InstructorPool(user_id=random.choice(self.instructor_ids),
                                      course_id=random.choice(list(self.courses.keys())),
                                      semester_id=random.choice(list(self.semesters.keys())),
                                      instructor_role='TA')

            db_session.add(db_ipool)

        db_session.commit()

    def create_student_demand(self):
        student_schedule = {}
        for student_id in self.student_ids:
            student_schedule = []
            for semester_id in self.semesters.keys():
                if len(student_schedule) >= 11:
                    continue

                for _ in range(random.choice([1, 1, 1, 2])):
                    course_id = None
                    while(True):
                        proposed_course = random.choice(list(self.courses.keys()))
                        if proposed_course in student_schedule:
                            continue
                        if proposed_course in self.prereq_reversed.keys() and self.prereq_reversed[proposed_course] not in student_schedule:
                            continue

                        course_id = proposed_course
                        break

                    db_demand = StudentDemand(student_id=student_id,
                                              course_id=course_id,
                                              semester_id=semester_id,
                                              is_current=True)

                    db_session.add(db_demand)
                    db_session.flush()
                    student_schedule.append(course_id)

            db_session.commit()

    def create_student_records(self):
        for s in self.student_ids:
            db_record = StudentRecord(user_id=s,
                                      seniority=random.randint(1, 7),
                                      current_gpa=float(random.randint(1, 8)/8))

            db_session.add(db_record)

        db_session.commit()

if __name__ == '__main__':
    reset_database()

    # Base data
    base = BaseData()
    base.create_courses()
    base.create_semesters()
    base.create_prerequisites()
    base.create_admin_user()

    if len(sys.argv) > 1:
        if sys.argv[1] == 'sample':
            sample = SampleData()
            sample.create_users()
            sample.create_instructor_pool()
            sample.create_student_demand()
            sample.create_student_records()

        if sys.argv[1] == 'random':
            student_count = int(sys.argv[2])
            instructor_count = int(sys.argv[3])

            rand = RandomData(base.semesters, base.courses, base.prerequisites_reversed, student_count, instructor_count)
            rand.create_users()
            rand.create_instructor_pool()
            rand.create_student_demand()
            rand.create_student_records()
