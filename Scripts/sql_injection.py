import requests
import rpa as r
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from pprint import pprint
from fpdf import FPDF
import time

s = requests.Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"

def get_all_forms(url):
    """Given a `url`, it returns all forms from the HTML content"""
    soup = bs(s.get(url).content, "html.parser")
    return soup.find_all("form")


def get_form_details(form):
    """
    This function extracts all possible useful information about an HTML `form`
    """
    details = {}
    # get the form action (target url)
    try:
        action = form.attrs.get("action").lower()
    except:
        action = None
    # get the form method (POST, GET, etc.)
    method = form.attrs.get("method", "get").lower()
    # get all the input details such as type and name
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value", "")
        inputs.append({"type": input_type, "name": input_name, "value": input_value})
    # put everything to the resulting dictionary
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

def is_vulnerable(response):
    """A simple boolean function that determines whether a page 
    is SQL Injection vulnerable from its `response`"""
    errors = {
        # MySQL
        "you have an error in your sql syntax;",
        "warning: mysql",
        # SQL Server
        "unclosed quotation mark after the character string",
        # Oracle
        "quoted string not properly terminated",
    }
    for error in errors:
        # if you find one of these errors, return True
        if error in response.content.decode().lower():
            return True
    # no error detected
    return False

def scan_sql_injection(url):
    # generate pdf
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', size=16)
    pdf.cell(200, 10, txt="RTA Integrated RPA", ln=2, align='L')
    pdf.set_font('')
    pdf.set_font('Arial', size=12)
    pdf.cell(200, 10, txt="Scanner: SQL Injection", ln=1, align='L')
    timestart = time.strftime("%d/%m/%Y %I:%M:%S")
    time1 = time.strftime("%-H%M")
    imageTime = time.strftime("%-H%M")
    pdf.cell(200, 10, txt=f"Scan Time: {timestart}", ln=1, align="L")
    pdf.cell(200, 10, txt="Results: ", ln=1, align='L')
    # test on URL
    for c in "\"'":
        # add quote/double quote character to the URL
        new_url = f"{url}{c}"
        print("[!] Trying", new_url)
        # make the HTTP request
        res = s.get(new_url)
        if is_vulnerable(res):
            # SQL Injection detected on the URL itself, 
            # no need to preceed for extracting forms and submitting them
            print("[+] SQL Injection vulnerability detected, link:", new_url)
             # rpa 
            r.init()
            r.url(url+'%27')
            r.wait()
            x = url
            n = x.translate({ord(i): None for i in ':/.'})
            r.snap('page', 'sql-injection-'+imageTime+'.png')
            r.close()

            pdf.cell(200, 10, txt="Target Scanned: "+ url, ln=1, align="L")
            pdf.cell(200, 10, txt="Summary:", ln=1, align="L")
            pdf.cell(200, 10, txt= "[+] SQL Injection vulnerability detected (URL):"+ url, ln=1, align="L")
            pdf.cell(200, 10, txt="End of Results.", ln=1, align="L")
            pdf.cell(40, 10, txt=f"Screenshot(s) will be in the following page(s).", ln=1, align="L")

            # to add screenshots of all vulnerable pages to the pdf report
            pdf.add_page()
            pdf.set_font('Arial', size=12)
            pdf.cell(200, 10, txt=f"({url})", ln=1, align='L')
            pdf.image(f'/media/sf_Kali_VM_Shared_Folder/RedTeamAutomation/Scripts/sql-injection-{imageTime}.png',50,50,300,120)

            pdf.output(f'sql_injection({time1}).pdf')

            #RPA (To open PDF file after scan)
            outputfile = f"sql_injection({time1}).pdf"
            r.init(visual_automation=True)
            r.clipboard(f"file:///media/sf_Kali_VM_Shared_Folder/RedTeamAutomation/Scripts/{outputfile}")
            r.url()
            r.keyboard("[ctrl]l")
            r.keyboard("[ctrl]v")
            r.keyboard("[enter]")
            return
    # test on HTML forms
    forms = get_all_forms(url)
    print(f"[+] Detected {len(forms)} forms on {url}.")
    for form in forms:
        form_details = get_form_details(form)
        for c in "\"'":
            # the data body we want to submit
            data = {}
            for input_tag in form_details["inputs"]:
                if input_tag["value"] or input_tag["type"] == "hidden":
                    # any input form that has some value or hidden,
                    # just use it in the form body
                    try:
                        data[input_tag["name"]] = input_tag["value"] + c
                    except:
                        pass
                elif input_tag["type"] != "submit":
                    # all others except submit, use some junk data with special character
                    data[input_tag["name"]] = f"test{c}"
            # join the url with the action (form request URL)
            url = urljoin(url, form_details["action"])
            if form_details["method"] == "post":
                res = s.post(url, data=data)
            elif form_details["method"] == "get":
                res = s.get(url, params=data)
            # test whether the resulting page is vulnerable
            if is_vulnerable(res):
                print("[+] SQL Injection vulnerability detected, link:", url)
                print("[+] Form:")
                pprint(form_details)
                  # rpa 
                r.init()
                r.url(url)
                r.wait()
                ss = []
                ss.append(f"sql-injection-{url}.png")
                n = s.translate({ord(i): None for i in ':/'})
                r.snap('page', n+'.png')
                r.close()

                pdf.cell(200, 10, txt="Target Scanned: "+ url, ln=1, align="L")
                pdf.cell(200, 10, txt="Summary:", ln=1, align="L")
                pdf.cell(200, 10, txt= "[+] SQL Injection vulnerability detected with specified link (FORM):", ln=1, align="L")
                pdf.cell(200, 10, txt= "[+] Form:", ln=1, align="L")
                pdf.cell(200, 10, print(form_details), ln=1, align="L")
                pdf.cell(40, 10, txt=f"Screenshot(s) will be in the following page(s).", ln=1, align="L")
                pdf.cell(200, 10, txt="End of Results.", ln=1, align="L")

                # # To add screenshots of all vulnerable pages to the PDF Report
                # for i in ss:
                #     pdf.add_page(orientation="L", format="A4")
                #     pdf.set_font('Arial', size=12)
                #     pdf.cell(200, 10, txt=f"Screenshots: ({i})", ln=1, align='L')
                #     pdf.image(f'/media/sf_Shared_VM_Folder_(Kali)/Scripts/{i}',50,50,300,120)

                pdf.output(f'sql_injection({time1}).pdf')

                #RPA (To open PDF file after scan)
                outputfile = f"sql_injection({time1}).pdf"
                r.init(visual_automation=True)
                r.clipboard(f"file:///media/sf_Kali_VM_Shared_Folder/RedTeamAutomation/Scripts/{outputfile}")
                r.url()
                r.keyboard("[ctrl]l")
                r.keyboard("[ctrl]v")
                r.keyboard("[enter]")
                break   
            
if __name__ == "__main__":
    import sys
    url = sys.argv[1]
    scan_sql_injection(url)