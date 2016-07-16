#!/usr/bin/env python2

# Ampuni aku... :(
import os
import sqlite3

SETTINGS_FILE = "data/settings.sqlite"

def initDB(settingsFile = SETTINGS_FILE):
    with sqlite3.connect(settingsFile) as con:
        cur = con.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            chat_id INT PRIMARY KEY,
            rating TEXT,
            character TEXT,
            copyright TEXT,
            general TEXT)""")

def loadSettings(chat_id, settingsFile = SETTINGS_FILE):
    default = {
        "rating":    set(),
        "character": set(),
        "copyright": set(),
        "general":   set()
    }

    if not os.path.exists(settingsFile):
        return default

    with sqlite3.connect(settingsFile) as con:
        cur = con.cursor()
        cur.execute("""
        SELECT rating, character, copyright, general
          FROM settings
         WHERE chat_id = ?""", (chat_id,))
        data = cur.fetchone()
        if data is None:
            return default

        return {
            "rating":    set(data[0].split(",")),
            "character": set(data[1].split(",")),
            "copyright": set(data[2].split(",")),
            "general":   set(data[3].split(","))
        }

def saveSettings(chat_id, settings, settingsFile = SETTINGS_FILE):
    if not os.path.exists(settingsFile):
        initDB()

    rating    = ",".join(settings["rating"])
    character = ",".join(settings["character"])
    copyright = ",".join(settings["copyright"])
    general   = ",".join(settings["general"])

    with sqlite3.connect(settingsFile) as con:
        cur = con.cursor()
        cur.execute("""
        INSERT OR REPLACE INTO settings (chat_id, rating, character, copyright, general)
        VALUES (?, ?, ?, ? ,?)""",
        (chat_id, rating, character, copyright, general))