"""
Soltify/Radar/ReleaseManager

Helper functions for working with a release list (e.g. sorting, removing, 
getting data, etc)
"""

def sort(release_list, weight_taste, weight_critic):
    """
    Calculate an overall score for each release in a list by applying weights
    to the taste score and critic score, then sort by the overall score
    """
    print("TODO: sort()")

def get_songs_for_playlist(release_list):
    """
    Get a list of songs that should be added to a playlist (e.g. all that are not
    removed) and return a list of their uris.
    """
    songs = []
    print("TODO: get_songs_for_playlist()")
    return songs


def mark_songs_as_removed(release_list, playlist_songs):
    """
    Compare list of songs from playlist to a release list and mark any songs
    that are no longer in the playlist as removed
    """
    print("TODO: mark_songs_as_removed()")
