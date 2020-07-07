from datetime import datetime, timedelta
from funcs import per_overflow
import constants as C

#define game state
class GameStates(object):
    def __init__(self, manpower = {"home": 5, "away": 5}):
        self._manpower = manpower
        self._active_penalties = { "home": [], "away": [] }

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
        print(value)
        print(f"active {value['team']} penalties: {len(self._active_penalties[value['team']]) + 1}")
        # period_multiplier = -1 if (value["period_taken"] == 4 and value['game_type'] != 'Playoff') else 1 #if non-playoff OT
        # If I'm in overtime and the team that DIDN'T take the penalty has fewer than 5 guys on the ice, check active penalties and add a guy
        if (value["period_taken"] == 4 and value['game_type'] != 'Playoff'):
            opponent = "away" if value["team"] == "home" else "home"
           
            # check active penalties to see if you can reduce before adding penalty
            self.overtime_reduction()

            # if team penalty was taken against has room, add skater
            if self._manpower[opponent] < 5:
                self._manpower[opponent] += 1
            else:
                self.queue_penalty(value)
                return
        elif len(self._active_penalties[value['team']]) >= 2: # if the team penalized already has the max number of penalties
            self.queue_penalty(value)
            return
        self._manpower[value['team']] -= 1
        value['expires_at'] = datetime.strptime(value['taken_at'], C.FMT) + timedelta(minutes=value['pim']) #'dt.strptime('2:00', C.FMT)


        def queue_penalty(self, value):
            penalty_number = len(self._active_penalties[value['team']])
            penalty_to_follow = penalty_number - 2
            value['expires_at'] = datetime.strptime(self._active_penalties[value['team']][penalty_to_follow]['expires_at'], C.FMT) + timedelta(minutes=value['pim'])
            return
        # else:
        #     # If I'm in overtime and the team that DIDN'T take the penalty has fewer than 5 guys on the ice, check active penalties and add a guy
        #     if (value["period_taken"] == 4 and value['game_type'] != 'Playoff'):   
        #         pass






        value['expires_at'], value['period_expires'] = per_overflow(value['expires_at'], value['period_taken'])

        self._active_penalties[value['team']].append(value) #add penalty to team array
        return
    # def overtime_reduction(self):
    #     pass

    def overtime_reduction(self):
        if self._manpower["home"] == self._manpower["away"]: #if even strength, go to 3v3
            self._manpower["home"] = 3
            self._manpower["away"] = 3
        elif max(self._manpower.values()) == 5 and min(self._manpower.values()) == 4: #if 5 on 4, go down to 4 on 3
            self._manpower[max(self._manpower, key=self._manpower.get)] = 4
            self._manpower[min(self._manpower, key=self._manpower.get)] = 3
        return


    def clear_expired(self, value):
        for team in self._active_penalties:
            
            for penalty in self._active_penalties[team][:]:
               
                if (penalty['period_expires'] < value['period']) or ((penalty['period_expires'] == value['period']) and (penalty['expires_at'] <= value['time'])):
                    
                    if len(self._active_penalties[team]) <= 2:
                        self._manpower[team] += 1

                    self._active_penalties[team].remove(penalty)
        return

    def event_check(self, value):
        # first, clear penalties on both teams that expired prior to the event
        self.clear_expired(value)

        team = value['team']
        opponent = 'away' if value['team'] == 'home' else 'home'

        # return game state
        print(f'goal scored at {self._manpower}')

        # Next, if goal, wipe out opponent's next penalty (if it exists)
        if value['event'] == 'GOAL' and (self._manpower[team] > self._manpower[opponent]):
                del self._active_penalties[opponent][0]
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
    states.add_penalty({ 'team': 'home', 'player_number': 27, 'pim': 2, 'taken_at': '16:00', 'period_taken': 1 })
    states.add_penalty({ 'team': 'home', 'player_number': 28, 'pim': 2, 'taken_at': '16:01', 'period_taken': 1 })
    states.add_penalty({ 'team': 'home', 'player_number': 29, 'pim': 2, 'taken_at': '16:02', 'period_taken': 1 })
    states.add_penalty({ 'team': 'home', 'player_number': 30, 'pim': 2, 'taken_at': '16:03', 'period_taken': 1 })
    # print(states.manpower)
    # for team in states.active_penalties:
    #     for penalty in states.active_penalties[team]:
    #         print(penalty)

    states.event_check({ 'event': 'GOAL', 'team': 'away', 'time': '18:03', 'period': 1, 'game_type': 'Regular'})

    for team in states.active_penalties:
        for penalty in states.active_penalties[team]:
            print(penalty)
