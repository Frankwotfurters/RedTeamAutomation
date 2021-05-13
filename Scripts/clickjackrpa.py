from urllib.request import urlopen
from sys import argv, exit
import rpa as r
import requests

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
    #print(target)
    try: sites = open(target, 'r').readlines()
    except: print("[*] Usage: python(3) clickjacking_tester.py <file_name>"); exit(0)
    #file = open("sites.txt", 'r').readlines()

    for site in sites[0:]:
        print("\n[*] Checking " + site)
        status = check(site)

        if status:
            print("[+] Website is vulnerable!")
            create_poc(site.split('\n')[0])
            print("[*] Created a poc and saved to <URL>.html")
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

        elif not status: print("[-] Website is not vulnerable!")
        else: print('Everything crashed, RIP.')

if __name__ == '__main__': 
    main()