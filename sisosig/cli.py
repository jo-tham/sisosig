# TODO: write forecast(s) to file(s)/database
# TODO: get observations for the locations
# TODO: tabular (lat, long, date, nDayForecast, observation)
# TODO: use a file with list of locations
# TODO: sample locations of interest - subcommand to generate locations
# for a bounding box
import os
import click
from pymongo import MongoClient

from .sisosig import DarkskyClient


@click.group()
def cli():
    pass

@cli.command()
@click.option('-l', '--location', type=(float, float), multiple=True,
              help='Coordinates of location for which to get data')
@click.option('-h', '--db-host', type=str, default='localhost',
              help='MongoDB host')
@click.option('-p', '--db-port', type=int, default=27107,
              help='MongoDB port')
@click.option('-d', '--db-name', type=str, default='sisosig',
              help='MongoDB database name')
@click.option('-c', '--collection-name', type=str, default='forecasts',
              help='MongoDB collection name')
@click.option('-k', '--api-key', type=str,
              default=lambda: os.environ.get('DARKSKY_API_KEY'),
              help='darksky.net API key')
def get(location, api_key, db_name, collection_name, db_host, db_port):
    """Get forecasts or observations"""
    client = DarkskyClient(key=api_key)
    client = MongoClient()
    collection = client[db_name][collection_name]
    import ipdb; ipdb.set_trace()
    # would rather apply the get function over locations
    for l in location:
        click.echo('location lat: %s long: %s' % l)
        lat, lon = l
        data = client.get_forecast(lat, lon)
        click.echo(data)


if __name__ == "__main__":
    cli()
