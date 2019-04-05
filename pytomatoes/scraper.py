import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime

class Movie:

    """Movie on RottenTomatoes.

    Params
    ------
    name : str, required
        Name of the movie.
    url : str, required
        URL to the page of all its reviews.

    Attr
    ----
    reviews : List[Dict]
        List of reviews, where each review is
        a dictionary. Initialized to an empty list.
    """

    def __init__(self, name, url):
        self.name = name
        if '/reviews/' not in url:
            self.url = '{}/reviews/'.format(url)
        else:
            self.url = url
        self.url = url
        self.reviews = []

    def get_reviews(self):
        review_pages = self._get_review_pages()
        for i, page in enumerate(review_pages):
            if i > 0 and (i + 1) % 5 == 0:
                time.sleep(5)
            self._get_reviews_on_page(page)

    def unpack_reviews(self):
        unpacked_reviews = []
        for review in self.reviews:
            record = review.to_record()
            record['name'] = self.name
            record['url'] = self.url
            record['date'] = record['date'].strftime('%Y-%m-%d')
            unpacked_reviews.append(record)
        return unpacked_reviews

    def _get_review_pages(self):
        base_url = self.url
        r = requests.get(base_url)
        soup = BeautifulSoup(r.content, features='html.parser')
        page_info = soup.find('span', class_='pageInfo').text
        pages = int(page_info.split(' ')[-1])
        if pages == 1:
            return [base_url]
        else:
            review_pages = []
            for i in range(1, pages + 1):
                review_pages.append('{}?page={}&sort='.format(base_url, i))
            return review_pages

    def _get_reviews_on_page(self, page):
        r = requests.get(page)
        soup = BeautifulSoup(r.content, features='html.parser')
        reviews = soup.find_all('div', class_='row review_table_row')
        for review in reviews:
            self.reviews.append(Review(review))

class Review:

    """Review of a movie.
    """

    def __init__(self, review):
        self.review = review

    def to_record(self):
        return dict(critic=self.critic,
            is_fresh=self.is_fresh,
            date=self.date,
            text=self.text)

    @property
    def critic(self):
        critic_class = 'col-sm-13 col-xs-24 col-sm-pull-4 critic_name'
        return self.review.find('div', class_=critic_class).a.text

    @property
    def is_fresh(self):
        fresh_class = 'review_icon icon small fresh'
        if self.review.find('div', class_=fresh_class) is None:
            return 0
        else:
            return 1

    @property
    def date(self):
        date_class = 'review_date subtle small'
        date = self.review.find('div', class_=date_class).text
        return datetime.strptime(date.strip(), '%B %d, %Y').date()

    @property
    def text(self):
        text = self.review.find('div', class_='the_review').text
        return text.strip()