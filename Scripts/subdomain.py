import requests
import rpa as r
from fpdf import FPDF
import time
import os.path
import logging
import sendmail

# the domain to scan for subdomains
domain = "google.com"

# to name screenshot
imageTime = time.strftime("%-H%M")

def subdCode(target, receiver=""):
    logging.basicConfig(level=logging.INFO, filename="logfile", filemode="a+", format="%(asctime)-15s %(levelname)-8s %(message)s")
    print("Running Subdomain Scanner")
    logging.info("Running Subdomain Scanner")
    print(f"Target: {target}")
    logging.info(f"Target: {target}")
    logging.info(f"Using Domain: {domain}")

    # generate pdf
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', size=16)
    pdf.cell(200, 10, txt="RTA Integrated RPA", ln=2, align='L')
    pdf.set_font('')
    pdf.set_font('Arial', size=12)
    pdf.cell(200, 10, txt="Scanner: Subdomain Scanner", ln=1, align='L')
    timestart = time.strftime("%d/%m/%Y %I:%M:%S")
    time1 = time.strftime("%d-%m-%Y%H%M%S")
    pdf.cell(200, 10, txt=f"Scan Time: {timestart}", ln=1, align="L")
    pdf.cell(200, 10, txt="Results: ", ln=1, align='L')
    ss = []
    subdomain_tested = []
    subdomain_result = []
    r.init()

    # read all subdomains
    file = open(target, 'r')
    # read all content
    content = file.read()
    # split by new lines
    subdomains = content.splitlines()

    for subdomain in subdomains:
        # construct the url
        url = f"http://{subdomain}.{domain}"
        try:
          # if this raises an ERROR, that means the subdomain does not exist
            requests.get(url)
        except requests.ConnectionError:
            # if the subdomain does not exist, just pass, print nothing
            logging.info(f"[+] Subdomain does not exist: {url}")
            pass
        else:
            print("[+] Discovered subdomain:", url)
            #rpa
            r.url(url)
            r.wait()
            ss.append(f"{subdomain}({imageTime}).png")
            r.snap('page', f"{subdomain}({imageTime}).png")
            pdf.cell(200, 10, txt="Target Scanned: "+ url, ln=1, align="L")
            logging.info(f"Target Scanned: {url}")
            pdf.cell(200, 10, txt= "[+] Discovered subdomain:"+ url, ln=1, align="L")
            logging.info(f"[+] Discovered subdomain: {url}")

            subdomain_tested.append(subdomain)
            subdomain_result.append("Subdomain Detected")
    r.close()

    pdf.cell(200, 10, txt="End of Results.", ln=1, align="L")
    logging.info(f"End of Results.")
    pdf.cell(40, 10, txt=f"Screenshot(s) will be in the following page(s).", ln=1, align="L")

    #OS Path
    pwd = os.path.dirname(os.path.realpath(__file__))

    # To add screenshots of all vulnerable pages to the PDF Report
    for i in ss:
        pdf.add_page(orientation="L")
        pdf.set_font('Arial', size=12)
        pdf.cell(200, 10, txt=f"{i}", ln=1, align='L')
        pdf.image(f'{pwd}/{i}',50,50,300,120)

    pdf.output(f'Subdomain_{time1}.pdf')

    # RPA (To open PDF file after scan)
    outputfile = f"{pwd}/Subdomain_{time1}.pdf"
    displayfile = []
    displayfile.append(f"{pwd}/Subdomain_{time1}.pdf")

    if not receiver == "":
        # Send email
        sendmail.main("Subdomain", target, outputfile, receiver)

    r.init(visual_automation=True)
    r.clipboard(f"file://{outputfile}")
    r.url()
    r.keyboard("[ctrl]l")
    r.keyboard("[ctrl]v")
    r.keyboard("[enter]")
    r.wait(10)
    r.close()

    #Display PDF link on results page
    results = {}
    results["displayfile"] = displayfile
    results["subdomain_tested"] = subdomain_tested
    results["subdomain_result"] = subdomain_result
    return results

if __name__ == "__main__":
    subdCode()