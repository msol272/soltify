"""
Soltify/Radar/AOTYReader

Helper class that handle reading data from albumoftheyear.org
"""
import requests_html
from datetime import datetime, timedelta

class AOTYReader:
    def __init__(self):
        self.sess = requests_html.HTMLSession()

    def get_new_albums(self, page):
        """
        Load one page worth of new albums
        """
        entries = []
        if page == 1:
            response = self.sess.get(f'https://www.albumoftheyear.org/releases')
        else:
            response = self.sess.get(f'https://www.albumoftheyear.org/releases/{page}/')
        elements = response.html.find(".albumBlock")
        for e in elements:
            date_element = e.find(".date", first=True)
            artist = e.find(".artistTitle", first=True).text
            album = e.find(".albumTitle", first=True).text
            entry = dict()
            entry["release_date"] = self._get_release_date(date_element)
            entry["artist"] = artist
            entry["name"] = album
            entry["critic_rating"], entry["num_critics"] = self._get_critic_rating(e)
            entry["release_link"] = self._get_album_link(e)
            entries.append(entry)
        return entries

    def get_genres(self, link):
        """
        Get an album's genre string given a link to the albums page. This will
        be a comma seperated list of genres
        """
        response = self.sess.get(f'https://www.albumoftheyear.org/{link}')
        info_box = response.html.find(".albumTopBox")[-1]
        # Genre is the 4th "detailRow""
        return info_box.find(".detailRow")[3].text

################################################################################
# Private functions
################################################################################    
    def _get_release_date(self, date_element):
        """
        From a date element, create a datetime object representing the most 
        recent occurence of that date. There are 3 possibilities:

        1. date_element has text in the format "Jan 6", assume its the most recent year
        2. date_element has text in the format "Jan", assume its the 1st day of that month
        3. date_element is None. Assume its Jan 1 of this year.
        """
        
        # Add a year to the date (note: for now we assume it's this year, not last year)
        current_year = datetime.now().year
        
        if not date_element:
            full_date_str = f"Jan 1 {current_year}"
        elif len(date_element.text) == 3:
            full_date_str = f"{date_element.text} 1 {current_year}"
        else:
            full_date_str = f"{date_element.text} {current_year}"

        # Convert to a datetime object
        date = datetime.strptime(full_date_str, "%b %d %Y").date()

        # Check if it is in the future. If it is, set it to last year
        if date > datetime.now().date():
            date = date.replace(year=current_year-1)

        return date

    def _get_critic_rating(self, element):
        """
        Parse an Album's HTML element to get its critic rating (if available)
        and the total number of critic reviews
        """
        critic_score = 0.0
        num_critics = 0
        for rating_row in element.find(".ratingRow"):
            rating_texts = rating_row.find(".ratingText")
            if rating_texts[0].text == "critic score":
                critic_score = float(rating_row.find(".rating", first=True).text)
                num_critics_str = rating_texts[1].text.replace("(", "").replace(")", "")
                num_critics = int(num_critics_str)
                break
        return critic_score, num_critics

    def _get_album_link(self, element):
        """
        Parse an Album's HTML element to get a link to the album's page
        """

        # Each link uses "a" as its seperator, and we want the 2nd link because
        # the first is the artist page.
        link_element = element.find("a")[-1]

        return link_element.attrs["href"]
