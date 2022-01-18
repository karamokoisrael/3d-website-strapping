from bs4 import *
import requests
import os, sys
from tinydb import TinyDB, Query

categoriesData = [
    {
    "name": "genesis-3-female",
    "start": 1,
    # "end": 653
    "end": 2
    }
]

db = TinyDB('./strapping-db.json')
strapStore = db.table('strapping')

def getImageLink(image, key=""):
    imageLink = None
    try:
        imageLink = image["data-src"]
    except:
        try:
            imageLink = image["data-srcset"]
        except:
            try:
                imageLink = image["data-fallback-src"]
            except:
                try:
                    imageLink = image["src"]
                except:
                    print() 
    return imageLink

def argIs(value):
    return len(sys.argv) > 1 and sys.argv[1] == value

def argInList(list):
    return len(sys.argv) > 1 and sys.argv[1] in list

def noArgGiven():
    return len(sys.argv) <= 1

def getPageImageUrls(url):
    imageUrls = []
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    images = soup.select('#featured-thumbnail img')
    if len(images) != 0:
        for i, image in enumerate(images):
            imageLink = getImageLink(image)
            if imageLink == None:
                pass
            imageUrls.append(imageLink)
    return imageUrls

if argIs("strap") or noArgGiven():
    for categoryData in categoriesData:
        for i in range(categoryData["start"], categoryData["end"]):
                url = "https://render-state.to/category/{0}/page/{1}/".format(categoryData["name"], i)
                r = requests.get(url)
                # Parse HTML Code
                soup = BeautifulSoup(r.text, 'html.parser')
            
                # find all images in URL
                navs = soup.select('#featured-thumbnail')
                images = soup.select('#featured-thumbnail img')
                if len(images) != 0:
                    for i, image in enumerate(images):
                        imageLink = getImageLink(image)
                        if imageLink == None:
                            pass
                        try:
                            additionalImageUrls = getPageImageUrls(navs[i]["href"])
                            strapStore.insert({"id": categoryData["name"]+"-"+str(i), "opId": i,  "categoryName": categoryData["name"], "pageLink": url, "imageLink": imageLink,"additionalImageUrls": additionalImageUrls, "proceedLink": navs[i]["href"]})
                        except:
                            pass
                        
elif argIs("server"):
    os.system("json-server --watch strapping-db.json --port 3004")