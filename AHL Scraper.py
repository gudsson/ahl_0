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
#game_details = []

game_details = driver.find_element_by_xpath("//div[@class='ht-gc-game-details']")

game_tables = []

game_tables = game_details.find_elements_by_xpath("//table[@class='ht-table ht-table-no-overflow']")

tbl_scoring_summary = game_tables[0]
tbl_shot_summary = game_tables[1]
tbl_details_summary = game_tables[2]

print(tbl_scoring_summary.find_elements_by_xpath("//td[contains(@ng-repeat, 'visitingScoreSummary')]")[0].text)
print(tbl_scoring_summary.find_elements_by_xpath("//td[contains(@ng-repeat, 'visitingScoreSummary')]")[1].text)

# <div class="ht-gc-game-details">
# 			<!-- Scoring -->
# 			<div ng-class="gcDetailTable" class="ht-gc-game-detail">
# 				<table class="ht-table ht-table-no-overflow">
# 					<thead>
# 						<tr>
# 							<th class="ng-binding">Scoring</th>
# 							<!-- ngRepeat: heading in scoreSummaryHeadings track by $index --><th style="width: 34px" ng-repeat="heading in scoreSummaryHeadings track by $index" class="ng-scope">
# 								<span ng-bind="heading" class="ng-binding">1</span>
# 							</th><!-- end ngRepeat: heading in scoreSummaryHeadings track by $index --><th style="width: 34px" ng-repeat="heading in scoreSummaryHeadings track by $index" class="ng-scope">
# 								<span ng-bind="heading" class="ng-binding">2</span>
# 							</th><!-- end ngRepeat: heading in scoreSummaryHeadings track by $index --><th style="width: 34px" ng-repeat="heading in scoreSummaryHeadings track by $index" class="ng-scope">
# 								<span ng-bind="heading" class="ng-binding">3</span>
# 							</th><!-- end ngRepeat: heading in scoreSummaryHeadings track by $index --><th style="width: 34px" ng-repeat="heading in scoreSummaryHeadings track by $index" class="ng-scope">
# 								<span ng-bind="heading" class="ng-binding">T</span>
# 							</th><!-- end ngRepeat: heading in scoreSummaryHeadings track by $index -->
# 						</tr>
# 					</thead>
# 					<tbody>
# 						<tr>
# 							<td>
# 								<a ng-href="/stats/roster/324/65" target="_self" ng-bind="gameSummary.visitingTeam.info.abbreviation" class="ng-binding" href="/stats/roster/324/65">SYR</a>
# 							</td>
# 							<!-- ngRepeat: stat in visitingScoreSummary track by $index --><td ng-repeat="stat in visitingScoreSummary track by $index" class="ng-scope">
# 								<span ng-bind="stat" class="ng-binding">0</span>
# 							</td><!-- end ngRepeat: stat in visitingScoreSummary track by $index --><td ng-repeat="stat in visitingScoreSummary track by $index" class="ng-scope">
# 								<span ng-bind="stat" class="ng-binding">2</span>
# 							</td><!-- end ngRepeat: stat in visitingScoreSummary track by $index --><td ng-repeat="stat in visitingScoreSummary track by $index" class="ng-scope">
# 								<span ng-bind="stat" class="ng-binding">1</span>
# 							</td><!-- end ngRepeat: stat in visitingScoreSummary track by $index --><td ng-repeat="stat in visitingScoreSummary track by $index" class="ng-scope">
# 								<span ng-bind="stat" class="ng-binding">3</span>
# 							</td><!-- end ngRepeat: stat in visitingScoreSummary track by $index -->
# 						</tr>
# 						<tr>
# 							<td>
# 								<a ng-href="/stats/roster/390/65" target="_self" ng-bind="gameSummary.homeTeam.info.abbreviation" class="ng-binding" href="/stats/roster/390/65">UTI</a>
# 							</td>
# 							<!-- ngRepeat: stat in homeScoreSummary track by $index --><td ng-repeat="stat in homeScoreSummary track by $index" class="ng-scope">
# 								<span ng-bind="stat" class="ng-binding">1</span>
# 							</td><!-- end ngRepeat: stat in homeScoreSummary track by $index --><td ng-repeat="stat in homeScoreSummary track by $index" class="ng-scope">
# 								<span ng-bind="stat" class="ng-binding">0</span>
# 							</td><!-- end ngRepeat: stat in homeScoreSummary track by $index --><td ng-repeat="stat in homeScoreSummary track by $index" class="ng-scope">
# 								<span ng-bind="stat" class="ng-binding">0</span>
# 							</td><!-- end ngRepeat: stat in homeScoreSummary track by $index --><td ng-repeat="stat in homeScoreSummary track by $index" class="ng-scope">
# 								<span ng-bind="stat" class="ng-binding">1</span>
# 							</td><!-- end ngRepeat: stat in homeScoreSummary track by $index -->
# 						</tr>
# 					</tbody>
# 				</table>
# 			</div>
# 			<!-- Shots -->
# 			<div ng-class="gcDetailTable" class="ht-gc-game-detail">
# 				<table class="ht-table ht-table-no-overflow">
# 					<thead>
# 					<tr>
# 						<th class="ng-binding">Shots on Goal</th>
# 						<!-- ngRepeat: heading in shotSummaryHeadings track by $index --><th style="width: 34px" ng-repeat="heading in shotSummaryHeadings track by $index" class="ng-scope">
# 							<span ng-bind="heading" class="ng-binding">1</span>
# 						</th><!-- end ngRepeat: heading in shotSummaryHeadings track by $index --><th style="width: 34px" ng-repeat="heading in shotSummaryHeadings track by $index" class="ng-scope">
# 							<span ng-bind="heading" class="ng-binding">2</span>
# 						</th><!-- end ngRepeat: heading in shotSummaryHeadings track by $index --><th style="width: 34px" ng-repeat="heading in shotSummaryHeadings track by $index" class="ng-scope">
# 							<span ng-bind="heading" class="ng-binding">3</span>
# 						</th><!-- end ngRepeat: heading in shotSummaryHeadings track by $index --><th style="width: 34px" ng-repeat="heading in shotSummaryHeadings track by $index" class="ng-scope">
# 							<span ng-bind="heading" class="ng-binding">T</span>
# 						</th><!-- end ngRepeat: heading in shotSummaryHeadings track by $index -->
# 					</tr>
# 					</thead>
# 					<tbody>
# 					<tr>
# 						<td>
# 							<a ng-href="/stats/roster/324/65" target="_self" ng-bind="gameSummary.visitingTeam.info.abbreviation" class="ng-binding" href="/stats/roster/324/65">SYR</a>
# 						</td>
# 						<!-- ngRepeat: stat in visitingShotSummary track by $index --><td ng-repeat="stat in visitingShotSummary track by $index" class="ng-scope">
# 							<span ng-bind="stat" class="ng-binding">9</span>
# 						</td><!-- end ngRepeat: stat in visitingShotSummary track by $index --><td ng-repeat="stat in visitingShotSummary track by $index" class="ng-scope">
# 							<span ng-bind="stat" class="ng-binding">11</span>
# 						</td><!-- end ngRepeat: stat in visitingShotSummary track by $index --><td ng-repeat="stat in visitingShotSummary track by $index" class="ng-scope">
# 							<span ng-bind="stat" class="ng-binding">6</span>
# 						</td><!-- end ngRepeat: stat in visitingShotSummary track by $index --><td ng-repeat="stat in visitingShotSummary track by $index" class="ng-scope">
# 							<span ng-bind="stat" class="ng-binding">26</span>
# 						</td><!-- end ngRepeat: stat in visitingShotSummary track by $index -->
# 					</tr>
# 					<tr>
# 						<td>
# 							<a ng-href="/stats/roster/390/65" target="_self" ng-bind="gameSummary.homeTeam.info.abbreviation" class="ng-binding" href="/stats/roster/390/65">UTI</a>
# 						</td>
# 						<!-- ngRepeat: stat in homeShotSummary track by $index --><td ng-repeat="stat in homeShotSummary track by $index" class="ng-scope">
# 							<span ng-bind="stat" class="ng-binding">13</span>
# 						</td><!-- end ngRepeat: stat in homeShotSummary track by $index --><td ng-repeat="stat in homeShotSummary track by $index" class="ng-scope">
# 							<span ng-bind="stat" class="ng-binding">8</span>
# 						</td><!-- end ngRepeat: stat in homeShotSummary track by $index --><td ng-repeat="stat in homeShotSummary track by $index" class="ng-scope">
# 							<span ng-bind="stat" class="ng-binding">7</span>
# 						</td><!-- end ngRepeat: stat in homeShotSummary track by $index --><td ng-repeat="stat in homeShotSummary track by $index" class="ng-scope">
# 							<span ng-bind="stat" class="ng-binding">28</span>
# 						</td><!-- end ngRepeat: stat in homeShotSummary track by $index -->
# 					</tr>
# 					</tbody>
# 				</table>
# 			</div>
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