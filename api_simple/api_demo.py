from nturl2path import url2pathname
from flask import Flask, request, json
from constant.http_status_codes import *
from exercice import channel_dictionary


api = Flask(__name__)

@api.route("/channels/list")
def list_channels():
    return {"data": [x for x in channel_dictionary]}

@api.route("/channels/<string:name>", methods=["GET", "PUT"])
def specific_channels(name):
    if request.method == 'PUT':
        channel = channel_dictionary.get(name)
        new_language = request.json.get("language")
        print(channel, new_language)
        if channel is not None and new_language is not None:
            channel["language"] = new_language
            return {"done": f"{new_language} has been added to {channel['title']}"}
        else:
            return {"error": "Channel doesn't exist or language is not specified"}, HTTP_400_BAD_REQUEST
    else:
        return {"data": channel_dictionary[name]}

@api.route("/channels/new", methods=["POST"])
def add_channel():
    title = request.json.get("title")
    description = request.json.get("description")
    language = request.json.get("language")
    url = request.json.get("url")
    subjects = request.json.get("subjects")
    image_url = request.json.get("image_url")

    if title in channel_dictionary.keys():
        return {"error": "Already in db"}, HTTP_400_BAD_REQUEST

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

@api.route("/channels/<string:name>/delete", methods=["DELETE"])
def delete_channel(name):
    if channel_dictionary.get(name) is None:
        return {"error": "channel not in our db"}, HTTP_404_NOT_FOUND
    channel_dictionary.pop(name)
    return {"removed": name}


if __name__ == "__main__":
    api.run(debug=True)














