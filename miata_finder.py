#Program that checks craiglist miata listings and saves PID's in a cache so that when it scans again it can notice differences
#and alert me that a new listing has been created. This alert will contain information such as price and location
from bs4 import BeautifulSoup
import requests
from cache import cache_list


class Miata:
    def __init__(self, name, pid, price):
        self.name = name
        self.pid = pid
        self.price = price



def craigslistSearch(city):
    '''
    parses craigslist miata serach and returns miata object list
    '''
    url = requests.get("https://{}.craigslist.org/search/cta?query=miata".format(city))
    url = url.text
    soup = BeautifulSoup(url, "html.parser")

    miata_prices = soup.find_all("span", {"class": "result-price"})
    miata_namesandpid = soup.find_all("a",{"class": "result-title hdrlnk"})
    miata_list = [] #holds miata objects
    for price, npid in zip(miata_prices[::2], miata_namesandpid):
        if "miata" not in npid.text.lower():
            continue
        else:
            miata_list.append(Miata(npid.text, npid.get("data-id"), price.text))
    return miata_list


def c_updateCache(miata_list):
    '''
    takes in a miata object list as a parameter and stores miata pid in cache.py
    '''
    cacheFile = open("cache.py","w")
    cacheFile.write("cache_list = [")
    for miatas in miata_list:
        cacheFile.write("{},".format(miatas.pid))
    cacheFile.write("]")

def c_checkCache(city):
    '''
    parses craigslist miata search and compares it to cache to find changes returns a list of miata objects
    '''
    not_in = []
    current_pids = craigslistSearch(city)
    for pids in current_pids:
        if str(pids.pid) not in str(cache_list):
            not_in.append(pids)
    return not_in

#testing
not_in = c_checkCache("houston")
for nots in not_in:
    print(nots)






