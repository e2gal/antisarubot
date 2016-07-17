#!/usr/bin/env python2

import importlib
import re
import string
import tempfile

import telepot

from config import HANDLERS
import data
import messages
import settings

handlers_list = []
for i in HANDLERS:
    try:
        m = importlib.import_module("." + i, "handlers")
        handlers_list.append(m)
    except ImportError as e:
        print e

    if len(handlers_list) == 0:
        raise ImportError("No handler specified")

class InferenceError(Exception):
    def __init__(self, message):
        self.message = message

class AntisaruBot(telepot.Bot):
    def __init__(self, *args, **kwargs):
        super(AntisaruBot, self).__init__(*args, **kwargs)
        self._answerer = telepot.helper.Answerer(self)
        self.username = "@" + self.getMe()["username"]

    def _get_tag_list(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        if content_type != "photo":
            return None

        file_id = msg["photo"][-1]["file_id"]
        (rating, character, copyright, general) = ("", set(), set(), set())

        db_data = data.load_data(chat_id, file_id)
        if db_data:
            rating    = db_data["rating"]
            character = db_data["character"]
            copyright = db_data["copyright"]
            general   = db_data["general"]

            return (rating, character, copyright, general)

        handler_name = ""
        with tempfile.NamedTemporaryFile() as f:
            self.download_file(file_id, f.name)

            for h in handlers_list:
                res = h.run(f)
                if res:
                    (rating, character, copyright, general) = res
                    handler_name = h.HANDLER_NAME
                    break
                else:
                    # Rewind file for reading with other handler.
                    f.seek(0)

            if not res:
                raise InferenceError("Cannot do inference on this image")

        data.save_data(chat_id, file_id, {
            "rating":    rating,
            "character": character,
            "copyright": copyright,
            "general":   general,
            "time":      msg["date"],
            "handler":   handler_name
        })

        return (rating, character, copyright, general)

    def _get_chat_settings(self, chat_id):
        s = settings.load_settings(chat_id)

        rating    = s["rating"]
        character = s["character"]
        copyright = s["copyright"]
        general   = s["general"]

        return (rating, character, copyright, general)

    def _add_settings(self, chat_id, category, tagList):
        tl = map(lambda s : string.replace(s, "_", " "), tagList)
        s = settings.load_settings(chat_id)

        try:
            s[category] |= set(tl)
        except:
            s[category]  = set(tl)

        settings.save_settings(chat_id, s)

    def _rm_settings(self, chat_id, category, tagList):
        tl = map(lambda s : string.replace(s, "_", " "), tagList)
        s = settings.load_settings(chat_id)

        try:
            s[category] -= set(tl)
        except:
            pass

        settings.save_settings(chat_id, s)

    def on_edited_chat_message(self, msg):
        pass

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        mt = None

        if content_type == "photo":
            (rating, character, copyright, general) = self._get_tag_list(msg)
            (warn_rating, warn_character, warn_copyright, warn_general) = self._get_chat_settings(chat_id)
            if character & warn_character:
                mt = messages.tag_error(character & warn_character)

            if copyright & warn_copyright:
                mt = messages.tag_error(copyright & warn_copyright)

            if general & warn_general:
                mt = messages.tag_error(general & warn_general)

            if rating in warn_rating:
                mt = messages.rating_error

            if mt:
                self.sendMessage(chat_id, mt, reply_to_message_id = msg["message_id"])

        if content_type == "text":
            command = msg['text'].strip().lower()
            if re.match(r"^/tagmgr(" + self.username + r")?\b", command):
                command = re.sub(r"^/tagmgr(" + self.username + r")?\s", "", command)
                mt = messages.tagmgr_usage

                if re.match(r"^add.+$", command):
                    params = re.sub(r"^add\s", "", command).split()
                    if len(params) == 0 or params[0] not in ['rating', 'character', 'copyright', 'general']:
                        mt = "Please specify tag category and tags to add."
                    else:
                        self._add_settings(chat_id, params[0], params[1:])
                        mt = messages.okay

                if re.match(r"^rm.+$", command):
                    params = re.sub(r"^rm\s", "", command).split()
                    if len(params) == 0 or params[0] not in ['rating', 'character', 'copyright', 'general']:
                        mt = "Please specify tag category and tags to remove."
                    else:
                        self._rm_settings(chat_id, params[0], params[1:])
                        mt = messages.okay

                if re.match(r"^clear.+$", command):
                    params = re.sub(r"^clear\s", "", command).split()
                    if len(params) != 1 or params[0] not in ['rating', 'character', 'copyright', 'general']:
                        mt = "Please specify tag category to clear."
                    else:
                        all_ntries = settings.load_settings(chat_id)[params[0]]
                        self._rm_settings(chat_id, params[0], all_entries)
                        mt = messages.okay

                if re.match(r"^show$", command):
                    (rating, character, copyright, general) = self._get_chat_settings(chat_id)
                    mt  = "Warned tag list\n"
                    mt += "Rating:    " + ", ".join(rating) + "\n"
                    mt += "Character: " + ", ".join(character) + "\n"
                    mt += "Copyright: " + ", ".join(copyright) + "\n"
                    mt += "General:   " + ", ".join(general)

                self.sendMessage(chat_id, mt, reply_to_message_id = msg["message_id"])

            if re.match(r"^/showtags(" + self.username + r")?$", command):
                mt = "Please use this command to reply to an image post."
                reply_id = msg["message_id"]

                if "reply_to_message" in msg:
                    rmsg = msg["reply_to_message"]
                    rcontent_type, rchat_type, rchat_id = telepot.glance(rmsg)
                    if rcontent_type == "photo":
                        (rating, character, copyright, general) = self._get_tag_list(rmsg)

                        mt  = "Inferred tags for this image\n"
                        mt += "Rating:    " + rating + "\n"
                        mt += "Character: " + ", ".join(character) + "\n"
                        mt += "Copyright: " + ", ".join(copyright) + "\n"
                        mt += "General:   " + ", ".join(general)

                        reply_id = rmsg["message_id"]

                self.sendMessage(chat_id, mt, reply_to_message_id = reply_id, disable_notification = True)
