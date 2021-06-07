from urllib.request import urlopen
from sys import argv, exit
import rpa as r
import requests
from fpdf import FPDF
import time
import os.path
import logging

def check(url):
    ''' check given URL is vulnerable or not '''

    try:
        if "http" not in url: url = "http://" + url

        data = urlopen(url)
        headers = data.info()

        if not "X-Frame-Options" in headers: return True

    except: return False


def create_poc(url):
    ''' create HTML page of given URL '''

    code = """
<html>
   <head><title>Clickjack test page</title></head>
   <body>
     <p>Website is vulnerable to clickjacking!</p>
     <iframe src="{}" width="500" height="500"></iframe>
   </body>
</html>
    """.format(url)

    with open(url + ".html", "w") as f:
        f.write(code)
        f.close()

def main(target):
    ''' Everything comes together '''
    #Logfile
    logging.basicConfig(level=logging.INFO, filename="logfile", filemode="a+", format="%(asctime)-15s %(levelname)-8s %(message)s")
    logging.info("Running Clickjacking Scanner")
    logging.info(f"Test File: {target}")


    #Generate PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', size=16)
    pdf.cell(200, 10, txt="RTA Integrated RPA", ln=2, align='L')
    pdf.set_font('')
    pdf.set_font('Arial', size=12)
    pdf.cell(200, 10, txt="Scanner: Clickjacking", ln=1, align='L')

    timestart = time.strftime("%d/%m/%Y %I:%M:%S")
    time1 = time.strftime("%-H%M")
    imgtime = time.strftime("(%d%m-%I%M%S)")
    pdf.cell(200, 10, txt=f"Scan Time: {timestart}", ln=1, align="L")
    pdf.cell(200, 10, txt="Results: ", ln=1, align='L')

    try: 
        sites = open(target, 'r').readlines()
        if not sites:
            exit()
    except: 
        print("Error: Text File is empty"); exit(0)
 
    for site in sites[0:]:
        print("\n[*] Checking " + site)
        pdf.cell(200, 10, txt="[*] Checking " + site, ln=1, align="L")
        status = check(site)

        if status:
            print("[+] Website is vulnerable!")
            logging.info(f"{site} is vulnerable")
            pdf.cell(200, 10, txt=f"[+] {site} is vulnerable!", ln=1, align="L")
            create_poc(site.split('\n')[0])
            print("[*] Created a poc and saved to <URL>.html")
            pdf.cell(40, 10, txt=f"[*] Created a POC and saved to {site}.html", ln=1, align="L")
            pdf.cell(40, 10, txt=f"Screenshot(s) of POC will be in the following page(s).", ln=1, align="L")
            r.init(visual_automation=True)
            #file:///root/Documents/ProjectScripts/www6.turkhackteam.com.html
            #test = "file:///root/Documents/ProjectScripts/"

            pwd = os.path.dirname(os.path.realpath(__file__))
            saved = pwd + "/" + site + ".html"
            #RPA (To take screenshot)
            r.clipboard(f"file://{saved}")
            r.url()
            r.keyboard("[ctrl]l")
            r.keyboard("[ctrl]v")
            r.keyboard("[enter]")
            r.wait()
            ss = []
            ss.append(f"clickjack-{imgtime}.png")
            r.snap("page", f"clickjack-{imgtime}.png")
            r.close()

            print(" ")
            for i in ss:
                pdf.add_page(orientation="L")
                pdf.set_font('Arial', size=12)
                pdf.cell(200, 10, txt=f"Proof of Concept ({i})", ln=1, align='L')
                pdf.image(f'{pwd}/{i}',50,50,300,120)

        elif not status: 
            print("[-] Website is not vulnerable!") 
            logging.info(f" {site} is not vulnerable!")
            pdf.cell(200, 10, txt=f"[-] {site} is not vulnerable!", ln=1, align="L")
            pdf.cell(200, 10, txt=" ", ln=1, align="L")
        else: 
            print('Everything crashed, RIP.') 
            logging.info(f"Everything crashed, RIP.")
            pdf.cell(200, 10, txt="[-] Everything crashed, RIP.", ln=1, align="L")
            pdf.cell(200, 10, txt="[-] Please run the scanner again.", ln=1, align="L")
    
    pdf.cell(200, 10, txt="End of Results.", ln=1, align="L")
    # To add screenshots of all vulnerable pages to the PDF Report
    # for i in ss:
    #     pdf.add_page(orientation="L", format="A4")
    #     pdf.set_font('Arial', size=12)
    #     pdf.cell(200, 10, txt=f"Proof of Concept ({i})", ln=1, align='L')
    #     pdf.image(f'{pwd}/{i}',50,50,300,120)


    imgTime = time.strftime("%d-%m-%Y%H%M%S")
    pdf.output(f"Clickjacking_{imgTime}.pdf")
    pwd = os.path.dirname(os.path.realpath(__file__))
    displayfile = []
    displayfile.append(f"{pwd}/Clickjacking_{imgTime}.pdf")
    outputfile = f"{pwd}/Clickjacking_{imgTime}.pdf"

    #RPA (To open PDF file after scan)
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
    return results


if __name__ == '__main__': 
    main()