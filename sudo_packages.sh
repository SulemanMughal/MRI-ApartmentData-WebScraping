#!/bin/bash

sudo apt-get install xvfb

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

sudo dpkg -i google-chrome-stable_current_amd64.deb

sudo apt --fix-broken install


sudo apt install google-chrome-stable
