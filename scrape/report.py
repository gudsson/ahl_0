import urllib.request
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from driver import driver
from time import sleep

def raw_page(game_id, wait=10):
    domain = 'https://theahl.com/stats/game-center/'
    url = domain + str(game_id)
    driver.get(url)
    sleep(10)
    summary_container = driver.find_element_by_xpath("//div[@class='ht-summary-container']")
    print(f"Opening Game #{game_id}... {domain}{str(game_id)}")
    return driver