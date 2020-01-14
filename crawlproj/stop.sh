#!/usr/bin/env bash

if [ $USER == "vagrant" ]; then
    VENVDIR=/home/$USER/venv
    WORKDIR=/home/$USER/workspace/crawlproj/crawlproj
else
    VENVDIR=/home/$USER/webcrawler/venv
    WORKDIR=/home/$USER/webcrawler/crawlproj/crawlproj
fi

if [ -z "$VIRTUAL_ENV" ]; then
    source $VENVDIR/bin/activate
fi
echo "halting crawler daemons..."
supervisorctl stop all
echo "checking status..."
supervisorctl status all
