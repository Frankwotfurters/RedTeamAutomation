import os
import rpa as r
from bs4 import BeautifulSoup
import link_extractor
from urllib.request import urlparse, urljoin

creds = ["admin", "password"]
creds[1] += "[enter]" # have RPA press enter after typing credentials
loginPage = 'http://localhost/DVWA/login.php'

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
				print(f"[!] External link: {href}")
				external_urls.append(href)
			continue
		print(f"[*] Internal link: {href}")
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

def create_poc():
	folder = get_domain(r.url())
	print(folder)
	if not os.path.exists(folder):
		os.makedirs(folder)
	f = open(folder + "/" + r.url().split('/')[-2], "w")
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
internal_urls = []
external_urls = []
visited_urls = []
form_urls = []
find_forms()
print(form_urls)

for url in form_urls:
	r.url(url)
	html = r.dom('return document.querySelector("html").outerHTML')
	soup = BeautifulSoup(html, 'html.parser')
	form = soup.find("form")
	print(check(form))
	try:
		form['action'] = r.url() + form['action']
	except:
		pass

	if check(form):
		print(check(form))
		create_poc()

# Cleanup
r.wait(60)
r.close()