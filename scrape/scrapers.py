from datetime import datetime
from func import get_summary

#extract game data
def game_data(game_id, driver):
    
    def get_game_data(matchup_container):
        #declarations
        game_info = dict()
        arena = dict()
        game_data = []
        
        #get various elements
        scores = matchup_container.find_elements_by_xpath("//div[@class='ht-gc-score-container']")
        date = matchup_container.find_element_by_xpath("//*[contains(@class,'ht-game-date')]").text.split(", ", 1)

        #add scraping to dict
        game_info["game_id"] = game_id
        game_info["game_number"] = matchup_container.find_element_by_xpath("//*[@class='ht-game-number']").text.split("#: ")[1]
        
        #establish date
        game_info["date"] = date[1]
        game_date = datetime.strptime(game_info["date"],"%B %d, %Y")

        game_info["dow"] = date[0]
        game_info["status"] = matchup_container.find_element_by_xpath("//*[contains(@ng-bind,'gameSummary.details.status')]").text
        game_info["away_team"] = matchup_container.find_element_by_xpath("//*[contains(@class,'ht-gc-visiting-team')]").text
        game_info["away_score"] = scores[0].text
        game_info["home_score"] = scores[1].text
        game_info["home_team"] = matchup_container.find_element_by_xpath("//*[contains(@class,'ht-gc-home-team')]").text

        #Gets game_type
        if game_date.month == 9:
            game_info["game_type"] = "Pre-Season"
        elif 4 <= game_date.month <= 7:
            if int(game_info["game_number"]) <= 7:
                game_info["game_type"] = "Playoff"
        elif "All-Star" in game_info["home_team"] or "All-Star" in game_info["away_team"]:
            game_info["game_type"] = "All-Star"
        else:
            game_info["game_type"] = "Regular"

        #Gets season based on date.  Assumes season will always end before September 1
        game_info["season"] = game_info["date"].split(",")[1].strip()
        game_info["season"] = game_info["season"] + str(int(game_info["season"])+1) if game_date.month > 8 else str(int(game_info["season"])-1) + game_info["season"]
        
        #add arena to game_info dict
        arena = arena_data(driver)
        game_info.update(arena)

        #append all game data to return array
        game_data.append(game_info)

        #return array
        return game_data

    try:
        container = driver.find_element_by_xpath("//div[@class='ht-gc-header-row']")
        return get_game_data(container)
    except:
        raise ValueError('Cannot find game data')

#extract arena data
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

#get referee data
def referee_data(game, driver):
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

def boxscore(game, driver):
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

#get penalty summary
def penalty_summary(game, driver):
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
    penalty_summary.append({"game_id": game.game_id, "team": game.teams["away"], "side": "away", "pp_goals": away_pp[0], "pp_opps": away_pp[1], "pims": away_penalties[0], "infracs": away_penalties[1].split(" ",1)[0]})
    penalty_summary.append({"game_id": game.game_id, "team": game.teams["home"], "side": "home", "pp_goals": home_pp[0], "pp_opps": home_pp[1], "pims": home_penalties[0], "infracs": home_penalties[1].split(" ",1)[0]})

    #return array of dicts
    return penalty_summary

#get three stars
def three_stars(game, driver):
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
        star_side = "away" if star_team == game.teams["away"] else game.teams["home"]
        stars.append({"game_id": game.game_id, "team": star_team, "side": star_side, "star_number": star_number, "name": star_name, "jersey_number": star_jersey})
    
    #return array of dicts
    return stars

#get coaches
def coaches(game, driver):
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
        coaches.append({"game_id": game.game_id, "team": game.teams["away"], "side": "away", "role": coach_role, "name": coach_name})

    for line in home_coach_lines:
        coach_role = line.text.split(": ")[0]
        coach_name = line.text.split(": ")[1]
        coaches.append({"game_id": game.game_id, "team": game.teams["home"], "side": "home", "role": coach_role, "name": coach_name})

    #return dict of arrays
    return coaches

def player_scorelines(game, driver):
    
    def get_scoreline(line, side):
        #declarations
        player = dict()

        #get elements
        td = line.find_elements_by_xpath("td")

        #dump scrapings into dict
        player["game_id"] = game.game_id
        player["team"] = game.teams[side] #getattr(game, str(side + "_team"))
        player["side"] = side
        player["opponent"] = game.teams["away"] if side == game.teams["home"] else game.teams["home"]
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

#get previous stats for current matchup
def preview_stats(game, driver):
    #declarations
    tables = []
    head2head_statlines, h2h_rows = [], [] # h2h_stats = [] #h2h
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

    #get head-to-head stats
    h2h_away = {"game_id": game.game_id, "team": game.teams["away"], "versus": game.teams["home"]}
    h2h_home = {"game_id": game.game_id, "team": game.teams["home"], "versus": game.teams["away"]}

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
    
    #get top scorers coming into game
    team = game.teams["away"]
    for table in top_scorer_tables:
        top_scorer_rows = table.find_elements_by_xpath("tr")

        for row in top_scorer_rows:
            top_details = []
            top_details = row.find_elements_by_xpath("td/a/div[@class='ht-top-details']/div")
            top_scorer = dict()
            top_scorer["game_id"] = game.game_id
            top_scorer["team"] = team
            top_scorer["side"] = "away" if team == game.teams["away"] else "home"
            top_scorer["player"] = top_details[0].text
            top_scorer["statline"] = top_details[1].text
            top_scorers.append(top_scorer)   
        team = game.teams["home"]
    ##### /top scorers #####

    #scrape recent games
    for row in recent_game_tables[0].find_elements_by_xpath("//tr[contains(@ng-repeat,'last5games in ::gameCP.visitingTeam')]/td"):
        recent_games.append({"game_id": game.game_id, "team": game.teams["away"], "side": "away", "game_info": row.text})

    for row in recent_game_tables[0].find_elements_by_xpath("//tr[contains(@ng-repeat,'last5games in ::gameCP.homeTeam')]/td"):
        recent_games.append({"game_id": game.game_id, "team": game.teams["home"], "side": "home", "game_info": row.text})
    ##### /recent games #####

    #scrape Matchup Stats
    matchup_away = {"game_id": game.game_id, "team": game.teams["away"], "side": "away"}
    matchup_home = {"game_id": game.game_id, "team": game.teams["home"], "side": "home"}
    
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