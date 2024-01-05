"""
Soltify/Common/File Manager

Helper functions related to reading and writing spotify data to and from files
"""
import os
import pickle
import re

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

