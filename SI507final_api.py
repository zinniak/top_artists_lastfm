import json
import csv
import requests
import pandas as pd
import matplotlib.pyplot as plt
import os
import codecs
import sys
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

LFM_KEY = "118458067274abc2709c8f06d5180c7b"

LFM_CACHE_FNAME = "lfm_top_tracks.json"

#testing to see if cache file for lfm requests already exists:
try:
    lfm_cache_file = open(LFM_CACHE_FNAME, "r")
    lfm_cache_data = lfm_cache_data.read()
    lfm_cache_file.close()
    lfm_diction_cache = json.loads(lfm_cache_data)
except:
    lfm_diction_cache = {}


# #function for creating unique url identifier:
# def params_unique_combination(baseurl, params_d, private_keys=["api-key"]):
#     alphabetized_keys = sorted(params_d.keys())
#     res = []
#     for k in alphabetized_keys:
#         if k not in private_keys:
#             res.append("{}-{}".format(k, params_d[k]))
#     return baseurl + "_".join(res)

#making requests:
LFM_baseurl= "http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&api_key=118458067274abc2709c8f06d5180c7b&format=json"
LFM_diction_parameters = {}
LFM_diction_parameters["api_key"] = LFM_KEY

response = requests.get(LFM_baseurl)
data = json.loads(response.text.encode("utf-8"))
with open(LFM_CACHE_FNAME, "w") as lfm_cache_object:
    lfm_cache_object.write(json.dumps(data))


# Defining Classes to write csv files
class TopTracks:
    def __init__(self,diction):
        self.title = diction["name"]
        self.artist = diction["artist"]["name"]
        self.playcount = diction['playcount']
        self.url = diction['url']
        self.image = diction['image'][2]["#text"]

    def __str__(self):
        return "{} by {}".format(self.title,self.artis)

    def csv_rows(self):
        return [self.title,self.artist,self.playcount,self.url,self.image]

lfm_search_result = data
lfm_track_lst = []
for track in lfm_search_result["tracks"]["track"]:
    lfm_track_lst.append(TopTracks(track))


# Writing data into a CSV file
with open("top_tracks.csv", 'w') as csv_file:
    #line 186: From my code in Problem Set 11
    trackwriter = csv.writer(csv_file, delimiter=",",quotechar='"', quoting=csv.QUOTE_ALL, lineterminator="\n")
    trackwriter.writerow(["Title","Artist","Playcount","URL","Image"])
    for track in lfm_track_lst:
        trackwriter.writerow(track.csv_rows())
            # print(article.csv_rows())


#  Getting Artist Info
ART_CACHE_FNAME = "top_artist_info.json"
#testing to see if cache file already exists:
try:
    art_cache_file = open(ART_CACHE_FNAME, "r")
    art_cache_data = art_cache_data.read()
    art_cache_file.close()
    art_diction_cache = json.loads(art_cache_data)
except:
    art_diction_cache = {}

#function for creating unique url identifier:
def params_unique_combination(baseurl, params_d, private_keys=["api_key"]):
    alphabetized_keys = sorted(params_d.keys())
    res = []
    for k in alphabetized_keys:
        if k not in private_keys:
            res.append("{}-{}".format(k, params_d[k]))
    return baseurl + "_".join(res)

#making requests:
def get_artist(artist):
    ART_baseurl= "http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist=" + artist + "&api_key=118458067274abc2709c8f06d5180c7b&format=json"
    ART_diction_parameters = {}
    ART_diction_parameters["artist"] = artist

    unique_identifier = params_unique_combination(ART_baseurl,ART_diction_parameters)
    if unique_identifier in art_diction_cache:
        return art_diction_cache[unique_identifier]
    else:
        response = requests.get(ART_baseurl,params=ART_diction_parameters)
        art_diction_cache[unique_identifier] = json.loads(response.text.encode("utf-8"))
        with open(ART_CACHE_FNAME, "w") as art_cache_object:
            art_cache_object.write(json.dumps(art_diction_cache))
        return art_diction_cache[unique_identifier]

top_tracks = pd.read_csv("top_tracks.csv")
for artist in top_tracks["Artist"]:
    get_artist(artist)

# Defining Class to create Artist CSV.

class TopArtist:
    def __init__(self,diction):
        self.name = diction["artist"]["name"]
        self.listeners = diction["artist"]["stats"]["listeners"]
        self.playcount = diction["artist"]["stats"]["playcount"]
        self.bio = diction["artist"]["bio"]["summary"]
        self.url = diction['artist']['url']
        self.image = diction['artist']['image'][2]["#text"]

    def __str__(self):
        return "{} - {} listeners".format(self.name,self.listeners)

    def csv_rows(self):
        return [self.name,self.listeners,self.playcount,self.bio,self.url,self.image]

#creating lsit of artist instances
artist_search_result = art_diction_cache
lfm_artist_lst = []
for artist in artist_search_result:
    # print(artist_search_result[artist])
    lfm_artist_lst.append(TopArtist(artist_search_result[artist]))

# Writing data into a CSV file
with open("top_artists.csv", 'w') as csv_file2:
    #line 186: From my code in Problem Set 11
    artistwriter = csv.writer(csv_file2, delimiter=",",quotechar='"', quoting=csv.QUOTE_ALL, lineterminator="\n")
    artistwriter.writerow(["Name","Listeners","Playcount","Bio","URL","Image"])
    for artist in lfm_artist_lst:
        artistwriter.writerow(artist.csv_rows())
