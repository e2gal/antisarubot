#!/usr/bin/env python2

import i2v
from PIL import Image

import time

print "Loading model..."
start = time.time()

illust2vec = i2v.make_i2v_with_chainer("data/i2v_model.caffemodel", "data/i2v_tag_list.json")

end   = time.time()
print "Done. Took " + str(end - start) + "s"

def run(fname):
    def fst(p):
        return p[0]

    print "Doing inference..."
    start = time.time()

    img = Image.open(fname)
    res = fst(illust2vec.estimate_plausible_tags([img], threshold=0.5))

    end   = time.time()
    print "Done. Took " + str(end - start) + "s"

    rating    = fst(res["rating"][0])
    character = set(map(fst, res["character"]))
    copyright = set(map(fst, res["copyright"]))
    general   = set(map(fst, res["general"]))

    return (rating, character, copyright, general)
