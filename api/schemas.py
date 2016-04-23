from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    role = fields.Str(required=True)

class CourseSchema(Schema):
    id = fields.Int(dump_only=True)
    course_name = fields.Str(required=True)
    course_number = fields.Str(required=True)

    is_fall = fields.Boolean()
    is_spring = fields.Boolean()
    is_summer = fields.Boolean()
    availability_string = fields.Str(required=True)

class SemesterSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)

class DemandSchema(Schema):
    course = fields.Nested(CourseSchema, required=True)
    semester = fields.Nested(SemesterSchema, required=True)

class AggregateDemandSchema(Schema):
    course = fields.Nested(CourseSchema, required=True)
    semester = fields.Nested(SemesterSchema, required=True)
    demand = fields.Int()

class ScheduleSchema(Schema):
    course = fields.Nested(CourseSchema, required=True)
    semester = fields.Nested(SemesterSchema, required=True)
    instructors = fields.Nested(UserSchema, many=True)

class InstructorPoolSchema(Schema):
    course = fields.Nested(CourseSchema, required=True)
    semester = fields.Nested(SemesterSchema, required=True)
    instructor = fields.Nested(UserSchema, required=True)

class ScheduleDetailSchema(Schema):
    course = fields.Nested(CourseSchema, required=True)
    semester = fields.Nested(SemesterSchema, required=True)
    instructors = fields.Nested(UserSchema, many=True)
    students = fields.Nested(UserSchema, required=True, many=True)