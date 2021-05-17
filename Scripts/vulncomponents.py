import rpa as r
import re
import retirejs
import requests
import json
from bs4 import BeautifulSoup as bs
import urllib3
from urllib.parse import urljoin
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

script_files = []
jsOutput = {}
nvdOutput = ""
searchsploitOutput = ""

def scan_js(url):
	#compiles list of js files loaded	
	html = requests.get(url).content
	soup = bs(html, "html.parser")
	for script in soup.find_all("script"):
	    if script.attrs.get("src"):
	        # if the tag has the attribute 'src'
	        script_url = urljoin(url, script.attrs.get("src"))
	        script_files.append(script_url)

	#run retire.js on each script
	for js in script_files:
		print("Scanning file: " + js)
		scan = retirejs.scan_endpoint(js)
		print(json.dumps(scan, indent=2))
		jsOutput[js]=scan

	print(json.dumps(jsOutput, indent=2))

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
	r.snap('page', server+'NVD.png')
	nvdOutput = server+'NVD.png'
	r.wait(1.5)
	r.close()

	#Searchsploit
	# r.init(visual_automation = True, chrome_browser = False)
	# r.keyboard("[win]")
	# r.keyboard("terminal[enter]") # open new shell
	# r.keyboard("searchsploit " + server + "[enter]")
	# r.snap('page', server+'Searchsploit.png')
	# r.wait(1.5)
	# r.keyboard("[ctrl][shift][w]") # close shell
	# r.close()

def main(url):
	scan_js(url)
	scan_server(url)

	results = {}
	results["jsOutput"] = jsOutput
	results["nvdOutput"] = nvdOutput
	results["searchsploitOutput"] = searchsploitOutput

	return results #retirejs output, screenshots from searchsploit & nvd

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("target")
	args = parser.parse_args()
	args = vars(parser.parse_args())["target"]

	if args.startswith('http://') or args.startswith('https://'):
		print(main(args))
	else:
		parser.error("Target must start with http:// or https://")