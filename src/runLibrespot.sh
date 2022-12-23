#!/bin/bash

ROOT_PATH=/home/tyler/app
DOT_ENV_PATH=$ROOT_PATH/.env

if [ ! -f FILENAME$DOT_ENV_PATH ]; then
  echo "loading .env"
  export $(cat $DOT_ENV_PATH | xargs)
fi

/usr/bin/librespot --name soundsnearone --onevent=$ROOT_PATH/app/src/onLibrespotEvent.py --username $SPOTIFY_USERNAME --password $SPOTIFY_PASSWORD