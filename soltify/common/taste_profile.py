"""
Soltify/Common/Taste Profile

Helper functions related to creating a taste profile for you based on your liked
songs and scoring artists against that profile
"""
import copy
from datetime import datetime, timedelta

from . import log

def update_taste_profile(songs, taste, taste_years, sp, show_progress):
    """
    From a list of liked songs, generate or update a taste profile.

    A taste profile is data on the number of liked songs by artists or related
    artists

    When necessary, connect to spotify to get related artist information
    """

    # For the list of songs, get a count of how many songs there are by each
    # artist
    min_release_date = datetime.now() - timedelta(days=365.25*taste_years)
    artist_counts, artist_names = _get_artist_counts(songs, min_release_date)
    if show_progress:
        total = len(artist_counts)
        i = 0
        log.show_progress(0, total)
    for artist_id, count in artist_counts.items():
        _add_to_taste_profile(taste, artist_names, artist_id, count, sp)
        if show_progress:
            i += 1
            log.show_progress(i, total)

def assign_scores(taste, taste_pts0, taste_pts1):
    """
    Update taste profile with scores for each artist where each liked song is
    worth taste_pts0 and each liked related song is worth taste_pts1
    """
    for artist_id in taste:
        liked = taste[artist_id]["liked_songs"]
        related = taste[artist_id]["liked_related"]
        taste[artist_id]["score"] = liked * taste_pts0 + related * taste_pts1

def sort_and_filter(taste, threshold):
    """
    Sort a taste profile by taste score and filter out any that are below
    a given threshold
    """
    taste = {artist_id:entry for artist_id, entry in taste.items() if entry["score"] > threshold}
    taste = dict(sorted(taste.items(), key=lambda item: item[1]["score"], reverse=True))
    return taste

################################################################################
# Private Functions
################################################################################

def _get_artist_counts(songs, min_release_date):
    """
    Create a dictionary of <artist_id : count> pairs summarizing a song list
    and a second dictionary of <artist_id : name> identifying each artist
    """
    counts = dict()
    names = dict()
    for song in songs:
        if song["release_date"] >= min_release_date:
            artist_id = song["artist_id"]
            if artist_id in counts:
                counts[artist_id] += 1
            else:
                counts[artist_id] = 1
                names[artist_id] = song["artist"]
    return counts, names

def _add_to_taste_profile(taste, artist_names, artist_id, liked_songs, sp):
    """
    Add a new artist to the taste profile with a specific number of liked songs
    """

    # If this is the first time we've encountered this artist, add a blank entry
    # for them
    if not artist_id in taste:
        _create_taste_profile_entry(taste, artist_names[artist_id], artist_id)

    # Populate related artist list for this artist and all of its related artists
    _populate_related_artists(taste, artist_names, artist_id, sp)

    # Make sure all related artists have entries in the taste profile
    for related in taste[artist_id]["related_artists"]:
        if not related in taste:
            _create_taste_profile_entry(taste, artist_names[related], related)

    # Update liked count
    taste[artist_id]["liked_songs"] += liked_songs
    for related in taste[artist_id]["related_artists"]:
        taste[related]["liked_related"] += liked_songs

def _create_taste_profile_entry(taste, artist_name, artist_id):
        entry = dict()

        entry["artist_name"] = artist_name
        entry["score"] = 0.0
        entry["liked_songs"] = 0
        entry["liked_related"] = 0
        entry["related_artists"] = []
        taste[artist_id] = copy.deepcopy(entry)

def _populate_related_artists(taste, artist_names, artist_id, sp):
    """
    Populate the "related_artists" field in taste profile for a given artist_id.

    If it doesn't already exist, we go out to spotify for this.
    """
    related_artists = taste[artist_id]["related_artists"]
    if not related_artists:
        related_artist_ids, related_artist_names = sp.get_related_artists(artist_id)
        taste[artist_id]["related_artists"] = copy.deepcopy(related_artist_ids)
        for i, artist_id in enumerate(related_artist_ids):
            artist_names[artist_id] = related_artist_names[i]
