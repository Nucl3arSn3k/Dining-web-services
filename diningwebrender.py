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

#
def main():
    # webscrape()
    a = open("test.html", "r")
    index = a.read()
    soup_2 = BeautifulSoup(index, "lxml")

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
    contents = [x.strip(" ") for x in contents]
    r = regex.compile("((1[0-2]|0?[1-9]):([0-5][0-9]) ?([AaPp][Mm]))")

    new_contents = list(filter(r.match, contents))
    index_pos_list = []
    i = 0
    for index, x in enumerate(new_contents):
        var_loc = get_index_positions(contents, new_contents[index])
        index_pos_list.append(var_loc)
        i += 1

    print(index_pos_list)
    print(new_contents)
    # print(contents)
    res = []

    [res.append(x) for x in contents if x not in res]

    print(res)

    """
    for x in range(len(index_pos_list)):
        print(isinstance(index_pos_list[x], list))
    """


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