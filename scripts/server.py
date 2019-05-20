#!/usr/bin/env python3
from flask import *
import pandas
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


def cluster(playlistid, k, usesimple=False):
    """
    This function clusters the tracks.
    :param playlistid: the playlist id
    :param k: the number of clusters
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
    def index():
        return render_template('indexd.html')

    @app.route('/', methods=['POST'])
    def show_tables():
        playlistid = request.form['playlistid']
        k = int(request.form['k'])
        simple = True
        if request.form['method'] == 'complex':
            simple = False
        data = cluster(playlistid, k, usesimple=simple)
        data = data.rename(str.upper, axis=1)
        tables = []
        for i in range(k):
            tables.append(data.loc[data['GROUP'] == i,
                                   ['ARTIST', 'ALBUM',
                                    'TRACK']].to_html(classes='w3-table-all'))
        return render_template('tables.html', tables=tables)

    return app


if __name__ == '__main__':
    app = flask_app()
    app.run(debug=True, host='0.0.0.0')
