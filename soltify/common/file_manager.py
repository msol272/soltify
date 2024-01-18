"""
Soltify/Common/File Manager

Helper functions related to reading and writing spotify data to and from files
"""
import csv
import os
import pickle
import re

# Hard-coded filenames
LIBRARY_FILENAME = "library.pkl"
RELEASE_ALBUMS_FILENAME = "soltify_radar_albums.csv"
RELEASE_SINGLES_FILENAME = "soltify_radar_singles.csv"
TASTE_PROFILE_FILENAME = "soltify_taste_profile.csv"

def library_cache_exists(directory):
    """
    Check if a cached copy of a user's library exists in this directory
    """
    path = os.path.join(directory, LIBRARY_FILENAME)
    return os.path.exists(path)

def save_library(directory, songs, artist_tree, run_time):
    """
    Save a user's library to a file that can be loaded later
    """

    # Make sure the output directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Create a valid filename and build the full path
    path = os.path.join(directory, LIBRARY_FILENAME)

    # Write the file
    data = {"songs":songs, "artist_tree":artist_tree, "run_time":run_time}
    file = open(path, "wb")
    pickle.dump(data, file)

def load_library(directory):
    """
    Load a user's library from a file that was created by a previous call to
    save_library()
    """
    path = os.path.join(directory, LIBRARY_FILENAME)

    # Make sure the file exists
    if not os.path.exists(path):
        raise RuntimeError("File does not exist: {}".format(path))

    file = open(path, 'rb')
    data = pickle.load(file)
    return data["songs"], data["artist_tree"], data["run_time"]

def save_playlist(directory, playlist_name, songs, playlist_uri):
    """
    Save a playlist's data to a file
    """

    # Make sure the output directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Create a valid filename and build the full path
    filename = _playlist_name_to_filename(playlist_name)
    path = os.path.join(directory, filename)

    # Write the file
    data = {"songs":songs, "playlist_uri":playlist_uri}
    file = open(path, "wb")
    pickle.dump(data, file)


def load_playlist(directory, playlist_name):
    """
    Load a playlist from a file that was created by a previous call to
    save_playlist()

    Returns a list of songs and the playlist's URI
    """

    # Create a valid filename and build the full path
    filename = _playlist_name_to_filename(playlist_name)
    path = os.path.join(directory, filename)

    # Make sure the file exists
    if not os.path.exists(path):
        raise RuntimeError("File does not exist: {}".format(path))

    file = open(path, 'rb')
    data = pickle.load(file)
    return data["songs"], data["playlist_uri"]

def release_lists_exist(directory):
    """
    Check if .csv files containing release radar output exist
    """
    albums_path = os.path.join(directory, RELEASE_ALBUMS_FILENAME)
    singles_path = os.path.join(directory, RELEASE_SINGLES_FILENAME)
    return os.path.exists(albums_path) and os.path.exists(singles_path)

def save_release_lists(directory, album_releases, single_releases):
    """
    Save album and single release lists to .csv files
    """
    print("TODO: save_release_lists()")

def load_release_lists(directory):
    """
    Load release list data from .csv
    """
    album_releases = []
    single_releases = []
    print("TODO: load_release_lists()")
    return album_releases, single_releases

def save_taste_profile(directory, taste):
    """
    Save taste profile to .csv file for viewing
    """
    path = os.path.join(directory, TASTE_PROFILE_FILENAME)
    with open(path, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Artist", "Score", "Liked Songs", "Liked Related"])
        for artist_name, entry in taste.items():
            row = [
                artist_name, 
                "{:.3f}".format(entry["score"]), 
                entry["liked_songs"], 
                entry ["liked_related"]
            ]
            writer.writerow(row)

################################################################################
# Private functions
################################################################################
def _playlist_name_to_filename(playlist_name):
    """
    Convert a playlist name to a filename used for saving/loading it
    """

    # Replace invalid characters with underscores
    filename = re.sub(r'[\/:*?"<>|\s]', '_', playlist_name)

    # Remove leading and trailing whitespaces
    filename = filename.strip()

    # Remove consecutive underscores
    filename = re.sub('_+', '_', filename)

    # Add extension
    filename += ".pkl"

    return filename
