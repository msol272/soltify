"""
Soltify/Radar/ReleaseFinder

Helper functions that handle finding new releases from a list of artists via
Spotify
"""
from datetime import datetime, timedelta

from ..common import log
from .aoty_reader import AOTYReader

# Index of each filter. These indices align allow_flags, FILTER_KEYWORDS,
# and FILTER_NAMES
FILTER_FLAG_REMASTER = 0
FILTER_FLAG_LIVE     = 1
FILTER_FLAG_ACOUSTIC = 2
FILTER_FLAG_REMIX    = 3
FILTER_FLAG_COVER    = 4

# Keywords used to identify each type of release that can be filtered out.
# All keywords are in lowercase only.
FILTER_KEYWORDS = [
    ["remaster", "anniversary"],
    ["live"],
    ["acoustic"],
    ["remix", "version"],
    ["cover", "tribute"],
]

# Names of each filter that can be printed to the console
FILTER_NAMES = ["remastered", "live", "acoustic", "remix", "cover"]

def build_list_from_playlist(playlist):
    """
    Build a release list from a Spotify playlist's contents
    """
    print("TODO: build_list_from_playlist()")
    return []

def find_releases_spotify(album_releases, single_releases, taste, min_date, allow_flags, force_filter, sp):
    """
    Search Spotify for new releases by artists in taste profile that came out 
    between now and min_date. Certain types of releases (e.g. live, cover, remix)
    are filtered out unless the corresponding allow_flag is set. Unless 
    force_filter=True, the user will be prompted for each one to confirm.
    """

    # First, just gather a list of releases
    total = len(taste)
    new_albums = []
    new_singles = []
    log.show_progress(0, total)
    for i, artist_name in enumerate(taste):
        artist_id = taste[artist_name]["artist_id"]
        new_albums.extend(sp.get_new_albums(artist_id, min_date, False))
        new_singles.extend(sp.get_new_albums(artist_id, min_date, True))
        log.show_progress(i+1, total)

    _filter_and_add("NEW ALBUMS", album_releases, new_albums, allow_flags, force_filter)
    _filter_and_add("NEW SINGLES", single_releases, new_singles, allow_flags, force_filter)

def find_releases_aoty(album_releases, taste, min_date,
                       cutoff_t2, cutoff_t3, critic_t3, critic_t4, 
                       critic_genres, min_critics, 
                       allow_flags, force_filter):
    """
    Search AlbumOfTheYear for new releases by artists in taste profile that came out 
    between now and min_date. Certain types of releases (e.g. live, cover, remix)
    are filtered out unless the corresponding allow_flag is set. Unless 
    force_filter=True, the user will be prompted for each one to confirm.

    If it has a taste score >= cutoff_t2, it is automatically added
    If it has a taste score >= cutoff_t3, it is added if its critic rating is
      >= critic_t3.
    Otherwise, it is added if its critic rating >= critic_t4 and its in a genre
    listed in critic_genres. 
    """

    # First, just gather a list of releases
    aoty_reader = AOTYReader()
    num_days = (datetime.now().date() - min_date).days
    total_days = num_days
    page = 1
    done = False

    next_date =  datetime.now().date() - timedelta(days=1)
    last_date = min_date
    progress = 0

    new_albums = []

    log.show_progress(progress, total_days)
    while not done:
        aoty_data = aoty_reader.get_new_albums(page)
        for entry in aoty_data:
            artist = entry["artist"]
            if not artist in taste or taste[artist]["score"] < cutoff_t3:
                if entry["num_critics"] >= min_critics and entry["critic_rating"] >= critic_t4:
                    genres = aoty_reader.get_genres(entry["release_link"])
                    if _check_genre(genres, critic_genres):
                        new_albums.append(entry)
            elif taste[artist]["score"] < cutoff_t2:
                if entry["num_critics"] >= min_critics and entry["critic_rating"] >= critic_t3:
                    new_albums.append(entry)
            else:
                new_albums.append(entry)
            if entry["release_date"] <= last_date:
                log.show_progress(total_days, total_days)
                done = True
                break
            elif entry["release_date"] <= next_date:
                next_date -= timedelta(days=1)
                progress += 1
                log.show_progress(progress, total_days)
        page += 1

    # If any were found, run them through the filters
    _filter_and_add("NEW ALBUMS", album_releases, new_albums, allow_flags, force_filter)


################################################################################
# Private Functions
################################################################################
def _filter_and_add(release_type, all_releases, new_releases, allow_flags, force_filter):
    """
    Add any new releases to the full release list if they pass filter conditions
    """
    new_releases = [r for r in new_releases if not _release_in_list(r, all_releases)]

    if new_releases:
        print(f"  {release_type}:")
        print("  -----------------")
        for r in new_releases:
            if _check_filters(r, allow_flags, force_filter):
                all_releases.append(r)
        print("")

def _release_in_list(release, list):
    """
    Check if a release is already in a list of releases
    """
    found = False
    for r in list:
        if r["artist"] == release["artist"] and r["name"] == release["name"]:
            found = True
            break
    return found

def _check_filters(release, allow_flags, force_filter):
    """
    Check if this release against all enabled filters and return True if it passes
    and should be kept. This function will print to the console and possibly
    prompt the user for input.
    """
    passed = True
    name = release['name']
    artist = release["artist"]
    release_date = release["release_date"].strftime("%Y-%m-%d")
    lc_name = name.lower()
    print(f"    {artist} - {name} [{release_date}]")
    # Check each filter that is enabled
    for idx, flag in enumerate(allow_flags):
        if not flag:
            passed, override = _check_filter(lc_name, idx, force_filter)
        if not passed or override:
            break
    return passed

def _check_filter(name, flag_idx, force_filter):
    """
    Check a single filter based on flag_idx
    """
    passed = True
    override = False
    # Check if any of the keywords for this filter are in the release name
    for keyword in FILTER_KEYWORDS[flag_idx]:
        if keyword in name:
            if force_filter:
                # Filter this use without prompting the user
                print(f"    └ Ignoring {FILTER_NAMES[flag_idx]} release")
                passed = False
            else:
                # Prompt user to determine if they want to filter this release
                prompt = f"    └ Ignore this as a {FILTER_NAMES[flag_idx]} release?"
                passed = not log.prompt_user(prompt)
                override = True
            break
    return passed, override

def _check_genre(genre, allowed_genres):
    """
    Given a comma-separated list of genres, check that it includes at least
    one of the allowed genres
    """
    passed = False
    for allowed in allowed_genres:
        if allowed in genre:
            passed = True
            break
    return passed
