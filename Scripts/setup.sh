#!/bin/bash

#Install Google Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install -y ./google-chrome-stable_current_amd64.deb
sed -i '$ s/$/ --no-sandbox/' $(readlink -f /usr/bin/google-chrome)
rm -f ./google-chrome-stable_current_amd64.deb
clear

#Install python modules
apt update
apt install -y pip
pip install bs4
pip install requests
pip install rpa
pip install retirejs
pip install fpdf
pip install urllib
pip install sys
pip install time
pip install os
pip install pprint
pip install colorama
pip install flask
export OPENSSL_CONF=/etc/ssl/
clear

#Setup services for DVWA
apt install -y apache2
systemctl start apache2
systemctl start mysql
systemctl enable apache2
systemctl enable mysql
clear

#Setup DVWA
git clone https://github.com/digininja/DVWA.git /var/www/html/DVWA
clear

#RPA for Python first time setup
python3 rpaSetup.py
export OPENSSL_CONF=/etc/ssl/
echo "export OPENSSL_CONF=/etc/ssl/" > /etc/profile.d/openssf_conf
echo "Setup complete!"