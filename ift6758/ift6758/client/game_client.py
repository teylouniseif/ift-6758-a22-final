import json
import requests
import pandas as pd
import logging


logger = logging.getLogger(__name__)


class GameClient:
    def __init__(self, ip: str = "0.0.0.0", port: int = 5000, features=None):
        self.base_url = f"http://{ip}:{port}"
        logger.info(f"Initializing client; base URL: {self.base_url}")

        if features is None:
            features = ["distance"]
        self.features = features

        # any other potential initialization
        self.last_event=None

    def get_game_events(self, game_id) -> pd.DataFrame:
        url = "https://statsapi.web.nhl.com/api/v1/game/"+str(game_id)+"/feed/live/"
        r = requests.get(url = url)
        new_plays = r.json()['liveData']['plays']['allPlays']
        new_plays = sorted(new_plays, key=lambda x: x['about']['eventId'])
        tmp = new_plays[-1]
        new_plays = list(filter(lambda x: x['about']['eventId'] > self.last_event['about']['eventId'] if self.last_event else True, new_plays))
        self.last_event=tmp


        return new_plays
