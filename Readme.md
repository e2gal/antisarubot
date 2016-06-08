i2vbot - A Telegram bot based on illustration2vec
-----

## Requirements
- Python 2.7
- illustration2vec
- telepot

## Setup Instructions
- Clone and init the submodules
```
git clone https://github.com/e2gal/i2vbot
cd i2vbot
git submodule update --init
```

- Install required libraries (please do this in a
  [virtualenv](https://virtualenv.pypa.io/en/stable/) environment)
```
for r in `cat requirements.txt`; do
    pip install $r
done
```

- Create `bottoken.py` and add your Telegram bot token there.
```
cp bottoken.py.example bottoken.py
nano bottoken.py
```

- Download the models.
```
sh get_models.sh
```

- Run the bot.
```
python2 main.py
```
