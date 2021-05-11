#!/bin/bash

OPENSSL_CONF=/etc/ssl/
pip install rpa
pip install retirejs
wget https://www.google.com/chrome/thank-you.html?platform=linux&statcb=0&installdataindex=empty&defaultbrowser=0# -O chrome.deb
apt install -y chrome.deb
