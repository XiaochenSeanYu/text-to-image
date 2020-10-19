import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_soup(url, header):
    """
    Returns the soup parsed html of the Yandex url
    """
    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


def get_all_images(url):
    """
    Returns in a dictionary with the search index as the key and a tuple of the 
    all image URLs and their descriptions on a single `url`
    """
    header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
              "X-Requested-With": "XMLHttpRequest"}
    soup = get_soup(url, header)
    urls = {}
    id = 0
    for img in tqdm(soup.find_all("img"), "Extracting images"):
        img_url = img.attrs.get("src")
        desc = img.attrs.get("alt")
        if not img_url:
            # if img does not contain src attribute, just skip
            continue
        # make the URL absolute by joining domain with the URL that is just extracted
        img_url = urljoin(url, img_url)
        pass
        # finally, if the url is valid
        if is_valid(img_url):
            urls[id] = (img_url, desc)
            id += 1
    return urls


print(get_all_images("https://yandex.com/images/search?text=opening%20drain%20plug"))
