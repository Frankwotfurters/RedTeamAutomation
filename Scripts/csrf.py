import os
import rpa as r
from bs4 import BeautifulSoup
from urllib.request import urlparse, urljoin
import sys

internal_urls = []
external_urls = []
visited_urls = []
form_urls = []
vuln_forms = []
non_vuln_forms = []
generated_pocs = []

def login(loginPage, creds):
	r.url(loginPage)
	r.type('//*[@name="username"]', creds[0])
	r.type('//*[@name="password"]', creds[1])

def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_domain(url):
	return urlparse(url).netloc

def find_forms():
	# From landing page, finds links to crawl to and spot forms
	html = r.dom('return document.querySelector("html").outerHTML')
	url = r.url()
	domain_name = get_domain(url)
	soup = BeautifulSoup(html, "html.parser")

	form = soup.find("form")
	if form:
		form_urls.append(url)

	for a_tag in soup.findAll("a"):
		href = a_tag.attrs.get("href")
		if href == "" or href is None:
			# href empty tag
			continue
		# join the URL if it's relative (not absolute link)
		href = urljoin(url, href)
		parsed_href = urlparse(href)
		# remove URL GET parameters, URL fragments, etc.
		href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
		if not is_valid(href):
			# not a valid URL
			continue
		if href in internal_urls:
			# already in the set
			continue
		if domain_name not in href:
			# external link
			if href not in external_urls:
				# print(f"[!] External link: {href}")
				external_urls.append(href)
			continue
		# print(f"[*] Internal link: {href}")
		internal_urls.append(href)

	# crawl recursively to search for forms
	for page in internal_urls:
		if page not in visited_urls:
			if "logout" in page:
				continue # dont logout
			else:
				visited_urls.append(page)
				r.url(page)
				find_forms()

def check(form):
	# Checks if form requires a token or some type of hidden field to be submitted
	if 'token' in str(form) or 'type="hidden"' in str(form) or "type='hidden'" in str(form):
		return False
	else:
		return True

def create_poc(form):

	#First creates a folder based on domain name
	folder = get_domain(r.url())
	if not os.path.exists(folder):
		os.makedirs(folder)
	f = open(folder + "/" + r.url().split('/')[-2], "w")
	f.write(str(form))
	pwd = os.path.dirname(os.path.realpath(__file__))
	output = pwd + "/" + folder + "/" + r.url().split('/')[-2]
	print("Exported PoC to " + output)
	generated_pocs.append(output)

	# r.clipboard("file://"+output)
	# r.keyboard("[ctrl][t]")
	# r.keyboard("[ctrl][v]")
	# r.keyboard("[enter]")

def main(creds, loginPage):
	creds[1] += "[enter]" # have RPA press enter after typing credentials
	# loginPage = 'http://localhost/DVWA/login.php'

	r.init(visual_automation = True)
	login(loginPage, creds)
	find_forms()

	for url in form_urls:
		r.url(url)
		html = r.dom('return document.querySelector("html").outerHTML')
		soup = BeautifulSoup(html, 'html.parser')
		form = soup.find("form")
		try:
			form['action'] = r.url() + form['action']
		except:
			pass

		if check(form):
			# If form is potentially vulnerable to CSRF
			vuln_forms.append(url)
			create_poc(form)
		else:
			non_vuln_forms.append(url)

	# Cleanup
	r.close()

	results = {}
	results["internal_urls"] = internal_urls
	results["visited_urls"] = visited_urls
	results["vuln_forms"] = vuln_forms
	results["non_vuln_forms"] = non_vuln_forms
	results["generated_pocs"] = generated_pocs
	return results #returns dictionary of found urls, form urls, possibly vulnerable forms, non-vulnerable forms

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("-c", "--creds", help = "Supply credentials to log into web app. Format = userid:password.", required = True)
	parser.add_argument("-u", "--url", help = "URL of login page to web app.", required = True)
	args = parser.parse_args()
	args = vars(parser.parse_args())

	try:
		# Split username:password into a list and test if valid url
		creds = args["creds"].split(":")
		loginPage = args["url"]
		r.init(chrome_browser=False)
		r.url(loginPage)
		r.close()

	except:
		print("Please provide credentials in the format userid:password")

	main(creds, loginPage)