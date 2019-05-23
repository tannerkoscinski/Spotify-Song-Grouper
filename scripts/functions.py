"""This file contains the functions."""
import pandas
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import Spotipy
import Spotipy.util as util
from private import SCOPE, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI


def initializer(scope=SCOPE, client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                redirect_uri=REDIRECT_URI):
    """
    This function creates the spotify object.
    :param scope: Spotify application's scope
    :param client_id: Spotify application's client id
    :param client_secret: Spotify application's client secret
    :param redirect_uri: Spotify application's redirect URI
    :return: the spotify object needed to access the API
    """
    username = 'username'
    token = util.prompt_for_user_token(username, scope, client_id,
                                       client_secret, redirect_uri)
    spotify_object = Spotipy.Spotify(auth=token)
    return spotify_object


SPOTIFY = initializer()


def searchartist(artist, spotifyobject=SPOTIFY):
    """
    This function searches for an artist.
    :param artist: the artist's name
    :param spotifyobject: the spotify object
    :return: the possible artists' ids and names
    """
    result = spotifyobject.search(artist, limit=1, type='artist')['artists'][
        'items'][0]
    artistid = result['id']
    name = result['name']
    return artistid, name


def searchalbums(artist, spotifyobject=SPOTIFY):
    """
    This function searches for the albums of an artist.
    :param artist: the artist's name
    :param spotifyobject: the spotify object
    :return: the artist's albums' ids and names
    """
    result = spotifyobject.artist_albums(searchartist(artist,
                                                      spotifyobject)[0],
                                         album_type='album')['items']
    for i in result:
        print(i['id'], i['name'])


def getalbum(albumid, album, artist, spotifyobject=SPOTIFY):
    """
    This function gets the track ids of an album.
    :param albumid: the album id
    :param album: the album name
    :param artist: the artist name
    :param spotifyobject: the spotify object
    :return: a csv with the track ids of the album is saved
    """
    result = spotifyobject.album_tracks(albumid)['items']
    data = pandas.DataFrame()
    for i in result:
        row = pandas.DataFrame([[i['id'], i['name'], album, artist]],
                               columns=['trackid', 'track', 'album', 'artist'])
        data = data.append(row)
    data.to_csv('trackids/' + albumid + '.csv', index=False)


def searchplaylist(playlist, spotifyobject=SPOTIFY):
    """
    This function searches for a playlist.
    :param playlist: the name of the playlist
    :param spotifyobject: the spotify object
    :return: the id, name, and owner of the possible playlists
    """
    result = spotifyobject.search(playlist, limit=5, type='playlist')[
        'playlists']['items']
    for i in result:
        print(i['id'], i['name'], 'by', i['owner']['id'])


def getplaylist(userid, playlistid, playlist, spotifyobject=SPOTIFY):
    """
    This function gets the track ids of a playlist.
    :param userid: the user id of the owner of the playlist
    :param playlistid: the playlist id
    :param playlist: the playlist name
    :param spotifyobject: the spotify object
    :return: a csv with the track ids of the playlist is saved
    """
    result = spotifyobject.user_playlist_tracks(userid, playlistid)['items']
    data = pandas.DataFrame()
    for i in result:
        row = pandas.DataFrame([[playlist, i['track']['artists'][0]['name'],
                                 i['track']['name'], i['track']['id']]],
                               columns=['playlist', 'artist', 'track',
                                        'trackid'])
        data = data.append(row)
    data.to_csv('trackids/' + playlistid + '.csv', index=False)


def getplaylist2(userid, playlistid, spotifyobject):
    """
    This function gets the track ids of a playlist.
    :param userid: the user id of the owner of the playlist
    :param playlistid: the playlist id
    :param spotifyobject: the spotify object
    :return: a csv with the track ids of the playlist is saved
    """
    result = spotifyobject.user_playlist_tracks(userid, playlistid)['items']
    data = pandas.DataFrame()
    for i in result:
        row = pandas.DataFrame([[i['track']['artists'][0]['name'],
                                 i['track']['album']['name'],
                                 i['track']['name'], i['track']['id']]],
                               columns=['artist', 'album', 'track', 'trackid'])
        data = data.append(row)
    data.to_csv('scripts/trackids/' + playlistid + '.csv', index=False)


def getanalysis(album, spotifyobject=SPOTIFY):
    """
    This function gets the timbre of the tracks of the album or playlist.
    :param album: the album id or playlist id
    :param spotifyobject: the spotify object
    :return: a csv with the timbre is saved for each track
    """
    trackids = pandas.read_csv('trackids/' + album + '.csv')['trackid']
    for i in trackids:
        try:
            pandas.read_csv('analysis/' + i + '.csv', nrows=1)
        except IOError:
            result = spotifyobject.audio_analysis(i)['segments']
            data = pandas.DataFrame()
            for j in result:
                row = pandas.DataFrame([j['timbre']])
                data = data.append(row)
            data.to_csv('analysis/' + i + '.csv', index=False)


def getanalysis2(album, spotifyobject):
    """
    This function gets the timbre of the tracks of the album or playlist.
    :param album: the album id or playlist id
    :param spotifyobject: the spotify object
    :return: a csv with the timbre is saved for each track
    """
    trackids = pandas.read_csv('scripts/trackids/' + album + '.csv')['trackid']
    for i in trackids:
        try:
            pandas.read_csv('scripts/analysis/' + i + '.csv', nrows=1)
        except IOError:
            result = spotifyobject.audio_analysis(i)['segments']
            data = pandas.DataFrame()
            for j in result:
                row = pandas.DataFrame([j['timbre']])
                data = data.append(row)
            data.to_csv('scripts/analysis/' + i + '.csv', index=False)


def cluster(ownerid, playlistid, k, spotifyobject, usesimple=False):
    """
    This function clusters the tracks.
    :param ownerid: the playlist's owner id
    :param playlistid: the playlist id
    :param k: the number of clusters
    :param spotifyobject: the Spotify object
    :param usesimple: a faster, simpler, less accurate method should be used
    :return: the playlist with cluster labels
    """
    # Get audio analyses
    getplaylist2(ownerid, playlistid, spotifyobject)
    getanalysis2(playlistid, spotifyobject)

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
