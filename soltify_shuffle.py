"""
Soltify Shuffle

Script to shuffle a Spotify playlist better than Spotify does.

See README.md for full description, run with -h option for usage.
"""
import argparse

from soltify.common import spotify
from soltify.common import file_manager
from soltify.common import log

from soltify.shuffle import shuffle

def main():
    parser = argparse.ArgumentParser(
      description='Soltify Shuffle: a better shuffle for Spotify playlists')
    parser.add_argument("playlist", type=str, 
      help="Name of playlist to shuffle")

    shuffle_group = parser.add_argument_group("shuffle options")
    shuffle_group.add_argument("--ignoreartist", action="store_true",
      help="Do a truly random shuffle, without trying to evenly space out songs" \
           " by the same artist.")

    cache_group = parser.add_argument_group("local cache options")
    cache_group.add_argument("--cachedir", type=str, default="./soltify_cache", 
      help="Directory to save/load cached playlists from (default=./soltify_cache)")
    cache_group.add_argument("--uselocal", action="store_true", 
      help="Load the playlist from the local cache instead of reloading it from" \
           " Spotify. This will run much faster, but will not pick up any changes" \
           " made to the playlist since last time Soltify tools loaded it.")

    args = parser.parse_args()

    # Open connection to spotify
    spot = spotify.Spotify()
    spot.connect()

    # Load songs from the playlist
    if args.uselocal:
        # Try to load from a local cache file
        try:
            songs, playlist_uri = file_manager.load_playlist(args.cachedir, args.playlist)
        except RuntimeError as err:
            log.error(err)
            return
    else:  # not args.uselocal
        # Try to load from spotify
        try:
            songs, playlist_uri = spot.load_playlist(args.playlist)
        except RuntimeError as err:
            log.error(err)
            return

        # Save to the local cache for future runs
        file_manager.save_playlist(args.cachedir, args.playlist, songs, playlist_uri)

    # Shuffle the songs
    songs = shuffle.shuffle(songs, args.ignoreartist)

    # Update the playlist to be in the new shuffled order
    spot.write_playlist(playlist_uri, songs, overwrite=True)

if __name__ == "__main__":
    main()
