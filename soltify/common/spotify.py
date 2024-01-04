"""
Soltify/Common/Spotify

Helper class, Spotify, that handles communication with a Spotify account
"""

class Spotify:
    """
    Represents a single connection to a Spotify account
    """

    def __init__(self):
        """
        Default constructor
        """
        pass

    def connect(self):
        """
        Create connection to account. This must be called before any other
        functions.
        """
        pass

    def load_playlist(self, playlist_name):
        """
        Find a playlist with the specified name and load a list of songs from it
        """
        songs = []
        uri = ""
        return songs, uri

    def write_playlist(self, uri, songs, overwrite=True):
        """
        Add the specified songs to the playlist with the specified URI. If overwrite
        is True, then all previous content will be wiped out.
        """
        pass
