import rpa as r
import requests
from pprint import pprint
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import re

def main(url):

    def get_all_forms(url):
        """Given a url, it returns all forms from the HTML content"""
        soup = bs(requests.get(url).content, "html.parser")
        return soup.find_all("form")


    def get_form_details(form):
        """
        This function extracts all possible useful information about an HTML form
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
        print(details)
        return details

    def submit_form(form_details, url, value):
        """
        Submits a form given in `form_details`
        Params:
            form_details (list): a dictionary that contain form information
            url (str): the original URL that contain that form
            value (str): this will be replaced to all text and search inputs
        Returns the HTTP Response after form submission
        """
        # construct the full URL (if the url provided in action is relative)
        target_url = urljoin(url, form_details["action"])
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


    def scan_form(url):
        """
        Given a `url`, it prints all XSS vulnerable forms and 
        returns True if any is vulnerable, False otherwise
        """
        # get all the forms from the URL
        forms = get_all_forms(url)
        #print(f"[+] Detected {len(forms)} forms on {url}.")
        js_script = "<Script>alert('hi')</scripT>"
        # returning value
        #is_vulnerable = False
        # iterate over all forms
        for form in forms:
            form_details = get_form_details(form)
            content = submit_form(form_details, url, js_script).content.decode()
            #if js_script in content:
                #print(f"[+] XSS Detected on {url}")
                #print(f"[*] Form details:")
                #pprint(form_details)
                #is_vulnerable = True
                # won't break because we want to print other available vulnerable forms
        #return is_vulnerable

    s = requests.Session()
    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser")
    form = soup.find('form')
    fields = form.findAll('input')

    formdata = dict( (field.get('name'), field.get('id')) for field in fields)

    # formdata['name'] = u'username'
    # formdata['hello'] = u'password'

    # print(formdata)
    posturl = urljoin(url, form['action'])
    #print(posturl)

    #r = s.post(posturl, data=formdata)
    #print(r.text)

    data = list(formdata)

    r.init()
    r.url(url)
    for i in data:
        r.type('//*[@name=' + '"' + i + '"]', 'username')
        data.remove(i)
        break
    for i in data:
        r.type('//*[@name=' + '"' + i + '"]', 'password[enter]')

    if "Incorrect username or password" in r.text():
        print("Sensitive Data Exposure: False")
    else:
        print("Sensitive Data Exposure: True")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help = "URL of login page to web app.", required = True)
    args = parser.parse_args()
    args = vars(parser.parse_args())

    main(url)