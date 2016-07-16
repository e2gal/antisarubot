#!/usr/bin/env python2

HANDLER_NAME = "iqdb"

import re
import requests
import string
import time
from bs4 import BeautifulSoup

danbooruRegex = re.compile("^//danbooru.donmai.us/posts/(.*)$")

ratingTable = {
    "s": "safe",
    "q": "questionable",
    "e": "explicit"
}

def tagsDanbooru(imgID):
    resp = requests.get("http://danbooru.donmai.us/posts/" + imgID + ".json")
    decoded = resp.json()
    resp.close()

    chars = map(lambda s : string.replace(s, "_", " "), decoded["tag_string_character"].split(" "))
    copys = map(lambda s : string.replace(s, "_", " "), decoded["tag_string_copyright"].split(" "))
    gens  = map(lambda s : string.replace(s, "_", " "), decoded["tag_string_general"].split(" "))

    rating    = ratingTable[decoded["rating"]]
    character = set(chars)
    copyright = set(copys)
    general   = set(gens)

    return (rating, character, copyright, general)

def run(fname):
    print "Doing inference (iqdb - Danbooru)..."
    start = time.time()

    files = {"file":fname}

    # Get Danbooru id
    resp = requests.post("http://danbooru.iqdb.org", files=files)
    soup = BeautifulSoup(resp.text, "html5lib")
    resp.close()

    bestMatch = soup.find(text="Best match")
    if not bestMatch:
        end = time.time()
        print "Failed. Took " + str(end - start) + "s"
        return None

    match = danbooruRegex.match(bestMatch.parent.parent.parent.find("a")["href"])
    if not match:
        end = time.time()
        print "Failed. Took " + str(end - start) + "s"
        return None

    res = tagsDanbooru(match.group(1))

    end = time.time()
    print "Done. Took " + str(end - start) + "s"

    return res
