import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys


url = "https://www.ebay.com/b/PC-Laptops-Netbooks/177/bn_317584"

def get_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup

def parse(soup):
    productlist = []
    results = soup.find_all("div",{ "class": "s-item__wrapper clearfix"})
    for item in results:
        products = {
            "title": item.find("h3", {"class": "s-item__title" }).text,
            "soldprice": float(item.find("span", {"class": "s-item__price"}).text.replace("$","").replace(",","").strip().split()[0]),
            #"shipping": item.find("span", { "class": "s-item__shipping s-item__logisticsCost"}).text.replace("shipping",""),
        }
        print(products)
        productlist.append(products)
    return productlist

def output(productlist) :
    productsdf = pd.DataFrame(productlist)
    productsdf.to_csv("output.csv", mode='a', header=False)

    return

n = 0
p = 0
try:
    while n == 0:
        soup = get_data(url)
        productlist = parse(soup)
        output(productlist)
        url = soup.find("div", {"class": "b-pagination"}).find("a", {"_sp":"p2489527.m4335.l8631"})["href"]
        p += 1
        print("Page number: ",p )
except:
    print("importing CSV data to Excel Data...")
    time.sleep(3)

    read_file = pd.read_csv(r"D:\PYTHON\PROGRAMAS PYCHARM\output.csv")
    read_file.to_excel(r"D:\PYTHON\PROGRAMAS PYCHARM\output.xlsx", index=None, header=["1","title","Soldprice"] )
    print("Acomplished")
