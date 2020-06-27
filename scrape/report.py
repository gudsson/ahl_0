import urllib.request
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from driver import driver
from time import sleep

class Loader(object):
    def __init__(self, game_id, report_type=''):
        self.game_key = game_key
        self.report_type = report_type

def raw_page(game_id, wait=10):
    domain = 'https://theahl.com/stats/game-center/'
    url = domain + str(game_id)
    # print(url)
    driver.get(url)
    # sleep(wait)
    # print(report.title)
    return driver

class ScrapeReport(object):
    #scrapes GameCenter
    __domain = 'https://theahl.com/stats/game-center/'

    def __init__(self):
        self.raw_src = None #source of the last page requested
        self.req_err = None #error from the last request
        # self

    def raw_report(self, game_id): #Pulls raw report for specified game code.
        url = [ self.__domain, str(game_id)]
        url = ''.join(url)

        return self.__open(url)
    
    def __open(self, url):
        # try:
        #     # pass
            
        #     # global game
        #     # game = Game(id)

        #     # urlpage = 'https://theahl.com/stats/game-center/' + str(id)
        #     # logger.info(f'Pulling AHL Game #{id} from: {urlpage}')

        #     self.raw_src = driver.get(url)

        #     # return driver
        # except Exception as e:
        #     self.req_err = e

        return url#self.raw_src
    #     def get_driver(id, driver):
    
    # global game
    # game = Game(id)

    # urlpage = 'https://theahl.com/stats/game-center/' + str(id)
    # logger.info(f'Pulling AHL Game #{id} from: {urlpage}')

    # driver.get(urlpage)

    # return driver
    # report = ScrapeReport()
