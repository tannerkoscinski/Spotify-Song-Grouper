#!/usr/bin/env python3
from flask import *
from functions import cluster


def flask_app():
    app = Flask(__name__)

    @app.route('/', methods=['GET'])
    def index():
        return render_template('indexf.html')

    @app.route('/', methods=['POST'])
    def show_tables():
        ownerid = request.form['ownerid']
        playlistid = request.form['playlistid']
        k = int(request.form['k'])
        simple = True
        if request.form['method'] == 'complex':
            simple = False
        data = cluster(ownerid, playlistid, k, usesimple=simple)
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
