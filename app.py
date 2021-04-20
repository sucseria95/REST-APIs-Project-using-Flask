from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,Integer,String,Float,CheckConstraint,DateTime
import os
from datetime import datetime
from flask_marshmallow import Marshmallow

app=Flask(__name__)

#database intialization

basedir=os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///"+os.path.join(basedir,"Music.db")
db=SQLAlchemy(app)
ma=Marshmallow(app)

@app.cli.command("db_create")
def db_create():
    db.create_all()
    print("Database created")

@app.cli.command("db_drop")
def db_drop():
    db.drop_all()
    print("database dropped")
@app.cli.command("db_seed")
def db_seed():
    alone=Song(id=1245,name="alone",duration=15644)
    db.session.add(alone)
    db.session.commit()
    print("db seeded")
#Endpoints for CRUD

@app.route("/")
def hello():
    return jsonify(message="hello welcome to Music Library")

#Read Endpoint
@app.route("/audio_details/<string:audio_type>/<int:audio_id>",methods=["GET"])
def get_audio(audio_type:str,audio_id:int):
    if audio_type.lower()=="song":
        song=Song.query.filter_by(id=audio_id).first()
        if song:
            result=song_schema.dump(song)
            return jsonify(result)
        else:

            return "error"

    elif audio_type.lower()=="podcast":
        podcast=Podcast.query.filter_by(id=audio_id).first()
        if podcast:
            result=podcast_schema.dump(podcast)
            return jsonify(result)
        else:
            return "error"

    else:
        audiobook=Audiobook.query.filter_by(id=audio_id).first()
        if audiobook:
            result=audiobook_schema.dump(audiobook)
            return jsonify(result)
        else:
            return "error"

#Create Endpoint
@app.route("/add_music/<string:audio_type>",methods=["POST","GET"])
def add_music(audio_type:str):
    if audio_type.lower()=="song":
        name=request.form["name"]
        test=Song.query.filter_by(name=name).first()
        if test:
            return jsonify("There is already song present"),409
        else:
            id=int(request.form["id"])
            duration=int(request.form["duration"])
            new_song=Song(id=id,name=name,duration=duration)

            db.session.add(new_song)
            db.session.commit()
            return jsonify(message="you added song"),201

    elif audio_type.lower()=="podcast":
        name=request.form["name"]
        test=Podcast.query.filter_by(name=name).first()
        if test:
            return jsonify("There is already podcast present"),409
        else:
            id=int(request.form["id"])
            duration=int(request.form["duration"])
            host=request.form["host"]
            new_podcast=Podcast(id=id,name=name,host=host,duration=duration)
            db.session.add(new_podcast)
            db.session.commit()
            return jsonify(message="you added podcast"),201
    else:
        title=request.form["title"]
        test=Audiobook.query.filter_by(title=title).first()
        if test:
            return jsonify("There is already podcast present"),409
        else:
            id=int(request.form["id"])
            author=request.form["author"]
            narrator=request.form["narrator"]
            duration=int(request.form["duration"])
            new_audiobook=Audiobook(title=title,narrator=narrator,duration=duration,author=author,id=id)
            db.session.add(new_audiobook)
            db.session.commit()
            return jsonify(message="you added audiobook"),201

#Update Endpoint
@app.route("/update_music/<string:audio_type>",methods=["PUT","GET"])
def update_music(audio_type:str):
    if audio_type=="song":
        id=int(request.form["id"])
        song=Song.query.filter_by(id=id).first()
        if song:
            song.name=request.form["name"]
            song.duration=int(request.form["duration"])
            db.session.commit()
            return jsonify(message="you updated one song"),202
        else:
            return jsonify(message="there is no such song"),404
    elif audio_type=="podcast":
        id=int(request.form["id"])
        podcast=Podcast.query.filter_by(id=id).first()
        if podcast:
            podcast.name=request.form["name"]
            podcast.duration=int(request.form["duration"])
            podcast.host=request.form["host"]
            db.session.commit()
            return jsonify(message="you updated the podcast"),202
        else:
            return jsonify(messgae="there is no such podcast")
    else:
        id=int(request.form["id"])
        test=Audiobook.query.filter_by(id=id).first()
        if test:
            test.title=request.form["title"]
            test.duration=int(request.form["duration"])
            test.author=request.form["author"]
            test.narrator=request.form["narrator"]
            db.session.commit()
            return jsonify(message="you updated the audiobook"),202
        else:
            return jsonify(message="there is no such audiobook")




#Delete Endpoint

@app.route("/remove_music/<string:audio_type>/<int:id>",methods=["DELETE"])
def remove_music(audio_type:str,id:int):
    if audio_type.lower()=="song":
        result=Song.query.filter_by(id=id)
        if result:
            db.session.delete(result)
            db.session.commit()
            return jsonify(message="You deleted a song")
        else:
            jsonify(message="There is no such song")
    elif audio_type.lower()=="podcast":
        result=Podcast.query.filter_by(id=id).first()
        if result:
            db.session.delete(result)
            db.session.commit()
            return jsonify(message="You deleted a podcast")
        else:
            return jsonify(message="there is no such podcast")
    else:
        result=Audiobook.query.filter_by(id=id).first()
        if result:
            db.session.delete(result)
            db.session.commit()
            return jsonify(message="You deleted a audio library")
        else:
            return jsonify(message="there is no such audio library")



#Database Models


class Song(db.Model):

    
   
    id=Column(Integer,unique=True,nullable=False,primary_key=True)
    name=Column(String(100))
    duration=Column(Integer,CheckConstraint("duration>=0"),nullable=False)
    


class Podcast(db.Model):
    
    
    id=Column(Integer,unique=True,nullable=False,primary_key=True)
    name=Column(String(100),nullable=False)
    duration=Column(Integer,CheckConstraint("duration>0"),nullable=False)
    
    host=Column(String(100),nullable=False)
    


class Audiobook(db.Model):
    
    id=Column(Integer,unique=True,nullable=False,primary_key=True)
    title=Column(String(100),nullable=False)
    duration=Column(Integer,CheckConstraint("duration>0"),nullable=False)
    
    author=Column(String(100),nullable=False)
    narrator=Column(String(100),nullable=False)

class SongSchema(ma.Schema):
    class Meta:
        fields=("id","name","duration")

class PodcastSchema(ma.Schema):
    class Meta:
        fields=("id","name","duration","host")

class AudiobookSchema(ma.Schema):
    class Meta:
        fields=("id","title","duration","author","narrator")

song_schema=SongSchema()
songs_schema=SongSchema(many=True)

podcast_schema=PodcastSchema()
podcasts_schema=PodcastSchema(many=True)

audiobook_schema=AudiobookSchema()
audiobooks_schema=AudiobookSchema(many=True)

if __name__=="__main__":
    app.run(debug=True)
