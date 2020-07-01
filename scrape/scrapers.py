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