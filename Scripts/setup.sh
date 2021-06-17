#!/bin/bash

#Install Google Chrome
echo "Installing Google Chrome"
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install -y ./google-chrome-stable_current_amd64.deb
sed -i '$ s/$/ --no-sandbox/' $(readlink -f /usr/bin/google-chrome)
rm -f ./google-chrome-stable_current_amd64.deb
clear

#Install python modules
echo "Installing Python Modules"
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
pip install urljoin
pip install smtplib
pip install email
clear

#Setup DVWA and Services
echo "Setting up DVWA and its services"
git clone https://github.com/digininja/DVWA.git /var/www/html/DVWA
apt install -y apache2
systemctl start apache2
systemctl start mysql
systemctl enable apache2
systemctl enable mysql
cp /var/www/html/DVWA/config/config.inc.php.dist /var/www/html/DVWA/config/config.inc.php
mysql -Bse "create database dvwa;create user dvwa@localhost identified by 'p@ssw0rd';grant all on dvwa.* to dvwa@localhost;flush privileges;"
sed -i "33s/impossible/low/" /var/www/html/DVWA/config/config.inc.php
clear

#RPA for Python first time setup
echo "Performing first time setup for RPA for Python"
echo "export OPENSSL_CONF=/etc/ssl/" > /etc/profile.d/openssl_conf
source /etc/profile.d/openssl_conf
python3 rpaSetup.py
echo "Setup complete!"
echo "Head to http://localhost/DVWA/setup.php to complete DVWA's first time setup."
echo "Run the command <source /etc/profile.d/openssl_conf> followed by <python3 app.py> and head to http://localhost:5000 to access the GUI."
