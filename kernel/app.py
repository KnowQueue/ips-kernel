from flask import Flask
from flask import request
from .parsers.global_loader import global_loader
from .parsers.request_session import request_session
from settings import APP_KB
import os
import shutil
from pathlib import Path

app = Flask(__name__)

Path(os.path.join(APP_KB,"concepts")).mkdir(parents=True, exist_ok=True)
Path(os.path.join(APP_KB,"hierarchy")).mkdir(parents=True, exist_ok=True)
Path(os.path.join(APP_KB,"relations")).mkdir(parents=True, exist_ok=True)
Path(os.path.join(APP_KB,"rules")).mkdir(parents=True, exist_ok=True)

kernel_globals = {
    "concepts": {}
}
global_loader(kernel_globals)

@app.route("/")
def hello():
    print("Hello, World!")
    return "Hello, World!"

@app.route('/query', methods=['GET'])
def query():
    # import KB
    return request_session(request.get_data(), kernel_globals)
    # exec(request.get_data())
    # return result

@app.route("/deploy", methods=['PUT'])
def deploy():
    shutil.rmtree(os.path.join(APP_KB,"concepts"))
    shutil.rmtree(os.path.join(APP_KB,"hierarchy"))
    shutil.rmtree(os.path.join(APP_KB,"relations"))
    shutil.rmtree(os.path.join(APP_KB,"rules"))
    for filePath in request.files.keys():
        directoryPath = os.path.dirname(os.path.join(APP_KB, filePath))
        Path(directoryPath).mkdir(parents=True, exist_ok=True)
        Path(os.path.join(APP_KB, filePath)).touch()
        request.files[filePath].save(os.path.join(APP_KB, filePath))
        request.files[filePath].close()
    return str([key for key in request.files.keys()])

@app.route("/clone")
def clone():
    return "Hello, World!"