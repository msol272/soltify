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
