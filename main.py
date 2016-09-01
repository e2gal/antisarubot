#!/usr/bin/env python2

from antisarubot import bot
import config

app = None
update_queue = None

if config.WEBHOOK:
    from flask import Flask, request
    from Queue import Queue

    app = Flask(__name__)
    update_queue = Queue()  # channel between `app` and `bot`

    @app.route('/' + config.TOKEN, methods = ['GET', 'POST'])
    def pass_update():
        update_queue.put(request.data)  # pass update to bot
        return 'OK'

def main():
    print('Listening...')

    bot_obj = bot.AntisaruBot(config.TOKEN)

    if config.WEBHOOK:
        bot_obj.setWebhook(config.WEBHOOK_HOST + "/" + config.TOKEN)
        bot_obj.message_loop(source = update_queue)
    else:
        bot_obj.setWebhook(None)
        bot_obj.message_loop(run_forever = True)

if __name__ == "__main__":
    main()
    if config.WEBHOOK:
        app.run(port = config.WEBHOOK_PORT, debug = True)
