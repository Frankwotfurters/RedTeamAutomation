import rpa as r
import re
import retirejs
import requests
import json
import os.path
from fpdf import FPDF
import time
from bs4 import BeautifulSoup as bs
import urllib3
from urllib.parse import urljoin
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main(url):
	script_files = []
	jsOutput = {}

	#Generate PDF
	pdf = FPDF()
	pdf.add_page()
	pdf.set_font('Arial', 'B', size=16)
	pdf.cell(200, 10, txt="RTA Integrated RPA", ln=2, align='L')
	pdf.set_font('')
	pdf.set_font('Arial', size=12)
	pdf.cell(200, 10, txt="Scanner: Using Components with Known Vulnerabilities", ln=1, align='L')

	timestart = time.strftime("%d/%m/%Y %I:%M:%S")
	time1 = time.strftime("%-H%M")
	imgtime = time.strftime("(%d%m-%I%M%S)")
	pdf.cell(200, 10, txt=f"Scan Time: {timestart}", ln=1, align="L")
	pdf.cell(200, 10, txt="Results: ", ln=1, align='L')

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
		pdf.cell(200, 10, txt=f"[!] Scanned file: {js}", ln=1, align="L")
		scan = retirejs.scan_endpoint(js)
		jsOutput[js]=scan
		if scan == []:
			print("[-] No vulnerabiities found")
			pdf.cell(200, 10, txt="[-] No vulnerabiities found", ln=1, align="L")
		else:
			print(json.dumps(scan, indent=4))
			pdf.cell(200, 10, txt=json.dumps(scan, indent=4), ln=1, align="L")

	#Banner grabbing to retrieve web server (and version)
	server = requests.get(url).headers['Server']
	server = re.sub(r" ?\([^)]+\)", "", server).replace('/', ' ')
	print(f"[!] Scanning Server Version: {server}")
	pdf.cell(200, 10, txt=f"[!] Server Version: {server}", ln=1, align="L")

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
	pdf.add_page(orientation="L")
	pdf.cell(200, 10, txt=f"National Vulnerability Database query result for [{server}]", ln=1, align='L')
	pdf.image(f'{pwd}/{nvdOutput}',10,30,250,130)

	#Exploit-DB Query using banner grabbing result
	r.url("https://www.exploit-db.com/search")
	r.type('//*[@name="q"]', server + "[enter]")
	r.wait(1)
	r.snap('page', f'{server}_Exploit-DB.png')
	eDBOutput = f'{server}_Exploit-DB.png'
	print(f"[+] Saved Exploit-DB Query to {pwd}/{eDBOutput}")
	pdf.add_page(orientation="L")
	pdf.cell(200, 10, txt=f"Exploit-DB query result for [{server}]", ln=1, align='L')
	pdf.image(f'{pwd}/{eDBOutput}',10,30,250,130)

	#Cleanup
	pdf.output(f"vulncomponents({time1}).pdf")
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