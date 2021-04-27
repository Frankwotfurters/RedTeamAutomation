#pip install retirejs
import retirejs
import requests
import json
from bs4 import BeautifulSoup as bs
import urllib3
from urllib.parse import urljoin
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "http://localhost:8000/test.html"

html = requests.get(url).content
soup = bs(html, "html.parser")

#print(requests.get(url).headers)

def scan_js(html):
	#compiles list of js files loaded	
	script_files = []
	for script in html.find_all("script"):
	    if script.attrs.get("src"):
	        # if the tag has the attribute 'src'
	        script_url = urljoin(url, script.attrs.get("src"))
	        script_files.append(script_url)

	#run retire.js on each script
	for js in script_files:
		print(js)
		scan = retirejs.scan_endpoint(js)
		print(json.dumps(scan, indent=2))

scan_js(soup)