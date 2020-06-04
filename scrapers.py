# import libraries
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
from datetime import datetime
import pandas as pd

game_id = ''
home_team = ''
away_team = ''
# specify the url
# gamenumber = 1020544
# urlpage = 'https://theahl.com/stats/game-center/' + str(gamenumber)
# print(urlpage)

# options = Options()
# options.headless = True



# get data from webpage
# driver = webdriver.Firefox(options=options)
# driver.get(urlpage)
# game_tables = driver.find_element_by_xpath("//div[@class='ht-gc-game-details']/div[@ng-class='gcDetailTable' and @class='ht-gc-game-detail']/table[@class='ht-table ht-table-no-overflow']")

# matchup_container = driver.find_element_by_xpath("//div[@class='ht-gc-header-row']")
# summary_container = driver.find_element_by_xpath("//div[@class='ht-summary-container']")

# rink = driver.find_element_by_xpath("//div[@ng-class='rinkContainer']")
# pbp = driver.find_elements_by_xpath(
#     "//div[contains(@ng-show,'ht_') and contains(@ng-repeat,'PlayByPlayPeriodBreakdown')]/div[contains(@ng-show,'ht_')]")
# pbp_periods = driver.find_elements_by_xpath(
#     "//div[contains(@ng-show,'ht_') and contains(@ng-repeat,'PlayByPlayPeriodBreakdown')]")


# execute script to scroll down the page
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
# sleep for 10s


# pull highest-level web elements


# time.sleep(5)
# saved_driver = driver

def get_driver(id):
    global game_id
    game_id = id

    urlpage = 'https://theahl.com/stats/game-center/' + str(id)
    print(urlpage)

    options = Options()
    options.headless = True

    driver = webdriver.Firefox(options=options)
    driver.get(urlpage)

    return driver

def game_data(driver): ###COMPLETE`
    game = dict()
    arena = dict()

    matchup_container = driver.find_element_by_xpath("//div[@class='ht-gc-header-row']")
    scores = matchup_container.find_elements_by_xpath("//div[@class='ht-gc-score-container']")
    date = matchup_container.find_element_by_xpath("//*[contains(@class,'ht-game-date')]").text.split(", ", 1)

    game["game_id"] = game_id
    game["game_number"] = matchup_container.find_element_by_xpath("//*[@class='ht-game-number']").text.split("#: ")[1]
    game["date"] = date[1]
    game["season"] = game["date"].split(",")[1].strip()
    game["dow"] = date[0]
    game["status"] = matchup_container.find_element_by_xpath("//*[contains(@ng-bind,'gameSummary.details.status')]").text
    game["away_team"] = matchup_container.find_element_by_xpath("//*[contains(@class,'ht-gc-visiting-team')]").text
    game["away_score"] = scores[0].text
    game["home_score"] = scores[1].text
    game["home_team"] = matchup_container.find_element_by_xpath("//*[contains(@class,'ht-gc-home-team')]").text

    #Gets season based on date.  Assumes season will always end before September 1 
    game_date = datetime.strptime(game["date"],"%B %d, %Y")

    game["season"] = game["season"] + str(int(game["season"])+1) if game_date.month > 8 else str(int(game["season"])-1) + game["season"]

    arena = arena_data(driver)
    game_data = {**game, **arena}

    global home_team, away_team
    home_team = game["home_team"]
    away_team = game["away_team"]

    return game_data

def arena_data(driver):  ###COMPLETE
    arena_data = dict()

    summary = driver.find_element_by_xpath("//div[@class='ht-summary-container']")

    arena_data["venue"] = summary.find_element_by_xpath("//td[contains(@ng-bind,'gameSummary.details.venue')]").text
    arena_data["attendance"] = summary.find_element_by_xpath("//td[contains(@ng-bind,'gameSummary.details.attendance')]").text
    arena_data["start_time"] = summary.find_element_by_xpath("//td[contains(@ng-bind,'gameSummary.details.startTime')]").text
    arena_data["end_time"] = summary.find_element_by_xpath("//td[contains(@ng-bind,'gameSummary.details.endTime')]").text
    arena_data["duration"] = summary.find_element_by_xpath("//td[contains(@ng-bind,'gameSummary.details.duration')]").text

    return arena_data

def referee_data(driver):   ###COMPLETE
    game_officials = []
    referees = []
    summary = driver.find_element_by_xpath("//div[@class='ht-summary-container']")
    referees = summary.find_elements_by_xpath("//tr[contains(@ng-repeat,'gameSummary.referees') or contains(@ng-repeat,'gameSummary.linesmen')]")

    for line in referees:
        referee_data = line.find_elements_by_xpath("td")
        referee_role = referee_data[0].text
        referee_name = referee_data[1].find_element_by_xpath("span[contains(@ng-show,'hide_official_names')]").text
        referee_number = referee_data[1].find_element_by_xpath("span[contains(@ng-show,'jerseyNumber')]/span").text
        game_officials.append({'game_id': game_id, 'role': referee_role, 'name': referee_name, 'number': referee_number})

    return game_officials

def boxscore(driver):   ###COMPLETE
    summary = driver.find_element_by_xpath("//div[@class='ht-summary-container']")
    
    #Periods (last period is total)
    goal_periods = []
    goal_periods = summary.find_elements_by_xpath("//tr/th[contains(@ng-repeat,'scoreSummaryHeadings')]")

    #Periods (last period is total)
    shot_periods = []
    shot_periods = summary.find_elements_by_xpath("//tr/th[contains(@ng-repeat,'shotSummaryHeadings')]")

    #Away Stats#
    away_goals = []
    away_shots = []
    away_goals = summary.find_elements_by_xpath("//tr/td[contains(@ng-repeat,'visitingScoreSummary')]")
    away_shots = summary.find_elements_by_xpath("//tr/td[contains(@ng-repeat,'visitingShotSummary')]")

    #Home Stats#
    home_goals = []
    home_shots = []
    home_goals = summary.find_elements_by_xpath("//tr/td[contains(@ng-repeat,'homeScoreSummary')]")
    home_shots = summary.find_elements_by_xpath("//tr/td[contains(@ng-repeat,'homeShotSummary')]")

    goal_summary = dict()
    shot_summary = dict()

    for period, agoals, hgoals in zip(goal_periods, away_goals, home_goals):
        goal_summary[period.text] = {"game_id": game_id, "away_goals": agoals.text, "home_goals": hgoals.text}

    for period, ashots, hshots in zip(shot_periods, away_shots, home_shots):
        shot_summary[period.text] = {"game_id": game_id, "home_shots": hshots.text, "away_shots": ashots.text}

    scoring_summary = dict() #["period","home_goals","away_goals","home_shots","away_shots"]]

    for summary in goal_summary:

        scoring_summary[summary] = goal_summary[summary]

        try:
            scoring_summary[summary].update(shot_summary[summary])
        except:
            scoring_summary[summary].update({"home_shots": 0, "away_shots": 0})

    return scoring_summary

def penalty_summary(driver):   ###COMPLETE
    summary = driver.find_element_by_xpath("//div[@class='ht-summary-container']")
    penalty_summary = []

    #Away PP#
    away_pp = []
    away_penalties = []

    away_pp = summary.find_element_by_xpath("//tr/td/span[contains(@ng-bind,'gameSummary.visitingTeam.stats.powerPlayGoals')]").text.replace(" ","").split("/",1) #get away PP fraction string and split
    away_penalties = summary.find_element_by_xpath("//tr/td/span[contains(@ng-bind,'gameSummary.visitingTeam.stats.penaltyMinuteCount')]").text.split(" min / ",1) #get away PP fraction string and split
    
    #Home PP#
    home_pp = []
    home_penalties = []

    home_pp = summary.find_element_by_xpath("//tr/td/span[contains(@ng-bind,'gameSummary.homeTeam.stats.powerPlayGoals')]").text.replace(" ","").split("/",1) #get home PP fraction string and split
    home_penalties = summary.find_element_by_xpath("//tr/td/span[contains(@ng-bind,'gameSummary.homeTeam.stats.penaltyMinuteCount')]").text.split(" min / ",1) #get home PP fraction string and split
    
    #build return array
    penalty_summary.append({"game_id": game_id, "team": "away", "pp_goals": away_pp[0], "pp_opps": away_pp[1], "pims": away_penalties[0], "infracs": away_penalties[1].split(" ",1)[0]})
    penalty_summary.append({"game_id": game_id, "team": "home", "pp_goals": home_pp[0], "pp_opps": home_pp[1], "pims": home_penalties[0], "infracs": home_penalties[1].split(" ",1)[0]})

    return penalty_summary

def three_stars(driver):  ###COMPLETE
    summary = driver.find_element_by_xpath("//div[@class='ht-summary-container']")
    
    stars = []
    star_containers = []
    
    star_containers = summary.find_elements_by_xpath("//div[@class='ht-three-stars']/div/div[@class='ht-star-container']")

    for star in star_containers:
        star_number = star.find_element_by_xpath("div[@class='ht-star-number']").text
        star_rawname = star.find_element_by_xpath("div[@class='ht-star-name']").text.split(" (#")
        star_name = star_rawname[0]
        star_jersey = star_rawname[1].replace(")","")
        star_team = star.find_element_by_xpath("div[@class='ht-star-team']").text
        stars.append({"game_id": game_id, "star_number": star_number, "name": star_name, "jersey_number": star_jersey, "team": star_team})
    
    return stars

def coaches(driver):   ###COMPLETE
    summary = driver.find_element_by_xpath("//div[@class='ht-summary-container']")
    
    coaches = []
    away_coach_lines = []
    home_coach_lines = []

    # away_team = summary.find_element_by_xpath("//div[@ng-class='sumTableHalfLeft']/div[@class='ht-gc-section-header']/a").attribute("innerHTML")
    # home_team = summary.find_element_by_xpath("//div[@ng-class='sumTableHalfRight']/div[@class='ht-gc-section-header']/a").attribute("innerHTML")
    
    away_coach_lines = summary.find_elements_by_xpath("//div[@ng-class='sumTableHalfLeft']//tr[contains(@ng-repeat,'visitingTeam.coaches')]")
    home_coach_lines = summary.find_elements_by_xpath("//div[@ng-class='sumTableHalfRight']//tr[contains(@ng-repeat,'homeTeam.coaches')]")

    for line in away_coach_lines:
        coach_role = line.text.split(": ")[0]
        coach_name = line.text.split(": ")[1]
        coaches.append({"game_id": game_id, "team": away_team, "role": coach_role, "name": coach_name})

    for line in home_coach_lines:
        coach_role = line.text.split(": ")[0]
        coach_name = line.text.split(": ")[1]
        coaches.append({"game_id": game_id, "team": home_team, "role": coach_role, "name": coach_name})

    return coaches

def player_scorelines(driver):   ###COMPLETE
    summary = driver.find_element_by_xpath("//div[@class='ht-summary-container']")

    players = []
    away_player_lines = []
    home_player_lines = []

    away_team = summary.find_element_by_xpath("//div[@ng-class='sumTableHalfLeft']/div[@class='ht-gc-section-header']/a").attribute("innerHTML")
    home_team = summary.find_element_by_xpath("//div[@ng-class='sumTableHalfRight']/div[@class='ht-gc-section-header']/a").attribute("innerHTML")
    
    away_player_lines = summary.find_elements_by_xpath("//div[@ng-class='sumTableHalfLeft']/div[@ng-class='sumTableMobile']//tr[contains(@ng-repeat,'visitingTeam.skaters')]") #find_elements_by_xpath("//div[@ng-class='sumTableHalfLeft']//tr[contains(@ng-repeat,'visitingTeam.coaches')]")
    home_player_lines = summary.find_elements_by_xpath("//div[@ng-class='sumTableHalfRight']/div[@ng-class='sumTableMobile']//tr[contains(@ng-repeat,'homeTeam.skaters')]")

    for line in away_player_lines:
    	away_td = line.find_elements_by_xpath("td")
    	awayplyr_number = away_td[0].text
    	awayplyr_letter = away_td[1].text
    	awayplyr_name = away_td[2].text.split(", ",1)[1] + " " + away_td[2].text.split(", ",1)[0]
    	awayplyr_id = away_td[2].find_element_by_xpath("a").attribute('href').split('/player/')[1].split('/')[0]
    	awayplyr_pos = away_td[3].text
    	awayplyr_goals = away_td[4].text
    	awayplyr_assists = away_td[5].text
    	awayplyr_pim = away_td[6].text
    	awayplyr_shots = away_td[7].text
    	awayplyr_plusminus = away_td[8].text
    	players.append([away_team, awayplyr_number, awayplyr_letter, awayplyr_name, awayplyr_id, awayplyr_pos, awayplyr_goals, awayplyr_assists, awayplyr_pim, awayplyr_shots, awayplyr_plusminus])

    for line in home_player_lines:
    	home_td = line.find_elements_by_xpath("td")
    	homeplyr_number = home_td[0].text
    	homeplyr_letter = home_td[1].text
    	homeplyr_name = home_td[2].text.split(", ",1)[1] + " " + home_td[2].text.split(", ",1)[0]
    	homeplyr_id = home_td[2].find_element_by_xpath("a").attribute('href').split('/player/')[1].split('/')[0]
    	homeplyr_pos = home_td[3].text
    	homeplyr_goals = home_td[4].text
    	homeplyr_assists = home_td[5].text
    	homeplyr_pim = home_td[6].text
    	homeplyr_shots = home_td[7].text
    	homeplyr_plusminus = home_td[8].text
    	players.append([home_team, homeplyr_number, homeplyr_letter, homeplyr_name, homeplyr_id, homeplyr_pos, homeplyr_goals, homeplyr_assists, homeplyr_pim, homeplyr_shots, homeplyr_plusminus])

    return players

def pins(driver, pbp_arr):   ###COMPLETE
    pins = []
    rink = driver.find_element_by_xpath("//div[@id='ht-icerink']")
    pins = rink.find_elements_by_xpath("div[contains(@id,'ht_pin_')]")
    i = 1

    if len(pins) == len(pbp_arr):
        print("Arrays are equal")

    for pin, data in zip(pins, pbp_arr):
        event_id = pin.attribute("id").split("ht_pin_")[1] #get index
        event_type = pin.text
        event_loc = pin.attribute("style")
        event_loc_top = pin.attribute("style").split("%; left: ")[0].split("top:")[1]
        event_loc_left = pin.attribute("style").split("%; left: ")[1].split("%;")[0]

        print(f'#{i} (id={event_id}) | {pin.attribute("id")} @ top: {event_loc_top}, left: {event_loc_left} | {data[0]} {data[1]} on {data[2]} {data[3]} at {data[5]} of Period {data[4]} ({event_type}|{data[6]})')
        i += 1

def pbp(driver):   ###COMPLETE
    pbp = []
    pbp_periods = []

    pbp_periods = driver.find_elements_by_xpath("//div[@ng-repeat='gamePBP in PlayByPlayPeriodBreakdown track by $index']")

    pbp_assists = []
    pbp_assist_line = []
    pbp_plus_players = []
    pbp_minus_players = []
    plus_minus_tables = []
    plus_minus_rows = []
    pbp_events = []

    pbp_arr = []

    for period in pbp_periods:
        period_number = period.attribute('ng-show').split("ht_")[1]
        period_name = period.find_element_by_xpath(
            "div[@ng-bind='gamePBP.longName']").text
        # print(f"{period_number} | {period_name}")

        pbp_events = period.find_elements_by_xpath("div[contains(@ng-show,'ht_')]")

        for event in pbp_events:
            pbp_event_row = event.find_element_by_xpath(
                "div[contains(@class,'ht-event-row')]")
            pbp_team = pbp_event_row.find_element_by_xpath(
                "div[@class='ht-home-or-visit']/div").attribute('class').split("team")[0].split("ht-")[1]
            pbp_team_name = pbp_event_row.find_element_by_xpath(
                "div[@class='ht-event-image']/img").attribute('title')
            pbp_event_time = pbp_event_row.find_element_by_xpath(
                "div[@class='ht-event-time']").text

            # Pull Event Details
            pbp_event_details = pbp_event_row.find_element_by_xpath(
                "div[@class='ht-event-details']")
            pbp_event_type = pbp_event_details.find_element_by_xpath(
                "div[contains(@class,'ht-event-type')]").text

            # Pull Shot Info
            if "SHOT" in pbp_event_type:
                pbp_shooter_number = pbp_event_details.find_element_by_xpath(
                    "div/span[contains(@ng-bind,'shooter.jerseyNumber')]").text.replace("#", "")
                pbp_shooter = pbp_event_details.find_element_by_xpath(
                    "div/a/span[contains(@ng-bind,'shooter.lastName')]").text
                pbp_goalie_number = pbp_event_details.find_element_by_xpath(
                    "div/span[contains(@ng-bind,'goalie.jerseyNumber')]").text.replace("#", "")
                pbp_goalie = pbp_event_details.find_element_by_xpath(
                    "div/a/span[contains(@ng-bind,'goalie.lastName')]").text

                pbp_arr.append([pbp_shooter_number, pbp_shooter, pbp_goalie_number, pbp_goalie, period_number, pbp_event_time, ""])

                try:
                    pbp_shot_success = "[" + pbp_event_details.find_element_by_xpath(
                        "div/span[@ng-if='pbp.details.isGoal']").text + "]"

                    # if shot successful, add new line for goal pin
                    goal_arr = pbp_arr[-1]
                    goal_arr.pop()
                    goal_arr.append("GOAL")
                    pbp_arr.append(goal_arr)

                except:
                    pbp_shot_success = ""

                print(f"{pbp_event_type} | {pbp_team} | {pbp_team_name} | {pbp_event_type} by #{pbp_shooter_number} {pbp_shooter} on #{pbp_goalie_number} {pbp_goalie} at {pbp_event_time} {pbp_shot_success}")
            
            # Pull Goal Info
            elif pbp_event_type == "GOAL":
                pbp_goal_types = []

                # Goal Info2
                pbp_shooter_number = pbp_event_details.find_element_by_xpath(
                    "div/span[contains(@ng-bind,'scoredBy.jerseyNumber')]").text.replace("#", "")
                pbp_shooter = pbp_event_details.find_element_by_xpath(
                    "div/a[contains(@ng-bind,'scoredBy.lastName')]").text
                pbp_goal_count = pbp_event_details.find_element_by_xpath(
                    "div/span[contains(@ng-bind,'pbp.details.scorerGoalNumber')]").text.replace("(", "").replace(")", "")

                pbp_goal_types = pbp_event_details.find_elements_by_xpath(
                    "div/span[contains(@ng-if,'pbp.details.properties')]")
                pbp_goal_type = ""

                if(len(pbp_goal_types)) != 0:
                    for goal_type in pbp_goal_types:
                        pbp_goal_type = pbp_goal_type + " [" + goal_type.text + "]"

                pbp_goal_str = f"\n {pbp_team} | {pbp_team_name} | {pbp_event_type} by #{pbp_shooter_number} {pbp_shooter} ({pbp_goal_count}){pbp_goal_type} at {pbp_event_time} of the {period_name} period"

                # Assist1 Info
                pbp_assists = pbp_event_details.find_elements_by_xpath(
                    "div/span[@ng-show='pbp.details.assists.length']/span[contains(@ng-repeat,'assist in pbp.details.assists')]")

                pbp_assists_given = len(pbp_assists)

                if pbp_assists_given == 0:
                    pbp_goal_str = pbp_goal_str + ", unassisted"
                else:
                    pbp_goal_str = pbp_goal_str + ", assisted by:"
                    for assist in pbp_assists:
                        pbp_assistor_number = assist.find_element_by_xpath(
                            "span[contains(@ng-bind,'assist.jerseyNumber')]").text.replace("#", "")
                        pbp_assistor = assist.find_element_by_xpath(
                            "a[contains(@ng-bind,'assist.lastName')]").text
                        pbp_assist_count = assist.text.split("(")[1].split(")")[0]
                        pbp_goal_str = pbp_goal_str + \
                            f"\n     #{pbp_assistor_number} {pbp_assistor} ({pbp_assist_count})"

                print(pbp_goal_str + "\n")

                # Plus-Minus
                plus_minus_button = pbp_event_row.find_elements_by_xpath(
                    "div[@class='ht-event-time']/div/span[@ng-show='!pmbutton.expanded']")[0]
                plus_minus_button.click()

                plus_minus_tables = pbp_event_row.find_elements_by_xpath(
                    "div[@ng-show='pmbutton.expanded']/table")

                for table in plus_minus_tables:
                    plus_or_minus = table.find_element_by_xpath(
                        "tbody/tr/th").text.lower()

                    plus_minus_rows = table.find_elements_by_xpath(
                        "tbody/tr[contains(@ng-repeat,'in pbp.details')]")

                    for row in plus_minus_rows:
                        plus_minus_number = row.find_element_by_xpath(
                            "td/span[contains(@ng-bind,'.jerseyNumber')]").text.replace("#", "")
                        plus_minus_player = row.find_element_by_xpath(
                            "td/a[contains(@ng-bind,'.lastName')]").text

                        print(f"{plus_or_minus} | #{plus_minus_number} {plus_minus_player}")
                        # /Plus-Minus

            elif pbp_event_type == "PENALTY":
                pbp_penalized_number = pbp_event_details.find_element_by_xpath(
                    "div/span[contains(@ng-bind,'takenBy.jerseyNumber')]").text.replace("#", "")
                pbp_penalized_player = pbp_event_details.find_element_by_xpath(
                    "div/a/span[contains(@ng-bind,'takenBy.lastName')]").text
                pbp_penalty_name = pbp_event_details.find_element_by_xpath(
                    "div/span[@ng-bind='pbp.details.description']").text
                pbp_penalty_length = pbp_event_details.find_element_by_xpath(
                    "div/span[contains(@ng-bind,'pbp.details.minutes')]").text
                pbp_pim = pbp_event_details.find_element_by_xpath(
                    "div/span[contains(@ng-bind,'pbp.details.minutes')]").text.split(" ")[0]
                try:
                    pbp_pp_type = pbp_event_details.find_element_by_xpath("div/span[@ng-if='pbp.details.isPowerPlay']").text
                except:
                    pbp_pp_type = "ES"
                print(f"PENALTY | #{pbp_penalized_number} {pbp_penalized_player} | {pbp_penalty_name} | {pbp_penalty_length} ({pbp_pp_type}) at {pbp_event_time} of {period_name} period")

            elif pbp_event_type == "GOALIE CHANGE":
                goalies_changing = pbp_event_details.find_elements_by_xpath("div/section[contains(@ng-if,'pbp.details.goalie')]")
                
                for goalie in goalies_changing:
                    changing_goalie_number = goalie.find_element_by_xpath(
                        "span[contains(@ng-bind,'jerseyNumber')]").text.replace("#", "").replace("- ", "")
                    changing_goalie_name = goalie.find_element_by_xpath(
                        "a/span[contains(@ng-bind,'lastName')]").text
                    changing_goalie_action = goalie.find_element_by_xpath(
                        "span[@class='ng-binding' and not(contains(@ng-bind,'jerseyNumber'))]").text

                    print(f"GOALIE CHANGE | #{changing_goalie_number} {changing_goalie_name} {changing_goalie_action} at {pbp_event_time}, {period_name} period.")

            elif pbp_event_type == " ":  # in shootout
                attempt_results = []

                so_shooter_number = pbp_event_details.find_element_by_xpath(
                    "div/span[contains(@ng-bind,'shooter.jerseyNumber')]").text.replace("#", "")
                so_shooter_name = pbp_event_details.find_element_by_xpath(
                    "div/a/span[contains(@ng-bind,'shooter.lastName')]").text
                # so_shooter_team = pbp_event_details.find_element_by_xpath("div/span[contains(@ng-bind,'shooter.jerseyNumber')]").text.replace("#","")

                so_goalie_number = pbp_event_details.find_element_by_xpath(
                    "div/span[contains(@ng-bind,'goalie.jerseyNumber')]").text.replace("#", "")
                so_goalie_name = pbp_event_details.find_element_by_xpath(
                    "div/a/span[contains(@ng-bind,'goalie.lastName')]").text
                # so_goalie_team = pbp_event_details.find_element_by_xpath("div/span[contains(@ng-bind,'shooter.jerseyNumber')]").text.replace("#","")

                # results
                attempt_results = pbp_event_details.find_elements_by_xpath(
                    "div/span[contains(@class,'ht-gc-marker')]")
                attempt_result = ""

                if(len(attempt_results)) != 0:
                    for result in attempt_results:
                        attempt_result = attempt_result + "[" + result.text + "] "

                print(f"SO ATTEMPT | {pbp_team_name} #{so_shooter_number} {so_shooter_name} shootout attempt on #{so_goalie_number} {so_goalie_name}:   {attempt_result}")

            else:
                print(f"EVENT NOT ACCOUNTED FOR: {pbp_event_type}")


    print("==========")
    
    # for element in pbp_arr:
    #     print(element)

    pins(driver, pbp_arr)


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

def preview_stats(driver):   ###COMPLETE
    hth_stats = []
    hth_rows = []

    previous_meeting_rows = []
    previous_meetings = []

    top_scorers = []
    top_scorer_tables = []
    top_scorer_rows = []

    tables = []
    tables = driver.find_elements_by_xpath("//div[@ng-if='PreviewDataLoaded']/div/div[contains(@ng-class,'sumTableHalf')]/div[@ng-class='sumTableMobile']/table/tbody")

    hth_rows = tables[0].find_elements_by_xpath("tr")
    previous_meeting_rows = tables[1].find_elements_by_xpath("tr[@class='ng-scope']")

    #Head-to-Head Stats
    #season | away_team_record | home_team_record
    hth_stats.append([hth_rows[0].text, hth_rows[1].find_elements_by_xpath("td")[1].text, hth_rows[1].find_elements_by_xpath("td")[3].text]) #previous season
    hth_stats.append([hth_rows[2].text, hth_rows[3].find_elements_by_xpath("td")[1].text, hth_rows[3].find_elements_by_xpath("td")[3].text]) #current season
    hth_stats.append([hth_rows[4].text, hth_rows[5].find_elements_by_xpath("td")[1].text, hth_rows[5].find_elements_by_xpath("td")[3].text]) #Last 5 seasons

    print(*hth_stats)

    print("====")
    
    # Previous Meetings
    for row in previous_meeting_rows:
        td = row.find_elements_by_xpath("td")
        away_team = td[0].find_element_by_xpath("a/img").attribute("title")
        score = td[1].text.split(":")
        away_score = score[0]
        home_team = td[2].find_element_by_xpath("a/img").attribute("title")
        home_score = score[1]
        date = td[3].text
        previous_meetings.append([away_team, away_score, home_team, home_score, date])

    print(*previous_meetings)
    print("===")

    #Top Scorers Heading Into Game
    away_team = tables[2].find_elements_by_xpath("tr/th")[0].text
    home_team = tables[2].find_elements_by_xpath("tr/th")[1].text
    team = [away_team, home_team]
    top_scorer_tables = tables[2].find_elements_by_xpath("//table[@class='ht-table-data']/tbody")
    i = 0

    for table in top_scorer_tables:
        top_scorer_rows = table.find_elements_by_xpath("tr")

        for row in top_scorer_rows:
            top_details = []
            top_details = row.find_elements_by_xpath("td/a/div[@class='ht-top-details']/div")

            for detail in top_details:
                top_scorer_name = top_details[0].text
                top_scorer_stats = top_details[1].text
            
            top_scorers.append([team[i], top_scorer_name, top_scorer_stats])
            
        i += 1

    # print(*top_scorers)


    ###LAST 5 GAMES TBA
    l5g_stats = []
    l5g_tables = []
    l5g_tables = tables[3].find_elements_by_xpath("//td[@class='ht-table-last-5']")
    i = 0

    for table in l5g_tables:
        for row in table.find_elements_by_xpath("//tr[contains(@ng-repeat,'last5games')]/td"):
            l5g_stats.append([team[i], row.text])
        i += 1

    # print(*l5g_stats)


    #Match Up Stats
    matchup_stats = []
    matchup_table = driver.find_element_by_xpath("//div[@ng-if='PreviewDataLoaded']/div[@ng-class='sumTableContainter']/div[@ng-class='sumTableMobile']//tbody")

    for row in matchup_table.find_elements_by_xpath("tr"):
        tds = []
        tds = row.find_elements_by_xpath("td")
        matchup_stats.append([tds[0].text, tds[1].text, tds[2].text])

    print(*matchup_stats)

def nothing():
    #### # loop over results
    #### for result in results:
    ####     product_name = result.text
    ####     link = result.find_element_by_tag_name('a')
    ####     product_link = link.attribute("href")

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

# start = time.time()

####PRINT OUTS###

# game_data = []
# game_data = game_data(driver)
# game_data = arena_data(driver)
# game_data = referee_data(driver)
# game_data = boxscore(driver)
# game_data = penalty_summary(driver)
# game_data = three_stars(driver)
# game_data = coaches(driver)
# game_data = player_scorelines(driver)
# preview_stats(driver)
# pins(driver)  
#pbp(driver)

# print(*game_data)
# for item in game_data:
#     print(*item)

# end = time.time()

# print(end - start)

###/PRINT OUTS###



# if __name__ == "__main__":
#     # game_data = game_data(saved_driver)
#     # print(*game_data)
