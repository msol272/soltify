"""
Soltify/Radar/ReleaseFinder

Helper functions that handle finding new releases from a list of artists via
Spotify
"""
from ..common import log

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

def find_releases_t1(album_releases, single_releases, taste, min_time, allow_flags, force_filter, sp):
    """
    Search for new releases by artists in taste profile that came out between now
    and min_time. Certain types of releases (e.g. live, cover, remix) are filtered
    out unless the corresponding allow_flag is set. Unless force_filter=True,
    the user will be prompted for each one to confirm.
    """

    # First, just gather a list of releases
    total = len(taste)
    albums = []
    singles = []
    log.show_progress(0, total)
    for i, artist_id in enumerate(taste):
        albums.extend(sp.get_new_albums(artist_id, min_time, False))
        singles.extend(sp.get_new_albums(artist_id, min_time, True))
        log.show_progress(i+1, total)

    # If any were found, run them through the filters
    if albums:
        print("  NEW ALBUMS:")
        print("  -----------------")
        for album in albums:
            if _check_filters(album, allow_flags, force_filter):
                album_releases.append(album)
        print("")

    if singles:
        print("  NEW SINGLES:")
        print("  -----------------")
        for single in singles:
            if _check_filters(single, allow_flags, force_filter):
                single_releases.append(single)
        print("")

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


