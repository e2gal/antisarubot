#!/usr/bin/env python2

import os
import sqlite3

from config import SETTINGS_FILE
import util

def init_db():
    with sqlite3.connect(SETTINGS_FILE) as con:
        cur = con.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            chat_id INT PRIMARY KEY,
            rating TEXT,
            character TEXT,
            copyright TEXT,
            general TEXT)""")

def load_settings(chat_id):
    default = {
        "rating":    set(),
        "character": set(),
        "copyright": set(),
        "general":   set()
    }

    if not os.path.exists(SETTINGS_FILE):
        init_db()

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
            "rating":    set(util.split_or_empty(data[0], ",")),
            "character": set(util.split_or_empty(data[1], ",")),
            "copyright": set(util.split_or_empty(data[2], ",")),
            "general":   set(util.split_or_empty(data[3], ","))
        }

def save_settings(chat_id, settings):
    if not os.path.exists(SETTINGS_FILE):
        init_db()

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
