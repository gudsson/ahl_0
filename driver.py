from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import atexit

def initialize_driver():
    try:
        options = Options()
        options.headless = False#True

        driver = webdriver.Firefox(options=options)
        print("Initialized driver")
        return driver
    except:
        raise RuntimeError("Could not initialize firefox driver")

#initialize headless firefox driver
driver = initialize_driver()

#close driver on program exit
atexit.register(lambda: driver.quit())
atexit.register(lambda: print(f'Exiting program.'))