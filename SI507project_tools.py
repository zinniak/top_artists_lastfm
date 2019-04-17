import json
import requests
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

LFM_KEY = "118458067274abc2709c8f06d5180c7b"

##### Getting Last.fm top 50 tracks info #####
LFM_CACHE_FNAME = "lfm_top_tracks.json"

# testing to see if cache file for lfm tracks requests already exists:
try:
    lfm_cache_file = open(LFM_CACHE_FNAME, "r")
    lfm_cache_data = lfm_cache_data.read()
    lfm_cache_file.close()
    lfm_diction_cache = json.loads(lfm_cache_data)
except:
    lfm_diction_cache = {}

# making track request:
LFM_baseurl= "http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&api_key=118458067274abc2709c8f06d5180c7b&format=json"
LFM_diction_parameters = {}
LFM_diction_parameters["api_key"] = LFM_KEY

# saving json object as python object
response = requests.get(LFM_baseurl)
data = json.loads(response.text.encode("utf-8"))
with open(LFM_CACHE_FNAME, "w") as lfm_cache_object:
    lfm_cache_object.write(json.dumps(data))

### creating a list of tracks ###
lfm_search_result = data
lfm_track_lst = [["Title","Artist","Playcount","URL","Image"]]
# function to extract track information into a list
def create_track_list(track):
    track_info = [track["name"],track["artist"]["name"],track["playcount"],track['url'],track['image'][2]['#text']]
    lfm_track_lst.append(track_info)
# invoking the function
for track in lfm_search_result["tracks"]["track"]:
    create_track_list(track)

# creating pandas dataframe from the list of tracks
df_tracks = pd.DataFrame(lfm_track_lst)
header = df_tracks.iloc[0]
df_tracks = df_tracks.rename(columns = header)
df_tracks = df_tracks.drop(0)
df_tracks.to_csv("top_tracks.csv",index=False)


##### Getting Artist Info #####
ART_CACHE_FNAME = "top_artist_info.json"
# testing to see if cache file already exists:
try:
    art_cache_file = open(ART_CACHE_FNAME, "r")
    art_cache_data = art_cache_data.read()
    art_cache_file.close()
    art_diction_cache = json.loads(art_cache_data)
except:
    art_diction_cache = {}

# function for creating unique url identifier:
def params_unique_combination(baseurl, params_d, private_keys=["api_key"]):
    alphabetized_keys = sorted(params_d.keys())
    res = []
    for k in alphabetized_keys:
        if k not in private_keys:
            res.append("{}-{}".format(k, params_d[k]))
    return baseurl + "_".join(res)

# making artist requests:
def get_artist(artist):
    ART_baseurl= "http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist=" + artist + "&api_key=118458067274abc2709c8f06d5180c7b&format=json"
    ART_diction_parameters = {}
    ART_diction_parameters["artist"] = artist

    unique_identifier = params_unique_combination(ART_baseurl,ART_diction_parameters)
    if unique_identifier in art_diction_cache:
        return art_diction_cache[unique_identifier]
    else:
        response = requests.get(ART_baseurl,params=ART_diction_parameters)
        art_diction_cache[unique_identifier] = json.loads(response.text.encode("UTF-8"))
        with open(ART_CACHE_FNAME, "w") as art_cache_object:
            art_cache_object.write(json.dumps(art_diction_cache))
        return art_diction_cache[unique_identifier]


### making API requests for the artists in the top tracks list ###
for row in lfm_track_lst[1:]:
    get_artist(row[1])
    # get_artist(artist)

### extracting artist information into a list ###
artist_search_result = art_diction_cache
lfm_artist_lst = [["Name","Listeners","Playcount","Bio","URL","Image"]]
# creating function to add to artist list
def create_artist_list(artist):
    artist_info = [artist_search_result[artist]["artist"]["name"],artist_search_result[artist]["artist"]["stats"]["listeners"],artist_search_result[artist]["artist"]["stats"]["playcount"],artist_search_result[artist]["artist"]["bio"]["summary"],artist_search_result[artist]['artist']['url'],artist_search_result[artist]['artist']['image'][2]["#text"]]
    lfm_artist_lst.append(artist_info)
# invoking the function
for artist in artist_search_result:
    create_artist_list(artist)

# creating a pandas dataframe of the artist info
df_artists = pd.DataFrame(lfm_artist_lst)
header = df_artists.iloc[0]
df_artists = df_artists.rename(columns = header)
df_artists = df_artists.drop(0)


##### Setting up flask application #####
app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'asdadafaads'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./lastfm_top_tracks.db' # TODO: decide what your new database name will be -- that has to go here
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) # For database use
session = db.session # to make queries easy

##### cleaning data in artists dataframe #####
bio_list = []
df_artists["Bio"] = df_artists["Bio"].str.replace("\n"," ")
for bio in df_artists["Bio"]:
    clean = bio.split(" <a")
    clean = clean[0]
    bio_list.append(clean)
df_artists["Bio"] = bio_list
# saving cleaned artist file as CSV
df_artists.to_csv("cleaned_artists.csv",index=False)


##### creating artist statistics graphs ######
df_artists["Listeners"] = pd.to_numeric(df_artists["Listeners"])
from matplotlib import rcParams # to adjust the layout of the figure when saves as image
rcParams.update({'figure.autolayout': True})
# plotting listeners
df_artists.plot.bar(x='Name', y='Listeners')
plt.xlabel('Artist')
plt.savefig('static/listeners.png')
# plotting playcounts
df_artists["Playcount"] = pd.to_numeric(df_artists["Playcount"])
df_artists.plot.bar(x='Name', y='Playcount',color=['red'])
plt.xlabel('Artist')
plt.savefig('static/playcounts.png')



##### Setting up models #####
class Artist(db.Model):
    __tablename__ = "artists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    listeners = db.Column(db.Integer)
    playcount = db.Column(db.Integer)
    bio = db.Column(db.String)
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
    if Artist.query.filter_by(name=row[0]).first():
        return "Artist already exists"
    else:
        artist = Artist(name=row[0],listeners=row[1],playcount=row[2],bio=row[3],url=row[4],image=row[5])
        session.add(artist)
        session.commit()
        return artist

# adding tracks to database
def create_track(row):
    if Track.query.filter_by(title=row[0]).first():
        return "Track already exists"
    else:
        artist = Artist.query.filter_by(name=row[1]).first()
    # print(artist)
        title = Track(title=row[0],playcount=row[2],url=row[3],image=row[4],artist_id=artist.id)
        session.add(title)
        session.commit()
        return title

# creating database
db.create_all()

# creating list of artists
with open("cleaned_artists.csv", encoding="UTF-8") as csvfile:
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

# invoking Artist class to add data to table
for artist in artists_list[1:]:
    # print(artist[3])
    create_artist(artist)

# invoking Track class to add data to table
for track in tracks_list[1:]:
    create_track(track)
