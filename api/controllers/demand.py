from flask import Blueprint, request, jsonify, g
from sqlalchemy import func

from api.utils import requires_authentication
from api.models import db_session, StudentDemand, Course, Semester
from api.schemas import DemandSchema, AggregateDemandSchema

demand_bp = Blueprint('demand', __name__, url_prefix='/api/demand')

@demand_bp.route('/', methods=['GET'])
@demand_bp.route('/<user_id>', methods=['GET'])
@requires_authentication()
def get_user_demand(user_id=None):
    if g.user_role == 'administrator':
        id_to_check = int(user_id or g.user_id)
    else:
        id_to_check = g.user_id

    course_demand = []
    for c in StudentDemand.query.filter(StudentDemand.student_id == id_to_check).all():
        course_demand.append({
            'course': c.course,
            'semester': c.semester,
            'instructors': None
        })

    return jsonify(demand=DemandSchema().dump(course_demand, many=True).data)

@demand_bp.route('/aggregate', methods=['GET'])
@requires_authentication()
def get_aggregate_demand():
    course_demand = []
    aggregate_sub = db_session.query(StudentDemand.course_id, StudentDemand.semester_id, func.count(StudentDemand.id)
                                     .label('student_count')).group_by(StudentDemand.course_id)\
                                     .group_by(StudentDemand.semester_id).subquery()

    merged_query = db_session.query(Course, Semester, aggregate_sub.c.student_count).select_from(aggregate_sub)\
        .join(Course, Course.id == aggregate_sub.c.course_id).join(Semester, Semester.id == aggregate_sub.c.semester_id)\
        .all()

    for (course, semester, count) in merged_query:
        course_demand.append({
            'course': course,
            'semester': semester,
            'demand': count
        })

    return jsonify(demand=AggregateDemandSchema().dump(course_demand, many=True).data)

@demand_bp.route('/', methods=['POST'])
@requires_authentication()
def create_demand():
    j = request.get_json()

    if not StudentDemand.query.filter_by(student_id=g.user_id, semester_id=j['semester_id'], course_id=j['course_id']).first():
        db_session.add(StudentDemand(student_id=g.user_id,
                      semester_id=j['semester_id'],
                      course_id=j['course_id']))
        db_session.commit()

    return get_user_demand()

@demand_bp.route('/', methods=['DELETE'])
@requires_authentication()
def delete_demand():
    s = StudentDemand.query.filter_by(student_id=g.user_id, semester_id=int(request.args['semester_id']),
                                      course_id=int(request.args['course_id'])).first()

    db_session.delete(s)
    db_session.commit()

    return get_user_demand()