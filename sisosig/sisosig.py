# -*- coding: utf-8 -*-
import requests
from typing import List
from concurrent.futures import Future, wait
from datetime import datetime
from requests_futures.sessions import FuturesSession


class DarkskyClient:

    def __init__(self, key: str, threads: int) -> None:
        self.key = key  # type: str
        self.session = FuturesSession(
            max_workers=threads
        )  # type: FuturesSession

    def _get_forecast(self, lat: float, lon: float) -> Future:
        template = ('https://api.darksky.net/forecast/'
                    '{key}/{lat},{lon}'
                    '?exclude=currently,minutely,hourly'
                    '&units=si')  # type: str
        endpoint = template.format(
            key=self.key, lat=lat, lon=lon
        )  # type: str
        return self.session.get(endpoint)

    def get_observation(self, lat: float, lon: float,
                        time: datetime) -> dict:
        template = ('https://api.darksky.net/time-machine/'
                    '{key}/{lat},{lon},{time}'
                    '?exclude=currently,minutely,hourly'
                    '&units=si')  # type: str
        endpoint = template.format(key=self.key, lat=lat, lon=lon,
                                   time=time.timestamp())  # type: str

        return requests.get(endpoint).json()

    def get_forecasts(self, locations: List) -> List[dict]:
        done, incomplete = wait(
            [self._get_forecast(*l) for l in locations]
        )  # TODO: what's the type annotation here?
        return [d.result().json() for d in done]
