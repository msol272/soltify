"""
Soltify/Common/Taste Profile

Helper functions related to creating a taste profile for you based on your liked
songs and scoring artists against that profile
"""
from datetime import datetime, timedelta

from . import log

def build_taste_profile(songs, artist_tree, pts_like, pts_related, decay_age, max_age):
    """
    From a list of liked songs and artist tree, build a taste profile that assigns
    points to each artist based on how many songs you like from them or their related
    artists in the past <max_age> years.
    """
    taste = dict()
    min_release_date = datetime.now() - timedelta(days=365.25*max_age)
    decay_release_date = datetime.now() - timedelta(days=365.25*decay_age)
    for song in songs:
        release_date = song["release_date"]
        if release_date >= decay_release_date:
            # Song was released after decay starts, so it gets full points
            _add_to_taste_profile(taste, song, artist_tree, pts_like, pts_related)
        elif release_date > min_release_date:
            # Song was released before decay starts, so it gets partial points
            decay_factor = _get_decay_factor(release_date, decay_release_date, min_release_date)
            _add_to_taste_profile(taste, song, artist_tree, pts_like*decay_factor, pts_related*decay_factor)
        else:
            # Song was released after minimum release date, so it doesn't count
            pass
    # Sort artists by score
    return dict(sorted(taste.items(), key=lambda item: item[1]["score"], reverse=True))

################################################################################
# Private Functions
################################################################################

def _add_to_taste_profile(taste, song, artist_tree, pts_like, pts_related):
    """
    Add a new song to the taste profile
    """

    # If this is the first time we've encountered this artist, add a blank entry
    # for them
    artist_id = song["artist_id"]
    artist_name = song["artist"]
    if not artist_id in taste:
        _create_taste_profile_entry(taste, artist_name, artist_id)

    taste[artist_id]["score"] += pts_like
    taste[artist_id]["liked_songs"] += 1

    # Give all related songs points
    for i, related_id in enumerate(artist_tree[artist_id]["related_ids"]):
        related_name = artist_tree[artist_id]["related_names"][i]
        if not related_id in taste:
            _create_taste_profile_entry(taste, related_name, related_id)
        taste[related_id]["score"] += pts_related
        taste[related_id]["liked_related"] += 1

def _create_taste_profile_entry(taste, artist_name, artist_id):
        entry = dict()

        entry["artist_name"] = artist_name
        entry["score"] = 0.0
        entry["liked_songs"] = 0
        entry["liked_related"] = 0
        taste[artist_id] = entry

def _get_decay_factor(release_date, max_release_date, min_release_date):
    """
    Get a decay factor from 1.0 to 0.0 based on a release date
    """
    return (release_date - min_release_date)/(max_release_date - min_release_date)
