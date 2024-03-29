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
import time
import json

import re

#
def main():
    webscrape()
    
    a = open("test.html", "r")
    index = a.read()
    soup_2 = BeautifulSoup(index, "lxml")
    summer = True
    # handles url extraction
    link_list = []
    soup = BeautifulSoup(index, "html.parser")
    S = soup_2.html
    open_now_links = soup.find_all(class_="open-now-location-link")
    for link in open_now_links:
        link_list.append(link["href"])
        print(link)

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
    menu = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
    }
    key = None

    with open("txtdumpv2.txt", "r") as input_file:
        lines = input_file.readlines()

    with open("txtdumpv2.txt", "w") as f:  # takes out first line
        f.writelines(lines[1:])

    with open("txtdumpv2.txt", "r") as input_file:
        lines = input_file.readlines()

    unique_lines = []
    for line in lines:
        line = line.strip()
        if line not in unique_lines:
            unique_lines.append(line)

    with open("outputv2.txt", "w") as output_file:
        for line in unique_lines:
            output_file.write(line + "\n")

    dining_names = {
        "Douglass_Dining_Center",
        "Danforth_Dining_Center",
        "Eastman_Dining_Center",
        "Rocky's_Sub_Shop",
        "The_Pit",
        "Grab_&_Go",
        "Connections",
        "Peet's_Coffee_@_Wegmans_Hall",
        "The_Brew_@_Simon_School",
        "Hillside_Market",
        "California_Rollin_II",
    }

    if(summer == True):
        print("summertime eating schedule")


    else:

        with open("outputv2.txt", "r") as f:
            key = None
            link_index = 0
            for line in f:
                # remove any leading or trailing whitespace
                line = line.strip()

                # if the line contains the name of a dining center or location
                if line[0].isupper() and line.replace(" ", "_") in dining_names:
                    # use the name as a key and create an empty dictionary as its value
                    key = line.replace(" ", "_")
                    if key not in menu:
                        menu[key] = {}
                    # add the URL for the current dining center to its dictionary
                    if link_index < len(link_list):
                        menu[key]["url"] = link_list[link_index]
                        link_index += 1

                # if the line contains a meal period
                elif " - " in line:
                    # split the line into start and end times and meal type
                    start_end, meal_type = line.split("    ")
                    start, end = start_end.split(" - ")
                    meal_type = meal_type.strip()

                    # add the start and end times as a dictionary to the current dining center's value
                    if key is not None and meal_type not in menu[key]:
                        menu[key][meal_type] = []
                    menu[key][meal_type].append(
                        {"start": start.strip(), "end": end.strip()}
                    )

                # if the line contains a location or other attribute
                elif key is not None:
                    # add the attribute to the current dining center's value
                    attribute = line.replace(" ", "_")
                    if attribute not in menu[key]:
                        menu[key][attribute] = True

    print(menu)

    with open("output.json", "w") as x:
        json.dump(menu, x)

    a.close()
    os.remove("test.html")


def webscrape():
    optionsv2 = Options()
    optionsv2.add_argument("--headless")
    url = "https://dining.rochester.edu/menu-hours/"

    optionsv2.binary = FirefoxBinary(r"C:\Program Files\Mozilla Firefox\firefox.exe")
    browser = webdriver.Firefox(
        executable_path="C:\Program Files (x86)\geckodriver-v0.33.0-win32\geckodriver.exe",  # desktop gecko adress C:\Program Files (x86)\geckodriver-v0.32.2-win32\geckodriver.exe
        options=optionsv2,  # laptop gecko adress C:\geckodriver-v0.31.0-win64\geckodriver.exe
    )
    # Roc desktop gecko adress C:\Program Files (x86)\geckodriver-v0.32.2-win32\geckodriver.exe
    # laptop gecko adress C:\geckodriver-v0.31.0-win64\geckodriver.exe

    browret = browser.get(url)
    page_source = browser.page_source
    soup = BeautifulSoup(page_source, "lxml")
    job0 = soup.find(id="timepicker-stage")

    with open("test.html", "w+") as f:
        f.write(str(job0))
    f.close()


def url_extraction():
    # extractor = URLExtract()
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