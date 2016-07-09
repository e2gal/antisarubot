#!/usr/bin/env python2

from i2vbot import bot
import config

def main():
    print('Listening...')

    botObj = bot.I2VBot(config.TOKEN)
    botObj.message_loop(run_forever = True, relax = 1)

if __name__ == "__main__":
    main()
