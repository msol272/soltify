"""
Soltify/Common/Taste Profile

Helper functions related to creating a taste profile for you based on your liked
songs and scoring artists against that profile
"""

def assign_scores(artists, taste_pts0, taste_pts1, taste_pts2):
    """
    Create scores for each artist based on how many liked songs are by them
    (taste_pts0), by a related artist (taste_pts1), or by a related artist of
    a related artist (taste_pts2)
    """
    scores = []
    print("TODO: assign_scores()")
    return scores

def sort_and_filter(scores, threshold):
    """
    Sort a list of artists by taste score and filter out any that are below
    a given threshold
    """
    print("TODO: sort_and_filter()")
