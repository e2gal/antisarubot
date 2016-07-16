#!/usr/bin/env python2

import importlib
import re
import string
import tempfile
import telepot

import config
import data
import messages
import settings

handlersList = []
for i in config.HANDLERS:
    try:
        m = importlib.import_module("." + i, "handlers")
        handlersList.append(m)
    except ImportError as e:
        print e

    if len(handlersList) == 0:
        raise ImportError("No handler specified")

class InferenceError(Exception):
    def __init__(self, message):
        self.message = message

class AntisaruBot(telepot.Bot):
    def __init__(self, *args, **kwargs):
        super(AntisaruBot, self).__init__(*args, **kwargs)
        self._answerer = telepot.helper.Answerer(self)
        self.username  = "@" + self.getMe()["username"]

    def _getTagList(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        if content_type != "photo":
            return None

        fileID = msg["photo"][-1]["file_id"]
        (rating, character, copyright, general) = ("", set(), set(), set())

        dbData = data.loadData(chat_id, msg["message_id"])
        if dbData:
            rating    = dbData["rating"]
            character = dbData["character"]
            copyright = dbData["copyright"]
            general   = dbData["general"]

            return (rating, character, copyright, general)

        handlerName = ""
        with tempfile.NamedTemporaryFile() as f:
            self.download_file(fileID, f.name)

            for h in handlersList:
                res = h.run(f)
                if res:
                    (rating, character, copyright, general) = res
                    handlerName = h.HANDLER_NAME
                    break
                else:
                    # Rewind file for reading with other handler.
                    f.seek(0)

            if not res:
                raise InferenceError("Cannot do inference on this image")

        data.saveData(chat_id, msg["message_id"], {
            "rating":    rating,
            "character": character,
            "copyright": copyright,
            "general":   general,
            "time":      msg["date"],
            "handler":   handlerName
        })

        return (rating, character, copyright, general)

    def _getChatSettings(self, chat_id):
        s = settings.loadSettings(chat_id)

        rating    = s["rating"]
        character = s["character"]
        copyright = s["copyright"]
        general   = s["general"]

        return (rating, character, copyright, general)

    def _addSettings(self, chat_id, category, tagList):
        tl = map(lambda s : string.replace(s, "_", " "), tagList)
        s = settings.loadSettings(chat_id)

        try:
            s[category] |= set(tl)
        except:
            s[category]  = set(tl)

        settings.saveSettings(chat_id, s)

    def _rmSettings(self, chat_id, category, tagList):
        tl = map(lambda s : string.replace(s, "_", " "), tagList)
        s = settings.loadSettings(chat_id)

        try:
            s[category] -= set(tl)
        except:
            pass

        settings.saveSettings(chat_id, s)

    def on_edited_chat_message(self, msg):
        pass

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        mt = None

        if content_type == "photo":
            (rating, character, copyright, general) = self._getTagList(msg)
            (warnRating, warnCharacter, warnCopyright, warnGeneral) = self._getChatSettings(chat_id)
            if character & warnCharacter:
                mt = messages.tagError(character & warnCharacter)

            if copyright & warnCopyright:
                mt = messages.tagError(copyright & warnCopyright)

            if general & warnGeneral:
                mt = messages.tagError(general & warnGeneral)

            if rating in warnRating:
                mt = messages.ratingError

            if mt:
                self.sendMessage(chat_id, mt, reply_to_message_id = msg["message_id"])

        if content_type == "text":
            command = msg['text'].strip().lower()
            if re.match(r"^/tagmgr(" + self.username + r")?\b", command):
                command = re.sub(r"^/tagmgr(" + self.username + r")?\s", "", command)
                mt = messages.tagmgrUsage

                if re.match(r"^add.+$", command):
                    params = re.sub(r"^add\s", "", command).split()
                    if len(params) == 0 or params[0] not in ['rating', 'character', 'copyright', 'general']:
                        mt = "Please specify tag category and tags to add."
                    else:
                        self._addSettings(chat_id, params[0], params[1:])
                        mt = messages.okay

                if re.match(r"^rm.+$", command):
                    params = re.sub(r"^rm\s", "", command).split()
                    if len(params) == 0 or params[0] not in ['rating', 'character', 'copyright', 'general']:
                        mt = "Please specify tag category and tags to remove."
                    else:
                        self._rmSettings(chat_id, params[0], params[1:])
                        mt = messages.okay

                if re.match(r"^clear.+$", command):
                    params = re.sub(r"^clear\s", "", command).split()
                    if len(params) != 1 or params[0] not in ['rating', 'character', 'copyright', 'general']:
                        mt = "Please specify tag category to clear."
                    else:
                        allEntries = settings.loadSettings(chat_id)[params[0]]
                        self._rmSettings(chat_id, params[0], allEntries)
                        mt = messages.okay

                if re.match(r"^show$", command):
                    (rating, character, copyright, general) = self._getChatSettings(chat_id)
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
                        (rating, character, copyright, general) = self._getTagList(rmsg)

                        mt  = "Inferred tags for this image\n"
                        mt += "Rating:    " + rating + "\n"
                        mt += "Character: " + ", ".join(character) + "\n"
                        mt += "Copyright: " + ", ".join(copyright) + "\n"
                        mt += "General:   " + ", ".join(general)

                        reply_id = rmsg["message_id"]

                self.sendMessage(chat_id, mt, reply_to_message_id = reply_id, disable_notification = True)
