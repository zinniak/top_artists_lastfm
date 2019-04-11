import unittest
import csv
import json
from SI507final_tools import *

# testing content in json files
class StepOne(unittest.TestCase):
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

# testing CSV files
class StepTwo(unittest.TestCase):
    def test_names_track_file(self):
        with open("top_tracks.csv") as csvfile:
            self.assertTrue(csvfile is not None, "testing that file exists")
            content = csvfile.read()
            self.assertTrue('"Title"' in content.split("\n")[0])
            self.assertTrue('"Artist"' in content.split("\n")[0])
    def test_names_artist_file(self):
        with open("top_artists.csv") as csvfile2:
            self.assertTrue(csvfile is not None, "testing that file exists")
            content2 = csvfile2.read()
            self.assertTrue('"Name"' in content2.split("\n")[0])
            self.assertTrue('"Bio"' in content2.split("\n")[0])

# testing if artists file is clean
class StepThree(unittest.TestCase):
    def test_artist_listeners(self):
        self.cleaned_file = open('cleaned_artists.csv','r')
        self.row_reader = self.cleaned_file.readlines()
        print(self.row_reader) #For # DEBUG:
        self.assertTrue(type(self.row_reader[1][1]) == int and type(self.row_reader[1][2]) == int, "Testing that artist listeners and playcounts are integer not string.")
        self.assertTrue(type(self.row_reader[10][1]) == int and type(self.row_reader[10][2]) == int, "Testing that artist listeners and playcounts are integer not string.")


# test if figure exists

# test clean text
# test db





if __name__ == "__main__":
    unittest.main(verbosity=2)
