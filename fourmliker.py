import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import colorama
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
import os



user_id = 'INSERT ID'
files = 'Insert the path any blank txt file'
driver_file = 'Insert path to a chromedriver file'

#test stuff
# user_id = '23844'
# files = '/Users/ericbob/Documents/python/fourmlikebot/fourmliker.txt'
# driver_file = '/usr/local/bin/chromedriver'







#code shit below


#forums login stuff
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
options.binary_location = "/usr/local/bin/chromedriver "
driver = webdriver.Chrome(executable_path=driver_file)
url_login = 'https://login.proboards.com/login/3472638/1'

driver.get(url_login)
changed_url = 'totalfreedom.boards.net'
time.sleep(30)
WebDriverWait(driver, 60000).until(EC.url_changes(changed_url))





#everything else
colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
COOL = colorama.Fore.CYAN
RESET = colorama.Fore.RESET
internal_urls = set()
external_urls = set()
good_urls = set()
url = 'https://totalfreedom.boards.net/user/' + user_id + '/recent_threads'
driver.get(url)
headers = requests.utils.default_headers()
resp = requests.get(url)
headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
soup = BeautifulSoup(resp.text,'html.parser')
print(url)
req = requests.get(url, headers)
total_urls_visited = 0
def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)
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
        if href in good_urls:
            continue
        if domain_name not in href:
            # external link
            if href not in external_urls:
                print(f"{GRAY}[!] External link: {href}{RESET}")
                external_urls.add(href)
            continue
        if 'thread' in href:
            if 'www.proboards.com' not in href:
                if 'recent' not in href:
                    print(f"{COOL}[@] Good Link: {href}{RESET}")
                    good_urls.add(href)
                    urls.add(href)
                    text_file = open(files, "w")
                    n = text_file.write(href)
                    text_file.close()
                    with open(files) as r:
                        file_contents = [line.strip() for line in r.readlines()]
                    capture_pattern = re.compile(r"https://totalfreedom.boards.net/thread/(\w+)")
                    for chatline in file_contents:
                        try:
                            result = capture_pattern.search(chatline).group(1)
                        except:
                            result = None
                    print(result)
                    driver.get(f"{href}")
                    try:
                        time.sleep(0.5)
                        class_name = 'class="button likes-button js-likes-button"'
                        button_element = driver.find_element_by_class_name('button likes-button js-likes-button')
                        button_element.click()
                        time.sleep(0.5)
                        button_element = driver.find_element_by_class_name(class_name)
                        button_element.click()
                        time.sleep(0.5)
                        print('success')
                    except:
                        print('fail')
                        continue
                continue
            continue
        else:
            print(f"{GREEN}[*] Internal link: {href}{RESET}")
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
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="DragonSlayer2189's Fourm Liker Bot")

    
    args = parser.parse_args()
    max_urls = 30

    crawl(url, max_urls = max_urls)

    print("[+] Total Internal links:", len(internal_urls))
    print("[+] Total External links:", len(external_urls))
    print("[+] Total URLs:", len(external_urls) + len(internal_urls))

    domain_name = urlparse(url).netloc

    with open(f"{domain_name}_internal_links.txt", "w") as f:
        for internal_link in internal_urls:
            print(internal_link.strip(), file=f)

    with open(f"{domain_name}_external_links.txt", "w") as f:
        for external_link in external_urls:
            print(external_link.strip(), file=f)




#//*[@id="post-755287"]/td/table/tbody/tr[1]/td[2]/article/div[1]/div[2]/a[4]