from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import json

option = Options()
option.headless = False

driver = webdriver.Firefox(options=option)
driver.implicitly_wait(5)
basUrl = "https://www.youtube.com"

driver.get(f"{basUrl}/search?={keywords}")
