import requests
import rpa as r
from fpdf import FPDF

# the domain to scan for subdomains
domain = "google.com"

# read all subdomains
file = open("subdomains.txt")
# read all content
content = file.read()
# split by new lines
subdomains = content.splitlines()

def subdCode():
    # generate pdf
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', size=16)
    pdf.cell(200, 10, txt="RTA Integrated RPA", ln=2, align='L')
    pdf.set_font('')
    pdf.set_font('Arial', size=12)
    pdf.cell(200, 10, txt="Scanner: Subdomain Scanner", ln=1, align='L')
    pdf.cell(200, 10, txt="Results: ", ln=1, align='L')
    for subdomain in subdomains:
        # construct the url
        url = f"http://{subdomain}.{domain}"
        try:
          # if this raises an ERROR, that means the subdomain does not exist
            requests.get(url)
        except requests.ConnectionError:
            # if the subdomain does not exist, just pass, print nothing
            pass
    else:
        print("[+] Discovered subdomain:", url)
        r.init()
        r.url(url)
        r.wait()
        r.snap('page', url+'.png')
        r.close()
        
        pdf.cell(200, 10, txt="Target Scanned: "+ url, ln=1, align="L")
        pdf.cell(200, 10, txt="Summary:", ln=1, align="L")
        pdf.cell(200, 10, txt= "[+] Discovered subdomain:"+ url, ln=1, align="L")

    pdf.cell(200, 10, txt="End of Results.", ln=1, align="L")
    pdf.output(f'subdomains-scanned.pdf')
if __name__ == "__main__":
    subdCode()