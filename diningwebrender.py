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

    print(new_contents)
    # print(contents)


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


if __name__ == "__main__":
    main()