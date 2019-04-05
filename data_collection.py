from datetime import datetime
from pytomatoes import Movie
import csv
import json

with open('./movies_to_scrape.json', 'r') as f:
    data = json.load(f)

reviews = []
for row in data:
    movie = Movie(row['movie'], row['url'])
    print('Getting reviews for {}'.format(row['movie']))
    movie.get_reviews()
    movie_reviews = movie.unpack_reviews()
    for review in movie_reviews:
        reviews.append(review)

with open('./test_data.csv', 'w') as f:
    header = list(reviews[0].keys())
    csv_writer = csv.DictWriter(f, fieldnames=header)
    csv_writer.writeheader()
    for review in reviews:
        csv_writer.writerow(review)