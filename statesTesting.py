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
        if len(self._active_penalties[value['team']]) < 2:
            self._manpower[value['team']] -= 1
            value['expires_at'] = datetime.strptime(value['taken_at'], C.FMT) + timedelta(minutes=value['pim']) #'dt.strptime('2:00', C.FMT)

        else:
            penalty_number = len(self._active_penalties[value['team']])
            penalty_to_follow = penalty_number - 2
            value['expires_at'] = datetime.strptime(self._active_penalties[value['team']][penalty_to_follow]['expires_at'], C.FMT) + timedelta(minutes=value['pim'])

        value['expires_at'], value['period_expires'] = per_overflow(value['expires_at'], value['period_taken'])

        self._active_penalties[value['team']].append(value)

    def clear_expired(self, value):
        for team in self._active_penalties:
            
            for penalty in self._active_penalties[team][:]:
               
                if (penalty['period_expires'] < value['period']) or ((penalty['period_expires'] == value['period']) and (penalty['expires_at'] <= value['time'])):
                    
                    if len(self._active_penalties[team]) <= 2:
                        self._manpower[team] += 1

                    self._active_penalties[team].remove(penalty)
                    
                    
                    

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

    states.event_check({ 'event': 'GOAL', 'team': 'away', 'time': '18:03', 'period': 1})

    for team in states.active_penalties:
        for penalty in states.active_penalties[team]:
            print(penalty)
