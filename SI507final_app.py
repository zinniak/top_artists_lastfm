from SI507final_tools import *
from flask import Flask, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, Float

################ Setting up controllers ####################
@app.route('/')
def index():
    all_tracks = []
    tracks = Track.query.all()
    for t in tracks:
        artist = Artist.query.filter_by(id=t.artist_id).first()
        all_tracks.append((t.title,artist.name,t.playcount,t.url,t.image))
    # return all_tracks
    return render_template('index.html',all_tracks=all_tracks)

@app.route('/artist_listener_chart')
def see_chart():
    img = Image("books_read.png")
    return render_template("chart.html",img=img)

@app.route('/all_artists')
def see_all_songs():
    list_artists = []
    artists = Artist.query.all()
    for a in artists:
        list_artists.append((a.name,a.listeners,a.id))
    return render_template("all_artists.html",all_artists=list_artists)

# artists = Artist.query.all()
# for a in artists:
#     id = a.id
#     @app.route('/artist_detail/' + str(id))
#     def artist_detail_(id):
#         artist = Artist.query.filter_by(id=id).first()
#         details = [(artist.id,artist.name,artist.bio,artist.listeners,artist.playcount,artist.url,artist.image)]
#         return render_template("artist_details.html",details=details)
#

if __name__ == '__main__':
    app.run()
