import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import random


def create_folder(directory_name):
    os.makedirs(directory_name)


def download_image(image_url, directory_name):
    try:
        response = requests.get(image_url, stream=True)
        image_name = directory_name + "_" + str(random.randint(1, 1000)) + ".jpg"
        with open(os.path.join(directory_name, image_name), "wb") as out_file:
            out_file.write(response.content)
        print(f"Downloaded the image: {image_url}")
    except Exception as e:
        print(f"Failed to download the image: {image_url} : {e}")


def scrape_google_images(keyword_to_search, num_pages_to_scrape, directory_name):
    search_url = f"https://www.google.com/search?q={quote_plus(keyword_to_search)}&tbm=isch"

    for page in range(num_pages_to_scrape):
        page_url = f"{search_url}&start={page * 20}"
        try:
            response = requests.get(page_url)
            soup = BeautifulSoup(response.text, "html.parser")
            print(f"Soup: {soup}")
            image_tags = soup.find_all("img", class_="DS1iW")
            print(f"Image tags: {image_tags}")

            for image_tag in image_tags:
                imag_url = image_tag["src"]
                download_image(imag_url, directory_name)

        except Exception as e:
            print(f"Failed to scrape page {page} : {e}")


keyword = input("Enter the search keyword: ")
num_pages = int(input("Enter the number of pages to scrape: "))
directory = keyword.replace(" ", "_") + "_images" + str(random.randint(1, 1000))
create_folder(directory)
scrape_google_images(keyword, num_pages, directory)
