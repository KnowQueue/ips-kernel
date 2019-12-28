from flask import Flask
from flask import request
from kernel.parsers.global_loader import global_loader
from kernel.parsers.request_session import request_session

app = Flask(__name__)
kernel_globals = {
    "concepts": {}
}
global_loader(kernel_globals)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route('/query', methods=['GET'])
def query():
    # import KB
    return request_session(request.get_data(), kernel_globals)
    # exec(request.get_data())
    # return result

@app.route("/deploy")
def deploy():
    return "Hello, World!"

@app.route("/clone")
def clone():
    return "Hello, World!"