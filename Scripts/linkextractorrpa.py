import requests
from urllib.request import urlparse, urljoin
from bs4 import BeautifulSoup
import colorama
import rpa as r

# init the colorama module
colorama.init()

RED = colorama.Fore.RED
YELLOW = colorama.Fore.YELLOW
RESET = colorama.Fore.RESET

# initialize the set of links (unique links)
internal_urls = set()
external_urls = set()

total_urls_visited = 0


def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def scan_link_extract(url):
    get_all_website_links(url)
    crawl(url, max_urls=50)
    print_results(url)
    
    
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

def print_results(url):
    domain_name = urlparse(url).netloc
    r.init(chrome_browser = False)
    for internal_link in internal_urls:
        r.write(internal_link.strip() + "\n", f"{domain_name}_internal_links.txt")
        
    for external_link in external_urls:
        r.write(external_link.strip() + "\n", f"{domain_name}_external_links.txt")
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

    
    print("[+] Total Internal links:", len(internal_urls))
    print("[+] Total External links:", len(external_urls))
    print("[+] Total URLs:", len(external_urls) + len(internal_urls))

    domain_name = urlparse(url).netloc
#     #save the internal links to a file
#     with open(f"{domain_name}_internal_links.txt", "w") as f:
#         for internal_link in internal_urls:
#             print(internal_link.strip(), file=f)

#     # save the external links to a file
#     with open(f"{domain_name}_external_links.txt", "w") as f:
#         for external_link in external_urls:
#             print(external_link.strip(), file=f)
# print("[*] URL Links saved to respective files.")

