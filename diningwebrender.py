import requests
from xml.etree import ElementTree as et
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from bs4 import BeautifulSoup
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
    browret = browser.get(url)
    soup = BeautifulSoup(browret.content, "html.parser")
    job0 = soup.find_all("div", class_="timepicker-stage")

    with open("htmltxt.txt", "w+") as f:
        f.write(job0)


if __name__ == "__main__":
    main()