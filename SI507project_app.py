from SI507project_tools import *
from flask import url_for

################ Setting up controllers ####################

@app.route('/')
def index():
    all_tracks = []
    tracks = Track.query.all()
    for t in tracks:
        artist = Artist.query.filter_by(id=t.artist_id).first()
        all_tracks.append((t.title,artist.name,t.playcount,t.url,t.image))
    return render_template('index.html',all_tracks=all_tracks)

@app.route('/all_artists')
def see_all_songs():
    list_artists = []
    artists = Artist.query.all()
    for a in artists:
        list_artists.append((a.name,a.listeners,a.id,a.bio,a.image,a.url))
    return render_template("all_artists.html",all_artists=list_artists)

@app.route('/artist_statistics')
def see_chart():
    return render_template("chart.html")


if __name__ == '__main__':
    app.run()
