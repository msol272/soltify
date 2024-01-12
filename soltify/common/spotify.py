"""
Soltify/Common/Spotify

Helper class, Spotify, that handles communication with a Spotify account
"""
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from datetime import datetime

from . import log
from . import taste_profile

SPOTIFY_SCOPE = "user-library-read playlist-read-private playlist-modify-private"

class Spotify:
    """
    Represents a single connection to a Spotify account
    """
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

    def playlist_exists(self, name):
        """
        Check if a playlist exists with the specified name
        """
        print("TODO: playlist_exists()")
        return False

    def create_playlist(self, name):
        """
        Create a playlist with the specified name and return its uri
        """
        uri = ""
        print("TODO: create_playlist()")
        return uri

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

    def load_library(self, songs, show_progress):
        """
        Given a list of songs that have already been loaded, read this user's
        saved song list and return a list of any new songs that aren't already
        in that list. If show_progress=True, it will print dots to the console to
        show that it is running (useful for long runs)
        """
        new_songs = []
        results = self.sp.current_user_saved_tracks()
        total = results["total"]
        progress = 0
        done = False
        if show_progress:
            log.show_progress(0, total)

        while results:
            for i, item in enumerate(results["items"]):
                track = item['track']

                name = track["name"]
                artist = track["artists"][0]["name"]
                artist_id = track["artists"][0]["id"]
                album = track["album"]["name"]
                uri = track["uri"]
                release_date = self._get_release_date(track["album"])
                added_at = item['added_at']
                popularity = track["popularity"]
                duration = track["duration_ms"]
                explicit = track["explicit"]

                song = {
                    "name": name,
                    "artist": artist,
                    "artist_id": artist_id,
                    "album": album,
                    "uri": uri,
                    "release_date": release_date,
                    "added_at": added_at,
                    "popularity": popularity,
                    "duration": duration,
                    "explicit": explicit
                }
                if self._uri_in_song_list(songs, uri):
                    # Assumption: Songs are always in order by date added.
                    # If we get to one that's already in the song list, all of the
                    # rest of the list will also be in the songlist
                    done = True
                    break
                else:
                    # If this song is not in the list, add it now
                    new_songs.append(song)
            progress += len(results["items"])
            if results["next"] and not done:
                results = self.sp.next(results)
            else:
                results = None
            if show_progress:
                log.show_progress(progress, total)

        return new_songs

    def get_related_artists(self, artist_id):
        """
        Get a list of related artists for an artist based on its ID
        """
        result = self.sp.artist_related_artists(artist_id)
        artist_ids = []
        artist_names = []
        for artist in result["artists"]:
            artist_ids.append(artist["id"])
            artist_names.append(artist["name"])
        return artist_ids, artist_names

    def get_new_albums(self, artist_id, min_time, singles):
        """
        Get a list of all albums that an artist has released since a specific date.

        If singles=True, return singles & eps. If singles=False, return full albums.
        """
        albums = []
        done = False
        if singles:
            atype = "single"
        else:
            atype = "album,appears_on"
        results = self.sp.artist_albums(artist_id, album_type=atype, limit=50)
        while results:
            for i, item in enumerate(results["items"]):
                album = {
                    "name": item["name"],
                    "artist": item["artists"][0]["name"],
                    "id": item["id"],
                    "release_date": self._get_release_date(item)
                }
                if album["release_date"] < min_time:
                    done = True
                    break 
                else:
                    albums.append(album)
            if results["next"] and not done:
                results = self.sp.next(results)
            else:
                results = None
        return albums

    def get_artists_singles(self, artist_id):
        """
        Get a list of all singles (or eps) that an artist released
        """
        singles = []
        results = self.sp.artist_albums(artist_id, album_type="single", limit=50)
        while results:
            for i, item in enumerate(results["items"]):
                single = {
                    "name": item["name"],
                    "id": item["id"],
                    "release_date": self._get_release_date(item)
                }
                singles.append(single)
            if results["next"]:
                results = self.sp.next(results)
            else:
                results = None
        return singles

    ############################################################################
    # Private Functions
    ############################################################################
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
                artist_id = track["artists"][0]["id"]
                album = track["album"]["name"]
                uri = track["uri"]
                release_date = self._get_release_date(track["album"])
                added_at = item['added_at']
                popularity = track["popularity"]
                duration = track["duration_ms"]
                explicit = track["explicit"]

                song = {
                    "name": name,
                    "artist": artist,
                    "artist_id": artist_id,
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

    def _uri_in_song_list(self, songs, uri):
        """
        Check if a song is already in a songlist, based solely on URI.
        """
        return any(s["uri"] == uri for s in songs)

    def _get_release_date(self, item):
        """
        Extract release date as a datetime object
        """
        precision = item["release_date_precision"]
        release_string = item["release_date"]
        if precision == "day":
            release_date = datetime.strptime(release_string, "%Y-%m-%d")
        elif precision == "month":
            tokens = release_string.split("-")
            year = int(tokens[0])
            month = int(tokens[1])
            day = 28
            release_date = datetime(year, month, day)
        else:
            year = int(release_string)
            month = 12
            day = 31
            release_date = datetime(year, month, day)
        return release_date
