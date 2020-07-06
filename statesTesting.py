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

    # @active_penalties.setter
    # def active_penalties(self, value):
    #     print(value)
    #         # value['expires_at'] = '69'
    #         # self.active_penalties = self.active_penalties + [value]
    
    # def append(self, value):
    #     self.active_penalties = self.active_penalties + [value]
    #     # return self._active_penalties
    #     # value['expires_at'] = dt.strptime(value['taken_at'], C.FMT) + dt.strptime('2:00', C.FMT)
    #     # self.determine_expiry(value)
    #     # self.active_penalties = self.active_penalties + [value.update({"hello": "test"})]

    def determine_expiry(self, value):
        # self.expires_at = dt.strptime(value['taken_at'], C.FMT) + dt.strptime('2:00', C.FMT)
        # return self.expires_at
        print("success")

    def add_penalty(self, value):
        print(value)
        print(f"active {value['team']} penalties: {len(self._active_penalties[value['team']])}")
        if len(self._active_penalties[value['team']]) < 2:
            self._manpower[value['team']] -= 1
            value['expires_at'] = (datetime.strptime(value['taken_at'], C.FMT) + timedelta(minutes=2)).strftime(C.FMT) #'dt.strptime('2:00', C.FMT)
            self._active_penalties[value['team']].append(value)
        else:
            print(f'need to queue penalties')
        # value['player_number'] = value['player_number'] + 1
        # self.active_penalties = self.active_penalties + [value]


if __name__ == "__main__":
    states = GameStates()
    # print(states.manpower)
    # states.manpower["home"] -= 1
    # print(states.manpower)
    # states.active_penalties = { 'player_number': 27, 'taken_at': '1:00' }
    # states.active_penalties["home"].append({ 'player_number': 27, 'taken_at': '1:00' })
    states.add_penalty({ 'team': 'home', 'player_number': 27, 'taken_at': '1:00' })
    states.add_penalty({ 'team': 'home', 'player_number': 27, 'taken_at': '1:30' })
    states.add_penalty({ 'team': 'home', 'player_number': 27, 'taken_at': '2:00' })
    states.add_penalty({ 'team': 'home', 'player_number': 27, 'taken_at': '2:30' })
    print(states.manpower)
    print(states.active_penalties)

    # time1 = '1:00'
    # time2 = '1:30'

    # tdelta = dt.strptime(time2, C.FMT) - dt.strptime(time1, C.FMT)

    # print(tdelta)
