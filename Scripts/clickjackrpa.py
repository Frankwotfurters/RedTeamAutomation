from urllib.request import urlopen
from sys import argv, exit
import rpa as r
import requests
from fpdf import FPDF

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
    #Generate PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', size=16)
    pdf.cell(200, 10, txt="RTA Integrated RPA", ln=2, align='L')
    pdf.set_font('')
    pdf.set_font('Arial', size=12)
    pdf.cell(200, 10, txt="Scanner: Clickjacking", ln=1, align='L')
    pdf.cell(200, 10, txt="Results: ", ln=1, align='L')

    #print(target)
    try: sites = open(target, 'r').readlines()
    except: print("[*] Usage: python(3) clickjacking_tester.py <file_name>"); exit(0)
    #file = open("sites.txt", 'r').readlines()

    for site in sites[0:]:
        print("\n[*] Checking " + site)
        pdf.cell(200, 10, txt="[*] Checking " + site, ln=1, align="L")
        status = check(site)

        if status:
            print("[+] Website is vulnerable!")
            pdf.cell(200, 10, txt="[+] Website is vulnerable!", ln=1, align="L")
            create_poc(site.split('\n')[0])
            print("[*] Created a poc and saved to <URL>.html")
            pdf.cell(40, 10, txt=f"[*] Created a poc and saved to {site}.html", ln=1, align="L")
            r.init(visual_automation=True)
            #file:///root/Documents/ProjectScripts/www6.turkhackteam.com.html
            #test = "file:///root/Documents/ProjectScripts/"
            r.clipboard("file:///media/sf_Shared_VM_Folder_(Kali)/Scripts/"+site+".html")
            r.url()
            r.keyboard("[ctrl]l")
            r.keyboard("[ctrl]v")
            r.keyboard("[enter]")
            r.wait()
            r.snap("page", f"clickjack-{site}.png")
            r.close()

            print(" ")

        elif not status: 
            print("[-] Website is not vulnerable!") 
            pdf.cell(200, 10, txt="[-] Website is not vulnerable!", ln=1, align="L")
            pdf.cell(200, 10, txt=" ", ln=1, align="L")
        else: 
            print('Everything crashed, RIP.') 
            pdf.cell(200, 10, txt="[-] Everything crashed, RIP.", ln=1, align="L")

    pdf.cell(200, 10, txt="End of Results.", ln=1, align="L")
    pdf.output(f'clickjack-{target}.pdf')

if __name__ == '__main__': 
    main()