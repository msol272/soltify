"""
Soltify/Common/Spotify

Helper class, Spotify, that handles communication with a Spotify account
"""
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIFY_SCOPE = "user-library-read playlist-read-private playlist-modify-private"

class Spotify:
    """
    Represents a single connection to a Spotify account
    """

    def _lookup_playlist(self, name):
        """
        Lookup the URI of a playlist based on name. Returns None if the playlist
        is not found.
        """
        uri = None

        playlists = self.sp.current_user_playlists()
        while playlists:
            for i, playlist in enumerate(playlists['items']):
                if playlist['name'] == name:
                    uri = playlist['uri']
                    break
            if playlists["next"] and not uri:
                playlists = self.sp.next(playlists)
            else:
                playlists = None

        return uri

    def _load_playlist(self, uri):
        """
        Load all songs from a playlist to a list of dictionaries
        """
        songs = []
        results = self.sp.playlist_items(uri)
        while results:
            for i, item in enumerate(results["items"]):
                track = item['track']

                name = track["name"]
                artist = track["artists"][0]["name"]
                album = track["album"]["name"]
                uri = track["uri"]
                release_date = track["album"]["release_date"]
                added_at = item['added_at']
                popularity = track["popularity"]
                duration = track["duration_ms"]
                explicit = track["explicit"]

                song = {
                    "name": name,
                    "artist": artist,
                    "album": album,
                    "uri": uri,
                    "release_date": release_date,
                    "added_at": added_at,
                    "popularity": popularity,
                    "duration": duration,
                    "explicit": explicit
                }
                songs.append(song)
            if results["next"]:
                results = self.sp.next(results)
            else:
                results = None
        return songs

    def __init__(self):
        """
        Default constructor
        """
        self.sp = None

    def connect(self):
        """
        Create connection to account. This must be called before any other
        functions.
        """
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SPOTIFY_SCOPE))


    def load_playlist(self, playlist_name):
        """
        Find a playlist with the specified name and load a list of songs from it
        """

        # Search for a playlist with the specified name
        uri = self._lookup_playlist(playlist_name)
        if not uri:
            raise RuntimeError(
                "No playlist with name {} found in user library".format(playlist_name))

        # Load all songs from the playlist
        songs = self._load_playlist(uri)

        return songs, uri

    def create_playlist(self, name):
        """
        Create a playlist with the specified name and return its uri
        """
        uri = ""
        print("TODO: create_playlist()")
        return uri

    def load_library(self, show_progress):
        """
        Load a list of this user's saved songs
        """

        songs = []
        results = self.sp.current_user_saved_tracks()
        while results:
            for i, item in enumerate(results["items"]):
                track = item['track']

                name = track["name"]
                artist = track["artists"][0]["name"]
                album = track["album"]["name"]
                uri = track["uri"]
                release_date = track["album"]["release_date"]
                added_at = item['added_at']
                popularity = track["popularity"]
                duration = track["duration_ms"]
                explicit = track["explicit"]

                song = {
                    "name": name,
                    "artist": artist,
                    "album": album,
                    "uri": uri,
                    "release_date": release_date,
                    "added_at": added_at,
                    "popularity": popularity,
                    "duration": duration,
                    "explicit": explicit
                }
                songs.append(song)
            if results["next"]:
                results = self.sp.next(results)
                if show_progress:
                    print(".", end="", flush=True)
            else:
                results = None
        if show_progress:
            print("")
        return songs

    def load_artist_tree(self, songs):
        """
        From a list of liked songs, generate data on the number of liked songs
        by artists, related artists, and related artists of related artists
        """
        artists = []
        return artists

    def write_playlist(self, uri, songs, overwrite=True):
        """
        Add the specified songs to the playlist with the specified URI. If overwrite
        is True, then all previous content will be wiped out.
        """
        song_uris = [s["uri"] for s in songs]
        # Clear out playlist
        if overwrite:
            self.sp.playlist_replace_items(uri, [])
        # Add songs to playlist up to 100 at a time
        start_idx = 0
        while start_idx < len(song_uris):
            end_idx = min(start_idx + 100, len(song_uris))
            self.sp.playlist_add_items(uri, song_uris[start_idx:end_idx])
            start_idx = end_idx
