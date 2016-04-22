import os
import re
import arrow
import time

from sqlalchemy import create_engine, Column, DateTime, Integer, String, Enum, Date, ForeignKey, Boolean, Float
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declared_attr, declarative_base

engine = create_engine(os.getenv('DATABASE_URL', None))
db_session = scoped_session(sessionmaker(bind=engine))

class Base(object):
    """Base class for all models, includes table naming conventions and basic columns."""

    @declared_attr
    def __tablename__(cls):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', cls.__name__)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    id = Column(Integer, primary_key=True)

BaseModel = declarative_base(cls=Base)
BaseModel.query = db_session.query_property()

class User(BaseModel):
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum('student', 'professor', 'TA', 'administrator', name='user_enum'))

class LoginRecord(BaseModel):
    user_id = Column(Integer, ForeignKey('user.id', ondelete='cascade'), nullable=False)
    access_time = Column(DateTime, nullable=False)

class Course(BaseModel):
    course_name = Column(String, nullable=False)
    course_number = Column(String, nullable=False)

    is_fall = Column(Boolean, default=False)
    is_spring = Column(Boolean, default=False)
    is_summer = Column(Boolean, default=False)
    availability_string = Column(String, nullable=False)

class CourseDependency(BaseModel):
    first_course = Column(Integer, ForeignKey('course.id', ondelete='cascade'), nullable=False)
    second_course = Column(Integer, ForeignKey('course.id', ondelete='cascade'), nullable=False)

class Semester(BaseModel):
    name = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

class InstructorPool(BaseModel):
    user_id = Column(Integer, ForeignKey('user.id', ondelete='cascade'), nullable=False)
    course_id = Column(Integer, ForeignKey('course.id', ondelete='cascade'), nullable=False)
    semester_id = Column(Integer, ForeignKey('semester.id', ondelete='cascade'), nullable=False)
    instructor_role = Column(Enum('professor', 'TA', name='instructor_enum'), nullable=False)

class StudentRecord(BaseModel):
    user_id = Column(Integer, ForeignKey('user.id', ondelete='cascade'), nullable=False)
    seniority = Column(Integer, nullable=False)
    current_gpa = Column(Float, nullable=False)

class OptimizationRun(BaseModel):
    created_by = Column(Integer, ForeignKey('user.id', ondelete='cascade'), nullable=False)
    created_at = Column(DateTime, default=lambda: arrow.now().datetime)
    is_shadow = Column(Boolean, default=False)

class StudentDemand(BaseModel):
    student_id = Column(Integer, ForeignKey('user.id', ondelete='cascade'), nullable=False)
    course_id = Column(Integer, ForeignKey('course.id', ondelete='cascade'), nullable=False)
    semester_id = Column(Integer, ForeignKey('semester.id', ondelete='cascade'), nullable=False)
    created_at = Column(DateTime, default=lambda: arrow.now().datetime)
    is_current = Column(Boolean, default=False)

class StudentAssignment(BaseModel):
    student_id = Column(Integer, ForeignKey('user.id', ondelete='cascade'), nullable=False)
    course_id = Column(Integer, ForeignKey('course.id', ondelete='cascade'), nullable=False)
    semester_id = Column(Integer, ForeignKey('semester.id', ondelete='cascade'), nullable=False)
    run_id = Column(Integer, ForeignKey('optimization_run.id', ondelete='cascade'), nullable=False)

class InstructorAssignment(BaseModel):
    instructor_id = Column(Integer, ForeignKey('user.id', ondelete='cascade'), nullable=False)
    course_id = Column(Integer, ForeignKey('course.id', ondelete='cascade'), nullable=False)
    semester_id = Column(Integer, ForeignKey('semester.id', ondelete='cascade'), nullable=False)
    run_id = Column(Integer, ForeignKey('optimization_run.id', ondelete='cascade'), nullable=False)

def init_db():
    BaseModel.metadata.create_all(bind=engine)