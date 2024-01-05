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
that you don't care about, and it always favors certain artists. Plus, sometimes if you don't check
it for a few weeks, you permanently miss a release.

Soltify Radar grabs a list of music releases from the internet each week. It then compares these
to your "Liked Songs" list and creates a similarity score. If the release is above a certain
threshold, it gets added to your queue. There are separate album queues, EP queues, and single
queues, and each will remain sorted by similarity score.

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
3. Install the spotipy library
    - Open Terminal (on Mac) or Command Prompt (on Windows)
    - Type `pip install spotipy`

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
