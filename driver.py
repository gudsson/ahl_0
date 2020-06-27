from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def initialize_driver():
    try:
        options = Options()
        options.headless = False#True

        driver = webdriver.Firefox(options=options)
        print("Initialized driver")
        return driver
    except:
        raise RuntimeError("Could not initialize firefox driver")

driver = initialize_driver()