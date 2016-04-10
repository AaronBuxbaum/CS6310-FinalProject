from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def say_hello():
    return jsonify(status='hello there.')
