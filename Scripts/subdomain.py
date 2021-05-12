import requests
import rpa as r

# the domain to scan for subdomains
domain = "google.com"

# read all subdomains
file = open("subdomains.txt")
# read all content
content = file.read()
# split by new lines
subdomains = content.splitlines()

def subdCode():
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

if __name__ == "__main__":
    subdCode()