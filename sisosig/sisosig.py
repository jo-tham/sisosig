# -*- coding: utf-8 -*-

import os
import requests
from datetime import datetime

# def _get(lat: float, lon: float, :key str, template: str) -> dict:
#     endpoint = template.format() #type: str
#     return requests.get(endpoint).json()

class DarkskyClient:
    def __init__(self, key: str):
        self.key = key

    def get_forecast(self, lat: float, lon: float) -> dict:
        template = ('https://api.darksky.net/forecast/'
                    '{key}/{lat},{lon}'
                    '?exclude=currently,minutely,hourly'
                    '&units=si') #type: str
        endpoint = template.format(
            key=self.key, lat=lat, lon=lon
        ) #type: str
        return requests.get(endpoint).json()

    def get_observation(self, lat: float, lon: float,
                        time: datetime) -> dict:
        template = ('https://api.darksky.net/time-machine/'
                    '{key}/{lat},{lon},{time}'
                    '?exclude=currently,minutely,hourly'
                    '&units=si') #type: str
        endpoint = template.format(key=self.key, lat=lat, lon=lon,
                                   time=time.timestamp()) #type: str

        return requests.get(endpoint).json()

def save_forecast(forecast: dict) -> None:
    ...
