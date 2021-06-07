import os
import rpa as r
from bs4 import BeautifulSoup
from urllib.request import urlparse, urljoin
import sys
from fpdf import FPDF
import time
import logging
import sendmail

internal_urls = []
external_urls = []
visited_urls = []
form_urls = []
vuln_forms = []
non_vuln_forms = []
generated_pocs = {}

def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_domain(url):
	return urlparse(url).netloc

def find_forms(pdf):
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
				print(f"[+] Crawling: {page}")
				logging.info(f"[+] Crawling: {page}")
				pdf.cell(200, 10, txt=f"[+] Crawled: {page}", ln=1, align="L")
				visited_urls.append(page)
				r.url(page)
				find_forms(pdf)

def check(form):
	# Checks if form requires a token or some type of hidden field to be submitted
	if 'token' in str(form) or 'type="hidden"' in str(form) or "type='hidden'" in str(form):
		return False
	else:
		return True

def main(creds, loginPage, receiver=""):
	logging.basicConfig(level=logging.INFO, filename="logfile", filemode="a+", format="%(asctime)-15s %(levelname)-8s %(message)s")
	print("Running Cross-Site Request Forgery Scanner")
	logging.info("Running Cross-Site Request Forgery Scanner")
	print(f"Target: {loginPage}")
	logging.info(f"Target: {loginPage}")

	#Empty lists
	internal_urls.clear()
	external_urls.clear()
	visited_urls.clear()
	form_urls.clear()
	vuln_forms.clear()
	non_vuln_forms.clear()
	generated_pocs.clear()

	#Generate PDF
	pdf = FPDF()
	pdf.add_page()
	pdf.set_font('Arial', 'B', size=16)
	pdf.cell(200, 10, txt="RTA Integrated RPA", ln=2, align='L')
	pdf.set_font('')
	pdf.set_font('Arial', size=12)
	pdf.cell(200, 10, txt="Scanner: Cross-Site Request Forgery", ln=1, align='L')

	timestart = time.strftime("%d/%m/%Y %I:%M:%S")
	time1 = time.strftime("%-H%M")
	imgtime = time.strftime("(%d%m-%I%M%S)")
	pdf.cell(200, 10, txt=f"Scan Time: {timestart}", ln=1, align="L")
	pdf.cell(200, 10, txt="Results: ", ln=1, align='L')

	r.init(visual_automation = True)
	r.timeout(2.5)

	#Login
	r.url(loginPage)

	#Username input
	for tag in 'username','login','email','id':
		if r.type(tag, creds[0]):
			break

	#Password input
	for tag in 'password','pw':
		if r.type(tag, f'{creds[1]}[enter]'):
			break

	#Find forms
	find_forms(pdf)

	print()
	print("[!] Scanning individual forms")
	pdf.cell(200, 10, txt="Form vulnerability results:", ln=1, align='L')
	print()

	for url in form_urls:
		#Retrieve HTML code and search for form tags
		r.url(url)
		html = r.dom('return document.querySelector("html").outerHTML')
		soup = BeautifulSoup(html, 'html.parser')
		form = soup.find("form")
		try:
			#Set action to full url path
			form['action'] = r.url() + form['action']
		except:
			pass

		if check(form):
			# If form is potentially vulnerable to CSRF
			vuln_forms.append(url)

			#Create PoC
			#Determines file name based on html page name
			url = r.url()
			if url[-1] == "/":
				filename = url.split('/')[-2]
			else:
				filename = url.split('/')[-1]

			#Creates a folder based on domain name
			folder = get_domain(url)
			if not os.path.exists(folder):
				os.makedirs(folder)

			#Writes html of PoC to file
			f = open(f"{folder}/{filename}", "w")
			f.write(str(form))
			pwd = os.path.dirname(os.path.realpath(__file__))

			output = f"{pwd}/{folder}/{filename}"
			print(f"[+] Vulnerable! Exported PoC for {url} to {output}")
			logging.info(f"[+] Vulnerable! Exported PoC for {url} to {output}")
			pdf.cell(200, 10, txt=f"[+] Vulnerable: {url}", ln=1, align="L")
			pdf.cell(200, 10, txt=f"\t[!] Exported PoC to {output}", ln=1, align="L")
			generated_pocs[url] = output

		else:
			print(f"[-] Not Vulnerable: {url}")
			logging.info(f"[-] Not Vulnerable: {url}")
			pdf.cell(200, 10, txt=f"[-] Not Vulnerable: {url}", ln=1, align="L")
			non_vuln_forms.append(url)

	# Cleanup
	imgTime = time.strftime("%d-%m-%Y%H%M%S")
	pdf.output(f"CSRF_{imgTime}.pdf")
	if not receiver == "":
		# Send email
		sendmail.mail("Cross-Site Request Forgery", loginPage, f"CSRF_{imgTime}.pdf", receiver)
	r.close()

	results = {}
	results["internal_urls"] = internal_urls
	results["form_urls"] = form_urls
	results["vuln_forms"] = vuln_forms
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

	except:
		print("Please provide credentials in the format userid:password")

	main(creds, loginPage)