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

`presentation.pdf` is a brief presentation of the Spotify Song Grouper.

`scripts` is a folder that contains all of the Spotify Song Grouper code and related files.

`docker` is a folder that contains everything that is required to build a Docker container.

---

## How to Use the Spotify Song Grouper

### Option 1: Docker

To use the Spotify Song Grouper to group songs in a playlist that has already been downloaded, simply navigate to the `docker` folder in Terminal, run the command `docker-compose up`, and click the link to open the Spotify Song Grouper in your browser. (Note: You must have Docker installed and running.)

A sample playlist has already been downloaded, and its ID is set as the default, so you can get a feel for how it works. You can adjust the number of song groups you would like, and you can select a quick, less accurate grouping method or a slower, more accurate grouping method. The less accurate method just uses the column averages for the timbre vectors for each track. The more accurate method uses the two-part k-means clustering method.

To group songs in a playlist that has not already been downloaded, you will have to [create a Spotify app](https://developer.spotify.com/dashboard/applications). Then click Edit Settings and add http://google.com/ under Redirect URIs. Copy your Client ID and Client Secret into `private-template.py` in the `scripts` folder and change the file name to `private.py`. Then open `getanalysis.ipynb` in JupyterLab and follow the instructions there.

### Option 2: Terminal

Prerequisites:

* Install Python 3.7 and everything in the `requirements.txt` file located in the `docker` folder.

* [Create a Spotify app](https://developer.spotify.com/dashboard/applications). Then click Edit Settings and add http://google.com/ under Redirect URIs.

* Copy your Client ID and Client Secret into `private-template.py` in the `scripts` folder and change the file name to `private.py`.

In Terminal, navigate to the `scripts` folder, and run `python3 grouper.py`. You will have to authorize a Spotify account before you can click the link to open the Spotify Song Grouper in your browser.

A sample playlist has already been downloaded, and its owner ID and playlist ID are set as the defaults, so you can get a feel for how it works. You can adjust the number of song groups you would like, and you can select a quick, less accurate grouping method or a slower, more accurate grouping method. The less accurate method just uses the column averages for the timbre vectors for each track. The more accurate method uses the two-part k-means clustering method. You can input any owner ID and playlist ID, but it may take a while to download all of the audio analyses depending on the length of the playlist.
