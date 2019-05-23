#!/usr/bin/env python3
"""This script builds the Flask app."""
from flask import Flask, request, render_template, redirect
import Spotipy.oauth2 as oauth2
from Spotipy.client import SpotifyException
from functions import initializer, cluster
from private import SCOPE, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI


def flask_app():
    """This function builds the Flask app."""
    app = Flask(__name__)

    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html')

    @app.route('/', methods=['POST'])
    def show_tables():
        ownerid = request.form['ownerid']
        playlistid = request.form['playlistid']
        k = int(request.form['k'])
        simple = True
        if request.form['method'] == 'complex':
            simple = False
        try:
            spotifyobject = initializer()
            data = cluster(ownerid, playlistid, k, spotifyobject,
                           usesimple=simple)
            data = data.rename(str.upper, axis=1)
            tables = []
            for i in range(k):
                tables.append(data.loc[data['GROUP'] == i,
                                       ['ARTIST', 'ALBUM', 'TRACK']].to_html(
                                           classes='w3-table-all'))
            return render_template('tables.html', tables=tables)
        except SpotifyException:
            sp_oauth = oauth2.SpotifyOAuth(CLIENT_ID, CLIENT_SECRET,
                                           REDIRECT_URI, scope=SCOPE)
            return redirect(sp_oauth.get_authorize_url())

    @app.route('/authorize', methods=['GET'])
    def authorize():
        sp_oauth = oauth2.SpotifyOAuth(CLIENT_ID, CLIENT_SECRET,
                                       REDIRECT_URI, scope=SCOPE,
                                       cache_path='scripts/.cache-username')
        code = sp_oauth.parse_response_code(request.url)
        sp_oauth.get_access_token(code)
        return redirect('/')

    return app


if __name__ == '__main__':
    APP = flask_app()
    APP.run(debug=True, host='0.0.0.0')
