# scripts

This folder contains all of the Spotify Song Grouper code and related files.

`functions.py` contains all of the functions for the Spotify Song Grouper.

`private-template.py` is a template for defining the `CLIENT_ID` and `CLIENT_SECRET` variables that you must define after creating a Spotify developer application. You should change the name of this file to `private.py` after defining these variables.

`grouper.ipynb` is a notebook detailing the full process of the Spotify Song Grouper including background information, a description of the methodology, data collection, exploration of the effectiveness of the grouping method on several different larger groups of songs, and final thoughts on the grouping method.

`getanalysis.ipynb` is a notebook that can be used for downloading the Spotify audio analysis for each song in a Spotify playlist. If you will be using Docker and want to group songs in a playlist that has not already been downloaded, you will need to use this notebook to first download the audio analyses.

`server.py` is the Python script that will be used by Docker to set up a server to run the Spotify Song Grouper.

`grouper.py` is the Python script that can be run from Terminal to set up a server to run the Spotify Song Grouper. It is almost identical to `server.py` except it also includes the Spotify authorization and audio analysis collection steps, so it is not necessary to use `getanalysis.ipynb` before running this script.

`trackids` is a folder that contains all of the track IDs from each playlist and album that has already been downloaded.

`analysis` is a folder that contains all of the Spotify audio analysis timbre vectors for each song in each playlist and album that has already been downloaded.

`templates` is a folder that contains all of the HTML files that are used to build the Spotify Song Grouper.
