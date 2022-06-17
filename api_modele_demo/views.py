from flask import Flask, request, jsonify, render_template
from .constant.http_status_codes import *
import validators
from .models import Channel, Video
from api_modele_demo import app,db


@app.route("/channels/")
def get_channels():
    channel_list=[]
    for channel in Channel.query.all():
        channel_list.append(channel.title)
    # return {"channels_list" : channel_list}
    return render_template("channel_list.html", channel_list=channel_list)


@app.route("/channels/<string:channel>/")
def get_single_channel(channel):
    query_result = Channel.find_by_title(title = channel)
    return { channel : query_result.json() }

@app.post("/channels/")
def post_new_channel():
    
    # On vérifie que le json envoyé possède les bonnes clefs
    if request.form["title"] in [channel.title for channel in Channel.query.all()]:
        return jsonify({'error': 'This channel is already in the database'}), HTTP_400_BAD_REQUEST
    
    # On vérifie que le json envoyé possède les bonnes clefs
    if set(request.form.keys()) != set(["title","description","url","image_url","language","subjects"]):
        return jsonify({'error': 'Wrong key'}), HTTP_400_BAD_REQUEST
    
    # On vérifie que le titre n'est pas trop long et est bien un string 
    if len(request.form["title"]) > 50 or not isinstance(request.form["title"],str):
        return jsonify({'error': 'Title too long or not in good format '}), HTTP_400_BAD_REQUEST

    # on vérifie que l'url est bien un url
    if not validators.url(request.form["url"]):
        return jsonify({'error': 'url not an url'}), HTTP_400_BAD_REQUEST
    
    
    Channel(**request.form).save_to_db()
     
    return {"message" : "nouvelle chaine ajoutée",
            "nouvelle chaine" : request.form
            }

@app.route("/channels/<string:channel>/videos", methods=["GET"])
def get_channel_videos(channel):
    query_results = Channel.find_by_title(title=channel).videos
    return {channel: [x.title for x in query_results]}

@app.route("/videos/<int:id>", methods=["GET"])
def get_video(id):
    video = Video.query.get_or_404(id)
    return video.json()

@app.route("/videos/new", methods=["POST"])
def new_video():
    # has channel, length, title
    # if request.form is None:
    #     return "hy"

    # channel = request.form.get("channel_id")
    # length = request.form.get("length")
    # title = request.form.get("title")

    try:
        Video(**request.form).save_to_db()
        return jsonify({"success": f"{request.form.get('title')} added to the database"})
    except:
        return jsonify({"error": "can't add to db"}), HTTP_406_NOT_ACCEPTABLE
    
    # if any([x is None for x in [channel, length, title]]):
    #     return jsonify({"error": "form is not good"}), HTTP_406_NOT_ACCEPTABLE

    # if set(request.form.keys()) != set(["channel_id","length","title"]):
    #     return jsonify({'error': 'Wrong key'}), HTTP_400_BAD_REQUEST

    # if request.form.get("title") in [video.title for video in Video.query.all()]:
    #     return jsonify({"error": "This video title is already in our database"}), HTTP_400_BAD_REQUEST

