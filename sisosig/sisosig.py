# -*- coding: utf-8 -*-
import requests
from typing import List
from concurrent.futures import Future, wait
from datetime import datetime
from requests_futures.sessions import FuturesSession


# TODO: optionally use regular requests session
class DarkskyClient:
    def __init__(self, key: str, threads: int) -> None:
        self.key = key  # type: str
        self.session = FuturesSession(
            max_workers=threads
        )  # type: FuturesSession

    def _get_location(self, lat: float, lon: float, date: str) -> Future:
        if date:
            date = ',{}'.format(date)
        template = ('https://api.darksky.net/forecast/'
                    '{key}/{lat},{lon}{date}'
                    '?exclude=currently,minutely,hourly'
                    '&units=si')  # type: str

        endpoint = template.format(
            key=self.key, lat=lat, lon=lon, date=date,
        )  # type: str
        return self.session.get(endpoint)

    def get_locations(self, locations: List, date: str) -> List[dict]:
        done, incomplete = wait(
            [self._get_location(*l, date) for l in locations]
        )  # TODO: what's the type annotation here?
        return [d.result().json() for d in done]
