# import libraries
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import pandas as pd
# specify the url
gamenumber = 1020558
urlpage = 'https://theahl.com/stats/game-center/' + str(gamenumber)


options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

print(urlpage)

# run firefox webdriver from executable path of your choice
#driver = webdriver.Firefox()

# get web page
driver.get(urlpage)

# execute script to scroll down the page
#driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
# sleep for 10s
time.sleep(5)

#Initialize Arrays
game_data = []
scoring_boxscore = []
#results = driver.find_elements_by_xpath("//*[@class=' co-product-list__main-cntr']//*[@class=' co-item ']//*[@class='co-product']//*[@class='co-item__title-container']//*[@class='co-product__title']")

#GAME STATUS BAND
game_data.append(["game_id", driver.find_element_by_xpath("//*[@class='ht-game-number']").text])
game_data.append(["game_date", driver.find_element_by_xpath("//*[contains(@class,'ht-game-date')]").text])
game_data.append(["game_status", driver.find_element_by_xpath("//*[contains(@class,'ht-gc-game-status')]").text])
game_data.append(["away_team", driver.find_element_by_xpath("//*[contains(@class,'ht-gc-visiting-team')]").text])
game_data.append(["away_score", driver.find_element_by_xpath("//*[contains(@ng-bind,'visitingTeam.stats.goals')]").text])
game_data.append(["home_team", driver.find_element_by_xpath("//*[contains(@class,'ht-gc-home-team')]").text])# print(game_id.text)
game_data.append(["home_score", driver.find_element_by_xpath("//*[contains(@ng-bind,'homeTeam.stats.goals')]").text])
#GAME STATUS BAND

#STAT SUMMARY BAND
#SCORING SUMMARY
# - need to account for playoff overtime


#SCORING SUMMARY
#STAT SUMMARY BAND

for item in game_data:
    #print(str(item[0]) + " " + str(item[1]))
    print(f"{item[0]} | {item[1]}")
#print('Number of results', len(results))

# # create empty array to store data
# data = []

# # loop over results
# for result in results:
#     product_name = result.text
#     link = result.find_element_by_tag_name('a')
#     product_link = link.get_attribute("href")

#     # append dict to array
#     data.append({"product" : product_name, "link" : product_link})

# # save to pandas dataframe
# df = pd.DataFrame(data)
# print(df)

# # write to csv
# path = 'C:\\Users\\Gudsson\\Documents\\Programming\\AHL Scrape\\'
# df.to_csv(path + 'asdaYogurtLink.csv')
driver.quit()