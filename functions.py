"""This file contains the functions."""
import pandas
import spotipy
import spotipy.util as util
from private import USERNAME, CLIENT_ID, CLIENT_SECRET


def initializer(username, client_id, client_secret):
    """
    This function creates the spotify object.
    :param username: username of Spotify account to use
    :param client_id: Spotify application's client id
    :param client_secret: Spotify application's client secret
    :return: the spotify object needed to access the API
    """
    scope = 'user-top-read'
    redirect_uri = 'http://google.com/'
    token = util.prompt_for_user_token(username, scope, client_id,
                                       client_secret, redirect_uri)
    spotify_object = spotipy.Spotify(auth=token)
    return spotify_object


SPOTIFY = initializer(USERNAME, CLIENT_ID, CLIENT_SECRET)


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
    data.to_csv('trackids/' + album + '.csv', index=False)


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
    The function gets the track ids of a playlist.
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
    data.to_csv('trackids/' + playlist + '.csv', index=False)


def getanalysis(album, spotifyobject=SPOTIFY):
    """
    This function gets the timbre of the tracks of the album or playlist.
    :param album: the album id or playlist id
    :param spotifyobject: the spotify object
    :return: a csv with the timbre is saved for each track
    """
    trackids = pandas.read_csv('trackids/' + album + '.csv')['trackid']
    for i in trackids:
        result = spotifyobject.audio_analysis(i)['segments']
        data = pandas.DataFrame()
        for j in result:
            row = pandas.DataFrame([j['timbre']])
            data = data.append(row)
        data.to_csv('analysis/' + i + '.csv', index=False)
