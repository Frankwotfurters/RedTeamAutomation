#!/bin/bash

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

#Setup services for DVWA
apt install -y apache2
systemctl start apache2
systemctl start mysql
systemctl enable apache2
systemctl enable mysql

#Setup DVWA
git clone https://github.com/digininja/DVWA.git /var/www/html/DVWA

#RPA for Python first time setup
./rpaSetup.py