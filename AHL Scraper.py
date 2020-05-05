# import libraries
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import pandas as pd
# specify the url
gamenumber = 1020541
urlpage = 'https://theahl.com/stats/game-center/' + str(gamenumber)
print(urlpage)

options = Options()
options.headless = True



# get data from webpage
driver = webdriver.Firefox(options=options)
driver.get(urlpage)
# game_tables = driver.find_element_by_xpath("//div[@class='ht-gc-game-details']/div[@ng-class='gcDetailTable' and @class='ht-gc-game-detail']/table[@class='ht-table ht-table-no-overflow']")

summary_container = driver.find_element_by_xpath("//div[@class='ht-summary-container']")

rink = driver.find_element_by_xpath("//div[@ng-class='rinkContainer']")
pbp = driver.find_elements_by_xpath(
    "//div[contains(@ng-show,'ht_') and contains(@ng-repeat,'PlayByPlayPeriodBreakdown')]/div[contains(@ng-show,'ht_')]")
pbp_periods = driver.find_elements_by_xpath(
    "//div[contains(@ng-show,'ht_') and contains(@ng-repeat,'PlayByPlayPeriodBreakdown')]")


# execute script to scroll down the page
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
# sleep for 10s


# pull highest-level web elements


time.sleep(5)


def get_game_data(main_driver): ###COMPLETE
    game_data = []
    matchup_container = main_driver.find_element_by_xpath("//div[@class='ht-gc-header-row']")

    game_data.append(["game_id", matchup_container.find_element_by_xpath("//*[@class='ht-game-number']").text])
    game_data.append(["game_date", matchup_container.find_element_by_xpath("//*[contains(@class,'ht-game-date')]").text])
    game_data.append(["game_status", matchup_container.find_element_by_xpath("//*[contains(@ng-bind,'gameSummary.details.status')]").text])
    game_data.append(["away_team", matchup_container.find_element_by_xpath("//*[contains(@class,'ht-gc-visiting-team')]").text])
    game_data.append(["home_team", matchup_container.find_element_by_xpath("//*[contains(@class,'ht-gc-home-team')]").text])# print(game_id.text)

    return game_data


def get_arena_data(summary):  ###COMPLETE
    arena_data = []

    arena_data.append(["venue", summary.find_element_by_xpath("//td[contains(@ng-bind,'gameSummary.details.venue')]").text])
    arena_data.append(["attendance", summary.find_element_by_xpath("//td[contains(@ng-bind,'gameSummary.details.attendance')]").text])
    arena_data.append(["start_time", summary.find_element_by_xpath("//td[contains(@ng-bind,'gameSummary.details.startTime')]").text])
    arena_data.append(["end_time", summary.find_element_by_xpath("//td[contains(@ng-bind,'gameSummary.details.endTime')]").text])
    arena_data.append(["duration", summary.find_element_by_xpath("//td[contains(@ng-bind,'gameSummary.details.duration')]").text])

    return arena_data


def get_referee_data(summary):
    game_officials = []
    referees = []

    referees = summary.find_elements_by_xpath("//tr[contains(@ng-repeat,'gameSummary.referees') or contains(@ng-repeat,'gameSummary.linesmen')]")

    for line in referees:
        referee_data = line.find_elements_by_xpath("td")
        referee_role = referee_data[0].text
        referee_name = referee_data[1].find_element_by_xpath("span[contains(@ng-show,'hide_official_names')]").text
        referee_number = referee_data[1].find_element_by_xpath("span[contains(@ng-show,'jerseyNumber')]/span").text
        game_officials.append([referee_role, referee_name, referee_number])

    return game_officials


# scoring_boxscore_WE = []
# scoring_boxscore = []
# game_tables = []



# pbp = []
# pbp_periods = []





def get_scoring_summary(tables): ####DOESN'T WORK

    ###SCORING SUMMARY###
    #Periods (last period is total)
    periods = []
    periods = tables.find_elements_by_xpath("//tr/th[contains(@ng-repeat,'scoreSummaryHeadings')]")


    #Away Stats#
    away_goals = []
    # away_shots = []
    away_goals = tables.find_elements_by_xpath("//tr/td[contains(@ng-repeat,'visitingScoreSummary')]")
    # away_shots = tables.find_elements_by_xpath("//tr/td[contains(@ng-repeat,'visitingShotSummary')]")

    for period in away_goals:
        print(period.text)

    # #Home Stats#
    # home_goals = []
    # home_shots = []
    # home_goals = tables.find_elements_by_xpath("//tr/td[contains(@ng-repeat,'homeScoreSummary')]")
    # home_shots = tables.find_elements_by_xpath("//tr/td[contains(@ng-repeat,'homeShotSummary')]")
    # ###/SCORING SUMMARY###


    # scoring_summary = [["period","home_goals","away_goals","home_shots","away_shots"]]

    # for per, hgoals, agoals, hshots, ashots in zip(periods, home_goals, away_goals, home_shots, away_shots):
    #     scoring_summary.append([per.text,hgoals.text,agoals.text,hshots.text,ashots.text])

    return# scoring_summary

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

# events = []
# event_info = []
# events = rink.find_elements_by_xpath("div[contains(@id,'ht_pin_')]")

# pbp_event_info = []
# shot_events = []
# other_events = []


# for pbp_data in pbp:
# 	# print(pbp_data.get_attribute('innerHTML'))
# 	# break#print(" ")
# 	#print(pbp_data.get_attribute("ng-show").split("ht_")[1]) #ok
# 	pbp_row = pbp_data.find_element_by_xpath("div[contains(@class,'ht-event-row')]")
# 	#pbp_team = pbp_row.find_element_by_xpath("div[@class='ht-home-or-visit']/div").get_attribute('class').split("team")[0].split("ht-")[1]
# 	pbp_team = pbp_data.find_element_by_xpath("div[contains(@class,'ht-event-row')]/div[@class='ht-home-or-visit']/div").get_attribute('class').split("team")[0].split("ht-")[1]
# 	print(pbp_team)
# print(pbp_data.find_element_by_xpath("//div[@class='ht-home-or-visit']/div").get_attribute('class'))#<div class="ht-home-or-visit">

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







# pbp_assists = []
# pbp_assist_line = []
# pbp_plus_players = []
# pbp_minus_players = []
# plus_minus_tables = []
# plus_minus_rows = []
# pbp_events = []


# for period in pbp_periods:
#     period_number = period.get_attribute('ng-show').split("ht_")[1]
#     period_name = period.find_element_by_xpath(
#         "div[@ng-bind='gamePBP.longName']").text
#     # print(f"{period_number} | {period_name}")

#     pbp_events = period.find_elements_by_xpath("div[contains(@ng-show,'ht_')]")

#     for event in pbp_events:
#         pbp_event_row = event.find_element_by_xpath(
#             "div[contains(@class,'ht-event-row')]")
#         pbp_team = pbp_event_row.find_element_by_xpath(
#             "div[@class='ht-home-or-visit']/div").get_attribute('class').split("team")[0].split("ht-")[1]
#         pbp_team_name = pbp_event_row.find_element_by_xpath(
#             "div[@class='ht-event-image']/img").get_attribute('title')
#         pbp_event_time = pbp_event_row.find_element_by_xpath(
#             "div[@class='ht-event-time']").text

#         # Pull Event Details
#         pbp_event_details = pbp_event_row.find_element_by_xpath(
#             "div[@class='ht-event-details']")
#         pbp_event_type = pbp_event_details.find_element_by_xpath(
#             "div[contains(@class,'ht-event-type')]").text

#         # Pull Shot Info
#         if "SHOT" in pbp_event_type:
#             pbp_shooter_number = pbp_event_details.find_element_by_xpath(
#                 "div/span[contains(@ng-bind,'shooter.jerseyNumber')]").text.replace("#", "")
#             pbp_shooter = pbp_event_details.find_element_by_xpath(
#                 "div/a/span[contains(@ng-bind,'shooter.lastName')]").text
#             pbp_goalie_number = pbp_event_details.find_element_by_xpath(
#                 "div/span[contains(@ng-bind,'goalie.jerseyNumber')]").text.replace("#", "")
#             pbp_goalie = pbp_event_details.find_element_by_xpath(
#                 "div/a/span[contains(@ng-bind,'goalie.lastName')]").text

#             try:
#                 pbp_shot_success = "[" + pbp_event_details.find_element_by_xpath(
#                     "div/span[@ng-if='pbp.details.isGoal']").text + "]"
#             except:
#                 pbp_shot_success = ""
#             # print(f"{pbp_event_type} | {pbp_team} | {pbp_team_name} | {pbp_event_type} by #{pbp_shooter_number} {pbp_shooter} on #{pbp_goalie_number} {pbp_goalie} at {pbp_event_time} {pbp_shot_success}")
#         # Pull Goal Info
#         elif pbp_event_type == "GOAL":
#             pbp_goal_types = []

#             # Goal Info2
#             pbp_shooter_number = pbp_event_details.find_element_by_xpath(
#                 "div/span[contains(@ng-bind,'scoredBy.jerseyNumber')]").text.replace("#", "")
#             pbp_shooter = pbp_event_details.find_element_by_xpath(
#                 "div/a[contains(@ng-bind,'scoredBy.lastName')]").text
#             pbp_goal_count = pbp_event_details.find_element_by_xpath(
#                 "div/span[contains(@ng-bind,'pbp.details.scorerGoalNumber')]").text.replace("(", "").replace(")", "")

#             pbp_goal_types = pbp_event_details.find_elements_by_xpath(
#                 "div/span[contains(@ng-if,'pbp.details.properties')]")
#             pbp_goal_type = ""

#             if(len(pbp_goal_types)) != 0:
#                 for goal_type in pbp_goal_types:
#                     pbp_goal_type = pbp_goal_type + " [" + goal_type.text + "]"

#             pbp_goal_str = f"\n {pbp_team} | {pbp_team_name} | {pbp_event_type} by #{pbp_shooter_number} {pbp_shooter} ({pbp_goal_count}){pbp_goal_type} at {pbp_event_time} of the {period_name} period"

#             # Assist1 Info
#             pbp_assists = pbp_event_details.find_elements_by_xpath(
#                 "div/span[@ng-show='pbp.details.assists.length']/span[contains(@ng-repeat,'assist in pbp.details.assists')]")

#             pbp_assists_given = len(pbp_assists)

#             if pbp_assists_given == 0:
#                 pbp_goal_str = pbp_goal_str + ", unassisted"
#             else:
#                 pbp_goal_str = pbp_goal_str + ", assisted by:"
#                 for assist in pbp_assists:
#                     pbp_assistor_number = assist.find_element_by_xpath(
#                         "span[contains(@ng-bind,'assist.jerseyNumber')]").text.replace("#", "")
#                     pbp_assistor = assist.find_element_by_xpath(
#                         "a[contains(@ng-bind,'assist.lastName')]").text
#                     pbp_assist_count = assist.text.split("(")[1].split(")")[0]
#                     pbp_goal_str = pbp_goal_str + \
#                         f"\n     #{pbp_assistor_number} {pbp_assistor} ({pbp_assist_count})"

#             # print(pbp_goal_str + "\n")

#             # Plus-Minus
#             plus_minus_button = pbp_event_row.find_elements_by_xpath(
#                 "div[@class='ht-event-time']/div/span[@ng-show='!pmbutton.expanded']")[0]
#             plus_minus_button.click()

#             plus_minus_tables = pbp_event_row.find_elements_by_xpath(
#                 "div[@ng-show='pmbutton.expanded']/table")

#             for table in plus_minus_tables:
#                 plus_or_minus = table.find_element_by_xpath(
#                     "tbody/tr/th").text.lower()

#                 plus_minus_rows = table.find_elements_by_xpath(
#                     "tbody/tr[contains(@ng-repeat,'in pbp.details')]")

#                 for row in plus_minus_rows:
#                     plus_minus_number = row.find_element_by_xpath(
#                         "td/span[contains(@ng-bind,'.jerseyNumber')]").text.replace("#", "")
#                     plus_minus_player = row.find_element_by_xpath(
#                         "td/a[contains(@ng-bind,'.lastName')]").text

#                     # print(f"{plus_or_minus} | #{plus_minus_number} {plus_minus_player}")
#                     # /Plus-Minus
#         elif pbp_event_type == "PENALTY":
#             pbp_penalized_number = pbp_event_details.find_element_by_xpath(
#                 "div/span[contains(@ng-bind,'takenBy.jerseyNumber')]").text.replace("#", "")
#             pbp_penalized_player = pbp_event_details.find_element_by_xpath(
#                 "div/a/span[contains(@ng-bind,'takenBy.lastName')]").text
#             pbp_penalty_name = pbp_event_details.find_element_by_xpath(
#                 "div/span[@ng-bind='pbp.details.description']").text
#             pbp_penalty_length = pbp_event_details.find_element_by_xpath(
#                 "div/span[contains(@ng-bind,'pbp.details.minutes')]").text
#             pbp_pim = pbp_event_details.find_element_by_xpath(
#                 "div/span[contains(@ng-bind,'pbp.details.minutes')]").text.split(" ")[0]
#             try:
#                 pbp_pp_type = pbp_event_details.find_element_by_xpath("div/span[@ng-if='pbp.details.isPowerPlay']").text
#             except:
#                 pbp_pp_type = "ES"
#             #print(f"#{pbp_penalized_number} {pbp_penalized_player} | {pbp_penalty_name} | {pbp_penalty_length} ({pbp_pp_type}) at {pbp_event_time} of {period_name} period")
#         elif pbp_event_type == "GOALIE CHANGE":
#             goalies_changing = pbp_event_details.find_elements_by_xpath("div/section[contains(@ng-if,'pbp.details.goalie')]")
            
#             for goalie in goalies_changing:
#                 changing_goalie_number = goalie.find_element_by_xpath(
#                     "span[contains(@ng-bind,'jerseyNumber')]").text.replace("#", "").replace("- ", "")
#                 changing_goalie_name = goalie.find_element_by_xpath(
#                     "a/span[contains(@ng-bind,'lastName')]").text
#                 changing_goalie_action = goalie.find_element_by_xpath(
#                     "span[@class='ng-binding' and not(contains(@ng-bind,'jerseyNumber'))]").text

#                 # print(f"#{changing_goalie_number} {changing_goalie_name} {changing_goalie_action} at {pbp_event_time}, {period_name} period.")
#         elif pbp_event_type == " ":  # in shootout
#             attempt_results = []

#             so_shooter_number = pbp_event_details.find_element_by_xpath(
#                 "div/span[contains(@ng-bind,'shooter.jerseyNumber')]").text.replace("#", "")
#             so_shooter_name = pbp_event_details.find_element_by_xpath(
#                 "div/a/span[contains(@ng-bind,'shooter.lastName')]").text
#             # so_shooter_team = pbp_event_details.find_element_by_xpath("div/span[contains(@ng-bind,'shooter.jerseyNumber')]").text.replace("#","")

#             so_goalie_number = pbp_event_details.find_element_by_xpath(
#                 "div/span[contains(@ng-bind,'goalie.jerseyNumber')]").text.replace("#", "")
#             so_goalie_name = pbp_event_details.find_element_by_xpath(
#                 "div/a/span[contains(@ng-bind,'goalie.lastName')]").text
#             # so_goalie_team = pbp_event_details.find_element_by_xpath("div/span[contains(@ng-bind,'shooter.jerseyNumber')]").text.replace("#","")

#             # results
#             attempt_results = pbp_event_details.find_elements_by_xpath(
#                 "div/span[contains(@class,'ht-gc-marker')]")
#             attempt_result = ""

#             if(len(attempt_results)) != 0:
#                 for result in attempt_results:
#                     attempt_result = attempt_result + "[" + result.text + "] "

#             # print(f"{pbp_team_name} #{so_shooter_number} {so_shooter_name} shootout attempt on #{so_goalie_number} {so_goalie_name}:   {attempt_result}")
#         else:
#                 print(f"EVENT NOT ACCOUNTED FOR: {pbp_event_type}")









			#print(pbp_event_type)
    # elif pbp_event_type == "PENALTY":

            # pbp_plus_players = pbp_event_row.find_elements_by_xpath("div[@ng-show='pmbutton.expanded']//tr[@ng-repeat='pmp in pbp.details.plus_players']")

            # #print(len(pbp_plus_players))
            # for player in pbp_plus_players:
            # 			pbp_plus_number = player.find_element_by_xpath("td/span[contains(@ng-bind,'pmp.jerseyNumber')]").text.replace("#","")
            # 			pbp_plus_player = player.find_element_by_xpath("td/a[contains(@ng-bind,'pmp.lastName')]").text
            # 			print(f"#{pbp_plus_number} {pbp_plus_player}")

            # print(player.text)
            # if len(pbp_assists) == 1:
        # 		pbp_goal_str

            # print(len(pbp_assists))

            # for assist in pbp_assists:
            # 		pbp_assist_number = pbp_event_details.find_elements_by_xpath("span[contains(@ng-bind,'assist.jerseyNumber')]").text.replace("#","")
            # 		print(f"#{pbp_assist_number}")

            # print(f"{pbp_team} | {pbp_team_name} | {pbp_event_type} by #{pbp_shooter_number} {pbp_shooter} ({pbp_goal_count}) at {pbp_event_time} from ")


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

# <div id="ht-icerink" ng-class="rinkContainer" class="ht-gc-icerink-container ng-scope">

# pbp_events = []

# pbp_events = pbp.find_elements_by_xpath("div[contains(@ng-show,'ht_')]")
    # print(event.text)
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

# scoring_boxscore = driver.find_element_by_xpath("//td[contains(@ng_repeat, 'visitingScoreSummary')]")


# scoring_boxscore_WE = driver.find_elements_by_xpath("//td[contains(@ng-repeat,'visitingScoreSummary')]")#='stat' and @class='ng-binding']") #<span ng-bind="stat" class="ng-binding">2</span>


# for item in scoring_boxscore_WE:
#      scoring_boxscore.append(item.find_element_by_xpath("//span[@ng-bind='stat' and @class='ng-binding']")) #<span ng-bind="stat" class="ng-binding">2</span>

# for item in scoring_boxscore:
#     print(item.text)



# # create empty array to store data
# data = []

def get_nothing():
    #### # loop over results
    #### for result in results:
    ####     product_name = result.text
    ####     link = result.find_element_by_tag_name('a')
    ####     product_link = link.get_attribute("href")

    ####     # append dict to array
    ####     data.append({"product" : product_name, "link" : product_link})
    pass

def save_to_pandas():
    # # save to pandas dataframe
    # df = pd.DataFrame(data)
    # print(df)
    pass

def write_to_csv():
    # # write to csv
    # path = 'C:\\Users\\Gudsson\\Documents\\Programming\\AHL Scrape\\'
    # df.to_csv(path + 'asdaYogurtLink.csv')
    pass



####PRINT OUTS###

# game_data = []
# game_data = get_game_data(driver)
# game_data = get_arena_data(summary_container)
game_data = get_referee_data(summary_container)
# game_data = get_scoring_summary(game_tables)

for item in game_data:
    print(*item)

###/PRINT OUTS###

driver.quit()
