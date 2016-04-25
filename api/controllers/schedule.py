from flask import Blueprint, request, jsonify, g
from sqlalchemy import desc

from api.utils import requires_authentication
from api.models import db_session, Course, StudentAssignment, OptimizationRun
from api.schemas import ScheduleSchema, SemesterSchema, CourseSchema

schedule_bp = Blueprint('schedule', __name__, url_prefix='/api/schedule')

@schedule_bp.route('/', methods=['GET'])
@schedule_bp.route('/<user_id>', methods=['GET'])
@requires_authentication()
def get_user_schedule(user_id=None):
    if g.user_role == 'administrator':
        id_to_check = int(user_id or g.user_id)
    else:
        id_to_check = g.user_id

    # Get current maximum run ID from database, should be a subquery
    current_run_id = db_session.query(OptimizationRun.id).order_by(desc(OptimizationRun.created_at)).limit(1).scalar()

    semester_contents = {}
    for c in StudentAssignment.query.filter(StudentAssignment.run_id == current_run_id)\
            .filter(StudentAssignment.student_id == id_to_check).all():

        if c.semester.id not in semester_contents.keys():
            semester_contents[c.semester.id] = (c.semester, [c.course])
        else:
            semester_contents[c.semester.id][1].append(c.course)

    semester_array = []
    for s in semester_contents.keys():
        semester_data = SemesterSchema().dump(semester_contents[s][0]).data
        semester_data['courses'] = CourseSchema().dump(semester_contents[s][1], many=True).data
        semester_array.append(semester_data)

    return jsonify(schedule=list(sorted(semester_array, key=lambda s: s['id'])))
