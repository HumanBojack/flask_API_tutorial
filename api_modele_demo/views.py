from flask import Flask, request, jsonify
from .constant.http_status_codes import *
import validators

app = Flask(__name__)
# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')


from .models import Channel,db

@app.route("/channels/")
def get_channels():
    channel_list=[]
    for channel in Channel.query.all():
        channel_list.append(channel.title)
    return {"channels_list" : channel_list}

@app.route("/channels/<string:channel>/")
def get_single_channel(channel):
    query_result = Channel.find_by_title(title = channel)
    return { channel : query_result.json()}

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

