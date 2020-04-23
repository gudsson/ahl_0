# import libraries
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import pandas as pd
# specify the url
gamenumber = 1020231
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

###THREE STARS###
three_stars = []
three_stars_WE = []

three_stars_WE = game_tables.find_element_by_xpath("//div[@class='ht-three-stars']")

star_number = []
star_team = []
star_name = []

star_number = three_stars_WE.find_elements_by_xpath("//div[@class='ht-star-number']/*")
star_team = three_stars_WE.find_elements_by_xpath("//div[@class='ht-star-team']/*")
star_name = three_stars_WE.find_elements_by_xpath("//div[@class='ht-star-name']/*")

for i in range(0, len(star_number)-1):
    three_stars.append([star_number[i].text, star_team[i].text, star_name[i].text.split(" (",1)[0]])
###/THREE STARS###

##AWAY STAT SUMMARY##
away_line_stats = []
away_line = []
away_td = []
away_coach_line = []
away_coaches = []

away_table = game_tables.find_element_by_xpath("//div[@ng-class='sumTableHalfLeft']/div[@ng-class='sumTableMobile']")
away_line = away_table.find_elements_by_xpath("//tr[contains(@ng-repeat,'visitingTeam.skaters')]")
away_coach_line = away_table.find_elements_by_xpath("//tr[contains(@ng-repeat,'visitingTeam.coaches')]")

for line in away_line:
	away_td = line.find_elements_by_xpath("td")
	awayplyr_number = away_td[0].text
	awayplyr_letter = away_td[1].text
	awayplyr_name = away_td[2].text.split(", ",1)[1] + " " + away_td[2].text.split(", ",1)[0]
	awayplyr_id = away_td[2].find_element_by_xpath("a").get_attribute('href').split('/player/')[1].split('/')[0]
	awayplyr_pos = away_td[3].text
	awayplyr_goals = away_td[4].text
	awayplyr_assists = away_td[5].text
	awayplyr_pim = away_td[6].text
	awayplyr_shots = away_td[7].text
	awayplyr_plusminus = away_td[8].text
	away_line_stats.append([awayplyr_number, awayplyr_letter, awayplyr_name, awayplyr_id, awayplyr_pos, awayplyr_goals, awayplyr_assists, awayplyr_pim, awayplyr_shots, awayplyr_plusminus])


for line in away_coach_line:
	awaycoach_role = line.text.split(": ")[0]
	awaycoach_name = line.text.split(": ")[1]
	away_coaches.append([awaycoach_role, awaycoach_name])
    
print(*away_coaches)
###/AWAY STAT SUMMARY

###AWAY COACHES###
# away_coach_rows = []
# print(len(away_line))
# print(len(away_coaches))


# away_coach_rows = away_table.find_elements_by_id("/table")#"//tr[contains(@ng-repeat,'visitingTeam.coaches')]")

# print(len(away_coach_rows))
# print(*away_coach_rows.text)

# for row in away_coach_rows:
# 	print(row.text)
###AWAY COACHES###





##HOME STAT SUMMARY##
home_line_stats = []
home_line = []
home_td = []
home_coach_line = []
home_coaches = []

home_table = game_tables.find_element_by_xpath("//div[@ng-class='sumTableHalfRight']/div[@ng-class='sumTableMobile']")
home_line = home_table.find_elements_by_xpath("//tr[contains(@ng-repeat,'homeTeam.skaters')]")
home_coach_line = home_table.find_elements_by_xpath("//tr[contains(@ng-repeat,'homeTeam.coaches')]")

for line in home_line:
	home_td = line.find_elements_by_xpath("td")
	homeplyr_number = home_td[0].text
	homeplyr_letter = home_td[1].text
	homeplyr_name = home_td[2].text.split(", ",1)[1] + " " + home_td[2].text.split(", ",1)[0]
	homeplyr_id = home_td[2].find_element_by_xpath("a").get_attribute('href').split('/player/')[1].split('/')[0]
	homeplyr_pos = home_td[3].text
	homeplyr_goals = home_td[4].text
	homeplyr_assists = home_td[5].text
	homeplyr_pim = home_td[6].text
	homeplyr_shots = home_td[7].text
	homeplyr_plusminus = home_td[8].text
	home_line_stats.append([homeplyr_number, homeplyr_letter, homeplyr_name, homeplyr_id, homeplyr_pos, homeplyr_goals, homeplyr_assists, homeplyr_pim, homeplyr_shots, homeplyr_plusminus])


for line in home_coach_line:
	homecoach_role = line.text.split(": ")[0]
	homecoach_name = line.text.split(": ")[1]
	home_coaches.append([homecoach_role, homecoach_name])

print(*home_coaches)

#print(*home_line_stats)
###/HOME STAT SUMMARY


# print(len(away_line))

# for cell in away_line:
#     print(cell.text)

# print(away_line_stats.text)
# for line in away_line_stats:
#     print(line.find_element_by_xpath("//td").text)

# print(*three_stars)
                #<div ng-class="gcThreeStar" ng-repeat="star in gameSummary.mostValuablePlayers track by $index" class="ng-scope ht-three-star">
				# 	<div class="ht-star-image">
				# 		<img ng-src="https://assets.leaguestat.com/ahl/240x240/5490.jpg" alt="Spencer Martin" title="Spencer Martin" src="https://assets.leaguestat.com/ahl/240x240/5490.jpg">
				# 	</div>
				# 	<div class="ht-star-container">
				# 		<div class="ht-star-number">
				# 			<!-- ngIf: $index == 0 -->
				# 			<!-- ngIf: $index == 1 --><span ng-if="$index == 1" class="ng-binding ng-scope">2nd</span><!-- end ngIf: $index == 1 -->
				# 			<!-- ngIf: $index == 2 -->
				# 		</div>
				# 		<div class="ht-star-name">
				# 			<a ng-href="/stats/player/5490/65/spencer-martin" target="_self" ng-bind="star.player.info.firstName +&quot; &quot;+ star.player.info.lastName + &quot; (#&quot; + star.player.info.jerseyNumber + &quot;)&quot;" class="ng-binding" href="/stats/player/5490/65/spencer-martin">Spencer Martin (#30)</a>
				# 		</div>
				# 		<div class="ht-star-team">
				# 			<span ng-bind="star.team.name" class="ng-binding">Syracuse Crunch</span>
				# 		</div>
				# 		<div class="ht-star-stats ng-hide" ng-hide="star.isGoalie">
				# 			<span ng-bind="&quot;G: &quot; + star.player.stats.goals + &quot; |&quot;" class="ng-binding">G: 0 |</span>
				# 			<span ng-bind="&quot;A: &quot; + star.player.stats.assists" class="ng-binding">A: 0</span>
				# 		</div>
				# 		<div class="ht-star-stats" ng-show="star.isGoalie">
				# 			<span ng-bind="&quot;SA: &quot; + star.player.stats.shotsAgainst + &quot; |&quot;" class="ng-binding">SA: 28 |</span>
				# 			<span ng-bind="&quot;SV: &quot; + star.player.stats.saves + &quot; |&quot;" class="ng-binding">SV: 27 |</span>
				# 			<span ng-bind="&quot;TOI: &quot; + star.player.stats.timeOnIce" class="ng-binding">TOI: 59:50</span>
				# 		</div>
				# 	</div>
				# </div>


# away_pts = []
# home_pp_goals = []
# home_pp_opps = []
# home_pims = []
# home_infracs = []
# home_pts = []

###GAME DETAILS###

# print(home_pims)
# print(home_infracs)

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