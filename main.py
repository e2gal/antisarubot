#!/usr/bin/env python2

from i2vbot import bot
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

    botObj = bot.I2VBot(config.TOKEN)

    if config.WEBHOOK:
        botObj.message_loop(source = update_queue)
        botObj.setWebhook(config.WEBHOOK_HOST + "/" + config.TOKEN)
    else:
        botObj.message_loop(run_forever = True, relax = 1)

if __name__ == "__main__":
    if config.WEBHOOK:
        app.run(port = config.WEBHOOK_PORT, debug = True)
    main()
