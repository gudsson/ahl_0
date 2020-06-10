# import libraries
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
from datetime import datetime
import pandas as pd
import copy

game_id = ''
home_team = ''
away_team = ''

class Game():
    def __init__(self, game_id=None, home_team=None, away_team=None):
        self.game_id = game_id
        self.home_team = home_team
        self.away_team = away_team

class Shot(Game):
    def __init__(self, game, event):
        self.__dict__ = copy.deepcopy(game.__dict__)
        # super().__init__(game_id, home_team, away_team)
        self.event = event

    def __repr__(self):
        return str(self.game_id) + ": " + str(self.event)

    # def __str__(self):
    #     return "From str method of Test: a is %s, b is %s" % (self.a, self.b)

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
    global game_id ####Delete at end
    game_id = id ####Delete at end

    global game
    game.game_id = id

    urlpage = 'https://theahl.com/stats/game-center/' + str(id)
    print(f'Pulling AHL Game #{id} from: {urlpage}')

    options = Options()
    options.headless = True

    driver = webdriver.Firefox(options=options)
    driver.get(urlpage)

    return driver

def get_summary(driver):
    return driver.find_element_by_xpath("//div[@class='ht-summary-container']")

def get_scoreline(line, side):
    #declarations
    player = dict()

    #get elements
    td = line.find_elements_by_xpath("td")

    #dump scrapings into dict
    player["game_id"] = game.game_id
    player["team"] = getattr(game, str(side + "_team"))
    player["side"] = side
    player["jersey_number"] = td[0].text
    player["letter"] = td[1].text
    player["name"] = td[2].text.split(", ",1)[1] + " " + td[2].text.split(", ",1)[0]
    player["player_id"] = td[2].find_element_by_xpath("a").get_attribute('href').split('/player/')[1].split('/')[0]
    player["position"] = td[3].text
    player["goals"] = td[4].text
    player["assists"] = td[5].text
    player["pims"] = td[6].text
    player["shots"] = td[7].text
    player["plus_minus"] = td[8].text
    
    #return dict
    return player

def game_data(driver):
    #declarations
    global game
    game_info = dict()
    arena = dict()

    #get various elements
    matchup_container = driver.find_element_by_xpath("//div[@class='ht-gc-header-row']")
    scores = matchup_container.find_elements_by_xpath("//div[@class='ht-gc-score-container']")
    date = matchup_container.find_element_by_xpath("//*[contains(@class,'ht-game-date')]").text.split(", ", 1)

    #add scraping to dict
    game_info["game_id"] = game.game_id
    game_info["game_number"] = matchup_container.find_element_by_xpath("//*[@class='ht-game-number']").text.split("#: ")[1]
    game_info["date"] = date[1]
    game_info["season"] = game_info["date"].split(",")[1].strip()
    game_info["dow"] = date[0]
    game_info["status"] = matchup_container.find_element_by_xpath("//*[contains(@ng-bind,'gameSummary.details.status')]").text
    game_info["away_team"] = matchup_container.find_element_by_xpath("//*[contains(@class,'ht-gc-visiting-team')]").text
    game_info["away_score"] = scores[0].text
    game_info["home_score"] = scores[1].text
    game_info["home_team"] = matchup_container.find_element_by_xpath("//*[contains(@class,'ht-gc-home-team')]").text

    #Gets season based on date.  Assumes season will always end before September 1 
    game_date = datetime.strptime(game_info["date"],"%B %d, %Y")
    game_info["season"] = game_info["season"] + str(int(game_info["season"])+1) if game_date.month > 8 else str(int(game_info["season"])-1) + game_info["season"]

    #add arena to returned dict
    arena = arena_data(driver)
    game_data = {**game_info, **arena}

    global home_team, away_team ####Delete at end
    home_team = game_info["home_team"]####Delete at end
    away_team = game_info["away_team"]####Delete at end

    #update class instance 'game'
    game.home_team = game_info["home_team"]
    game.away_team = game_info["away_team"]

    #return dict
    return game_data

def arena_data(driver):
    #declarations
    arena_data = dict()

    #get elements
    summary = get_summary(driver)

    #add scrapings to dict
    arena_data["venue"] = summary.find_element_by_xpath("//td[contains(@ng-bind,'gameSummary.details.venue')]").text
    arena_data["attendance"] = summary.find_element_by_xpath("//td[contains(@ng-bind,'gameSummary.details.attendance')]").text
    arena_data["start_time"] = summary.find_element_by_xpath("//td[contains(@ng-bind,'gameSummary.details.startTime')]").text
    arena_data["end_time"] = summary.find_element_by_xpath("//td[contains(@ng-bind,'gameSummary.details.endTime')]").text
    arena_data["duration"] = summary.find_element_by_xpath("//td[contains(@ng-bind,'gameSummary.details.duration')]").text

    #return
    return arena_data

def referee_data(driver):
    #declarations
    game_officials = []
    officials = []

    #get elements
    summary = get_summary(driver)
    officials = summary.find_elements_by_xpath("//tr[contains(@ng-repeat,'gameSummary.referees') or contains(@ng-repeat,'gameSummary.linesmen')]")

    #loop through officials and add scrapings to dict
    for official in officials:
        officials_dict = {"game_id": game.game_id}
        official_data = official.find_elements_by_xpath("td")
        officials_dict["role"] = official_data[0].text
        officials_dict["name"] = official_data[1].find_element_by_xpath("span[contains(@ng-show,'hide_official_names')]").text
        officials_dict["number"] = official_data[1].find_element_by_xpath("span[contains(@ng-show,'jerseyNumber')]/span").text
        game_officials.append(officials_dict)

    #return array of dicts
    return game_officials

def boxscore(driver):
    #declarations
    goal_periods = []
    shot_periods = []
    away_goals = []
    away_shots = []
    home_goals = []
    home_shots = []
    goal_summary = dict()
    shot_summary = dict()
    scoring_summary = dict()

    #scrape elements
    summary = get_summary(driver)
    goal_periods = summary.find_elements_by_xpath("//tr/th[contains(@ng-repeat,'scoreSummaryHeadings')]") #Goals by Period (last period is total)
    shot_periods = summary.find_elements_by_xpath("//tr/th[contains(@ng-repeat,'shotSummaryHeadings')]") #Shots by Period (last period is total)

    away_goals = summary.find_elements_by_xpath("//tr/td[contains(@ng-repeat,'visitingScoreSummary')]")
    away_shots = summary.find_elements_by_xpath("//tr/td[contains(@ng-repeat,'visitingShotSummary')]")

    home_goals = summary.find_elements_by_xpath("//tr/td[contains(@ng-repeat,'homeScoreSummary')]")
    home_shots = summary.find_elements_by_xpath("//tr/td[contains(@ng-repeat,'homeShotSummary')]")

    #dump scrapings into dicts
    for period, agoals, hgoals in zip(goal_periods, away_goals, home_goals):
        goal_summary[period.text] = {"game_id": game.game_id, "away_goals": agoals.text, "home_goals": hgoals.text}

    for period, ashots, hshots in zip(shot_periods, away_shots, home_shots):
        shot_summary[period.text] = {"game_id": game.game_id, "home_shots": hshots.text, "away_shots": ashots.text}

    for summary in goal_summary:
        scoring_summary[summary] = goal_summary[summary]
        try:
            scoring_summary[summary].update(shot_summary[summary]) #if nothing to update, shootout with no shot data
        except:
            scoring_summary[summary].update({"home_shots": 0, "away_shots": 0}) #insert shot data for shootout

    #return array of dicts
    return scoring_summary

def penalty_summary(driver):
    #declarations
    penalty_summary = []
    away_pp = []
    away_penalties = []
    home_pp = []
    home_penalties = []

    #get elements
    summary = get_summary(driver)
    away_pp = summary.find_element_by_xpath("//tr/td/span[contains(@ng-bind,'gameSummary.visitingTeam.stats.powerPlayGoals')]").text.replace(" ","").split("/",1) #get away PP fraction string and split
    home_pp = summary.find_element_by_xpath("//tr/td/span[contains(@ng-bind,'gameSummary.homeTeam.stats.powerPlayGoals')]").text.replace(" ","").split("/",1) #get home PP fraction string and split
    away_penalties = summary.find_element_by_xpath("//tr/td/span[contains(@ng-bind,'gameSummary.visitingTeam.stats.penaltyMinuteCount')]").text.split(" min / ",1) #get away PP fraction string and split
    home_penalties = summary.find_element_by_xpath("//tr/td/span[contains(@ng-bind,'gameSummary.homeTeam.stats.penaltyMinuteCount')]").text.split(" min / ",1) #get home PP fraction string and split
    
    #build return array
    penalty_summary.append({"game_id": game.game_id, "team": game.away_team, "side": "away", "pp_goals": away_pp[0], "pp_opps": away_pp[1], "pims": away_penalties[0], "infracs": away_penalties[1].split(" ",1)[0]})
    penalty_summary.append({"game_id": game.game_id, "team": game.home_team, "side": "home", "pp_goals": home_pp[0], "pp_opps": home_pp[1], "pims": home_penalties[0], "infracs": home_penalties[1].split(" ",1)[0]})

    #return array of dicts
    return penalty_summary

def three_stars(driver):
    #declarations
    stars = []
    star_containers = []

    #get elements
    summary = get_summary(driver)
    star_containers = summary.find_elements_by_xpath("//div[@class='ht-three-stars']/div/div[@class='ht-star-container']")

    #dump scrapings into dict, add dict to array
    for star in star_containers:
        star_number = star.find_element_by_xpath("div[@class='ht-star-number']").text
        star_rawname = star.find_element_by_xpath("div[@class='ht-star-name']").text.split(" (#")
        star_name = star_rawname[0]
        star_jersey = star_rawname[1].replace(")","")
        star_team = star.find_element_by_xpath("div[@class='ht-star-team']").text
        star_side = "away" if star_team == game.away_team else "home"
        stars.append({"game_id": game.game_id, "team": star_team, "side": star_side, "star_number": star_number, "name": star_name, "jersey_number": star_jersey})
    
    #return array of dicts
    return stars

def coaches(driver):
    #declarations
    coaches = []
    away_coach_lines = []
    home_coach_lines = []


    #get elements
    summary = get_summary(driver)
    away_coach_lines = summary.find_elements_by_xpath("//div[@ng-class='sumTableHalfLeft']//tr[contains(@ng-repeat,'visitingTeam.coaches')]")
    home_coach_lines = summary.find_elements_by_xpath("//div[@ng-class='sumTableHalfRight']//tr[contains(@ng-repeat,'homeTeam.coaches')]")

    #dump scrapings into dict, append to array
    for line in away_coach_lines:
        coach_role = line.text.split(": ")[0]
        coach_name = line.text.split(": ")[1]
        coaches.append({"game_id": game.game_id, "team": game.away_team, "side": "away", "role": coach_role, "name": coach_name})

    for line in home_coach_lines:
        coach_role = line.text.split(": ")[0]
        coach_name = line.text.split(": ")[1]
        coaches.append({"game_id": game.game_id, "team": game.home_team, "side": "home", "role": coach_role, "name": coach_name})

    #return dict of arrays
    return coaches

def player_scorelines(driver):
    #declarations
    players = []
    away_player_lines = []
    home_player_lines = []
    
    #get elements
    summary = get_summary(driver)
    away_player_lines = summary.find_elements_by_xpath("//div[@ng-class='sumTableHalfLeft']/div[@ng-class='sumTableMobile']//tr[contains(@ng-repeat,'visitingTeam.skaters')]") #find_elements_by_xpath("//div[@ng-class='sumTableHalfLeft']//tr[contains(@ng-repeat,'visitingTeam.coaches')]")
    home_player_lines = summary.find_elements_by_xpath("//div[@ng-class='sumTableHalfRight']/div[@ng-class='sumTableMobile']//tr[contains(@ng-repeat,'homeTeam.skaters')]")

    #dump player data into dict, append to player array
    for line in away_player_lines:
        players.append(get_scoreline(line, "away"))

    for line in home_player_lines:
        players.append(get_scoreline(line, "home"))

    #return array of dicts
    return players

def pbp(driver):   ###COMPLETE
    #declarations
    pbp_periods, pbp_events, pbp_arr = [], [], []
    pbp_assists, pbp_assist_line = [], []
    plus_minus_tables, pbp_plus_players, pbp_minus_players, plus_minus_rows = [], [], [], []
    goals, shots, onice_events, penalties, goalie_changes = [], [], [], [], []
    pbp_id = 0
    # shot = Shot(game,)

    #get elements
    pbp_periods = driver.find_elements_by_xpath("//div[@ng-repeat='gamePBP in PlayByPlayPeriodBreakdown track by $index']")
    
    #loop through each period
    for period in pbp_periods:
        period_number = period.get_attribute('ng-show').split("ht_")[1]
        period_name = period.find_element_by_xpath("div[@ng-bind='gamePBP.longName']").text

        #get event elements
        pbp_events = period.find_elements_by_xpath("div[contains(@ng-show,'ht_')]")

        #loop through events in period
        for event in pbp_events:
            #increment id
            pbp_id += 1

            #get elements
            pbp_event_row = event.find_element_by_xpath("div[contains(@class,'ht-event-row')]")
            pbp_side = "away" if pbp_event_row.find_element_by_xpath("div[@class='ht-home-or-visit']/div").get_attribute('class').split("team")[0].split("ht-")[1] == "visit" else "home"
            pbp_team = pbp_event_row.find_element_by_xpath("div[@class='ht-event-image']/img").get_attribute('title')
            pbp_event_time = pbp_event_row.find_element_by_xpath("div[@class='ht-event-time']").text

            # Pull Event Details
            pbp_event_details = pbp_event_row.find_element_by_xpath("div[@class='ht-event-details']")
            pbp_event_type = pbp_event_details.find_element_by_xpath("div[contains(@class,'ht-event-type')]").text

            #define base attribute dict
            base_dict = {"game_id": game.game_id, "pbp_id": pbp_id, "team": pbp_team, "side": pbp_side, "period": period_number, "time": pbp_event_time}

            # Pull Shot Info
            if "SHOT" in pbp_event_type:
                #delcarations
                shot_dict = base_dict
                
                #assign scraped shot info
                shot_dict["event"] = pbp_event_type
                shot_dict["player_number"] = pbp_event_details.find_element_by_xpath("div/span[contains(@ng-bind,'shooter.jerseyNumber')]").text.replace("#", "")
                shot_dict["player_name"] = pbp_event_details.find_element_by_xpath("div/a/span[contains(@ng-bind,'shooter.lastName')]").text
                shot_dict["goalie_number"] = pbp_event_details.find_element_by_xpath("div/span[contains(@ng-bind,'goalie.jerseyNumber')]").text.replace("#", "")
                shot_dict["goalie_name"] = pbp_event_details.find_element_by_xpath("div/a/span[contains(@ng-bind,'goalie.lastName')]").text
                shot_dict["result"] = ""
                pbp_arr.append(shot_dict)#[pbp_shooter_number, pbp_shooter, pbp_goalie_number, pbp_goalie, period_number, pbp_event_time, ""])

                try:
                    #if shot event resulted in a goal, add line to pbp_array as goal
                    shot_dict["result"] = pbp_event_details.find_element_by_xpath("div/span[@ng-if='pbp.details.isGoal']").text

                    pbp_arr.append(shot_dict)

                except:
                    pass

                shots.append(shot_dict)
                print(f'{shot_dict["event"]} | {shot_dict["side"]} | {shot_dict["team"]} | {shot_dict["event"]} by #{shot_dict["player_number"]} {shot_dict["player_name"]} on #{shot_dict["goalie_number"]} {shot_dict["goalie_name"]} at {shot_dict["time"]} {shot_dict["period"]}')

            # Pull Goal Info
            elif "GOAL" in pbp_event_type:
                #declarations
                pbp_goal_types = []
                pbp_goal_type = ""
                goal_dict = base_dict

                #get elements
                pbp_goal_types = pbp_event_details.find_elements_by_xpath("div/span[contains(@ng-if,'pbp.details.properties')]")

                #assign scraped goal info
                goal_dict["event"] = pbp_event_type
                goal_dict["player_number"] = pbp_event_details.find_element_by_xpath("div/span[contains(@ng-bind,'scoredBy.jerseyNumber')]").text.replace("#", "")
                goal_dict["player_name"] = pbp_event_details.find_element_by_xpath("div/a[contains(@ng-bind,'scoredBy.lastName')]").text
                goal_dict["season_total"] = pbp_event_details.find_element_by_xpath("div/span[contains(@ng-bind,'pbp.details.scorerGoalNumber')]").text.replace("(", "").replace(")", "")

                #search for and add any special goal-type tags
                if(len(pbp_goal_types)) != 0:
                    for goal_type in pbp_goal_types:
                        if goal_type.text == "GAME WINNING":
                            goal_dict["gwg"] = True
                        elif goal_type.text == "POWERPLAY":
                            goal_dict["ppg"] = True
                        elif goal_type.text == "SHORT HANDED":
                            goal_dict["shg"] = True
                        elif goal_type.text == "EMPTY NET":
                            goal_dict["eng"] = True
                        elif goal_type.text == "INSURANCE GOAL":
                            goal_dict["insurance"] = True
                        elif goal_type.text == "PENALTY SHOT":
                            goal_dict["psg"] = True

                pbp_goal_str = f'\n {goal_dict["team"]} {goal_dict["event"]} by #{goal_dict["player_number"]} {goal_dict["player_name"]} ({goal_dict["season_total"]}) {pbp_goal_type} at {goal_dict["time"]} of the {goal_dict["period"]} period'

            # Pull Assist Info
                #get assist elements
                pbp_assists = pbp_event_details.find_elements_by_xpath("div/span[@ng-show='pbp.details.assists.length']/span[contains(@ng-repeat,'assist in pbp.details.assists')]")
                
                #find number of assists assigned to goal (hopefully fewer than three)
                pbp_assists_given = len(pbp_assists)

                if pbp_assists_given == 0:
                    pbp_goal_str = pbp_goal_str + ", unassisted"
                else:
                    pbp_goal_str = pbp_goal_str + ", assisted by:"
                    for j, assist in enumerate(pbp_assists):
                        goal_dict["assist" + str(j+1) + "_number"] = assist.find_element_by_xpath("span[contains(@ng-bind,'assist.jerseyNumber')]").text.replace("#", "")
                        goal_dict["assist" + str(j+1) + "_name"] = assist.find_element_by_xpath("a[contains(@ng-bind,'assist.lastName')]").text
                        goal_dict["assist" + str(j+1) + "_total"] = assist.text.split("(")[1].split(")")[0]
                        pbp_goal_str = pbp_goal_str + f'\n     #{goal_dict["assist" + str(j+1) + "_number"]} {goal_dict["assist" + str(j+1) + "_name"]} ({goal_dict["assist" + str(j+1) + "_total"]})'

                goals.append(goal_dict)

                print(pbp_goal_str + "\n")

            # Pull Plus-Minus Info

                #get button and click
                plus_minus_button = pbp_event_row.find_elements_by_xpath("div[@class='ht-event-time']/div/span[@ng-show='!pmbutton.expanded']")[0]
                plus_minus_button.click()

                #get elements
                plus_minus_tables = pbp_event_row.find_elements_by_xpath("div[@ng-show='pmbutton.expanded']/table")

                #loop through +/- tables (note: not actual plus/minus, just who is on ice for a goal)
                for table in plus_minus_tables:
                    onice_dict = base_dict
                    onice_dict["event"] = table.find_element_by_xpath("tbody/tr/th").text.lower()
                    if onice_dict["event"] == "plus":
                        onice_dict["plus_minus"] = 1
                        onice_dict["team"] = pbp_team
                        onice_dict["side"] = pbp_side
                    else:
                        onice_dict["plus_minus"] = -1
                        onice_dict["team"] = game.away_team if pbp_team == game.home_team else home_team
                        onice_dict["side"] = "away" if pbp_team == game.home_team else "home"

                    #get individual players via rows
                    plus_minus_rows = table.find_elements_by_xpath("tbody/tr[contains(@ng-repeat,'in pbp.details')]")

                    for row in plus_minus_rows:
                        #scrape individual player data
                        onice_dict["player_number"] = row.find_element_by_xpath("td/span[contains(@ng-bind,'.jerseyNumber')]").text.replace("#", "")
                        onice_dict["player_name"] = row.find_element_by_xpath("td/a[contains(@ng-bind,'.lastName')]").text

                        #add to return array
                        onice_events.append(onice_dict)
                        print(f'{onice_dict["plus_minus"]} | #{onice_dict["player_number"]} {onice_dict["player_name"]}')

            # Pull Penalty Info
            elif pbp_event_type == "PENALTY":
                #declaration
                penalty_dict = base_dict

                #scrape player/penalty info
                penalty_dict["event"] = pbp_event_type
                penalty_dict["player_number"] = pbp_event_details.find_element_by_xpath("div/span[contains(@ng-bind,'takenBy.jerseyNumber')]").text.replace("#", "")
                penalty_dict["player_name"] = pbp_event_details.find_element_by_xpath("div/a/span[contains(@ng-bind,'takenBy.lastName')]").text
                penalty_dict["penalty"] = pbp_event_details.find_element_by_xpath("div/span[@ng-bind='pbp.details.description']").text
                penalty_dict["pim"] = pbp_event_details.find_element_by_xpath("div/span[contains(@ng-bind,'pbp.details.minutes')]").text.split(" ")[0]
                
                #get manpower advantage indicator
                try:
                    penalty_dict["pp"] = pbp_event_details.find_element_by_xpath("div/span[@ng-if='pbp.details.isPowerPlay']").text
                except:
                    penalty_dict["pp"] = "ES"

                #append dict to return array
                penalties.append(penalty_dict)
                print(f'PENALTY | #{penalty_dict["player_number"]} {penalty_dict["player_name"]} | {penalty_dict["penalty"]} | {penalty_dict["pim"]} ({penalty_dict["pp"]}) at {penalty_dict["time"]} of {penalty_dict["period"]} period')

            # Pull Goalie Change Info
            elif pbp_event_type == "GOALIE CHANGE":
                #get elements
                goalies_changing = pbp_event_details.find_elements_by_xpath("div/section[contains(@ng-if,'pbp.details.goalie')]")
                
                #loop through all goalie change elements
                for goalie in goalies_changing:
                    #declaration
                    goalie_dict = base_dict

                    #scrape goalie change info
                    goalie_dict["event"] = pbp_event_type
                    goalie_dict["goalie_number"] = goalie.find_element_by_xpath("span[contains(@ng-bind,'jerseyNumber')]").text.replace("#", "").replace("- ", "")
                    goalie_dict["goalie_name"] = goalie.find_element_by_xpath("a/span[contains(@ng-bind,'lastName')]").text
                    goalie_dict["action"] = goalie.find_element_by_xpath("span[@class='ng-binding' and not(contains(@ng-bind,'jerseyNumber'))]").text
                    goalie_dict["time"] = pbp_event_time
                    goalie_dict["period"] = period_name

                    #append dict to return array
                    goalie_changes.append(goalie_dict)
                    print(f'GOALIE CHANGE | {pbp_side} #{goalie_dict["goalie_number"]} {goalie_dict["goalie_name"]} {goalie_dict["action"]} at {pbp_event_time}, {period_name} period.')

            elif pbp_event_type == " ":  # in shootout
                #declaration
                shootout_attempts = []

                so_shooter_number = pbp_event_details.find_element_by_xpath("div/span[contains(@ng-bind,'shooter.jerseyNumber')]").text.replace("#", "")
                so_shooter_name = pbp_event_details.find_element_by_xpath("div/a/span[contains(@ng-bind,'shooter.lastName')]").text
                # so_shooter_team = pbp_event_details.find_element_by_xpath("div/span[contains(@ng-bind,'shooter.jerseyNumber')]").text.replace("#","")

                so_goalie_number = pbp_event_details.find_element_by_xpath("div/span[contains(@ng-bind,'goalie.jerseyNumber')]").text.replace("#", "")
                so_goalie_name = pbp_event_details.find_element_by_xpath("div/a/span[contains(@ng-bind,'goalie.lastName')]").text
                # so_goalie_team = pbp_event_details.find_element_by_xpath("div/span[contains(@ng-bind,'shooter.jerseyNumber')]").text.replace("#","")

                # results
                shootout_attempts = pbp_event_details.find_elements_by_xpath("div/span[contains(@class,'ht-gc-marker')]")
                attempt_result = ""

                if(len(shootout_attempts)) != 0:
                    for result in shootout_attempts:
                        attempt_result = attempt_result + "[" + result.text + "] "

                print(f"SO ATTEMPT | {pbp_team} #{so_shooter_number} {so_shooter_name} shootout attempt on #{so_goalie_number} {so_goalie_name}:   {attempt_result}")

            else:
                print(f"EVENT NOT ACCOUNTED FOR: {pbp_event_type}")


    print("==========")


    # pins = get_pins(driver, pbp_arr)

    pins = []


    
    # for element in pbp_arr:
    #     print(element)

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

            # print(f"{pbp_side} | {pbp_team} | {pbp_event_type} by #{pbp_shooter_number} {pbp_shooter} ({pbp_goal_count}) at {pbp_event_time} from ")
    return goals, shots, goalie_changes, penalties, onice_events, pins

def get_pins(driver, pbp_arr):   ###COMPLETE
    pins = []
    rink = driver.find_element_by_xpath("//div[@id='ht-icerink']")
    found_pins = rink.find_elements_by_xpath("div[contains(@id,'ht_pin_')]")
    i = 1

    # goal_dict = {"game_id": game_id, "event": pbp_event_type, "team": pbp_team, "time": pbp_event_time, "period": period_name}

    if len(found_pins) == len(pbp_arr):
        print("Arrays are equal")

    for pin, data in zip(found_pins, pbp_arr):
        pin_dict = {"game_id": game_id, "team": "FUCK", "time": data[5], "period": data[4]}
        pin_dict["event_id"] = 1 ####TBD
        pin_dict["pin_id"] = pin.get_attribute("id").split("ht_pin_")[1] #get index
        pin_dict["result"] = pin.text

        #player info
        pin_dict["player_number"] = data[0]
        pin_dict["player_name"] = data[1]
        pin_dict["goalie_number"] = data[2]
        pin_dict["goalie_name"] = data[3]

        #pin locations
        event_loc = pin.get_attribute("style")
        pin_dict["top_position"] = pin.get_attribute("style").split("%; left: ")[0].split("top:")[1]
        pin_dict["left_position"] = pin.get_attribute("style").split("%; left: ")[1].split("%;")[0]

        print(f'#{pin_dict["pin_id"]} (id={pin_dict["pin_id"]}) | {pin.get_attribute("id")} @ top: {pin_dict["top_position"]}, left: {pin_dict["left_position"]} | {data[0]} {data[1]} on {data[2]} {data[3]} at {data[5]} of Period {data[4]} ({pin_dict["result"]})')

        pins.append(pin_dict)
    
    return pins

def preview_stats(driver):
    #declarations
    tables = []
    head2head_statlines, h2h_rows, h2h_stats = [], [], [] #h2h
    previous_meeting_rows, previous_meetings = [], [] #previous meetings
    top_scorer_tables, top_scorer_rows, top_scorers = [], [], [] #top scorers
    recent_game_tables, recent_games = [], [] #recent games
    matchup_statlines = [] #matchup stats
    
    #get elements
    tables = driver.find_elements_by_xpath("//div[@ng-if='PreviewDataLoaded']/div/div[contains(@ng-class,'sumTableHalf')]/div[@ng-class='sumTableMobile']/table/tbody")
    h2h_rows = tables[0].find_elements_by_xpath("tr") #h2h
    previous_meeting_rows = tables[1].find_elements_by_xpath("tr[@class='ng-scope']") #previous meetings
    top_scorer_tables = tables[2].find_elements_by_xpath("//table[@class='ht-table-data']/tbody") #top scorers
    recent_game_tables = tables[3].find_elements_by_xpath("//td[@class='ht-table-last-5']") #recent games
    matchup_table = driver.find_element_by_xpath("//div[@ng-if='PreviewDataLoaded']/div[@ng-class='sumTableContainter']/div[@ng-class='sumTableMobile']//tbody") #matchup stats

    ##### h2h #####
    #get head-to-head stats
    h2h_away = {"game_id": game.game_id, "team": game.away_team, "versus": game.home_team}
    h2h_home = {"game_id": game.game_id, "team": game.home_team, "versus": game.away_team}

    h2h_away[h2h_rows[0].text.lower().replace(" ","_")] = h2h_rows[1].find_elements_by_xpath("td")[1].text #previous season
    h2h_home[h2h_rows[0].text.lower().replace(" ","_")] = h2h_rows[1].find_elements_by_xpath("td")[3].text

    h2h_away[h2h_rows[2].text.lower().replace(" ","_")] = h2h_rows[3].find_elements_by_xpath("td")[1].text #current season
    h2h_home[h2h_rows[2].text.lower().replace(" ","_")] = h2h_rows[3].find_elements_by_xpath("td")[3].text

    h2h_away[h2h_rows[4].text.lower().replace(" ","_")] = h2h_rows[5].find_elements_by_xpath("td")[1].text #last 5 seasons
    h2h_home[h2h_rows[4].text.lower().replace(" ","_")] = h2h_rows[5].find_elements_by_xpath("td")[3].text

    #append h2h stats to array
    head2head_statlines.append(h2h_away)
    head2head_statlines.append(h2h_home)
    ##### /h2h #####

    ##### previous meetings #####
    #get previous meetings
    for row in previous_meeting_rows:
        td = row.find_elements_by_xpath("td")

        previous_away_team = td[0].find_element_by_xpath("a/img").get_attribute("title")
        score = td[1].text.split(":")
        away_score = score[0]
        previous_home_team = td[2].find_element_by_xpath("a/img").get_attribute("title")
        home_score = score[1]
        date = td[3].text
        previous_meetings.append({"game_id": game.game_id, "away_team": previous_away_team, "away_score": away_score, "home_team": previous_home_team, "home_score": home_score, "date": date})
    ##### /previous meetings #####
    
    ##### top scorers #####
    #get top scorers coming into game
    team = game.away_team
    for table in top_scorer_tables:
        top_scorer_rows = table.find_elements_by_xpath("tr")

        for row in top_scorer_rows:
            top_details = []
            top_details = row.find_elements_by_xpath("td/a/div[@class='ht-top-details']/div")
            top_scorer = dict()
            top_scorer["game_id"] = game.game_id
            top_scorer["team"] = team
            top_scorer["side"] = "away" if team == game.away_team else "home"
            top_scorer["player"] = top_details[0].text
            top_scorer["statline"] = top_details[1].text
            top_scorers.append(top_scorer)   
        team = home_team
    ##### /top scorers #####

    ##### recent games #####
    #scrape recent games
    for row in recent_game_tables[0].find_elements_by_xpath("//tr[contains(@ng-repeat,'last5games in ::gameCP.visitingTeam')]/td"):
        recent_games.append({"game_id": game.game_id, "team": game.away_team, "side": "away", "game_info": row.text})

    for row in recent_game_tables[0].find_elements_by_xpath("//tr[contains(@ng-repeat,'last5games in ::gameCP.homeTeam')]/td"):
        recent_games.append({"game_id": game.game_id, "team": game.home_team, "side": "home", "game_info": row.text})
    ##### /recent games #####

    ##### matchup stats #####
    #scrape Matchup Stats
    matchup_away = {"game_id": game.game_id, "team": game.away_team, "side": "away"}
    matchup_home = {"game_id": game.game_id, "team": game.home_team, "side": "home"}
    
    for row in matchup_table.find_elements_by_xpath("tr"):
        tds = []
        tds = row.find_elements_by_xpath("td")
        
        matchup_away[tds[0].text.lower().replace(" ","_").replace("(","").replace(")","")] = tds[1].text
        matchup_home[tds[0].text.lower().replace(" ","_").replace("(","").replace(")","")] = tds[2].text
    
    #append dicts
    matchup_statlines.append(matchup_away)
    matchup_statlines.append(matchup_home)
    ##### /matchup stats #####

    ###Return Data
    return top_scorers, recent_games, matchup_statlines, head2head_statlines, previous_meetings

def nothing():

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
game = Game()
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

# dr = get_driver(1020540)

# pbp(dr)

if __name__ == "__main__":
    # g = Game(101, "Toronto","Utica")
    # e = Event(g, "Hello")
    # print(repr(e))
    drive = get_driver(1020531)
    pbp(drive)
    # print(*game_data)
