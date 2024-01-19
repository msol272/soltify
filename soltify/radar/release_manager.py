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
    release_list = _assign_ranks(release_list, "taste_score")
    release_list = _assign_ranks(release_list, "critic_rating")
    release_list = _assign_score(release_list, weight_taste, weight_critic)
    release_list = sorted(release_list, key=lambda x: (x["removed"],-x["sort_score"]))
    return release_list

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

################################################################################
# Private Functions
################################################################################
def _assign_ranks(release_list, field):
    """
    Add a field to the release list dictionaries that gives their rank, from
    highest to lowest, based on a specific field
    """
    release_list = sorted(release_list, key=lambda x: x[field], reverse=True)

    prev_rank = 1
    prev_value = 0
    for rank, release in enumerate(release_list, start=1):
        if release[field] == prev_value:
            release[f"{field}_rank"] = prev_rank
        else:    
            release[f"{field}_rank"] = rank
            prev_rank = rank
            prev_value = release[field]
    return release_list

def _assign_score(release_list, weight_taste, weight_critic):
    """
    Add a field to the release list dictionaries that gives their final sort score
    """
    total = len(release_list)
    for release in release_list:
        taste_pts = total - release["taste_score_rank"]
        critic_pts = total - release["critic_rating_rank"]
        release["sort_score"] = taste_pts * weight_taste + critic_pts * weight_critic
    return release_list
