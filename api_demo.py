from flask import Flask, request, json
from constant.http_status_codes import *

api = Flask(__name__)


@api.route("/helloworld/")
def hello_get():
    return {"data":"Hello Charles"}


@api.route("/helloworld/", methods=["POST"])
def hello_post():
    return {"data":"posted"}

@api.route("/hellouser/<string:user>")
def hello_user(user):
    return {"data":f"hello {user}"}


@api.route("/square", methods=["POST"])
def square():
    number = request.form["number"]
    return {"number": number, "square": int(number)**2}

@api.route("/hellouser_validator/<string:user>")  
def hello_user_validator(user):
    if not isinstance(user,str):
        return {"error":"wrong user type"}, HTTP_400_BAD_REQUEST
    return {"data":f"hello {user}"}, HTTP_200_OK


if __name__ == "__main__":
    api.run(debug=True)