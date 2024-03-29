import json
import requests
import pandas as pd
import logging
from ift6758.ift6758.client.mileston2_q4 import*
logger = logging.getLogger(__name__)


class GameClient:
    def __init__(self, ip: str = "127.0.0.1", port: int = 80, features=None):
        self.base_url = f"http://{ip}:{port}"
        logger.info(f"Initializing client game; base URL: {self.base_url}")

        self.teamNames = None
        self.Period_Number = None
        self.Period_Time = None
        self.vrai_scores = None

        #pour faciliter la calcul de la somme des buts attendus (xG) pour le jeu entier jusqu'à présent pour les deux équipes
        #on ajoute un colonne Team_of_Shooter pour distinguer les tir/buts pourduit par les deux epuipes
        if features is None:
            self.features = ["Distance","Team_of_Shooter"]
        else:
            self.features = features
            self.features.append("Team_of_Shooter")

        # any other potential initialization
        self.last_event=None


    def get_game_events(self, game_id) -> pd.DataFrame:
        url = "https://statsapi.web.nhl.com/api/v1/game/"+str(game_id)+"/feed/live/"
        r = requests.get(url = url)
        
        new_plays = get_df_from_game(r.json())

        # new_plays = sorted(new_plays, key=lambda x: x['about']['eventIdx']) #not eventId
        # new_plays = list(filter(lambda x: x['about']['eventIdx'] > self.last_event['about']['eventIdx'] if self.last_event else True, new_plays))
        tmp = new_plays.iloc[-1]

        self.teamNames =  [r.json()['gameData']['teams']['away']['triCode'],r.json()['gameData']['teams']['home']['triCode']]
        self.Period_Number = tmp['Period_Number']
        self.Period_Time = tmp['Period_Time']
        # self.vrai_scores = [tmp['Aways_goals'],tmp['Home_goals'] ]
        self.vrai_scores = { self.teamNames[0]: tmp['Aways_goals'], self.teamNames[1]: tmp['Home_goals']}

        if self.last_event is not None:
            new_plays = new_plays[new_plays['Event_ID'] >  self.last_event['Event_ID']]


        self.last_event=tmp

        return new_plays[self.features]


    def get_team_names(self):
        return self.teamNames
    
    def get_vrai_scores(self):
        return self.vrai_scores
    # cette fonction retour un dictonaire{'WSH': 4, 'CAR': 2}

    def get_period_info(self):
        return self.Period_Number ,self.Period_Time
