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
from soltify.common import taste_profile

from soltify.radar import release_finder
from soltify.radar import release_manager
from soltify.radar import rating_finder

DEFAULT_GENRES = [
    "Art Pop",
    "Contemporary Folk",
    "Country",
    "Folk",
    "Indie Pop",
    "Indie Rock",
    "Pop",
    "Psychedelic",
    "Rock",
    "Singer-Songwriter",
]

def main():
    parser = argparse.ArgumentParser(
      description='Soltify Radar: a better new music release tracker')

    selection_group = parser.add_argument_group("release selection parameters")
    selection_group.add_argument("--max-days", type=int, default=60,
        help="Only add releases that are up to this many days old [default:60]")
    selection_group.add_argument("--taste-thresh", type=float, default=10.0,
        help="Only add a release from Spotify if its taste score is at least this value [default:10]")
    selection_group.add_argument("--critic-thresh", type=int, default=82,
        help="Only add a release from internet if its critic score (out of 100) is at least this value [default:82]")
    selection_group.add_argument("--critic-genres", nargs='+', default=DEFAULT_GENRES,
        help="Only add a release from internet if its one of these genres [default:{}]".format(" ".join(["\"{}\"".format(g) for g in DEFAULT_GENRES])))

    filter_group = parser.add_argument_group("release filtering parameters")
    filter_group.add_argument("--allow-remaster", action="store_true",
        help="Allow remaster album releases to be added")
    filter_group.add_argument("--allow-live", action="store_true",
        help="Allow live songs and albums to be added")
    filter_group.add_argument("--allow-acoustic", action="store_true",
        help="Allow acoustic versions of songs to be added")
    filter_group.add_argument("--allow-remix", action="store_true",
        help="Allow remixes to be added")
    filter_group.add_argument("--allow-cover", action="store_true",
        help="Allow cover songs to be added")
    filter_group.add_argument("--force-filter", action="store_true",
        help="Filter releases out without prompting the user first")

    file_group = parser.add_argument_group("file options")
    file_group.add_argument("--out-dir", type=str, default="soltify_output", 
        help="Directory to save/load output .csv files from (default=soltify_output)")
    file_group.add_argument("--cache-dir", type=str, default="soltify_cache", 
        help="Directory to save/load cached playlists from (default=soltify_cache)")

    scoring_group = parser.add_argument_group("advanced release scoring parameters")
    scoring_group.add_argument("--taste-pts0", type=float, default=10.0,
        help="How many points an artist gets for each song you've liked by them [default:10.0]")
    scoring_group.add_argument("--taste-pts1", type=float, default=5.0,
        help="How many points an artist gets for each song you've liked by a related artist [default:5.0]")
    scoring_group.add_argument("--taste-pts2", type=float, default=2.0,
        help="How many points an artist gets for each song you've liked by a related artist of a related artist [default:2.0]")

    sorting_group = parser.add_argument_group("advanced release sorting parameters")
    sorting_group.add_argument("--weight-taste", type=float, default=0.75,
        help="Weight factor to apply to Taste Score when calculating a release's final score for sorting [default:0.75]")
    sorting_group.add_argument("--weight-critic", type=float, default=0.25,
        help="Weight factor to apply to Critic Rating when calculating a release's final score for sorting [default:0.25]")

    args = parser.parse_args()

    # Open connection to spotify
    sp = spotify.Spotify()
    sp.connect()

    current_time = datetime.now()

    # Check if a list of liked songs has already been collected. If it has, load it now
    print("Loading Spotify library from cache...")
    if file_manager.library_cache_exists(args.cache_dir):
        [songs, artists, last_run_time] = file_manager.load_library(args.cache_dir)
    else:
        log.warning("No library found in cache. We will need to load the entire library.")

        songs = []
        artists = dict()
        last_run_time = current_time - timedelta(days=365)

    # Check if there are song lists from a previous run
    print("Loading previous run's data...")
    if file_manager.release_lists_exist(args.out_dir):
        # Load data from the .csv files
        [album_releases, single_releases] = file_manager.load_release_lists(args.out_dir)
        print("Checking for removed songs in playlists...")
        # Load corresponding playlists
        albums_playlist, albums_playlist_uri = sp.load_playlist("Soltify Radar: Albums")
        singles_playlist, singles_playlist_uri = sp.load_playlist("Soltify Radar: Singles")
        # Mark any songs as removed that are no longer in the playlists
        release_manager.mark_songs_as_removed(album_releases, albums_playlist)
        release_manager.mark_songs_as_removed(single_releases, singles_playlist)
    else:
        log.warning("No previous runs found. Creating new data...")
        album_releases = []
        single_releases = []
        albums_playlist_uri = sp.create_playlist("Soltify Radar: Albums")
        singles_playlist_uri = sp.create_playlist("Soltify Radar: Singles")

    # Check for any newly liked songs
    print("Loading updates from Spotify library...")
    print("TODO: Skipping because this takes long")
    # songs = sp.load_library(True)
    songs = []
    artists = sp.load_artist_tree(songs)

    # Calculate taste scores for each artist and filter based on taste_thresh
    taste_scores = taste_profile.assign_scores(artists, args.taste_pts0, args.taste_pts1, args.taste_pts2)
    taste_profile.sort_and_filter(taste_scores, args.taste_thresh)

    # Search spotify for new releases
    print("Searching for new releases...")
    min_time = current_time - timedelta(days=args.max_days)
    filter_flags = [args.allow_remaster, args.allow_live, args.allow_acoustic, args.allow_remix, args.allow_cover]
    release_finder.find_releases(sp, artists, max(min_time, last_run_time), album_releases, single_releases, filter_flags, args.force_filter)

    # Lookup critic scores for all releases in list (both old and new)
    print("Searching for critic reviews...")
    rating_finder.find_critic_ratings(album_releases)

    # Find more releases based on critic score
    print("Searching for highly rated albums we missed...")
    rating_finder.add_top_albums(album_releases, args.critic_thresh, min_time, args.critic_genres)

    # Sort release list
    print("Finalizing lists and writing output...")
    release_manager.sort(album_releases, args.weight_taste, args.weight_critic)
    release_manager.sort(single_releases, 0.0, 1.0)

    # Write all output
    file_manager.save_release_lists(args.out_dir, album_releases, single_releases)
    album_uris = release_manager.get_songs_for_playlist(album_releases)
    single_uris = release_manager.get_songs_for_playlist(single_releases)
    print("TODO: Skipping because these will fail with no valid uris")
    # sp.write_playlist(albums_playlist_uri, album_uris, True)
    # sp.write_playlist(singles_playlist_uri, singles_uris, True)
    file_manager.save_library(args.cache_dir, songs, artists, current_time)
    print("Done!")


if __name__ == "__main__":
    main()
