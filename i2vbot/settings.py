#!/usr/bin/env python2

# Ampuni aku... :(
import pickle

SETTINGS_FILE = "data/settings.pickle"

def loadSettings(settingsFile = SETTINGS_FILE):
    with open(settingsFile, 'r') as f:
        try:
            return pickle.load(f)
        except:
            return {}

def saveSettings(settings, settingsFile = SETTINGS_FILE):
    with open(settingsFile, 'w') as f:
        pickle.dump(settings, f, -1)
