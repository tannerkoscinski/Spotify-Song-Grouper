# Spotify Song Grouper

The Spotify Song Grouper attempts to group songs together based on the sounds in the songs.

It uses the Spotify Web API to get an audio analysis for each track. Each track is broken into about 700 segments (plus or minus a few hundred). Most segments are less than a second long. Each segment has its own timbre vector composed of 12 numeric values.

The following is Spotify's description of timbre:

> *Timbre* is the quality of a musical note or sound that distinguishes different types of musical instruments, or voices. It is a complex notion also referred to as sound color, texture, or tone quality, and is derived from the shape of a segment’s spectro-temporal surface, independently of pitch and loudness. The timbre feature is a vector that includes 12 unbounded values roughly centered around 0. Those values are high level abstractions of the spectral surface, ordered by degree of importance.

More information can be found in [Spotify's Web API Documentation](https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-analysis/).

To group songs together, the Spotify Song Grouper uses a two-part k-means clustering method.

Each song is essentially a 700+/- row by 12 column data frame. To cluster songs, I first need to transform them all into equal length vectors. I accomplish this by clustering all of the sounds from all of the songs into a large number of groups (I chose 70). For each song, I calculate the proportion of the song's sounds that are in each group, so each song can now be described by a vector of length 70. I then cluster these song vectors together.

I explore the effectiveness of this grouping method on several different larger groups of songs.

---

`grouper.html` is an HTML document detailing the full process of the Spotify Song Grouper including background information, a description of the methodology, data collection, exploration of the effectiveness of the grouping method on several different larger groups of songs, and final thoughts on the grouping method.

`presentation.pdf` is a brief presentation of the Spotify Song Grouper.

`scripts` is a folder that contains all of the Spotify Song Grouper code and related files.

`docker` is a folder that contains everything that is required to build the Docker container.

---

## How to Use the Spotify Song Grouper

* [Create a Spotify app](https://developer.spotify.com/dashboard/applications)

* Click Edit Settings and add http://0.0.0.0:5000/authorize under Redirect URIs

* Install Docker and make sure it is running

* Download this repository

* Copy your Spotify app's Client ID and Client Secret into `private-template.py` in the `scripts` folder and change the file name to `private.py`

* Navigate to the `docker` folder in Terminal, run the command `docker-compose up`, and click the link to open the Spotify Song Grouper in your browser

A sample playlist has already been downloaded, and its owner ID and playlist ID are set as the defaults, so you can get a feel for how it works. You can adjust the number of song groups you would like, and you can select a quick, less accurate grouping method or a slower, more accurate grouping method. The less accurate method just uses the column averages for the timbre vectors for each track. The more accurate method uses the two-part k-means clustering method. You can input any owner ID and playlist ID, but it may take a while to download all of the audio analyses depending on the length of the playlist.
