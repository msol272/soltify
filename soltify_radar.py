"""
Soltify Radar

Script to find and track new music releases that you may be interested in

See README.md for full description, run with -h option for usage.
"""
import argparse
from datetime import datetime, timedelta

from soltify.common import file_manager
from soltify.common import log
from soltify.common import spotify
from soltify.common import taste_profile

from soltify.radar import release_finder
from soltify.radar import release_manager

# By default, we will only pull in highly rated albums from these Genres.
# This can be overriden with the --critic-genres flag
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

    taste_group = parser.add_argument_group("advanced taste profile parameters")
    taste_group.add_argument("--taste-pts-like", type=float, default=10,
        help="How many points an artist gets for each song you've liked by them [default:10]")
    taste_group.add_argument("--taste-pts-related", type=float, default=0.5,
        help="How many points an artist gets for each song you've liked by a related artist [default:0.5]")
    taste_group.add_argument("--taste-decay-age", type=float, default=5.0,
        help="If a liked song is more than this many years old, it will start to get less points based on age [default:5.0]")
    taste_group.add_argument("--taste-max-age", type=float, default=15.0,
        help="If a liked song is this many years old, it is excluded from the taste profile [default:15.0]")

    release_group = parser.add_argument_group("advanced release finder parameters")
    release_group.add_argument("--cutoff-t1", type=float, default=75,
        help="Any artist with a taste score above this number is considered Tier 1 and we will scan Spotify for new music for them every time [default:75]")
    release_group.add_argument("--cutoff-t2", type=float, default=30,
        help="Any artist with a taste score above this number is considered Tier 2 and we will always include new releases found on AlbumOfTheYear for them [default:30]")
    release_group.add_argument("--cutoff-t3", type=float, default=10,
        help="Any artist with a taste score above this number is considered Tier 3 and we will include new releases found on AlbumOfTheYear for them if the score is above --critic-t3 [default:10]")
    release_group.add_argument("--critic-t3", type=float, default=72,
        help="Any release from a Tier 3 artist and a critic score of this or higher is included [default:72]")
    release_group.add_argument("--critic-t4", type=float, default=82,
        help="Any release from a Tier 4 artist and a critic score of this or higher is included [default:82]")
    release_group.add_argument("--critic-genres", nargs='+', default=DEFAULT_GENRES,
        help="Only add a release from AlbumOfTheYear if its one of these genres [default:{}]".format(" ".join(["\"{}\"".format(g) for g in DEFAULT_GENRES])))
    release_group.add_argument("--min-critics", type=int, default=5,
        help="Only consider a critic rating valid if at least this many critics have reviewed the album [default:5]")
    release_group.add_argument("--max-days", type=int, default=60,
        help="Only add releases that are up to this many days old [default:60]")


    sort_group = parser.add_argument_group("advanced release sorting parameters")
    sort_group.add_argument("--weight-taste", type=float, default=75,
        help="Weight to give to this release's taste score when sorting [default:75]")
    sort_group.add_argument("--weight-critic", type=float, default=25,
        help="Weight to give to this release's critic score when sorting [default:25]")

    args = parser.parse_args()

    if args.max_days > MAX_HISTORY_DAYS:
        log.error("--max-days cannot be greater than {}. It is set to {}.".format(MAX_HISTORY_DAYS, args.max_days))
        return
    
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

    # Create a taste profile using specified parameters
    print("Building taste profile...")
    taste = taste_profile.build_taste_profile(songs, artist_tree, args.taste_pts_like, 
        args.taste_pts_related, args.taste_decay_age, args.taste_max_age)

    album_releases = []
    single_releases = []
    min_date = current_time.date() - timedelta(days=args.max_days)
    allow_flags = [args.allow_remaster, args.allow_live, args.allow_acoustic, args.allow_remix, args.allow_cover]

    print("Checking Spotify for new releases from your favorite artists...")
    taste_t1 = {artist_name:entry for artist_name, entry in taste.items() if entry["score"] >= args.cutoff_t1}
    release_finder.find_releases_spotify(album_releases, single_releases, taste_t1, 
        min_date, allow_flags, args.force_filter, sp)

    print("Checking AlbumOfTheYear for more releases...")
    release_finder.find_releases_aoty(
        album_releases, taste, min_date,
        args.cutoff_t2, args.cutoff_t3, args.critic_t3, args.critic_t4,
        args.critic_genres, args.min_critics,
        allow_flags, args.force_filter)

    print("Finalizing lists and writing output...")
    album_releases = release_manager.sort(album_releases, args.weight_taste, args.weight_critic)
    single_releases = release_manager.sort(single_releases, args.weight_taste, args.weight_critic)

    # Write all output
    file_manager.save_library(args.cache_dir, songs, artist_tree, current_time)
    file_manager.save_taste_profile(args.out_dir, taste)
    file_manager.save_release_lists(args.out_dir, album_releases, single_releases)
    print("Done!")


if __name__ == "__main__":
    main()
