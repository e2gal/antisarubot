#!/usr/bin/env python2

import re
import string
import tempfile
import telepot

import messages
import settings

from handlers import i2v_online

class I2VBot(telepot.Bot):
    def __init__(self, *args, **kwargs):
        super(I2VBot, self).__init__(*args, **kwargs)
        self._answerer = telepot.helper.Answerer(self)
        self.settings  = settings.loadSettings()
        self.username  = "@" + self.getMe()["username"]

    def _getSettings(self, chat_id, tagcategory):
        res = set()
        try:
            res = self.settings[chat_id][tagcategory]
        except:
            pass

        return res

    def _getChatSettings(self, chat_id):
        rating    = self._getSettings(chat_id, "rating")
        character = self._getSettings(chat_id, "character")
        copyright = self._getSettings(chat_id, "copyright")
        general   = self._getSettings(chat_id, "general")

        return (rating, character, copyright, general)

    def _getTagList(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        if content_type != "photo":
            return None

        fileID = msg["photo"][-1]["file_id"]
        (rating, character, copyright, general) = ("", set(), set(), set())
        with tempfile.NamedTemporaryFile() as f:
            self.download_file(fileID, f.name)
            (rating, character, copyright, general) = i2v_online.run(f)
        return (rating, character, copyright, general)

    def _addSettings(self, chat_id, category, tagList):
        tl = map(lambda s : string.replace(s, "_", " "), tagList)

        if chat_id not in self.settings:
            self.settings[chat_id] = {}

        try:
            self.settings[chat_id][category] |= set(tl)
        except:
            self.settings[chat_id][category]  = set(tl)

        settings.saveSettings(self.settings)

    def _rmSettings(self, chat_id, category, tagList):
        tl = map(lambda s : string.replace(s, "_", " "), tagList)

        try:
            self.settings[chat_id][category] -= set(tl)
        except:
            pass

        settings.saveSettings(self.settings)

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
                        try:
                            self.settings[chat_id][params[0]] = set()
                        except:
                            pass
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
