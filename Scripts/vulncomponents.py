#pip install retirejs
import rpa as r
import re
import retirejs
import requests
import json
from bs4 import BeautifulSoup as bs
import urllib3
from urllib.parse import urljoin
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://etsy.com"
#url = "http://localhost:8000/test.html"


def scan_js(url):
	#compiles list of js files loaded	
	html = requests.get(url).content
	soup = bs(html, "html.parser")
	script_files = []
	for script in soup.find_all("script"):
	    if script.attrs.get("src"):
	        # if the tag has the attribute 'src'
	        script_url = urljoin(url, script.attrs.get("src"))
	        script_files.append(script_url)

	print(script_files)

	#run retire.js on each script
	for js in script_files:
		print("Scanning file: " + js)
		scan = retirejs.scan_endpoint(js)
		# print(json.dumps(scan, indent=2))

def scan_server(url):
	#scans server version for CVEs
	server = requests.get(url).headers['Server']
	server = re.sub(r" ?\([^)]+\)", "", server).replace('/', ' ')
	print("Scanning Server Version: " + server)

	#NVD Query
	r.init(visual_automation = True)
	r.url("https://nvd.nist.gov/vuln/search")
	r.type('//*[@name="query"]', server + "[enter]")
	r.dom('window.scrollBy(0,400)')
	#SCREENSHOT
	r.wait(1.5)
	r.close()

	#Searchsploit
	r.init(visual_automation = True, chrome_browser = False)
	r.keyboard("[ctrl][shift][n]") # open new shell
	r.keyboard("searchsploit " + server + "[enter]")
	#SCREENSHOT
	r.wait(1.5)
	r.keyboard("[ctrl][shift][w]") # close shell
	r.close()


scan_server(url)