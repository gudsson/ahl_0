import urllib.request
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

class Loader(object):
    def __init__(self, game_id, report_type=''):
        self.game_key = game_key
        self.report_type = report_type

class Scraper(object):
    #scrapes GameCenter
    __domain = 'https://theahl.com/stats/game-center/'

    def __init__(self):
        self.raw_src = None #source of the last page requested
        self.req_err = None #error from the last request

    def __raw_report(self, game_id): #Pulls raw report for specified game code.
        url = [ self.__domain, str(game_id)]
        url = ''.join(url)

        return self.__open
    
    def __open(url):
        driver = None
        try:
            pass
        except Exception as e:
            self.req_err = e
    #     def get_driver(id, driver):
    
    # global game
    # game = Game(id)

    # urlpage = 'https://theahl.com/stats/game-center/' + str(id)
    # logger.info(f'Pulling AHL Game #{id} from: {urlpage}')

    # driver.get(urlpage)

    # return driver
