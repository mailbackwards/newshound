import string
import time
import requests
from bs4 import BeautifulSoup
import json
import random
import csv

from newshound.models import *


def scrape():
    all_breeds = []
    root_url = 'http://www.akc.org'
    for letter in string.ascii_uppercase:
        print('ON LETTER {}'.format(letter))
        r = requests.get(root_url + '/dog-breeds/?letter={}'.format(letter))
        soup = BeautifulSoup(r.text, 'html.parser')
        breeds = soup.find_all('article')[2:-1]
        for dog in breeds:
            try:
                detail_url = dog.a['href']
            except Exception as e:
                print('ERROR on dog {}, message {}'.format(dog, e.message))
            time.sleep(1)
            print('Requesting dog %s' % detail_url)
            detail_r = requests.get(root_url + detail_url)
            dog_detail = BeautifulSoup(detail_r.text, 'html.parser')
            breed_div = dog_detail.find('div', {'class': 'type'})
            intro_div = dog_detail.find('div', {'class': 'breed-intro'})

            all_breeds.append({
                'detail_url': detail_url,
                'name': dog.h2.text if dog.h2 else '',
                'blurb': dog.p.text if dog.p else '',
                'img': dog.img['src'] if dog.img else '',
                'breed_group': breed_div.a['href'] if breed_div.a else '',
                'intro': intro_div.text if intro_div else ''
            })
    with open('./breeds.json', 'w+') as f:
        f.write(json.dumps(all_breeds, indent=2))

GROUP_MAP = {
    '': None,
    '/dog-breeds/groups/working': 'Working',
    '/dog-breeds/groups/miscellaneous-class': 'Miscellaneous Class',
    '/dog-breeds/groups/herding': 'Herding',
    '/dog-breeds/groups/non-sporting': 'Non-sporting',
    '/dog-breeds/groups/sporting': 'Sporting',
    '/dog-breeds/groups/toy': 'Toy',
    '/dog-breeds/groups/foundation-stock-service': 'Foundation Stock Service',
    '/dog-breeds/groups/hound': 'Hound',
    '/dog-breeds/groups/terrier': 'Terrier'
}

def load():
    with open('./breeds.json', 'r') as f:
        breeds = json.load(f)
    for breed in breeds:
        if breed['breed_group']:
            group, _ = BreedGroup.objects.get_or_create(name=GROUP_MAP[breed['breed_group']])
        else:
            group = None
        Breed.objects.create(
            name=breed['name'],
            slug=breed['detail_url'].split('/')[-2],
            blurb=breed['blurb'],
            intro=breed['intro'],
            sample_photo=breed['img'],
            group=group
        )


def random_partition(l):
    results = []
    running = 0
    for i in range(l):
        if i + 1 == l:
            results.append(100 - running)
            break
        value = random.randint(1, 100 - running)
        results.append(value)
        running += value
    return results


def load_csv():
    all_names = []
    with open('./names.csv', 'r') as f:
        names = csv.reader(f)
        for row in names:
            all_names.append(row)
    clean_names = [(r[0].title(), int(r[1])) for r in all_names[1:]]
    all_breeds = Breed.objects.all()
    random_samples = []
    for name, count in clean_names:
        for i in range(count):
            random_samples.append(name)
    for i in range(1000):
        random_name = random.choice(random_samples)
        try:
            breed_breakdown = random_partition(random.randint(1, 3))
        except ValueError:
            breed_breakdown = [100]
        dog = Dog.objects.create(name=random_name)
        for percent in breed_breakdown:
            DogBreedRelationship.objects.create(
                dog=dog,
                breed=random.choice(all_breeds),
                percent=percent
            )



if __name__ == '__main__':
    load_csv()
