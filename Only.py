# 9.08.2023

# Class import
from util.Driver import Driver
from util.api import get_info_profile_scrape, scroll_to_end, dump_post, download_api_media

# General import
import time, json
from seleniumwire.utils import decode


def download(url, name, prefix_api, scroll_all_page):

    driver = Driver()
    driver.create(False)
    driver.get_page(url, sleep=10)
    for req in driver.driver.requests:
        if "api2" in str(req.url) and str(name) in str(req.url):
            response_body = decode(req.response.body, req.response.headers.get('Content-Encoding', 'identity'))
            json_data = json.loads(response_body)
            get_info_profile_scrape(json_data)

    if(scroll_all_page):
        scroll_to_end(driver.driver)
    else:
        pixel = 0
        for _ in range(5):
            driver.driver.execute_script(f"window.scrollTo({pixel}, document.body.scrollHeight + 500)")
            pixel += 500

    for req in driver.driver.requests:
        if "api2" in str(req.url) and prefix_api in str(req.url):
            response_body = decode(req.response.body, req.response.headers.get('Content-Encoding', 'identity'))
            json_data = json.loads(response_body)
            dump_post(json_data['list'])
        
    download_api_media(name, prefix_api.replace("?", ""))
    driver.close()

def donwload_stories(url, name, prefix_api = "stories"):
    driver = Driver()
    driver.create(False)
    driver.get_page(url, sleep=10)

    for req in driver.driver.requests:
        if "api2" in str(req.url) and str(name) in str(req.url):
            response_body = decode(req.response.body, req.response.headers.get('Content-Encoding', 'identity'))
            json_data = json.loads(response_body)
            get_info_profile_scrape(json_data)

    json_data = ""
    for req in driver.driver.requests:
        if "api2" in str(req.url) and prefix_api in str(req.url) and "highlights" not in str(req.url):
            response_body = decode(req.response.body, req.response.headers.get('Content-Encoding', 'identity'))
            json_data = json.loads(response_body)

    if(json_data != ""):
        print(json_data)
        dump_post(json_data)
    else:
        print("Cant find any stories")

    download_api_media(name, prefix_api.replace("?", ""))
    driver.close()

def download_archive(url, name, prefix_api = "archived"):

    driver = Driver()
    driver.create(False)
    driver.get_page(url, sleep=10)
    for req in driver.driver.requests:
        if "api2" in str(req.url) and str(name) in str(req.url):
            response_body = decode(req.response.body, req.response.headers.get('Content-Encoding', 'identity'))
            json_data = json.loads(response_body)
            get_info_profile_scrape(json_data)

    json_data = ""
    for req in driver.driver.requests:
        if prefix_api in str(req.url):
            response_body = decode(req.response.body, req.response.headers.get('Content-Encoding', 'identity'))
            json_data = json.loads(response_body)

    if(json_data != ""):
        print(json_data)
        dump_post(json_data['list'])
    else:
        print("Cant find any archived file")
    download_api_media(name, prefix_api.replace("?", ""))
    driver.close()

def download_streams(url, name, prefix_api = "streams"):

    driver = Driver()
    driver.create(False)
    driver.get_page(url, sleep=10)
    for req in driver.driver.requests:
        if "api2" in str(req.url) and str(name) in str(req.url):
            response_body = decode(req.response.body, req.response.headers.get('Content-Encoding', 'identity'))
            json_data = json.loads(response_body)
            get_info_profile_scrape(json_data)

    json_data = ""
    for req in driver.driver.requests:
        if prefix_api in str(req.url):
            response_body = decode(req.response.body, req.response.headers.get('Content-Encoding', 'identity'))
            json_data = json.loads(response_body)

    if(json_data != ""):
        print(json_data)
        dump_post(json_data['list'])
    else:
        print("Cant find any streams")
    download_api_media(name, prefix_api.replace("?", ""))
    driver.close()

def download_buttons(url, name, prefix_api = "social/buttons"):

    driver = Driver()
    driver.create(False)
    driver.get_page(url, sleep=10)
    for req in driver.driver.requests:
        if "api2" in str(req.url) and str(name) in str(req.url):
            response_body = decode(req.response.body, req.response.headers.get('Content-Encoding', 'identity'))
            json_data = json.loads(response_body)
            get_info_profile_scrape(json_data)

    json_data = ""
    for req in driver.driver.requests:
        if prefix_api in str(req.url):
            response_body = decode(req.response.body, req.response.headers.get('Content-Encoding', 'identity'))
            json_data = json.loads(response_body)
            for i in range(len(json_data)):
                print(f" - Find ({json_data[i]['label']}) = {json_data[i]['url']}")

    driver.close()

# Main function download message from chat
def download_chat(id_chat):
    driver = Driver()
    driver.create(headless=False)
    driver.get_page(f"https://onlyfans.com/my/chats/chat/{id_chat}/", sleep=10)

    driver.close()

class Only:

    # Variable
    username = ""

    # Costructor
    def __init__(self, username) -> None:
        self.username = username

    # [ function ]
    def make_login(self):
        driver = Driver()
        driver.create(False)
        driver.get_page(url="https://onlyfans.com/", sleep=999)

    def get_url(self):
        if(self.username != None and self.username != ""):
            return f"https://onlyfans.com/{self.username}"

    def get_all_post(self):
        download(
            url = self.get_url(), 
            name = self.username, 
            prefix_api = "posts?", 
            scroll_all_page = True
        )

    def get_all_media(self):
        download(
            url = self.get_url() + "/media", 
            name = self.username, 
            prefix_api = "medias?", 
            scroll_all_page = True
        )

    def get_last_post(self):
        download(
            url = self.get_url(), 
            name = self.username, 
            prefix_api = "posts?", 
            scroll_all_page = False
        )

    def get_last_media(self):
        download(
            url = self.get_url() + "/media", 
            name = self.username, 
            prefix_api = "medias?", 
            scroll_all_page = False
        )

    def get_stories(self):
        donwload_stories(
            url = self.get_url(), 
            name = self.username
        )

    def get_archived(self):
        download_archive(
            url = self.get_url() + "/archived", 
            name = self.username
        )

    def get_streams(self):
        download_streams(
            url = self.get_url() + "/streams", 
            name = self.username
        )

    def get_buttons(self):
        download_buttons(
            url = self.get_url() + "/button", 
            name = self.username
        )

    def get_chat(self, id_chat):
        download_chat(id_chat)

