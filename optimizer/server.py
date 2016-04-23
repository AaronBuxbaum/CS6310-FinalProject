from flask import Flask, request, jsonify
from solver import Solver

app = Flask(__name__)

@app.route('/solve', methods=['POST'])
def solve():
    j = request.get_json()

    assignments = []

    try:
        s = Solver(j)
        s.construct_model()
        val = s.optimize_model()
        assignments = s.get_student_assignments()
        app.logger.info('Solved model, {}.'.format(val))
    except:
        return jsonify(error=True)

    return jsonify(assignments=assignments)

if __name__ == '__main__':
    app.run('0.0.0.0', 8080, debug=True)
