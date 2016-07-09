#!/usr/bin/env python2

import i2vbot
import config

def main():
    print('Listening...')

    botObj = i2vbot.I2VBot(config.TOKEN)
    botObj.message_loop(run_forever = True, relax = 1)

if __name__ == "__main__":
    main()
