goal_periods = ["1", "2", "3", "OT", "SO", "T"]
# goal_periods = summary.find_elements_by_xpath("//tr/th[contains(@ng-repeat,'scoreSummaryHeadings')]")

#Periods (last period is total)
shot_periods = ["1", "2", "3", "OT", "SO", "T"]
# shot_periods = summary.find_elements_by_xpath("//tr/th[contains(@ng-repeat,'shotSummaryHeadings')]")

#Away Stats#
away_goals = [1,2,3,4,5,6]
away_shots = [1,2,3,4,5]

#Home Stats#
home_goals = [6,5,4,3,2,1]
home_shots = [5,4,3,2,1]
# home_goals = summary.find_elements_by_xpath("//tr/td[contains(@ng-repeat,'homeScoreSummary')]")
# home_shots = summary.find_elements_by_xpath("//tr/td[contains(@ng-repeat,'homeShotSummary')]")

goal_summary = dict()
shot_summary = dict()

goals = zip(goal_periods, home_goals, away_goals)

for period, hgoals, agoals in zip(goal_periods, home_goals, away_goals):
    goal_summary[period] = {"home_goals": hgoals, "away_goals": agoals}

for period, hshots, ashots in zip(shot_periods, home_shots, away_shots):
    shot_summary[period] = {"home_shots": hshots, "away_shots": ashots}
# new_thing = zip(goal_periods, goal_totals)

summarys = dict()

for summary in goal_summary:
    # # print(summary)
    summarys[summary] = goal_summary[summary]
    try:
        summarys[summary].update(shot_summary[summary])
    except:
        summarys[summary].update({"home_shots": 0, "away_shots": 0})
    # print(goal_summary[summary])

print(summarys)