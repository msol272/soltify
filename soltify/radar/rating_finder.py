"""
Soltify/Radar/RatingFinder

Helper functions that handle loading critic ratings from the internet
(albumoftheyear.org)
"""
import requests_html

def find_critic_ratings(album_releases):
    """
    Look up the specified albums and save their critic ratings. Add that information
    to the list.
    """
    print("TODO: find_critic_ratings()")

def add_top_albums(album_releases, rating_threshold, min_time, genres):
    """
    Search for albums with a rating above threshold and date after min_time in
    any of the specified genres and add them to the album_releases list.
    """
    print("TODO: add_top_albums()")


"""
Note: the code below works

self.sess = requests_html.HTMLSession()
page = 1
while True:
    if page == 1:
        response = self.sess.get(f'https://www.albumoftheyear.org/releases')
    else:
        response = self.sess.get(f'https://www.albumoftheyear.org/releases/{page}')
elements = response.html.find(".albumBlock")
for e in elements:
    date = e.find(".date", first=True).text
    artist = e.find(".artistTitle", first=True).text
    album = e.find(".albumTitle", first=True).text
    ratings = [float(r.text) for r in e.find(".rating")]
    if ratings:
        avg_rating = sum(ratings)/len(ratings)
    else:
        avg_rating = 0.0
    print("{}: {} - {}".format(date,artist,album))
    print(avg_rating)
"""
