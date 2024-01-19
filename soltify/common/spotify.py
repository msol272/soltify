"""
Soltify/Common/Spotify

Helper class, Spotify, that handles communication with a Spotify account
"""
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from datetime import datetime, date

from . import log
from . import taste_profile

# Scope to use when connecting to spotify API
SPOTIFY_SCOPE = "user-library-read playlist-read-private playlist-modify-private"

# When loading library or playlist, show a progress bar if we are loading this
# many songs or more
LOAD_PROGRESS_THRESHOLD = 50

# When loading library or playlist, show a list of added songs if we are loading
# this many songs or less
LOAD_SONGLIST_THRESHOLD = 50

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
        songs = []
        results = self.sp.playlist_items(uri)
        self._load_song_list(results, songs)

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

    def load_library(self, songs, artist_tree):
        """
        Read this user's saved tracks and add information about any missing songs
        to the provided song list and artist_tree.

        We assume that songs are sorted by most recently added, so we stop when
        we encounter the first song that's already in the list.
        """
        results = self.sp.current_user_saved_tracks()
        self._load_song_list(results, songs, artist_tree)

    def get_new_albums(self, artist_id, min_date, singles):
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
                    "release_date": self._get_release_date(item),
                    "critic_rating": 0.0,
                    "removed": False
                }
                if album["release_date"] < min_date:
                    done = True
                    break 
                else:
                    albums.append(album)
            if results["next"] and not done:
                results = self.sp.next(results)
            else:
                results = None
        return albums

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

    def _load_song_list(self, results, songs, artist_tree = None):
        """
        Load all songs from a playlist to a list of dictionaries
        """
        done = False
        total = results["total"] - len(songs)
        new_songs = []

        if total >= LOAD_PROGRESS_THRESHOLD:
            show_progress = True
            log.show_progress(0, total)
        else:
            show_progress = False
        while results:
            for i, item in enumerate(results["items"]):
                track = item['track']

                artist_name = track["artists"][0]["name"]
                artist_id =  track["artists"][0]["id"]
                uri = track["uri"]
                song = {
                    "name": track["name"],
                    "artist": artist_name,
                    "artist_id": artist_id,
                    "album": track["album"]["name"],
                    "uri": uri,
                    "release_date": self._get_release_date(track["album"]),
                    "added_at": item['added_at'],
                    "popularity": track["popularity"],
                    "duration": track["duration_ms"],
                    "explicit": track["explicit"]
                }
                if self._uri_in_song_list(songs, uri):
                    done = True
                    break
                else:
                    new_songs.append(song)
                    if artist_tree != None and not artist_id in artist_tree:
                        self._add_to_artist_tree(artist_id, artist_name, artist_tree)
            if not done and results["next"]:
                if show_progress:
                    log.show_progress(len(new_songs), total)
                results = self.sp.next(results)
            else:
                results = None

        # Ensure that the progress bar ends at 100%
        if show_progress:
            log.show_progress(total, total)

        # Print summary of songs that were added
        added = len(new_songs)
        if added == 0:
            print("  No new tracks found")
        elif added <= LOAD_SONGLIST_THRESHOLD:
            print(f"  {added} new tracks added:")
            for song in new_songs:
                artist = song["artist"]
                name = song["name"]
                print(f"    {artist} - {name}")
        else:
            print(f"  {added} new tracks added.")

        songs.extend(new_songs)
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
            release_date = datetime.strptime(release_string, "%Y-%m-%d").date()
        elif precision == "month":
            tokens = release_string.split("-")
            year = int(tokens[0])
            month = int(tokens[1])
            day = 28
            release_date = date(year, month, day)
        else:
            year = int(release_string)
            month = 12
            day = 31
            release_date = date(year, month, day)
        return release_date

    def _add_to_artist_tree(self, artist_id, artist_name, artist_tree):
        """
        Get a list of related artists for an artist based on its ID
        """
        entry = dict()
        entry["name"] = artist_name
        entry["related_ids"] = []
        entry["related_names"] = []

        result = self.sp.artist_related_artists(artist_id)
        for artist in result["artists"]:
            entry["related_ids"].append(artist["id"])
            entry["related_names"].append(artist["name"])

        artist_tree[artist_id] = entry
