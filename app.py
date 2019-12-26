from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route('/query', methods=['GET'])
def query():
    return request.get_data()

@app.route("/deploy")
def deploy():
    return "Hello, World!"

@app.route("/clone")
def clone():
    return "Hello, World!"