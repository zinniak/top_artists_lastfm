import csv
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, Float
import os
import codecs
import sys
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)


app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'asdadafaads'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./sample_tracks.db' # TODO: decide what your new database name will be -- that has to go here
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set up Flask debug stuff
db = SQLAlchemy(app) # For database use
session = db.session # to make queries easy


##### Setting up models #####
class Artist(db.Model):
    __tablename__ = "artists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    listeners = db.Column(db.Integer)
    playcount = db.Column(db.Integer)
    bio = db.Column(db.String(500))
    url = db.Column(db.String(200))
    image = db.Column(db.String(200))
    tracks = db.relationship('Track',backref='Artist')

    def __repr__(self):
        return "{} - {} listeners".format(self.name,self.listeners)


class Track(db.Model):
    __tablename__ = "tracks"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    playcount = db.Column(db.Integer)
    url = db.Column(db.String(200))
    image = db.Column(db.String(200))
    artist_id = db.Column(db.Integer,db.ForeignKey('artists.id'))

    def __repr__(self):
        return "{} by {}".format(self.title,self.artist)

# adding artists to database
def create_artist(row):
    artist = Artist(name=row[0],listeners=row[1],playcount=row[2],bio=row[3],url=row[4],image=row[5])
    session.add(artist)
    session.commit()
    # print(artist)
    return artist

# adding tracks to database
def create_track(row):
    artist = Artist.query.filter_by(name=row[1]).first()
    # print(artist)
    title = Track(title=row[0],playcount=row[2],url=row[3],image=row[4],artist_id=artist.id)
    session.add(title)
    session.commit()
    return title

# creating database
db.create_all()

# creating list of artists
with open("top_artists.csv") as csvfile:
    artists_list = []
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        artists_list.append(row)
    # print(artists_list[2])

# creating list of tracks
with open("top_tracks.csv") as csvfile2:
    tracks_list = []
    readCSV = csv.reader(csvfile2, delimiter=',')
    for row in readCSV:
        tracks_list.append(row)
# print(len(tracks_list))
# print(len(artists_list))

for artist in artists_list[1:]:
    print(artist[0])
    create_artist(artist)

for track in tracks_list[1:]:
    create_track(track)

##### creating graphs ######

df_artists = pd.DataFrame(artists_list)
df_artists.columns = df_artists.iloc[0]
df_artists = df_artists.drop([0])
df_artists["Listeners"] = pd.to_numeric(df_artists["Listeners"])
df_artists.plot.bar(x='Name', y='Listeners')
plt.savefig('listeners.png')
