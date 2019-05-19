#!/usr/bin/env python3
from flask import *
# from functions import cluster
import pandas
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


def cluster(ownerid, playlistid, k, useold=True, usesimple=False):
    """
    This function clusters the tracks.
    :param ownerid: the playlist's owner id
    :param playlistid: the playlist id
    :param k: the number of clusters
    :param useold: the previously downloaded playlist should be used
    :param usesimple: a faster, simpler, less accurate method should be used
    :return: the playlist with cluster labels
    """

    # Load the track ids
    playlist = pandas.read_csv('scripts/trackids/' + playlistid + '.csv')

    # Load the audio analyses
    data = pandas.DataFrame()
    for i, j in enumerate(playlist['trackid']):
        trackdata = pandas.read_csv('scripts/analysis/' + j + '.csv')
        if usesimple:
            trackdata = trackdata.mean()
        trackdata['track'] = playlist['track'][i]
        trackdata['album'] = playlist['album'][i]
        trackdata['artist'] = playlist['artist'][i]
        data = data.append(trackdata, ignore_index=True)

    # Standardize the data
    audio = data.iloc[:, 0:12].values
    audio = StandardScaler().fit_transform(audio)

    if not usesimple:
        # Cluster all the sounds from both playlists into 70 clusters
        kmeans = KMeans(n_clusters=70, random_state=0)
        labels = kmeans.fit_predict(audio)

        # Calculate the proportion of each song's sounds that are in each group
        soundtable = pandas.crosstab(data['track'], labels,
                                     normalize='index').reset_index()
        soundtable = playlist.merge(soundtable)

        # Standardize the data
        audio = soundtable.iloc[:, 4:].values
        audio = StandardScaler().fit_transform(audio)

    # Cluster the tracks into k groups
    kmeans2 = KMeans(n_clusters=k, random_state=0)
    playlist['group'] = kmeans2.fit_predict(audio)

    return playlist


def flask_app():
    app = Flask(__name__)

    @app.route('/', methods=['GET'])
    def show_tables():
        userid = 'tannerkoscinski'
        playlistid = '7oG3OYCE79smeQ2IgqbT8a'
        k = 2
        data = cluster(userid, playlistid, k, usesimple=True)
        tables = []
        for i in range(k):
            tables.append(data.loc[data['group'] == i,
                                   ['artist', 'album', 'track']].to_html())
        return render_template('tables.html', tables=tables)

    @app.route('/mpg', methods=['POST'])
    def mpg():
        return 'test'

    return app


if __name__ == '__main__':
    app = flask_app()
    app.run(debug=True, host='0.0.0.0')
