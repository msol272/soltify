"""
Soltify Radar

Script to find and track new music releases that you may be interested in

See README.md for full description, run with -h option for usage.
"""
import argparse
from datetime import datetime, timedelta

from soltify.common import spotify
from soltify.common import file_manager
from soltify.common import log

# Maximum number of days to look back for new releases
MAX_HISTORY_DAYS = 365

def main():
    parser = argparse.ArgumentParser(
      description='Soltify Radar: a better new music release tracker')

    file_group = parser.add_argument_group("file options")
    file_group.add_argument("--out-dir", type=str, default="soltify_output", 
        help="Directory to save/load output .csv files from (default=soltify_output)")
    file_group.add_argument("--cache-dir", type=str, default="soltify_cache", 
        help="Directory to save/load cached playlists from (default=soltify_cache)")


    args = parser.parse_args()
    current_time = datetime.now()

    # Open connection to spotify
    sp = spotify.Spotify()
    sp.connect()

    # Check if this user's library has previously been saved. If it has, load it now
    print("Loading Spotify library from cache...")
    if file_manager.library_cache_exists(args.cache_dir):
        [songs, artist_tree, last_run_time] = file_manager.load_library(args.cache_dir)
    else:
        log.warning("No library found in cache. We will need to load the entire library.")
        songs = []
        artist_tree = dict()
        last_run_time = current_time - timedelta(days=MAX_HISTORY_DAYS)

    # Read this user's library from Spotify and update song list and artist tree
    # to include all songs that they've saved
    print("Loading updates from Spotify library...")
    sp.load_library(songs, artist_tree)

    # Write all output
    print("Finalizing lists and writing output...")
    file_manager.save_library(args.cache_dir, songs, artist_tree, current_time)
    print("Done!")


if __name__ == "__main__":
    main()
