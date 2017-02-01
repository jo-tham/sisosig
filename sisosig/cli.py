# TODO: sample locations of interest - subcommand to generate locations
# TODO: use a file with list of locations
# TODO: get observations for the locations
# TODO: tabular (lat, long, date, nDayForecast, observation)
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
@click.option('-s', '--save-to-db', is_flag=True,
              help='Persist results to the database collection')
@click.option('-k', '--api-key', type=str,
              default=lambda: os.environ.get('DARKSKY_API_KEY'),
              help='darksky.net API key')
def get(location, api_key,
        db_name, collection_name,
        db_host, db_port,
        save_to_db):
    """Get forecasts or observations"""
    api_client = DarkskyClient(key=api_key)
    db_client = MongoClient()
    collection = db_client[db_name][collection_name]

    # TODO: update client to return future?
    result = [api_client.get_forecast(*loc) for loc in location]

    if save_to_db:
        collection.insert_many(result)
    else:
        click.echo(result)

if __name__ == "__main__":
    cli()
