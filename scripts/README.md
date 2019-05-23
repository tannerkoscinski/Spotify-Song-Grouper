# scripts

This folder contains all of the Spotify Song Grouper code and related files.

`functions.py` contains all of the functions for the Spotify Song Grouper.

`private-template.py` is a template for defining the `CLIENT_ID` and `CLIENT_SECRET` variables that you must define after creating a Spotify developer application. You should change the name of this file to `private.py` after defining these variables.

`grouper.ipynb` is a notebook detailing the full process of the Spotify Song Grouper including background information, a description of the methodology, data collection, exploration of the effectiveness of the grouping method on several different larger groups of songs, and final thoughts on the grouping method.

`server.py` is the Python script that will be used by Docker to set up a server to run the Spotify Song Grouper.

`trackids` is a folder that contains all of the track IDs from each playlist and album that has been downloaded.

`analysis` is a folder that contains all of the Spotify audio analysis timbre vectors for each song in each playlist and album that has been downloaded.

`templates` is a folder that contains all of the HTML files that are used to build the Spotify Song Grouper.

`Spotipy` is a folder that contains a modified version of [Paul Lamere's Spotipy library](https://github.com/plamere/spotipy).
