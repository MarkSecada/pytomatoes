# PyTomatoes

PyTomatoes is a web scraper for movie reviews on RottenTomatoes.

# Usage

Using PyTomatoes is simple. Pass the name of the movie, and the URL of all its reviews, and you'll be able to retrieve the reviews' authors, publication dates, blurbs, and score.

You could get all reviews for `Dumbo` below:

```python
from pytomatoes import Movie

name = "Dumbo"
url = "https://www.rottentomatoes.com/m/dumbo_2019/reviews/"
dumbo = Movie(name, url)
dumbo.get_reviews()
print(dumbo.reviews[0].to_record())
```