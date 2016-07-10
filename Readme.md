antisarubot - A Telegram bot to guess tags from an image
-----

## Requirements
- Python 2.7
- OpenBLAS (optional, for offline inference only)

## Setup Instructions
- Clone and init the submodules.
```
git clone https://github.com/e2gal/i2vbot
cd i2vbot
git submodule update --init
```

- Install required libraries (please do this in a
  [virtualenv](https://virtualenv.pypa.io/en/stable/) environment).
```
for r in `cat [requirements-file]`; do
    pip install $r
done
```
  There are three requirements file:
  - `requirements-basic.txt`: Basic dependencies. Needed to run the bot.
  - `requirements-offlineinference.txt`: Needed to run i2v's inference engine locally.
  - `requirements-webhook.txt`: Needed to run the bot in webhook mode.

- Create `config.py` and adjust the settings there as needed.
```
cp config.py.example config.py
nano config.py
```

- Download the models (optional, for offline inference only).
```
sh get_models.sh
```

- Run the bot.
```
python2 main.py
```
