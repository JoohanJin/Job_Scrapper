# from requests_html import HTMLSession
from bs4 import BeautifulSoup
from selenium import webdriver

from selenium.webdriver.chrome.options import Options

options = Options()

URL = "https://bet.hkjc.com/racing/index.aspx?lang=en"

browser = webdriver.Chrome(options=options)
browser.get(URL)

print(browser.page_source)