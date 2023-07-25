import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests

print("Que voulez vous télécharger de google images ?")
search_query = input(">")

folder_path = "../Datasets/Originals/" + search_query + "/Google"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

wd = webdriver.Chrome()
wd.get(f"https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={search_query}&oq={search_query}&gs_l=img")
time.sleep(2)

for _ in range(5):
    wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

images = wd.find_elements(By.CSS_SELECTOR, "img.rg_i")

links = []
for image in images:
    image_url = image.get_attribute("src")
    if image_url and image_url.startswith("http"):
        links.append(image_url)

wd.quit()
print(f"Il ya {len(links)} voulez vous les télécharger ?\n 1- Oui\n 2 - Non")
choice = int(input(">"))

if choice == 1:
    for i, link in enumerate(links):
        try:
            response = requests.get(link)
            response.raise_for_status()
            with open(os.path.join(folder_path, f"image_{i + 1}.jpg"), "wb") as f:
                f.write(response.content)
            print(f"Téléchargement : {i + 1} / {len(links)}")
        except requests.exceptions.RequestException as e:
            print(f"Echec lors du téléchargement de l'image {i + 1}: {e}")

