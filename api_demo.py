from nturl2path import url2pathname
from flask import Flask, request, json
from constant.http_status_codes import *
from exercice import channel_dictionary

api = Flask(__name__)


@api.route("/channels/list")
def list_channels():
    return {"data": [x for x in channel_dictionary]}

@api.route("/channels/list/<string:name>")
def specific_channels(name):
    return {"data": channel_dictionary[name]}

@api.route("/channels/new", methods=["POST"])
def add_channel():
    title = request.json.get("title")
    description = request.json.get("description")
    language = request.json.get("language")
    url = request.json.get("url")
    subjects = request.json.get("subjects")
    image_url = request.json.get("image_url")

    if all(x != "" and x is not None for x in [title, description, language, url, subjects, image_url]):
        if isinstance(subjects, list):
            new_dict = {
                "title": title,
                "description": description,
                "language": language,
                "url": url,
                "subjects": subjects,
                "image_url": image_url
                }
            channel_dictionary[title] = new_dict
            return new_dict
    return {"error": HTTP_406_NOT_ACCEPTABLE}, HTTP_406_NOT_ACCEPTABLE

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