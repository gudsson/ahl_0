# import libraries
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import pandas as pd
# specify the url
gamenumber = 1020356
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
# game_data.append(["game_id", driver.find_element_by_xpath("//*[@class='ht-game-number']").text])
# game_data.append(["game_date", driver.find_element_by_xpath("//*[contains(@class,'ht-game-date')]").text])
# game_data.append(["game_status", driver.find_element_by_xpath("//*[contains(@ng-bind,'gameSummary.details.status')]").text])
# game_data.append(["away_team", driver.find_element_by_xpath("//*[contains(@class,'ht-gc-visiting-team')]").text])
# game_data.append(["home_team", driver.find_element_by_xpath("//*[contains(@class,'ht-gc-home-team')]").text])# print(game_id.text)




# # Print Band One
# for item in game_data:
#     #print(str(item[0]) + " " + str(item[1]))
#     print(f"{item[0]} | {item[1]}")
# #print('Number of results', len(results))


# scoring_boxscore_WE = []
# scoring_boxscore = []
#game_tables = []

#pull highest-level web elements
# game_tables = driver.find_element_by_xpath("//div[@class='ht-gc-game-details']/div[@ng-class='gcDetailTable' and @class='ht-gc-game-detail']/table[@class='ht-table ht-table-no-overflow']")

pbp = []
pbp_periods = []

rink = driver.find_element_by_xpath("//div[@ng-class='rinkContainer']")
pbp = driver.find_elements_by_xpath("//div[contains(@ng-show,'ht_') and contains(@ng-repeat,'PlayByPlayPeriodBreakdown')]/div[contains(@ng-show,'ht_')]")
pbp_periods = driver.find_elements_by_xpath("//div[contains(@ng-show,'ht_') and contains(@ng-repeat,'PlayByPlayPeriodBreakdown')]")
# ###ARENA DETAILS###
# # game_data.append(["venue", game_tables.find_element_by_xpath("//td[contains(@ng-bind,'gameSummary.details.venue')]").text])
# # game_data.append(["attendance", game_tables.find_element_by_xpath("//td[contains(@ng-bind,'gameSummary.details.attendance')]").text])
# # game_data.append(["start_time", game_tables.find_element_by_xpath("//td[contains(@ng-bind,'gameSummary.details.startTime')]").text])
# # game_data.append(["end_time", game_tables.find_element_by_xpath("//td[contains(@ng-bind,'gameSummary.details.endTime')]").text])
# # game_data.append(["duration", game_tables.find_element_by_xpath("//td[contains(@ng-bind,'gameSummary.details.duration')]").text])
# ###/ARENA DETAILS###

# ###GAME OFFICIALS###
# game_officials = []
# referees = []

# referees = game_tables.find_elements_by_xpath("//tr[contains(@ng-repeat,'gameSummary.referees') or contains(@ng-repeat,'gameSummary.linesmen')]")

# for line in referees:
# 	referee_data = line.find_elements_by_xpath("td")
# 	referee_role = referee_data[0].text
# 	referee_name = referee_data[1].find_element_by_xpath("span[contains(@ng-show,'hide_official_names')]").text
# 	referee_number = referee_data[1].find_element_by_xpath("span[contains(@ng-show,'jerseyNumber')]/span").text
# 	game_officials.append([referee_role, referee_name, referee_number])
# ###/GAME OFFICIALS###

# ###SCORING SUMMARY###
# #Periods (last period is total)
# periods = []
# periods = game_tables.find_elements_by_xpath("//tr/th[contains(@ng-repeat,'scoreSummaryHeadings')]")

# #Away Stats#
# away_goals = []
# away_shots = []
# away_goals = game_tables.find_elements_by_xpath("//tr/td[contains(@ng-repeat,'visitingScoreSummary')]")
# away_shots = game_tables.find_elements_by_xpath("//tr/td[contains(@ng-repeat,'visitingShotSummary')]")

# #Home Stats#
# home_goals = []
# home_shots = []
# home_goals = game_tables.find_elements_by_xpath("//tr/td[contains(@ng-repeat,'homeScoreSummary')]")
# home_shots = game_tables.find_elements_by_xpath("//tr/td[contains(@ng-repeat,'homeShotSummary')]")
# ###/SCORING SUMMARY###

# ###GAME DETAILS###
# #Away PP#
# away_pp = []
# away_penalties = []
# away_pp = game_tables.find_element_by_xpath("//tr/td/span[contains(@ng-bind,'gameSummary.visitingTeam.stats.powerPlayGoals')]").text.replace(" ","").split("/",1) #get away PP fraction string and split
# away_pp_goals = away_pp[0]
# away_pp_opps = away_pp[1]
# away_penalties = game_tables.find_element_by_xpath("//tr/td/span[contains(@ng-bind,'gameSummary.visitingTeam.stats.penaltyMinuteCount')]").text.split(" min / ",1) #get away PP fraction string and split
# away_pims = away_penalties[0]
# away_infracs = away_penalties[1].split(" ",1)[0]

# #Home PP#
# home_pp = []
# home_penalties = []
# home_pp = game_tables.find_element_by_xpath("//tr/td/span[contains(@ng-bind,'gameSummary.homeTeam.stats.powerPlayGoals')]").text.replace(" ","").split("/",1) #get home PP fraction string and split
# home_pp_goals = home_pp[0]
# home_pp_opps = home_pp[1]
# home_penalties = game_tables.find_element_by_xpath("//tr/td/span[contains(@ng-bind,'gameSummary.homeTeam.stats.penaltyMinuteCount')]").text.split(" min / ",1) #get home PP fraction string and split
# home_pims = home_penalties[0]
# home_infracs = home_penalties[1].split(" ",1)[0]
# ###/GAME DETAILS###

# ###THREE STARS###
# three_stars = []
# three_stars_WE = []

# three_stars_WE = game_tables.find_element_by_xpath("//div[@class='ht-three-stars']")

# star_number = []
# star_team = []
# star_name = []

# star_number = three_stars_WE.find_elements_by_xpath("//div[@class='ht-star-number']/*")
# star_team = three_stars_WE.find_elements_by_xpath("//div[@class='ht-star-team']/*")
# star_name = three_stars_WE.find_elements_by_xpath("//div[@class='ht-star-name']/*")

# for i in range(0, len(star_number)-1):
#     three_stars.append([star_number[i].text, star_team[i].text, star_name[i].text.split(" (",1)[0]])
# ###/THREE STARS###

# ##AWAY STAT SUMMARY##
# away_line_stats = []
# away_line = []
# away_td = []
# away_coach_line = []
# away_coaches = []

# away_table = game_tables.find_element_by_xpath("//div[@ng-class='sumTableHalfLeft']/div[@ng-class='sumTableMobile']")
# away_line = away_table.find_elements_by_xpath("//tr[contains(@ng-repeat,'visitingTeam.skaters')]")
# away_coach_line = away_table.find_elements_by_xpath("//tr[contains(@ng-repeat,'visitingTeam.coaches')]")

# for line in away_line:
# 	away_td = line.find_elements_by_xpath("td")
# 	awayplyr_number = away_td[0].text
# 	awayplyr_letter = away_td[1].text
# 	awayplyr_name = away_td[2].text.split(", ",1)[1] + " " + away_td[2].text.split(", ",1)[0]
# 	awayplyr_id = away_td[2].find_element_by_xpath("a").get_attribute('href').split('/player/')[1].split('/')[0]
# 	awayplyr_pos = away_td[3].text
# 	awayplyr_goals = away_td[4].text
# 	awayplyr_assists = away_td[5].text
# 	awayplyr_pim = away_td[6].text
# 	awayplyr_shots = away_td[7].text
# 	awayplyr_plusminus = away_td[8].text
# 	away_line_stats.append([awayplyr_number, awayplyr_letter, awayplyr_name, awayplyr_id, awayplyr_pos, awayplyr_goals, awayplyr_assists, awayplyr_pim, awayplyr_shots, awayplyr_plusminus])


# for line in away_coach_line:
# 	awaycoach_role = line.text.split(": ")[0]
# 	awaycoach_name = line.text.split(": ")[1]
# 	away_coaches.append([awaycoach_role, awaycoach_name])
# ###/AWAY STAT SUMMARY

# ##HOME STAT SUMMARY##
# home_line_stats = []
# home_line = []
# home_td = []
# home_coach_line = []
# home_coaches = []

# home_table = game_tables.find_element_by_xpath("//div[@ng-class='sumTableHalfRight']/div[@ng-class='sumTableMobile']")
# home_line = home_table.find_elements_by_xpath("//tr[contains(@ng-repeat,'homeTeam.skaters')]")
# home_coach_line = home_table.find_elements_by_xpath("//tr[contains(@ng-repeat,'homeTeam.coaches')]")

# for line in home_line:
# 	home_td = line.find_elements_by_xpath("td")
# 	homeplyr_number = home_td[0].text
# 	homeplyr_letter = home_td[1].text
# 	homeplyr_name = home_td[2].text.split(", ",1)[1] + " " + home_td[2].text.split(", ",1)[0]
# 	homeplyr_id = home_td[2].find_element_by_xpath("a").get_attribute('href').split('/player/')[1].split('/')[0]
# 	homeplyr_pos = home_td[3].text
# 	homeplyr_goals = home_td[4].text
# 	homeplyr_assists = home_td[5].text
# 	homeplyr_pim = home_td[6].text
# 	homeplyr_shots = home_td[7].text
# 	homeplyr_plusminus = home_td[8].text
# 	home_line_stats.append([homeplyr_number, homeplyr_letter, homeplyr_name, homeplyr_id, homeplyr_pos, homeplyr_goals, homeplyr_assists, homeplyr_pim, homeplyr_shots, homeplyr_plusminus])


# for line in home_coach_line:
# 	homecoach_role = line.text.split(": ")[0]
# 	homecoach_name = line.text.split(": ")[1]
# 	home_coaches.append([homecoach_role, homecoach_name])
# ###/HOME STAT SUMMARY

###RinkPxP###

events = []
event_info = []
events = rink.find_elements_by_xpath("div[contains(@id,'ht_pin_')]")

pbp_event_info = []
shot_events = []
other_events = []



# for pbp_data in pbp:
# 	# print(pbp_data.get_attribute('innerHTML'))
# 	# break#print(" ")
# 	#print(pbp_data.get_attribute("ng-show").split("ht_")[1]) #ok
# 	pbp_row = pbp_data.find_element_by_xpath("div[contains(@class,'ht-event-row')]")
# 	#pbp_team = pbp_row.find_element_by_xpath("div[@class='ht-home-or-visit']/div").get_attribute('class').split("team")[0].split("ht-")[1]
# 	pbp_team = pbp_data.find_element_by_xpath("div[contains(@class,'ht-event-row')]/div[@class='ht-home-or-visit']/div").get_attribute('class').split("team")[0].split("ht-")[1]
# 	print(pbp_team)
	#print(pbp_data.find_element_by_xpath("//div[@class='ht-home-or-visit']/div").get_attribute('class'))#<div class="ht-home-or-visit">

# for event, pbp_data in zip(events, pbp):
# 	# event_id = event.get_attribute("id").split("ht_pin_")[1] #get index
# 	# event_type = event.text
# 	# event_loc = event.get_attribute("style")
# 	# event_loc_top = event.get_attribute("style").split("%; left: ")[0].split("top:")[1]
# 	# event_loc_left = event.get_attribute("style").split("%; left: ")[1].split("%;")[0]

# 	event_type = event.find_element_by_xpath("span").text #'get_attribute("ng-show").split("ht_")[1]
# 	pbp_team = pbp_data.find_element_by_xpath("div[contains(@class,'ht-event-row')]/div[@class='ht-home-or-visit']/div").get_attribute('class').split("team")[0].split("ht-")[1]
# 	#other_events.append(event_type)
# 	print(event_type + " | " + pbp_team)
pbp_assists = []
pbp_assist_line = []
pbp_plus_players = []
pbp_minus_players = []
plus_minus_tables = []
plus_minus_rows = []
pbp_events = []

for period in pbp_periods:
	period_number = period.get_attribute('ng-show').split("ht_")[1]
	period_name = period.find_element_by_xpath("div[@ng-bind='gamePBP.longName']").text
	#print(f"{period_number} | {period_name}")
	
	pbp_events = period.find_elements_by_xpath("div[contains(@ng-show,'ht_')]")

	for event in pbp_events:
		pbp_event_row = event.find_element_by_xpath("div[contains(@class,'ht-event-row')]")
		pbp_team = pbp_event_row.find_element_by_xpath("div[@class='ht-home-or-visit']/div").get_attribute('class').split("team")[0].split("ht-")[1]
		pbp_team_name = pbp_event_row.find_element_by_xpath("div[@class='ht-event-image']/img").get_attribute('title')
		pbp_event_time = pbp_event_row.find_element_by_xpath("div[@class='ht-event-time']").text
		
		#Pull Event Details
		pbp_event_details = pbp_event_row.find_element_by_xpath("div[@class='ht-event-details']")
		pbp_event_type = pbp_event_details.find_element_by_xpath("div[contains(@class,'ht-event-type')]").text

		#Pull Shot Info
		if pbp_event_type == "SHOT":
				pbp_shooter_number = pbp_event_details.find_element_by_xpath("div/span[contains(@ng-bind,'shooter.jerseyNumber')]").text.replace("#","")
				pbp_shooter = pbp_event_details.find_element_by_xpath("div/a/span[contains(@ng-bind,'shooter.lastName')]").text
				pbp_goalie_number = pbp_event_details.find_element_by_xpath("div/span[contains(@ng-bind,'goalie.jerseyNumber')]").text.replace("#","")
				pbp_goalie = pbp_event_details.find_element_by_xpath("div/a/span[contains(@ng-bind,'goalie.lastName')]").text
				
				try:
					pbp_shot_success = "[" + pbp_event_details.find_element_by_xpath("div/span[@ng-if='pbp.details.isGoal']").text +"]"
				except:
					pbp_shot_success = ""
				print(f"{pbp_team} | {pbp_team_name} | {pbp_event_type} by #{pbp_shooter_number} {pbp_shooter} on #{pbp_goalie_number} {pbp_goalie} at {pbp_event_time} {pbp_shot_success}")

		#Pull Goal Info
		elif pbp_event_type == "GOAL":

				#Goal Info
				pbp_shooter_number = pbp_event_details.find_element_by_xpath("div/span[contains(@ng-bind,'scoredBy.jerseyNumber')]").text.replace("#","")
				pbp_shooter = pbp_event_details.find_element_by_xpath("div/a[contains(@ng-bind,'scoredBy.lastName')]").text
				pbp_goal_count = pbp_event_details.find_element_by_xpath("div/span[contains(@ng-bind,'pbp.details.scorerGoalNumber')]").text.replace("(","").replace(")","")

				try:
					pbp_goal_type = "[" + pbp_event_details.find_element_by_xpath("div/span[contains(@ng-if,'pbp.details.properties')]").text +"] "
				except:
					pbp_goal_type = ""

				pbp_goal_str = f"\n {pbp_team} | {pbp_team_name} | {pbp_event_type} by #{pbp_shooter_number} {pbp_shooter} ({pbp_goal_count}) {pbp_goal_type}at {pbp_event_time}"
				
				#Assist1 Info
				pbp_assists = pbp_event_details.find_elements_by_xpath("div/span[@ng-show='pbp.details.assists.length']/span[contains(@ng-repeat,'assist in pbp.details.assists')]")
			
				pbp_assists_given = len(pbp_assists)

				if pbp_assists_given == 0:
						pbp_goal_str = pbp_goal_str + ", unassisted"
				else:
						pbp_goal_str = pbp_goal_str + ", assisted by:"
						for assist in pbp_assists:
							pbp_assistor_number = assist.find_element_by_xpath("span[contains(@ng-bind,'assist.jerseyNumber')]").text.replace("#","")
							pbp_assistor = assist.find_element_by_xpath("a[contains(@ng-bind,'assist.lastName')]").text
							pbp_assist_count = assist.text.split("(")[1].split(")")[0]
							pbp_goal_str = pbp_goal_str + f"\n     #{pbp_assistor_number} {pbp_assistor} ({pbp_assist_count})"
				
				print(pbp_goal_str + "\n")

				###Plus-Minus
				plus_minus_button = pbp_event_row.find_elements_by_xpath("div[@class='ht-event-time']/div/span[@ng-show='!pmbutton.expanded']")[0]
				plus_minus_button.click()

				plus_minus_tables = pbp_event_row.find_elements_by_xpath("div[@ng-show='pmbutton.expanded']/table")

				for table in plus_minus_tables:
					plus_or_minus = table.find_element_by_xpath("tbody/tr/th").text.lower()

					plus_minus_rows = table.find_elements_by_xpath("tbody/tr[contains(@ng-repeat,'in pbp.details')]")

					for row in plus_minus_rows:
						plus_minus_number = row.find_element_by_xpath("td/span[contains(@ng-bind,'.jerseyNumber')]").text.replace("#","")
						plus_minus_player = row.find_element_by_xpath("td/a[contains(@ng-bind,'.lastName')]").text
					
						print(f"{plus_or_minus} | #{plus_minus_number} {plus_minus_player}")
			###/Plus-Minus
	#elif pbp_event_type == "PENALTY":

			# pbp_plus_players = pbp_event_row.find_elements_by_xpath("div[@ng-show='pmbutton.expanded']//tr[@ng-repeat='pmp in pbp.details.plus_players']")

			# #print(len(pbp_plus_players))
			# for player in pbp_plus_players:
			# 			pbp_plus_number = player.find_element_by_xpath("td/span[contains(@ng-bind,'pmp.jerseyNumber')]").text.replace("#","")
			# 			pbp_plus_player = player.find_element_by_xpath("td/a[contains(@ng-bind,'pmp.lastName')]").text
			# 			print(f"#{pbp_plus_number} {pbp_plus_player}")

					#print(player.text)
			# if len(pbp_assists) == 1:
    		# 		pbp_goal_str

			# print(len(pbp_assists))

			# for assist in pbp_assists:
			# 		pbp_assist_number = pbp_event_details.find_elements_by_xpath("span[contains(@ng-bind,'assist.jerseyNumber')]").text.replace("#","")
			# 		print(f"#{pbp_assist_number}")

			#print(f"{pbp_team} | {pbp_team_name} | {pbp_event_type} by #{pbp_shooter_number} {pbp_shooter} ({pbp_goal_count}) at {pbp_event_time} from ")
	else:
			continue

	


# pbp_team = pbp_data.find_element_by_xpath("div[contains(@class,'ht-event-row')]/div[@class='ht-home-or-visit']/div").get_attribute('class').split("team")[0].split("ht-")[1]
# 	# if event_type == "S" or event_type == "goal":
# 		#shot_events.append(event)


# 	### gotta pull this out and iterate through like event and pbp_data
# 	team = pbp_data.find_element_by_xpath("//div[@class='ht-home-or-visit']/div").get_attribute("class").split("team ")[0]
# 	print(event_type + " | " + team)


# print(len(other_events))	
					# else:
			# 	other_events.append(event)
	# event_top_loc = event.get_attribute("style")
	# event_left_loc = event.get_attribute("style")

	# event_info.append(event_id)
	# event_info.append(event_type)
	# event_info.append(event_top_loc)
	# event_info.append(event_left_loc)
	# print(str(event_id) + " | " + str(event_type) + " | " + str(event_loc_top) + " | " + str(event_loc_left))

#<div id="ht-icerink" ng-class="rinkContainer" class="ht-gc-icerink-container ng-scope">

# pbp_events = []

# pbp_events = pbp.find_elements_by_xpath("div[contains(@ng-show,'ht_')]")


	#print(event.text)
# 
# for event in other_events:
    	# print(event.text)

# print("events: " + str(len(events)))
# print("shot events: " + str(len(shot_events)))
# print("non-shot events: " + str(len(other_events)))










###/RinkPxP###

###GamePxP###

# Will need to account for:
# - Penalty shots
# - Shootout Attempts
# - PP and SH shots








###GamePxP###

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