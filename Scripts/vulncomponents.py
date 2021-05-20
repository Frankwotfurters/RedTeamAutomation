import rpa as r
import re
import retirejs
import requests
import json
import os
from bs4 import BeautifulSoup as bs
import urllib3
from urllib.parse import urljoin
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main(url):
	script_files = []
	jsOutput = {}
	nvdOutput = ""
	eDBOutput = ""

	#Scan JS files loaded	
	html = requests.get(url).content
	soup = bs(html, "html.parser")
	for script in soup.find_all("script"):
	    if script.attrs.get("src"):
	        # if the tag has the attribute 'src'
	        script_url = urljoin(url, script.attrs.get("src"))
	        script_files.append(script_url)

	#run retire.js on each script
	for js in script_files:
		print(f"[!] Scanning file: {js}")
		scan = retirejs.scan_endpoint(js)
		jsOutput[js]=scan

	#Banner grabbing to retrieve web server (and version)
	server = requests.get(url).headers['Server']
	server = re.sub(r" ?\([^)]+\)", "", server).replace('/', ' ')
	print(f"[!] Scanning Server Version: {server}")

	#NVD Query using banner grabbing result
	r.init(visual_automation = True)
	r.url("https://nvd.nist.gov/vuln/search")
	r.type('//*[@name="query"]', f"{server}[enter]")
	r.wait(1)
	r.dom('window.scrollTo(0,400)')
	r.snap('page', f'{server}_NVD.png')
	nvdOutput = f'{server}_NVD.png'
	pwd = os.path.dirname(os.path.realpath(__file__))
	print(f"[+] Saved NVD Query to {pwd}/{nvdOutput}")

	#Exploit-DB Query using banner grabbing result
	r.url("https://www.exploit-db.com/search")
	r.type('//*[@name="q"]', server + "[enter]")
	r.wait(1)
	r.snap('page', f'{server}_Exploit-DB.png')
	eDBOutput = f'{server}_Exploit-DB.png'
	print(f"[+] Saved Exploit-DB Query to {pwd}/{eDBOutput}")
	r.close()

	results = {}
	results["jsOutput"] = jsOutput
	results["nvdOutput"] = nvdOutput
	results["eDBOutput"] = eDBOutput

	return results #retirejs output, screenshot outputs from nvd & e-db

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("target")
	args = parser.parse_args()
	args = vars(parser.parse_args())["target"]

	if args.startswith('http://') or args.startswith('https://'):
		main(args)
	else:
		parser.error("Target must start with http:// or https://")