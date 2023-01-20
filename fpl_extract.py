import datetime
import json
from urllib.request import urlopen
import config
import dateutil.parser
import pytz
import certifi


class FplDeadline:
    def __init__(self):
        self.countdown = 0
        self.localtime = []
        self.gameweek = 0
        self.url = config.bootstrap_link
        self.response = urlopen(self.url, cafile=certifi.where())
        self.data = json.loads(self.response.read())
        self.player_data = self.data['elements']

    def deadline(self):
        timezone = config.timezone

        games = self.data['events']
        time = []

        while self.gameweek < 38:
            for game in games:
                time.append(game['deadline_time'])
                self.gameweek += 1
        for iso in range(len(time)):
            zulu_time = dateutil.parser.parse(time[iso])
            self.localtime.append(zulu_time.astimezone(pytz.timezone(timezone)))

        for time in self.localtime:
            time.replace(tzinfo=None)

        while datetime.datetime.today().isoformat() > self.localtime[self.countdown].isoformat():
            self.countdown += 1

        return f"Gameweek {self.countdown + 1} \n Deadline date: {self.localtime[self.countdown].strftime('%d-%m-%y')} \n Deadline time: " \
               f"{self.localtime[self.countdown].strftime('%H:%M:%S')} "


    def price(self):
        player_change_price = []
        player_dict = {}

        for i in range(len(self.player_data)):
            player_change_price.append(self.player_data[i]['now_cost'])
            player_change_price.append(self.player_data[i]['cost_change_event'])
            player_dict[self.player_data[i]['web_name']] = player_change_price
            player_change_price = []

        fallers = []
        fall_price = []
        risers = []
        rise_price = []

        for k in player_dict:
            if player_dict[k][1] < 0:
                fallers.append(k)
                fall_price.append(str(player_dict[k][0]))
            elif player_dict[k][1] > 0:
                risers.append(k)
                rise_price.append(str(player_dict[k][0]))

        fallers_string = []
        rise_string = []
        new_line = '\n'
        up_arrow = '\u2B06\uFE0F'
        down_arrow = '\u2B07\uFE0F'
        for i in range(len(fallers)):
            if len(fall_price[i]) > 2:
                fallers_string.append(f"{fallers[i]} - £{fall_price[i][0]}{fall_price[i][1]}.{fall_price[i][2]}m")
            else:
                fallers_string.append(f"{fallers[i]} - £{fall_price[i][0]}.{fall_price[i][1]}m")
        for i in range(len(risers)):
            if len(rise_price[i]) > 2:
                rise_string.append(f"{risers[i]} - £{rise_price[i][0]}{rise_price[i][1]}.{rise_price[i][2]}m")
            else:
                rise_string.append(f"{risers[i]} - £{rise_price[i][0]}.{rise_price[i][1]}m")
        return f"RISERS {up_arrow}: \n{new_line.join(rise_string)}\n \nFALLERS {down_arrow}: \n{new_line.join(fallers_string)}"
