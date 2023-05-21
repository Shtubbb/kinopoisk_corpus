import requests
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import json
import os


def get_reviews_by_id(id):
    ref = f"https://www.kinopoisk.ru/film/{id}/reviews/ord/date/status/all/perpage/25/page/1/"
    response = requests.get(ref)
    results = []
    if response.status_code != 200:
        os.system('sleep 0.01')
        return None
    soup = BeautifulSoup(response.content, 'lxml')
    film = soup.find(class_="breadcrumbs__link").get_text()
    reviews = soup.find_all(class_="_reachbanner_")
    for i in range(len(reviews)):
        res = dict()
        res['film'] = film
        res['ref'] = ref
        res['uid'] = f"{id}_{i}"
        res['content'] = reviews[i].get_text()
        results.append(res)
    return results


    
filename = 'reviews.json'
result = []
iteration = 0
start = 404900
max_num_of_films = 5000
max_total_reviews = 3000
for film in range(start, start + max_num_of_films):
    iteration += 1
    res = get_reviews_by_id(film)
    if res is None or len(res) == 0:
        continue
    print(iteration, res[0]["film"])
    result.extend(res)
    if len(result) > max_total_reviews:
        break
    os.system('sleep 0.1')

with open(filename, 'w+') as file:
    json.dump(result, file)


# check some stats
with open('reviews.json', 'r') as file:
    reviews = json.JSONDecoder().decode(file.read())
    cnt = len(reviews)
    print(f"num_reviews: {cnt}")
    sum = 0
    for i in range(len(reviews)):
        sum += len(reviews[i]["content"]) 

print(f"avg chars: {sum/cnt}")
# num_reviews: 3011
# avg chars: 2247.03