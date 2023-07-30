import re
import os
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/58.0.3029.110 Safari/537.3'
}

images_links = []
for i in range(1):
    link = f"https://www.istockphoto.com/fr/search/2/image?mediatype=photography&phrase=barbe%20%C3%A0%20papa" \
          f"&alloweduse=off&page={i + 1}"
    res = requests.get(link, headers=headers)
    if res.status_code == 200:
        images = re.findall(r'<img .*?src="(https://media\.istockphoto\.com.*?)"', res.text)
        print(f"Sur la page {i} il y a {len(images)} images")
        images_links += images

print(f"--------------------------------------------\n total image {len(images_links)}")


def retire_ampersand(url):
    return url.replace("&amp;", "&")


images_links = [retire_ampersand(url) for url in images_links]

for i, image_l in enumerate(images_links):
    try:
        response = requests.get(image_l)
        response.raise_for_status()
        with open(os.path.join("../Datasets/Originals/Cotton_candy/istock", f"image_{i + 310}.jpg"), "wb") as f:
            f.write(response.content)
        if (i + 1) % 100 == 0:
            print(f"Téléchargement : {i + 1} / {len(images_links)}")
    except requests.exceptions.RequestException as e:
        print(f"Echec lors du téléchargement de l'image {i + 1}: {e}")
