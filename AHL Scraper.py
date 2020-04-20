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

game_data = []
#results = driver.find_elements_by_xpath("//*[@class=' co-product-list__main-cntr']//*[@class=' co-item ']//*[@class='co-product']//*[@class='co-item__title-container']//*[@class='co-product__title']")
game_data.append(["game_id", driver.find_element_by_xpath("//*[@class='ht-game-number']").text])
game_data.append(["game_date", driver.find_element_by_xpath("//*[contains(@class,'ht-game-date')]").text])
game_data.append(["game_status", driver.find_element_by_xpath("//*[contains(@class,'ht-gc-game-status')]").text])
game_data.append(["away_team", driver.find_element_by_xpath("//*[contains(@class,'ht-gc-visiting-team')]").text])
game_data.append(["away_team", driver.find_element_by_xpath("//*[contains(@class,'ht-gc-home-team')]").text])# print(game_id.text)
# print(game_date.text)
#print(*game_data)


# # Print Band One
# for item in game_data:
#     #print(str(item[0]) + " " + str(item[1]))
#     print(f"{item[0]} | {item[1]}")
# #print('Number of results', len(results))


# scoring_boxscore_WE = []
# scoring_boxscore = []
#game_tables = []

game_tables = driver.find_element_by_xpath("//div[@class='ht-gc-game-details']/div[@ng-class='gcDetailTable' and @class='ht-gc-game-detail']/table[@class='ht-table ht-table-no-overflow']")

#tbl_count = len(game_tables)

# print(f"Number of tables: {tbl_count}")



# print(len(game_tables))
# tbl_scoring_summary = game_tables[0]
# tbl_shot_summary = game_tables[1]
# tbl_details_summary = game_tables[2]


###SCORING SUMMARY###
#Periods (last period is total)
periods = []
periods = game_tables.find_elements_by_xpath("//tr/th[contains(@ng-repeat,'scoreSummaryHeadings')]")

#Away Stats#
away_goals = []
away_shots = []
away_goals = game_tables.find_elements_by_xpath("//tr/td[contains(@ng-repeat,'visitingScoreSummary')]")
away_shots = game_tables.find_elements_by_xpath("//tr/td[contains(@ng-repeat,'visitingShotSummary')]")

#Home Stats#
home_goals = []
home_shots = []
home_goals = game_tables.find_elements_by_xpath("//tr/td[contains(@ng-repeat,'homeScoreSummary')]")
home_shots = game_tables.find_elements_by_xpath("//tr/td[contains(@ng-repeat,'homeShotSummary')]")
###/SCORING SUMMARY###

###GAME DETAILS###
#Away PP#
away_pp = []
away_penalties = []
away_pp = game_tables.find_element_by_xpath("//tr/td/span[contains(@ng-bind,'gameSummary.visitingTeam.stats.powerPlayGoals')]").text.replace(" ","").split("/",1) #get away PP fraction string and split
away_pp_goals = away_pp[0]
away_pp_opps = away_pp[1]
away_penalties = game_tables.find_element_by_xpath("//tr/td/span[contains(@ng-bind,'gameSummary.visitingTeam.stats.penaltyMinuteCount')]").text.split(" min / ",1) #get away PP fraction string and split
away_pims = away_penalties[0]
away_infracs = away_penalties[1].split(" ",1)[0]

#Home PP#
home_pp = []
home_penalties = []
home_pp = game_tables.find_element_by_xpath("//tr/td/span[contains(@ng-bind,'gameSummary.homeTeam.stats.powerPlayGoals')]").text.replace(" ","").split("/",1) #get home PP fraction string and split
home_pp_goals = home_pp[0]
home_pp_opps = home_pp[1]
home_penalties = game_tables.find_element_by_xpath("//tr/td/span[contains(@ng-bind,'gameSummary.homeTeam.stats.penaltyMinuteCount')]").text.split(" min / ",1) #get home PP fraction string and split
home_pims = home_penalties[0]
home_infracs = home_penalties[1].split(" ",1)[0]
###/GAME DETAILS###



# away_pts = []
# home_pp_goals = []
# home_pp_opps = []
# home_pims = []
# home_infracs = []
# home_pts = []

###GAME DETAILS###

print(home_pims)
print(home_infracs)

# periods_row = tbl_scoring_summary.find_elements_by_xpath("//tr/th")

# # # print(periods_row.text[1])

# # # periods = periods_row.find_elements_by_xpath("/th")

# for period in periods:
#     print(period.text)
# print("home_shots:")
# for period in home_shots:
#     print(period.text)

# print("away_shots:")
# for period in away_shots:
#     print(period.text)

# print(tbl_scoring_summary.find_elements_by_xpath("//td[contains(@ng-repeat, 'visitingScoreSummary')]")[0].text)
# print(tbl_scoring_summary.find_elements_by_xpath("//td[contains(@ng-repeat, 'visitingScoreSummary')]")[1].text)

# <div class="ht-gc-game-details">
# 			<!-- Details -->
# 			<div ng-class="gcDetailTable" class="ht-gc-game-detail">
# 				<table class="ht-table ht-table-no-overflow">
# 					<thead>
# 						<tr>
# 							<th></th>
# 							<th class="ng-binding">PP</th>
# 							<th class="ng-binding">PIM</th>
# 							<th class="ng-binding">PTS</th>
# 						</tr>
# 					</thead>
# 					<tbody>
# 						<tr>
# 							<td>
# 								<a ng-href="/stats/roster/324/65" target="_self" ng-bind="gameSummary.visitingTeam.info.abbreviation" class="ng-binding" href="/stats/roster/324/65">SYR</a>
# 							</td>
# 							<td>
# 							   <span ng-bind="gameSummary.visitingTeam.stats.powerPlayGoals + &quot; / &quot; + gameSummary.visitingTeam.stats.powerPlayOpportunities" class="ng-binding">0 / 2</span>
# 							</td>
# 							<td>
# 							   <span ng-bind="gameSummary.visitingTeam.stats.penaltyMinuteCount +&quot; min / &quot;+ gameSummary.visitingTeam.stats.infractionCount + &quot; in&quot;" class="ng-binding">8 min / 4 in</span>
# 							</td>
# 							<td>
# 								<span ng-bind="gameSummary.visitingTeam.stats.goalCount + gameSummary.visitingTeam.stats.assistCount" class="ng-binding">7</span>
# 							</td>
# 						</tr>
# 						<tr>
# 							<td>
# 								<a ng-href="/stats/roster/390/65" target="_self" ng-bind="gameSummary.homeTeam.info.abbreviation" class="ng-binding" href="/stats/roster/390/65">UTI</a>
# 							</td>
# 							<td>
# 								<span ng-bind="gameSummary.homeTeam.stats.powerPlayGoals + &quot; / &quot; + gameSummary.homeTeam.stats.powerPlayOpportunities" class="ng-binding">1 / 4</span>
# 							</td>
# 							<td>
# 								<span ng-bind="gameSummary.homeTeam.stats.penaltyMinuteCount +&quot; min / &quot;+ gameSummary.homeTeam.stats.infractionCount + &quot; in&quot;" class="ng-binding">4 min / 2 in</span>
# 							</td>
# 							<td>
# 								<span ng-bind="gameSummary.homeTeam.stats.goalCount + gameSummary.homeTeam.stats.assistCount" class="ng-binding">3</span>
# 							</td>
# 						</tr>
# 					</tbody>
# 				</table>
# 			</div>
# 		</div>

#scoring_boxscore = driver.find_element_by_xpath("//td[contains(@ng_repeat, 'visitingScoreSummary')]")

# <td ng-repeat="stat in visitingScoreSummary track by $index" class="ng-scope">
#     <span ng-bind="stat" class="ng-binding">0</span>
# </td>

# scoring_boxscore_WE = driver.find_elements_by_xpath("//td[contains(@ng-repeat,'visitingScoreSummary')]")#='stat' and @class='ng-binding']") #<span ng-bind="stat" class="ng-binding">2</span>


# for item in scoring_boxscore_WE:
#      scoring_boxscore.append(item.find_element_by_xpath("//span[@ng-bind='stat' and @class='ng-binding']")) #<span ng-bind="stat" class="ng-binding">2</span>

# for item in scoring_boxscore:
#     print(item.text)

# <td ng-repeat="stat in visitingScoreSummary track by $index" class="ng-scope">
#     <span ng-bind="stat" class="ng-binding">0</span>
# </td>

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