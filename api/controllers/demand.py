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
    for c in StudentDemand.query.filter(StudentDemand.student_id == id_to_check).filter(StudentDemand.is_current == True).all():
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
                                     .label('student_count')).filter(StudentDemand.is_current == True).group_by(StudentDemand.course_id)\
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

    StudentDemand.query.filter(StudentDemand.student_id == g.user_id).update({StudentDemand.is_current: False})

    for s in j['courses']:
        db_session.add(StudentDemand(student_id=g.user_id,
                      semester_id=s['semester_id'],
                      course_id=s['course_id'],
                      is_current=True))

    db_session.commit()

    return get_user_demand()