#!/bin/bash

export OPENSSL_CONF=/etc/ssl/
pip install rpa
pip install retirejs
pip install fdpf

#Setup chrome for RPA
wget https://www.google.com/chrome/thank-you.html?platform=linux&statcb=0&installdataindex=empty&defaultbrowser=0# -O chrome.deb
apt install -y chrome.deb
sed -i '$ s/$/ --no-sandbox/' /usr/bin/google-chrome

#Setup services for DVWA
apt install -y apache2
systemctl start apache2
systemctl start mysql
systemctl enable apache2
systemctl enable mysql

#Setup DVWA
cd /var/www/html
git clone https://github.com/digininja/DVWA.git
