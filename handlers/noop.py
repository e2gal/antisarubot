#!/usr/bin/env python2

# A handler that always fails.
# Use this as a template for new handlers.

import time

HANDLER_NAME = "noop"

def run(fname):
    print "Doing inference (noop)..."
    start = time.time()

    # rating: "safe", "questionable", or "explicit"
    rating = ""
    character = set()
    copyright = set()
    general = set()

    end = time.time()
    print "Done. Took " + str(end - start) + "s"

    success = False
    if success:
        return (rating, character, copyright, general)
    else:
        return None
