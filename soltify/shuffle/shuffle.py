"""
Soltify/Shuffle/Shuffle

Helper functions that handle shuffling a list of songs
"""
import random

def _bin_songs_by_artist(songs):
    """
    Organize songs into bins by the artist name
    """
    bins = dict()
    for song in songs:
        artist = song["artist"]
        if not artist in bins:
            bins[artist] = []
        bins[artist].append(song)
    return bins

def _sort_bins_by_size(bins):
    """
    Sort bins from largest to smallest
    """
    bins = dict(sorted(bins.items(), key=lambda item:-len(item[1])))
    return bins


def shuffle(songs, ignore_artist):
    """
    Shuffle a list of songs. By default, this is a pseudo-random shuffle that
    intentionally spaces songs by the same artist out.  If ignore_artist=True,
    then it is purely pseudo-random.
    """
    
    # Create a list of available indices for final list and a blank list
    num_songs = len(songs)
    indices = [i for i in range(0, num_songs)]
    shuffled = [None] * num_songs

    bins = dict()
    if ignore_artist:
        # Add songs to the shuffled list in a random order
        for song in songs:
            index = random.choice(indices)
            indices.remove(index)
            shuffled[index] = song
    else:
        # Bin songs by artist
        bins = _bin_songs_by_artist(songs)
        bins = _sort_bins_by_size(bins)
        # For each artist (starting with the largest bin)
        for artist, songlist in bins.items():
            # target_spacing: if this artist was evenly distributed across the
            # playlist, there would be one song by them every target_spacing songs.
            target_spacing = len(indices)/len(songlist)
            # To choose the location of the first song by this artist, choose
            # any random index between 0 and target_spacing
            i = random.randint(0, int(target_spacing)-1)
            while songlist:
                # Get the i-th remaining index.
                index = indices[int(i)]
                # Choose a random song from the bin
                song = random.choice(songlist)
                songlist.remove(song)
                # Add it at the chosen index
                shuffled[index] = song
                indices.remove(index)
                i -= 1  # Because indices lost an element
                # After 1st song, space the songs evenly across the remaining
                # playlist
                i += target_spacing
    return shuffled
