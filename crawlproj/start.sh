#!/usr/bin/env bash

if [ $USER == "vagrant" ]; then
    VENVDIR=/home/$USER/venv
    WORKDIR=/home/$USER/workspace/crawlproj/crawlproj
else
    VENVDIR=/home/$USER/webcrawler/venv
    WORKDIR=/home/$USER/webcrawler/crawlproj/crawlproj
    eval $(/home/linuxbrew/.linuxbrew/bin/brew shellenv)
fi

cd $WORKDIR

if [ -z "$VIRTUAL_ENV" ]; then
    source $VENVDIR/bin/activate
fi
supervisorctl status > /dev/null
RESULT=$?

if [ $RESULT == 4 ]; then
    echo "starting superviord..."
    supervisord
else
    echo "supervisord already running"
fi

echo "starting crawler daemons..."
supervisorctl start all

echo "checking status..."
supervisorctl status all
