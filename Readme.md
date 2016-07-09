i2vbot - A Telegram bot based on illustration2vec
-----

## Requirements
- Python 2.7
- OpenBLAS (for NumPy)

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

- Create `config.py` and add your Telegram bot token there.
```
cp config.py.example config.py
nano config.py
```

- Download the models.
```
sh get_models.sh
```

- Run the bot.
```
python2 main.py
```
