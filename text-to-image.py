"""
Authors: Daisy Shu dds86, Sean Yu xsy3
Start Date: 10/9/2020
Completed: 10/13/2020
"""

from bs4 import BeautifulSoup
import requests
import urllib.request as urllib2
import os
import json
import urllib.request
import base64
import spacy

"""
gen(query, n) is the main function that takes a (query) input string,
and returns a list with (n) URL(s) corresponding to the tags most closely
correlated to the (query) input. This function web scrapes Google
images based on the (query) search, and retrieves the URL and tag of
desired images. This function also uses the cosine similarity metric
from the Python NLP library spacy in order to calculate the similaries
between the input (query) and corresponding image tags.

Input:
        query           string
        n               int
Output:
        top_n_images    string list
"""
def gen(query, n):
    org_query = query
    query = query.split()
    query = '+'.join(query)

    url = "https://www.google.com/search?q=" + query + "&source=lnms&tbm=isch"
    header = {"content-type": "image/png"}
    soup = get_soup(url, header)

    # Gives first 20 of thumbnail images
    image_dict = dict.fromkeys(range(100))
    index = 0
    for img in soup.find_all("img"):
        # Inserts URLs for first 20 thumbnail images into first position of tuple
        # Second position of tuple contains empty tag, which will be replaced later
        link = img["src"]
        image_dict[index] = [link]
        index += 1

    header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"}
    soup = get_soup(url, header)

    # Inserts tags for all images, and URLs for rest of desired images (after 20 images)
    soup_lst = soup.find_all("a", {"class": "wXeWr islib nfEiy mM5pbd"})
    for i in range(len(soup_lst)):
        tag = soup_lst[i].find('img')['alt']
        try:
            link = soup_lst[i].find('img')['data-src']
            image_dict[i+1] = [link, tag]
        except:
            image_dict[i+1] += [tag]
    
    # Deletes the irrelevant Google icon image at index 0
    image_dict.pop(0)

    print("There are a total of", len(soup_lst), "images.")

    similarity(org_query, image_dict, n)


"""
get_soup(url, header) is a helper function for gen(query) that takes
a specific (url) and (header), and outputs a soup object. This
function uses the Python web scraping library BeautifulSoup to
web scrape Google images based on the given URL and header.

Input:
        url             string
        header          string dictionary
Output:
        soup            soup object
"""
def get_soup(url, header):
    html = requests.get(url, headers=header).text
    soup = BeautifulSoup(html, "html.parser")
    return soup

"""
similarity(input_str, image_dict, n) is a helper function for gen(query)
that takes a query (input_str) string, (image_dict) dictionary, and outputs
a list of the top (n) image URLs corresponding to the tags most closely
correlated to the query.

Input:
        input_str       string
        image_dict      string dictionary
        n               int
Output:
        top_n_images    string list
"""
def similarity(input_str, image_dict, n):
    nlp = spacy.load("en_core_web_md")
    query = nlp(input_str)
    for key, val in image_dict.items():
        tag = nlp(val[1])
        # Appends similarities for each value in image_dict
        image_dict[key] += [query.similarity(tag)]

    # Sorts similarities for each image in descending order
    sorted_image_dict = sorted(image_dict.keys(), key=lambda k: image_dict[k][2], reverse=True)

    top_n_images = []
    # Inserts n images based on highest similarities
    for i in range(n):
        key_index = sorted_image_dict[i]
        top_n_images.append(image_dict[key_index][0])

    print(top_n_images)
    return top_n_images


if __name__ == "__main__":
    # Desired query
    query = "clean tank"
    # Top n images desired
    n = 5
    gen(query, n)