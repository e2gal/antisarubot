#!/usr/bin/env python2

import util

def tagError(tagList):
    return """
Iiih, kakak!
Ga boleh ngepost gambar """ + util.join(tagList, ", ", " sama ") + """ di sini, tau!
"""

ratingError = """
Iiih, kakak kok mesum sih!
Ga boleh ngepost gambar kaya gitu di sini, tau!
"""

okay = u"Okay\u2606"

tagmgrUsage = """
Usage :
- /tagmgr [add|rm] [category] [tags]: Add / remove tags from warn list
- /tagmgr clear [category]: Clear all tags from warn list
- /tagmgr show: Show warn list
[category] is one of 'rating', 'character', 'copyright', or 'general'.
"""
