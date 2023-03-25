from fileinput import close
import requests
from xml.etree import ElementTree as et
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from bs4 import BeautifulSoup
from lxml import html
from selenium.webdriver.firefox.options import Options
import bleach
import regex
import os
from urlextract import URLExtract
import json

import re

#
def main():
    webscrape()
    a = open("test.html", "r")
    index = a.read()
    soup_2 = BeautifulSoup(index, "lxml")
    url_list = extract_urls_from_html("test.html")
    S = soup_2.html

    # all_text = "".join(S.findAll(text=True)).encode("utf-8")
    """
    for tag in soup_2.find_all():
        print(f"{tag.name}: {tag.text}")
    """
    output_3 = bleach.clean(index, tags=[], attributes={}, styles=[], strip=True)
    # output = str(all_text)
    resultString = regex.sub("^\s+$[\r\n]*", "", output_3)
    # output_2 = output.join(output.splitlines())
    # print(resultString)

    with open("txtdump.txt", "w+") as f:
        f.write(resultString)

    with open("txtdump.txt", "r") as r, open("txtdumpv2.txt", "w+") as s:
        for line in r:
            if line.strip():
                s.write(line)
    os.remove("txtdump.txt")

    contents = []

    with open("txtdumpv2.txt", "r") as file:
        for x in file:
            x2 = x[:-1]
            contents.append(x2)
    menu = {}
    key = None

    with open("txtdumpv2.txt") as f:
        for line in f:
            # remove any leading or trailing whitespace
            line = line.strip()
            print("input line" + line)
            # if the line contains the name of a dining center or location
            if line[0].isupper():
                # use the name as a key and create an empty dictionary as its value
                key = line.replace(" ", "_")
                print("isupper" + key)
                menu[key] = {}

            # if the line contains a meal period
            elif " - " in line:
                # split the line into start and end times and meal type
                start_end, meal_type = line.split("    ")
                start, end = start_end.split(" - ")
                # add the start and end times as a dictionary to the current dining center's value
                if key is not None and meal_type.strip() not in menu[key]:
                    menu[key][meal_type.strip()] = []
                menu[key][meal_type.strip()].append(
                    {"start": start.strip(), "end": end.strip()}
                )
            # if the line contains a location or other attribute
            elif key is not None:
                # add the attribute to the current dining center's value
                menu[key][line.replace(" ", "_")] = True

    print(menu)
    with open("output.json", "w") as x:
        json.dump(menu, x)

    a.close()
    # os.remove("test.html")


def webscrape():
    optionsv2 = Options()
    optionsv2.add_argument("--headless")
    url = "https://dining.rochester.edu/menu-hours/"

    # binary = FirefoxBinary("C:\Program Files\Mozilla Firefox\firefox.exe")
    browser = webdriver.Firefox(
        executable_path="C:\geckodriver-v0.31.0-win64\geckodriver.exe",
        options=optionsv2,
    )

    # driver = webdriver.Firefox(options=optionsv2)
    browret = browser.get(url)
    page_source = browser.page_source
    soup = BeautifulSoup(page_source, "lxml")
    job0 = soup.find(id="timepicker-stage")

    # print(job0)

    with open("test.html", "w+") as f:
        f.write(str(job0))
    f.close()


def url_extraction():
    extractor = URLExtract()
    a = open("test.html")

    gfg = BeautifulSoup(a, features="lxml")
    links = []
    a.close()
    for link in gfg.findAll("a"):
        links.append(link.get("href"))

    return links


def extract_urls_from_html(html_file):
    with open(html_file, "r") as f:
        contents = f.read()

    # Find all URLs using regular expressions
    urls = re.findall("href=['\"]?([^'\" >]+)", contents)

    return urls


def get_index_positions(list_of_elems, element):
    """Returns the indexes of all occurrences of give element in
    the list- listOfElements"""
    index_pos_list = []
    index_pos = 0
    while True:
        try:
            # Search for item in list from indexPos to the end of list
            index_pos = list_of_elems.index(element, index_pos)
            # Add the index position in list
            index_pos_list.append(index_pos)
            index_pos += 1
        except ValueError as e:
            break
    return index_pos_list


if __name__ == "__main__":
    main()