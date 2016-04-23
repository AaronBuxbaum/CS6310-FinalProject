from flask import Blueprint, request, jsonify, g
from sqlalchemy import func

from api.utils import requires_authentication
from api.models import db_session, InstructorPool
from api.schemas import InstructorPoolSchema

instructor_bp = Blueprint('instructor', __name__, url_prefix='/api/instructor')

@instructor_bp.route('/', methods=['GET'])
@requires_authentication('administrator')
def get_instructor_pool():
    instructor_pool = []
    for c in InstructorPool.query.all():
        instructor_pool.append({
            'course': c.course,
            'semester': c.semester,
            'instructor': c.instructor
        })

    return jsonify(demand=InstructorPoolSchema().dump(instructor_pool, many=True).data)

@instructor_bp.route('/', methods=['POST'])
@requires_authentication()
def create_demand():
    j = request.get_json()

    if not InstructorPool.query.filter_by(user_id=j['instructor_id'], semester_id=j['semester_id'],
                                          course_id=j['course_id']).first():
        db_session.add(InstructorPool(user_id=j['instructor_id'],
                      semester_id=j['semester_id'],
                      course_id=j['course_id']))
        db_session.commit()

    return get_instructor_pool()

@instructor_bp.route('/', methods=['DELETE'])
@requires_authentication()
def delete_demand():
    s = InstructorPool.query.filter_by(student_id=int(request.args['instructor_id']),
                                       semester_id=int(request.args['semester_id']),
                                       course_id=int(request.args['course_id'])).first()

    db_session.delete(s)
    db_session.commit()

    return get_instructor_pool()