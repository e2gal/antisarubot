#!/usr/bin/env python2

def join(i, sep1, sep2):
    l = list(i)

    if len(l) < 2:
        return sep1.join(l)

    return sep1.join(l[:-1]) + sep2 + l[-1]
