import requests
from urllib.request import urlparse, urljoin
from bs4 import BeautifulSoup
import colorama
import rpa as r
from fpdf import FPDF
import time
import os.path
import logging

# init the colorama module
colorama.init()

RED = colorama.Fore.RED
YELLOW = colorama.Fore.YELLOW
RESET = colorama.Fore.RESET

# initialize the set of links (unique links)
internal_urls = set()
external_urls = set()

total_urls_visited = 0

#Generate PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', size=16)
pdf.cell(200, 10, txt="RTA Integrated RPA", ln=2, align='L')
pdf.set_font('')
pdf.set_font('Arial', size=12)
pdf.cell(200, 10, txt="Scanner: Link Extractor", ln=1, align='L')
timestart = time.strftime("%d/%m/%Y %I:%M:%S")
time1 = time.strftime("%-H%M")
pdf.cell(200, 10, txt=f"Scan Time: {timestart}", ln=1, align="L")
pdf.cell(200, 10, txt="Results: ", ln=1, align='L')

def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def scan_link_extract(url):
    #Logfile
    logging.basicConfig(level=logging.INFO, filename="logfile", filemode="a+", format="%(asctime)-15s %(levelname)-8s %(message)s")
    logging.info("Running Link Extractor")
    print("Running Link Extractor")
    logging.info(f"Target: {url}")
    print(f"Target: {url}")

    get_all_website_links(url)
    crawl(url, max_urls=50)
    print_results(url)
    print_report(url)
    
def get_all_website_links(url):
    """
    Returns all URLs that is found on `url` in which it belongs to the same website
    """
    # all URLs of `url`
    urls = set()
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            # not a valid URL
            continue
        if href in internal_urls:
            # already in the set
            continue
        if domain_name not in href:
            # external link
            if href not in external_urls:
                print(f"{YELLOW}[!] External link: {href}{RESET}")
                external_urls.add(href)
            continue
        print(f"{RED}[*] Internal link: {href}{RESET}")
        urls.add(href)
        internal_urls.add(href)
    return urls

def crawl(url, max_urls=50):
    """
    Crawls a web page and extracts all links.
    You'll find all links in `external_urls` and `internal_urls` global set variables.
    params:
        max_urls (int): number of max urls to crawl, default is 30.
    """
    global total_urls_visited
    total_urls_visited += 1
    links = get_all_website_links(url)
    for link in links:
        if total_urls_visited > max_urls:
            break
        crawl(link, max_urls=max_urls)

#rpa to write urls into text documents
def print_results(url):
    domain_name = urlparse(url).netloc
    r.init(chrome_browser = False)
    for internal_link in internal_urls:
        r.write(internal_link.strip() + "\n", f"{domain_name}_internal_links({time1}).txt")
        
    for external_link in external_urls:
        r.write(external_link.strip() + "\n", f"{domain_name}_external_links({time1}).txt")
    r.close()

#OS path
pwd = os.path.dirname(os.path.realpath(__file__))

outputfile = f"{pwd}/link-extractor({time1}).pdf" 
displayfile = []
displayfile.append(f"{pwd}/link-extractor({time1}).pdf") 

def return_result(url):
    results = {}
    results["displayfile"] = displayfile
    return results

def print_report(url):
    total_len = len(external_urls) + len(internal_urls)

    #print report details in pdf
    pdf.cell(200, 10, txt="Target Scanned: "+ url, ln=1, align="L")
    pdf.cell(200, 10, txt="Summary:", ln=1, align="L")
    pdf.cell(200, 10, txt= "[+] Total Internal links: "+ str(len(internal_urls)), ln=1, align="L")
    pdf.cell(200, 10, txt="[+] Total External links: "+ str(len(external_urls)), ln=1, align="L")
    pdf.cell(200, 10, txt="[+] Total URLs: "+ str(total_len), ln=1, align="L")
    pdf.cell(200, 10, txt="All links are saved in a Text Document file and will automatically be downloaded.", ln=1, align="L")
    pdf.cell(200, 10, txt="End of Results.", ln=1, align="L")
    pdf.output(f'link-extractor({time1}).pdf')

    #rpa to open pdf file
    r.init(visual_automation=True)
    r.clipboard(f"file://{outputfile}")
    r.url()
    r.keyboard("[ctrl]l")
    r.keyboard("[ctrl]v")
    r.keyboard("[enter]")
    r.wait(10)
    r.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Link Extractor Tool with Python")
    parser.add_argument("url", help="The URL to extract links from.")
    parser.add_argument("-m", "--max-urls", help="Number of max URLs to crawl, default is 30.", default=30, type=int)
    
    args = parser.parse_args()
    url = args.url
    max_urls = args.max_urls

    scan_link_extract(url)
    domain_name = urlparse(url).netloc


