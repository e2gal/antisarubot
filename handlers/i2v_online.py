#!/usr/bin/env python2

import re
import requests
import string
import time
from bs4 import BeautifulSoup

def run(fname):
    def fst(p):
        return p[0]

    print "Doing inference (i2v - online)..."
    start = time.time()

    files = {"image":fname}

    # Get Danbooru id
    resp = requests.post("http://demo.illustration2vec.net/upload", files=files)
    decoded = resp.json()
    resp.close()

    res = decoded["prediction"]

    rating    = fst(res["rating"][0])
    character = set(map(fst, res["character"]))
    copyright = set(map(fst, res["copyright"]))
    general   = set(map(fst, res["general"]))

    end   = time.time()
    print "Done. Took " + str(end - start) + "s"
    return (rating, character, copyright, general)