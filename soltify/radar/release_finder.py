"""
Soltify/Radar/ReleaseFinder

Helper functions that handle finding new releases from a list of artists via
Spotify
"""

def find_releases(sp, artists, min_time, album_releases, single_releases, filter_flags, force_filter):
    """
    Search for new releases by the given list of artists that came out between now
    and min_time. Filter out types of releases based on filter_flags, then
    add to album_releases and single_releases.
    """
    print("TODO: find_releases()")
