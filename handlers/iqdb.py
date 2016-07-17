#!/usr/bin/env python2

import re
import requests
import string
import time

from bs4 import BeautifulSoup

HANDLER_NAME = "iqdb"
RATING_TABLE = {
    "s": "safe",
    "q": "questionable",
    "e": "explicit"
}

danbooru_regex = re.compile("^//danbooru.donmai.us/posts/(.*)$")

def tags_danbooru(img_id):
    resp = requests.get("http://danbooru.donmai.us/posts/" + img_id + ".json")
    decoded = resp.json()
    resp.close()

    chars = map(lambda s : string.replace(s, "_", " "), decoded["tag_string_character"].split(" "))
    copys = map(lambda s : string.replace(s, "_", " "), decoded["tag_string_copyright"].split(" "))
    gens  = map(lambda s : string.replace(s, "_", " "), decoded["tag_string_general"].split(" "))

    rating    = RATING_TABLE[decoded["rating"]]
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

    best_match = soup.find(text="Best match")
    if not best_match:
        end = time.time()
        print "Failed. Took " + str(end - start) + "s"
        return None

    match = danbooru_regex.match(best_match.parent.parent.parent.find("a")["href"])
    if not match:
        end = time.time()
        print "Failed. Took " + str(end - start) + "s"
        return None

    res = tags_danbooru(match.group(1))

    end = time.time()
    print "Done. Took " + str(end - start) + "s"

    return res
