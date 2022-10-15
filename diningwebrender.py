import requests
from xml.etree import ElementTree as et
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from lxml import html
from selenium.webdriver.firefox.options import Options

#
def main():
    optionsv2 = Options()
    optionsv2.add_argument("--headless")
    url = "https://dining.rochester.edu/menu-hours/"

    # binary = FirefoxBinary("C:\Program Files\Mozilla Firefox\firefox.exe")
    browser = webdriver.Firefox(
        executable_path="C:\geckodriver-v0.31.0-win64\geckodriver.exe",
        options=optionsv2,
    )

    # driver = webdriver.Firefox(options=optionsv2)
    browser.get(url)
    page_source = browser.page_source

    tree = html.fromstring(page_source)
    # quotes = tree.xpath()
    # print("hey")
    print(type(tree))
    for div in tree:
        print(type(div.text_content()))
    """
    with open("htmltxt.txt", "w+") as f:
        f.write(var)
    """


if __name__ == "__main__":
    main()