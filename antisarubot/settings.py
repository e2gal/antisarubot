#!/usr/bin/env python2

import os
import sqlite3

import config
import util

SETTINGS_FILE = config.SETTINGS_FILE

def initDB():
    with sqlite3.connect(SETTINGS_FILE) as con:
        cur = con.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            chat_id INT PRIMARY KEY,
            rating TEXT,
            character TEXT,
            copyright TEXT,
            general TEXT)""")

def loadSettings(chat_id):
    default = {
        "rating":    set(),
        "character": set(),
        "copyright": set(),
        "general":   set()
    }

    if not os.path.exists(SETTINGS_FILE):
        initDB()

    with sqlite3.connect(SETTINGS_FILE) as con:
        cur = con.cursor()
        cur.execute("""
        SELECT rating, character, copyright, general
          FROM settings
         WHERE chat_id = ?""", (chat_id,))
        data = cur.fetchone()
        if data is None:
            return default

        return {
            "rating":    set(util.splitOrEmpty(data[0], ",")),
            "character": set(util.splitOrEmpty(data[1], ",")),
            "copyright": set(util.splitOrEmpty(data[2], ",")),
            "general":   set(util.splitOrEmpty(data[3], ","))
        }

def saveSettings(chat_id, settings):
    if not os.path.exists(SETTINGS_FILE):
        initDB()

    rating    = ",".join(settings["rating"])
    character = ",".join(settings["character"])
    copyright = ",".join(settings["copyright"])
    general   = ",".join(settings["general"])

    with sqlite3.connect(SETTINGS_FILE) as con:
        cur = con.cursor()
        cur.execute("""
        INSERT OR REPLACE INTO settings (chat_id, rating, character, copyright, general)
        VALUES (?, ?, ?, ? ,?)""",
        (chat_id, rating, character, copyright, general))