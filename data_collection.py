from pytomatoes import Movie
import json

with open('./movies_to_scrape.json', 'r') as f:
    data = json.load(f)

movies = {}
for row in data:
    movie = Movie(row['movie'], row['url'])
    print('Getting reviews for {}'.format(row['movie']))
    movie.get_reviews()
    movies[row['movie']] = [r.to_record() for r in movie.reviews]