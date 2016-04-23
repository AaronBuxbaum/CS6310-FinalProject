from flask import Blueprint, request, jsonify

from api.models import db_session, Course
from api.schemas import CourseSchema

course_bp = Blueprint('course', __name__, url_prefix='/api/course')

@course_bp.route('/', methods=['GET'])
def list_courses():
    return jsonify(courses=CourseSchema().dump(Course.query.all(), many=True))