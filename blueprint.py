from flask import Blueprint
api_blueprint = Blueprint('api',__name__)
STUDENT_ID=3
@api_blueprint.route("/hello-world")
def hello_world_def():
    return f"Hello world!!!"
@api_blueprint.route(f"/hello-world-9")
def hello_world():
    return f"Hello, World 9"
