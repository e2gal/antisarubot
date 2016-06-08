#!/usr/bin/env python2

import i2vbot
import bottoken

def main():
    print('Listening...')

    botObj = i2vbot.I2VBot(bottoken.TOKEN)
    botObj.message_loop(run_forever = True, relax = 1)

if __name__ == "__main__":
    main()
