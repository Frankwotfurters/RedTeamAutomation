import requests
import rpa as r
from fpdf import FPDF
import time

# the domain to scan for subdomains
domain = "google.com"

# read all subdomains
file = open("subdomains.txt")
# read all content
content = file.read()
# split by new lines
subdomains = content.splitlines()

imageTime = time.strftime("%-H%M")

def subdCode():
    # generate pdf
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', size=16)
    pdf.cell(200, 10, txt="RTA Integrated RPA", ln=2, align='L')
    pdf.set_font('')
    pdf.set_font('Arial', size=12)
    pdf.cell(200, 10, txt="Scanner: Subdomain Scanner", ln=1, align='L')
    timestart = time.strftime("%d/%m/%Y %I:%M:%S")
    time1 = time.strftime("%-H%M")
    pdf.cell(200, 10, txt=f"Scan Time: {timestart}", ln=1, align="L")
    pdf.cell(200, 10, txt="Results: ", ln=1, align='L')
    r.init()
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
        r.url(url)
        r.wait()
        ss = []
        ss.append(f"subdomains-{imageTime}.png")
        r.snap('page', 'subdomains-'+imageTime+'.png')
        r.close()
        
        pdf.cell(200, 10, txt="Target Scanned: "+ url, ln=1, align="L")
        pdf.cell(200, 10, txt="Summary:", ln=1, align="L")
        pdf.cell(200, 10, txt= "[+] Discovered subdomain:"+ url, ln=1, align="L")

    pdf.cell(200, 10, txt="End of Results.", ln=1, align="L")
    pdf.cell(40, 10, txt=f"Screenshot(s) will be in the following page(s).", ln=1, align="L")

    # To add screenshots of all vulnerable pages to the PDF Report
    for i in ss:
        pdf.add_page(orientation="L")
        pdf.set_font('Arial', size=12)
        pdf.cell(200, 10, txt=f"({i})", ln=1, align='L')
        pdf.image(f'/media/sf_Kali_VM_Shared_Folder/RedTeamAutomation/Scripts/subdomains-{imageTime}.png',50,50,300,120)

    pdf.output(f'subdomains-scanned({time1}).pdf')

    # RPA (To open PDF file after scan)
    outputfile = f"subdomains-scanned({time1}).pdf"
    r.init(visual_automation=True)
    r.clipboard(f"file:///media/sf_Kali_VM_Shared_Folder/RedTeamAutomation/Scripts/{outputfile}")
    r.url()
    r.keyboard("[ctrl]l")
    r.keyboard("[ctrl]v")
    r.keyboard("[enter]")

if __name__ == "__main__":
    subdCode()