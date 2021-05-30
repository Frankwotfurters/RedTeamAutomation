import rpa as r
import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import os.path
import time
from fpdf import FPDF


# url = input("Please Enter Target: ")
def get_all_forms(target):
    #"""Given a `url`, it returns all forms from the HTML content"""
    soup = bs(requests.get(target).content, "html.parser")
    form = soup.find('form')
    return soup.find_all("form")
    return new


def get_form_details(form):
    """
    This function extracts all possible useful information about an HTML `form`
    """
    details = {}
    # get the form action (target url)
    action = form.attrs.get("action").lower()
    # get the form method (POST, GET, etc.)
    method = form.attrs.get("method", "get").lower()
    # get all the input details such as type and name
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name": input_name})
    # put everything to the resulting dictionary
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details



def submit_form(form_details, target, value):
    """
    Submits a form given in `form_details`
    Params:
        form_details (list): a dictionary that contain form information
        url (str): the original URL that contain that form
        value (str): this will be replaced to all text and search inputs
    Returns the HTTP Response after form submission
    """
    # construct the full URL (if the url provided in action is relative)
    target_url = urljoin(target, form_details["action"])
    # get the inputs
    inputs = form_details["inputs"]
    data = {}
    for input in inputs:
        # replace all text and search values with `value`
        if input["type"] == "text" or input["type"] == "search":
            input["value"] = value
        input_name = input.get("name")
        input_value = input.get("value")

        if input_name and input_value:
            # if input name and value are not None, 
            # then add them to the data of form submission
            data[input_name] = input_value

    if form_details["method"] == "post":
        return requests.post(target_url, data=data)
    else:
        # GET request
        return requests.get(target_url, params=data)


def scan_xss(target):
    #PDF Report Generation
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', size=16)
    pdf.cell(200, 10, txt="RTA Integrated RPA", ln=2, align='L')
    pdf.set_font('')
    pdf.set_font('Arial', size=12)
    pdf.cell(200, 10, txt="Scanner: Cross Site Scripting", ln=1, align='L')
    timestart = time.strftime("%d/%m/%Y %I:%M:%S")
    time1 = time.strftime("%-H%M")
    imgtime = time.strftime("(%d%m-%I%M%S)")
    pdf.cell(200, 10, txt=f"Scan Time: {timestart}", ln=1, align="L")
    pdf.cell(200, 10, txt="Results: ", ln=1, align='L')


    # get all the forms from the URL
    forms = get_all_forms(target)
    formdata = get_all_forms(target)
    print(f"[+] Detected {len(forms)} forms on {target}.")
    js_script = "<Script>alert('hi')</scripT>"
    # returning value
    is_vulnerable = False
    # iterate over all forms

    ss = []
    for form in forms:
        pwd = os.path.dirname(os.path.realpath(__file__))
        form_details = get_form_details(form)
        #inputs = get_form_details(form)
        content = submit_form(form_details, target, js_script).content.decode()
        if js_script in content:
            
            print(f"[+] XSS Detected on {target}")
            print(f"[+] Form details:")
            pdf.cell(40, 10, txt=f"[+] {target} is vulnerble", ln=1, align="L")
            pdf.cell(40, 10, txt=f"[+] XSS Detected on {target}", ln=1, align="L")
            pdf.cell(40, 10, txt=f"[+] Form details:", ln=1, align="L")

            inputs = get_form_details(form)
            soup = bs(requests.get(target).content, "html.parser")
            fields = soup.findAll('input')
            formdata = dict( (field.get('name'), field.get('name')) for field in fields)
            new = formdata.copy()
            
            #Remove NoneType from dictionary
            for i in formdata:
                if i == None:
                    del new[i]

            #Enter JS Script into form(s)
            for i in new:
                    r.init()
                    r.url(target)
                    r.type(i, "<script>document.documentElement.innerHTML = 'Page is vulnerable to XSS. <br> Form did not execute properly when malicious javascript code was entered.'</script>[enter]")
                    ss.append(f"xssscanner-{imgtime}.png")
                    r.snap("page", f"xssscanner-{imgtime}.png")
                    r.close()
        
            pprint(form_details)
            pdf.cell(40, 10, txt=f"{form_details['inputs']}", ln=1, align="L")
            pdf.cell(40, 10, txt=f"Screenshot(s) of POC will be in the following page(s).", ln=1, align="L")
            is_vulnerable = True
            # won't break because we want to print other available vulnerable forms

        else:
            print(f"[-] {target} is not vulnerable!") 
            pdf.cell(200, 10, txt=f"[-] XSS was not detected on {target}", ln=1, align="L")
            pdf.cell(200, 10, txt=f"[-] {target} is not vulnerable!", ln=1, align="L")
            pdf.cell(40, 10, txt=f"[+] Form details:", ln=1, align="L")
            pdf.cell(40, 10, txt=f"{form_details['inputs']}", ln=1, align="L")
            pdf.cell(200, 10, txt=" ", ln=1, align="L")
    
    pdf.cell(200, 10, txt="End of Results.", ln=1, align="L")

    #Retrieve Screenshot path from ss
    if ss:
        for i in ss:
            pdf.add_page(orientation="L")
            pdf.set_font('Arial', size=12)
            pdf.cell(200, 10, txt=f"Proof of Concept ({i})", ln=1, align='L')
            pdf.image(f'{pwd}/{i}',50,50,300,120)

    pdf.output(f"xssscanner({time1}).pdf")
    pwd = os.path.dirname(os.path.realpath(__file__))
    displayfile = []
    displayfile.append(f"{pwd}/xssscanner({time1}).pdf")
    outputfile = f"{pwd}/xssscanner({time1}).pdf"

    #RPA (To open PDF file after scan)
    r.init(visual_automation=True)
    r.clipboard(f"file://{outputfile}")
    r.url()
    r.keyboard("[ctrl]l")
    r.keyboard("[ctrl]v")
    r.keyboard("[enter]")
    r.wait(10)
    r.close

    #Display PDF link on results page
    results = {}
    results["displayfile"] = displayfile
    return results

    return is_vulnerable




if __name__ == "__main__":
    scan_xss(target)
    # import sys
    # #url = sys.argv[1]
    # print(scan_xss(url))