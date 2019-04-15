import unittest
import csv
import json
import sqlite3
from SI507final_tools import *

# testing content in json files
class JsonFiles(unittest.TestCase):
    def test_tracks_json(self):
        with open('lfm_top_tracks.json') as jsonfile:
            self.assertTrue(jsonfile is not None, "testing that tracks file exists")
            res = json.loads(jsonfile.read())
            self.assertTrue(len(res["tracks"]["track"][0]["name"])>0,"Testing that file has track names")
    def test_artists_json(self):
        with open("top_artist_info.json") as jsonfile:
            self.assertTrue(jsonfile is not None, "testing that artists file exists")
            res = json.loads(jsonfile.read())
            for artist in res:
                self.assertTrue(len(res[artist]["artist"]["name"])>0,"Testing that file has artist names")

# testing if CSV files exist
class CSVFiles(unittest.TestCase):
    def test_names_track_file(self):
        with open("top_tracks.csv") as csvfile:
            self.assertTrue(csvfile is not None, "testing that file exists")
            content = csvfile.read()
            self.assertTrue('Title' in content.split("\n")[0])
            self.assertTrue('Artist' in content.split("\n")[0])

    def test_names_artist_file(self):
        with open("cleaned_artists.csv",encoding="UTF-8") as csvfile2:
            self.assertTrue(csvfile is not None, "testing that file exists")
            content2 = csvfile2.read()
            self.assertTrue('Name' in content2.split("\n")[0])
            self.assertTrue('Bio' in content2.split("\n")[0])

# testing to see if bargraph images exist
class BarGraphs(unittest.TestCase):
    def test_listener_graph(self):
            with open('static/listeners.png','r') as img1:
                self.assertTrue(img1 is not None,"Testing that listener graph image exists")

    def test_playcount_graph(self):
        with open('static/playcounts.png','r') as img2:
            self.assertTrue(img2 is not None,"Testing that playcount graph image exists")

# testing to see if tables exist in database
class Tables(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect("sample_tracks.db")
        # Connecting to database
        self.cur = self.conn.cursor()

    def test_for_artist_table(self):
        res = self.cur.execute("select * from artists")
        data = res.fetchall()
        self.assertTrue(data, 'Testing that you get a result from making a query to the artists table')

    def test_for_track_table(self):
        res = self.cur.execute("select * from tracks")
        data = res.fetchall()
        self.assertTrue(data, 'Testing that you get a result from making a query to the tracks table')


if __name__ == "__main__":
    unittest.main(verbosity=2)
