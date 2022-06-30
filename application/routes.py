from flask import Flask, request, jsonify, render_template, redirect, url_for
from .constant.http_status_codes import *
import validators
from .models import Channel, Video, User
from application import app, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from .oauth import GoogleOAuth
from helpers import commit_or_redirect

@app.route('/')
def home():
    return render_template('home.html')


@app.route("/channels/")
def get_channels():
    channel_list=[]
    for channel in Channel.query.all():
        channel_list.append(channel.title)
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

    try:
        Video(**request.form).save_to_db()
        return jsonify({"success": f"{request.form.get('title')} added to the database"})
    except:
        return jsonify({"error": "can't add to db"}), HTTP_406_NOT_ACCEPTABLE

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def connect():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = bool(request.form.get('remember'))

    user = User.query.filter_by(email=email).first()

    if password is None: return redirect(url_for('login'))
    if not user: return redirect(url_for('login'))
    
    if not check_password_hash(user.password, password):
        return redirect(url_for('login'))

    login_user(user, remember=remember)
    return redirect(url_for('private'))


@app.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    if user: return redirect(url_for('register'))

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)

    return commit_or_redirect(db, success='login', failure='register')


@app.route('/private')
@login_required
def private():
    return render_template('private.html', user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/authorize')
def oauth_authorize():
    if not current_user.is_anonymous:
        return redirect(url_for('home'))
    oauth = GoogleOAuth()
    return oauth.authorize()


@app.route('/callback')
def oauth_callback():
    if not current_user.is_anonymous:
        return redirect(url_for('home'))

    id, email, name = GoogleOAuth().callback()

    if id is None:
        redirect(url_for('home'))

    user = User.query.filter_by(id=id).first()
    if not user:
        user = User(id=id, email=email, name=name)
        db.session.add(user)
        commit_or_redirect(db, failure='home')

    login_user(user, True)
    return redirect(url_for('private'))