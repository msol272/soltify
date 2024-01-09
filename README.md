# Soltify Suite
My suite of tools for Spotify that help create playlists, build music brackets, and more!

## Soltify Shuffle

Spotify's built-in shuffle sucks. It always plays the same songs and clumps artists together.

Soltify Shuffle re-arranges a playlist to be truly shuffled. It also has the option to spread
artists out so that if you have 10 songs from one artist in a 100 song playlist, you will only
hear them once every 10 songs or so.

### Examples:

* Example 1: Shuffle playlist "My Songs" with artists evenly spaced

`python soltify_shuffle.py "My Songs"`

* Example 2: Repeat Example 1 without fetching playlist from Spotify a 2nd time (to speed it up)

`python soltify_shuffle.py "My Songs" --uselocal`

* Example 3: Shuffle playlist "My Songs" completely randomly, without spacing out artists

`python soltify_shuffle.py "My Songs" --ignoreartist`

* For more detailed usage, run:

`python soltify_shuffle.py -h`

## Soltify Radar (coming soon)

Spotify's built-in release radar sucks. It feeds you tons of covers, live tracks, and re-recordings
that you don't care about, and it always favors certain artists. It's hard to tell what is a single
and what's a full album. Plus, sometimes if you don't check it for a few weeks, you permanently miss
a release.

Soltify Radar creates and maintains a running list of Albums and Singles for you to check out. It is based on
similarity to your Liked Songs, as well as critic reviews of albums.  It tries to filter out stuff you don't
want like covers, live tracks, etc and differentiates singles from albums.

For more details, read on...

### Getting recommendations from Spotify

Soltify Radar maintains a list of all artists you've liked songs from, as well as their related artists (1st order)
and related artists of their related artist (2nd order). It assigns taste points to each artist as follows:

* Each song you've liked by the artist: +10 points (`--taste-pts0`)
* Each song you've liked by a 1st order relative: +5 points (`taste-pts1`)
* Each song you've liked by a 2nd order relative: +2 points (`--taste-pts2`)

For all artists with a taste score of 10 (`--taste-thresh`) or higher, Spotify is scanned for any releases since
last time Soltify Radar was run, or up to 60 (`--max-days`) back.

### Getting critic scores

For each selected album, we try to get a critic score from AlbumOfTheYear.org. If the album has at least 5 critic
reviews there, its score is extracted.

### Filtering

By default, Soltify Radar tries to detect and filter out certain types of albums/songs unless the override is given:

* Remasters (`--allow-remaster`)
* Live (`--allow-live`)
* Acoustic Versions (`--allow-acoustic`)
* Remixes (`--allow-remix`)
* Covers (`--allow-cover`)

Since this is not fool proof, you will be prompted about whether or not you want to keep these releases (unless you
specify `--force-filter`)

### Getting more recommendations from AlbumOfTheYear.org

Soltify Radar also uses AlbumOfTheYear.org to get a list of the top rated albums in the year(s) you are searching. If
an album meets the following criteria, it is added to your list, regardless of taste points:

* At least 5 critic reviews
* Average score of 82 (`--critic-thresh`) out of 100
* From one of the genres listed in `--critic-genres`:
    * Default: Art Pop, Contemporary Folk, Country, Folk, Indie Pop, Indie Rock, Pop, Psychedelic, Rock, Singer-Songwriter
    * For all options, see the GENRE dropdown at: https://www.albumoftheyear.org/ratings/6-highest-rated/2023/1

### Sorting the list

Once all of the releases are gathered, the critic score and taste score are normalized, then combined to get an overall
score as follows:
  * Overall Score = Critic Score * 0.25 [`--weight-critic`] + Taste Score * 0.75 [`--weight-taste`]

The songs are sorted from highest to lowest.

### Maintaining the list

The output of Soltify Radar goes into two places:

* Spotify Playlists: "Soltify Radar: Albums" and "Soltify Radar: Singles"
* Local files: soltify_radar_albums.csv and soltify_radar_singles.csv

The intended use is that the playlists act as your music queues. After you listen to something or decide
you don't want it, you can delete it from the playlists and Soltify Radar won't add it back.

The .csv files should be treated as Read-Only and never deleted. These save your history and are also
available to let you see more info (each albums' critic rating, similarity score, etc)

Each time you run Soltify, it will do a few maintainence steps:
* Lookup latest critic scores for each album on the list
* If an album is released featuring songs from your single list, they are removed from the single list
* If you've liked new songs, taste scores are updated and we scan any new artists

### Examples

* Example 1: Run with default parameters (standard usage)

`python soltify_radar.py`

* Example 2: Get fewer suggestions from Spotify (songs have to be more similar to your tastes)

`python soltify_radar.py --taste-thresh=50`

* Example 3: Get fewer suggestions from critics (songs have to have higher score and be specific genre)

`python soltify_radar.py --critic-thresh=90 --critic-genres Rock Singer-Songwriter`

* Example 4: Get all releases from the past year

`python soltify_radar.py --max-days=365`

* Example 5: Turn off filtering of songs

`python soltify_radar.py --allow-remaster --allow-cover --allow-live --allow-acoustic --allow-remix`

* Example 6: Sort playlist by critic score

`python soltify_radar.py --weight-critic=1.0 --weight-taste=0.0`

* For more detailed usage, run:

`python soltify_radar.py -h`

## Soltify Memories (coming soon)

Requested by Phil "The Thrill" Frandina.

Sometimes you listen to a song a few times and like it, but then you forget about it. This tool tries
to find those songs are remind you. It creates a playlist that specifically excludes anything you've listened
to very recently, but tries to find songs that you listened to multiple times in the past or "Liked" in the
past.  Optionally, it can add songs from related artists who you haven't heard to give it a Discover Weekly
kind of vibe.

## Soltify Playlist Builder (coming soon)

Create a playlist that contains a subset of songs from your liked songs.  Options include:

* Include all songs liked after a certain date
* Exclude songs liked before a certain date
* Include only certain artists from a list
* Exclude certain artists from a list
* Include only songs that are within a certain range of BPM (beats per minute)
* Include only songs in certain genres from a list
* Exclude songs from certain genres from a list
* Exclude songs over a certain length
* Make playlist a specified size or length
* Set maximum number of songs from a single artist
* Make playlist's artist counts proportional to the totals from each artist

## Soltify Bracket Builder (coming soon)

Turn a single playlist into a music bracket! This tool takes in a playlist of songs, seeds them, and creates
a bracket playlist and score sheet. Songs can be seeded based on playlist order (e.g. 1st song = 1 seed) or Spotify
popularity.  When using popularity, you can choose to favor songs you've personally liked and/or give each album
or artist a fair chance (e.g. if there are 5 albums, the 1st 5 seeds are the most popular songs from each album, etc).
You can also choose advanced features to avoid putting an artist or album against itself in early rounds.

## Soltify Bracket Builder Plus (coming soon)

Turn multiple playlists submitted by separate people into combined music brackets for each person! Each playlist is
treated as an ordered list of song nominations for a different person.  The songs are combined together, and each
person is given a custom music bracket with picks from all of them. Optionally, a matrix of scale factors for each
person can be given (e.g. give User A more of User B's songs).  Optionally, you can require that all songs are released
in the same year.

## Soltify History (coming soon)

Build a cumulative history of your Spotify music listening history by combining exports from Spotify.

# How To Run

## Spotify Setup

1. Login to https://developer.spotify.com/dashboard/ with your Spotify username and password
    - You *might* have to make a special developers account? I don't remember

2. Register an app
    - Click "Create app"
    - Enter an App Name (it can be "Soltify" or whatever you want)
    - Enter the following under Redirect URI: https://localhost:8888/callback
    - Check "I understand and agree..." and click Save

3. Get your Client ID and Client Secret
    - Click on your newly created app
    - Click Settings
    - Click "View client secret"
    - It should now show a Client ID and Client Secret

4. Set environment variables
    - Windows
        - Type "Edit the system environment variables" in search bar to bring up settings
        - Click "Environment Variables"
        - In the "System variables" panel (the bottom one), click "New..." 3 times to add 3 variables:
            - SPOTIPY_REDIRECT_URI = https://localhost:8888/callback
            - SPOTIPY_CLIENT_ID = (paste your client ID from Spotify)
            - SPOTIPY_CLIENT_SECRET = (paste your client secret from Spotify)
        - Make sure to click OK on every window to save
        - If you have Command Prompt open, close it to let the settings take effect
    - Mac
        - Open terminal and type `ls -a` to list all files
        - Depending on your version of Mac, you will have a file called .profile, .bash_profile, or
            .zprofile
        - Open that file in a text editor by typing `open -e [filename]`
        - Add the following lines to the end of it:
            ```
            export SPOTIPY_REDIRECT_URI=https://localhost:8888/callback
            export SPOTIPY_CLIENT_ID=(paste your client ID from Spotify)
            export SPOTIPY_CLIENT_SECRET=(paste your client secret from Spotify)
            ```
        - Save file and close terminal for settings to take effect

## Installation

1. Download and install python: https://www.python.org/downloads/
2. Download and unzip Soltify:
    - Go to https://github.com/msol272/soltify
    - Click Code -> Download ZIP
    - Unzip the files
3. Install the necessary libraries
    - Open Terminal (on Mac) or Command Prompt (on Windows)
    - Type `pip install spotipy requests_html`

## Running the tools

1. If you're on Mac, open Finder and click "View -> Path Bar"
2. Navigate to the `soltify-main` folder that contains files like README.md, etc and copy the path from the path bar
3. Open Terminal (on Mac) or Command Prompt (on Windows) and navigate to that path by typing `cd <path>`
    - Example: `cd C:\Users\msolt\Downloads\soltify-main\soltify-main`
4. Run a tool by typing a command as described in README.md:
    - Example `python soltify_shuffle.py "My Playlist"`

NOTE: The first time you run one of the tools, it will open a webpage in your browser and maybe ask you to login to Spotify.
Then, it will bring you to a blank webpage and you will need to copy/paste the URL from your web browser to Terminal/Command Prompt.
After that works once, it should never happen again.
