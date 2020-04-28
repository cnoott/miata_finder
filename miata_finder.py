#Program that checks craiglist miata listings and saves PID's in a cache so that when it scans again it can notice differences
#and alert me that a new listing has been created. This alert will contain information such as price and location
from bs4 import BeautifulSoup
import requests
from cache import cache_list
import os


class Miata:
    def __init__(self, name, pid, price, city):
        self.name = name
        self.pid = pid
        self.price = price
        self.city = city



def craigslistSearch():
    '''
    parses craigslist miata serach and returns miata object list
    '''
    cities = ["houston","austin","dallas","waco"]
    miata_list = [] #holds miata objects
    for city in cities:
        url = requests.get("https://{}.craigslist.org/search/cta?query=miata".format(city))
        url = url.text
        soup = BeautifulSoup(url, "html.parser")

        miata_prices = soup.find_all("span", {"class": "result-price"})
        miata_namesandpid = soup.find_all("a",{"class": "result-title hdrlnk"})
        for price, npid in zip(miata_prices[::2], miata_namesandpid):
            if "miata" not in npid.text.lower():
                continue
            elif npid in miata_list:
                continue
            else:
                miata_list.append(Miata(npid.text, npid.get("data-id"), price.text,city))
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

def c_checkCache():
    '''
    parses craigslist miata search and compares it to cache to find changes returns a list of miata objects
    '''
    not_in = []
    current_pids = craigslistSearch()
    for pids in current_pids:
        if str(pids.pid) not in str(cache_list):
            not_in.append(pids)
            emailString = "{}\nPrice:\{}\nLocation:{}".format(pids.name,pids.price,pids.city)
            os.system('echo "{}" | mail -s "New Miata Listing!" liamamadio@gmail.com'.format(emailString))
            print(pids.name,":",pids.price)
    return not_in

#testing

def main():
    not_in = c_checkCache()
    c_updateCache(craigslistSearch())
main()

