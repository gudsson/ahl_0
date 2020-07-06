from datetime import datetime, timedelta
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
            self.penalty_number = len(self._active_penalties[value['team']])
            self.penalty_to_follow = self.penalty_number - 2
            value['expires_at'] = datetime.strptime(self._active_penalties[value['team']][self.penalty_to_follow]['expires_at'], C.FMT) + timedelta(minutes=value['pim'])

        if value['expires_at'] > datetime.strptime('20:00', C.FMT): # if penalty expires after the end of the period, move expiry to beginning of next period.
            value['expires_at'] = (value['expires_at'] - timedelta(minutes=20)).strftime(C.FMT)
            value['period_expires'] = value['period_taken'] + 1 #pass
        else:
            value['expires_at'] = (value['expires_at']).strftime(C.FMT) #convert time to string
            value['period_expires'] = value['period_taken'] #else stay in current period
        self._active_penalties[value['team']].append(value)

    def clear_expired(self, value):
        for team in self._active_penalties:
            
            for penalty in self._active_penalties[team][:]:
               
                if (penalty['period_expires'] < value['period']) or ((penalty['period_expires'] == value['period']) and (penalty['expires_at'] <= value['time'])):
                    
                    if len(self._active_penalties[team]) <= 2:
                        self._manpower[team] += 1

                    self._active_penalties[team].remove(penalty)
                    print(self._manpower)
                    

    def event_check(self, value):
        self.clear_expired(value)
        # if value['event'] == 'GOAL':
        #     print("hello")


if __name__ == "__main__":
    states = GameStates()
    states.add_penalty({ 'team': 'home', 'player_number': 27, 'pim': 2, 'taken_at': '16:00', 'period_taken': 1 })
    states.add_penalty({ 'team': 'home', 'player_number': 28, 'pim': 2, 'taken_at': '16:30', 'period_taken': 1 })
    states.add_penalty({ 'team': 'home', 'player_number': 29, 'pim': 2, 'taken_at': '17:00', 'period_taken': 1 })
    states.add_penalty({ 'team': 'home', 'player_number': 30, 'pim': 2, 'taken_at': '17:30', 'period_taken': 1 })
    # print(states.manpower)
    # for team in states.active_penalties:
    #     for penalty in states.active_penalties[team]:
    #         print(penalty)

    states.event_check({ 'event': 'GOAL', 'team': 'away', 'time': '00:15', 'period': 2})

    for team in states.active_penalties:
        for penalty in states.active_penalties[team]:
            print(penalty)
