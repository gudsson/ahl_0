from datetime import datetime, timedelta
from funcs import per_overflow
import constants as C

#define game state
class GameStates(object):
    def __init__(self, manpower = {"home": 5, "away": 5}):
        self._manpower = manpower
        self._active_penalties = { "home": [], "away": [] }
        self._state_certainty = True

    @property
    def manpower(self):
        return self._manpower

    @manpower.setter
    def manpower(self, value):
        self._manpower = value

    @property
    def active_penalties(self):
        return self._active_penalties

    def add_penalty(self, value):
        # print(value)
        #print(f"active {value['team']} penalties before penalty: {len(self._active_penalties[value['team']])}")
        # self.overtime_reduction(value)
        # period_multiplier = -1 if (value["period_taken"] == 4 and value['game_type'] != 'Playoff') else 1 #if non-playoff OT
        # If I'm in overtime and the team that DIDN'T take the penalty has fewer than 5 guys on the ice, check active penalties and add a guy
        if (value["period"] == 4 and value['game_type'] != 'Playoff'):
            opponent = "away" if value["team"] == "home" else "home"
            # print("OT id'd")

            # check active penalties to see if you can reduce before adding penalty
            # self.overtime_reduction(value) #eventually move this to event check - > OT

            # if team penalty was taken against has room, add skater
            if self._manpower[opponent] < 5:
                self._manpower[opponent] += 1
            else:
                value = self.queue_penalty(value)

        elif len(self._active_penalties[value['team']]) >= 2: # if the team penalized already has the max number of penalties
            value = self.queue_penalty(value)
        else:
            self._manpower[value['team']] -= 1

        value['expires_at'] = datetime.strptime(value['time'], C.FMT) + timedelta(minutes=value['pim']) #'dt.strptime('2:00', C.FMT)
        value['expires_at'], value['period_expires'] = per_overflow(value['expires_at'], value['period']) #check if overflows to next period
       
        self._active_penalties[value['team']].append(value) #add penalty to team array

        # check active penalties to see if you can reduce before adding penalty
        # self.overtime_reduction(value)

        for team in self._active_penalties:
            print(f"active {team} penalties after penalty:")
            for penalty in self._active_penalties[team]:
                print(f"     #{penalty['player_number']}: expires at {penalty['expires_at']} of period {penalty['period_expires']}")#{}{len(self._active_penalties[value['team']])}")
        print(f'current manpower: {self._manpower}')
        print("=====")
        return
    # def overtime_reduction(self):
    #     pass

    def queue_penalty(self, value):
        penalty_number = len(self._active_penalties[value['team']])
        penalty_to_follow = penalty_number - 2
        value['expires_at'] = datetime.strptime(self._active_penalties[value['team']][penalty_to_follow]['expires_at'], C.FMT) + timedelta(minutes=value['pim'])
        return value

    def overtime_reduction(self, value):
        if (value["period"] == 4 and value['game_type'] != 'Playoff'):
            if self._manpower["home"] == self._manpower["away"]: #if even strength, go to 3v3
                self._manpower["home"] = 3
                self._manpower["away"] = 3
            elif max(self._manpower.values()) == 5 and min(self._manpower.values()) == 4: #if 5 on 4, go down to 4 on 3
                self._manpower[max(self._manpower, key=self._manpower.get)] = 4
                self._manpower[min(self._manpower, key=self._manpower.get)] = 3
            print(f'now after OT reduction: {self._manpower}')
        return


    def clear_expired(self, value):

        penalty_ended = False

        for team in self._active_penalties:
            
            for penalty in self._active_penalties[team][:]:
               
                if (penalty['period_expires'] < value['period']) or ((penalty['period_expires'] == value['period']) and (datetime.strptime(penalty['expires_at'], C.FMT) <= datetime.strptime(value['time'], C.FMT))):
                    # print(f"penalty[expires_at]: {penalty['expires_at']}")
                    # print(f"value[time]: {value['time']}")
                    # print(penalty['expires_at'] <= value['time'])

                    penalty_ended = True

                    if len(self._active_penalties[team]) <= 2:
                        self._manpower[team] += 1

                    self._active_penalties[team].remove(penalty)

        return penalty_ended

    def event_check(self, value):
        # get teams
        team = value['team']
        opponent = 'away' if value['team'] == 'home' else 'home'

        #introduce state certainty at some point

        # first, clear penalties on both teams that expired prior to the event
        # print(f'penalties before clear: {team} = {len(self._active_penalties[value[team]])} | {opponent} = {len(self._active_penalties[value[opponent]])}')
        penalty_cleared = self.clear_expired(value)
        print(penalty_cleared)
        # print(f'penalties after clear: {team} = {len(self._active_penalties[value[team]])} | {opponent} = {len(self._active_penalties[value[opponent]])}')

        #if event is a penalty, add to updated penalty array
        if value['event'] == "PENALTY":
            self.add_penalty(value) #add penalty already reduces manpower
        


        #####IF REGULAR SEASON
        # if in overtime, shots don't have known game state if penalties needed to be cleared
        if value["period"] == 4: #if in overtime
            if int(max(self._manpower.values())) > 3: #and not 3v3
                if value['event'] == "SHOT" or value['event'] == "GOALIE CHANGE": #non-guaranteed stoppage, and non-3v3 game_states are now uncertain
                    self._state_certainty = False
                else: #else stoppage, apply overtime reduction and state is again known with certainty
                    self.overtime_reduction(value)
                    self._state_certainty = True
        else: #now what?
            pass



        # If period start and overtime, call overtime reduction
        #

        # game state event occurred at:
        print(f'event occurred at {self._manpower}, state certainty = {self._state_certainty}')

        # if in overtime, shots don't have known game state if penalties needed to be cleared
        if value["period"] == 4: #if in overtime
            if int(max(self._manpower.values())) > 3: #and not 3v3
                if value['event'] == "SHOT": #if event is a shot, no stoppage, and non-3v3 game_states are now uncertain
                    self._state_certainty = False
                else: #else stoppage, apply overtime reduction and state is again known with certainty
                    self.overtime_reduction(value)
                    self._state_certainty = True

        # if goal
        #   a) game state can be cross-checked with +/-


        # return game state
        print(f'event occurred at {self._manpower}')

        #
        #
        #
        #
        #
        #
        #still have to do for overtime!!!!!
        # Next, if goal, wipe out opponent's next penalty (if it exists)
        if value['event'] == 'GOAL' and (self._manpower[team] > self._manpower[opponent]):
            print(f'goal scored at {self._manpower}')
            self._active_penalties[opponent].pop(0) if self._active_penalties[opponent] else None 
            if len(self._active_penalties[opponent]) < 2:
                self._manpower[opponent] += 1
            else: # Go through queue and move up penalties if need be

                # deal with first queued penalty
                self._active_penalties[opponent][1]['expires_at'] = datetime.strptime(value['time'], C.FMT) + timedelta(minutes=self._active_penalties[opponent][1]['pim'])
                self._active_penalties[opponent][1]['expires_at'], self._active_penalties[opponent][1]['period_expires'] = per_overflow(self._active_penalties[opponent][1]['expires_at'], value['period'])

                ##### I don't think I have to move any others up, only one penalty is affected at a time
                # if len(self._active_penalties[opponent]) > 2: #if there are still queued penalties, loop through and reduce their expiry time
                #     for i in range(2, len(self._active_penalties[opponent])):
                #         penalty_number = i
                #         penalty_to_follow = penalty_number - 2
                #         self._active_penalties[opponent][i]['expires_at'], self._active_penalties[opponent][i]['period_expires'] = per_overflow(datetime.strptime(self._active_penalties[opponent][penalty_to_follow]['expires_at'], C.FMT) + timedelta(minutes=value['pim'])
            print(f'now {self._manpower}')
        return

if __name__ == "__main__":
    states = GameStates()
    states.event_check({ 'event': 'PENALTY', 'team': 'home', 'player_number': 27, 'pim': 2, 'time': '19:59', 'period': 3, 'game_type': 'Regular'})
    states.event_check({ 'event': 'PENALTY', 'team': 'home', 'player_number': 28, 'pim': 2, 'time': '00:01', 'period': 4, 'game_type': 'Regular'})
    states.event_check({ 'event': 'PENALTY', 'team': 'away', 'player_number': 29, 'pim': 2, 'time': '00:02', 'period': 4, 'game_type': 'Regular' })

    # print(states.manpower)
    # for team in states.active_penalties:
    #     for penalty in states.active_penalties[team]:
    #         print(penalty)
    states.event_check({ 'event': 'SHOT', 'team': 'away', 'time': '1:01', 'period': 4, 'game_type': 'Regular'})
    states.event_check({ 'event': 'GOAL', 'team': 'away', 'time': '1:02', 'period': 4, 'game_type': 'Regular'})
    states.event_check({ 'event': 'GOAL', 'team': 'away', 'time': '3:02', 'period': 4, 'game_type': 'Regular'}) 
    # for team in states.active_penalties:
    #     for penalty in states.active_penalties[team]:
    #         print(penalty)
