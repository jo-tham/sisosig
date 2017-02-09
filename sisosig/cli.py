# TODO: tabular (lat, long, date, nDayForecast, observation)
# for a bounding box

# benchmark writing single results to db with as_completed
# benchmark writing to db as callback
import os
import json
import click
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from .sisosig import DarkskyClient


@click.group()
def cli():
    pass


@cli.command()
@click.option('-l', '--locations', type=(float, float), multiple=True,
              help='Coordinates of location for which to get data')
@click.option('--locations-file', type=click.File(),
              help='Geojson file with coordinates; overrides "-l"')
@click.option('-h', '--db-host', type=str, default='localhost',
              help='MongoDB host')
@click.option('-p', '--db-port', type=int, default=27017,
              help='MongoDB port')
@click.option('-d', '--db-name', type=str, default='sisosig',
              help='MongoDB database name')
@click.option('-c', '--collection-name', type=str, default='forecasts',
              help='MongoDB collection name')
@click.option('-s', '--save-to-db', is_flag=True,
              help='Persist results to the database collection')
@click.option('-t', '--threads', type=int, default=10,
              help='Maximum number of threads to use for api calls')
@click.option('-k', '--api-key', type=str,
              default=lambda: os.environ.get('DARKSKY_API_KEY'),
              help='darksky.net API key')
@click.option('-T', '--time', type=str,
              default='',
              help='Unix time for data - e.g. date --date="2 days ago" +%s')
def get(locations, locations_file,
        db_name, collection_name,
        db_host, db_port, save_to_db,
        threads, api_key, time):
    """Get forecasts or observations"""
    api_client = DarkskyClient(key=api_key, threads=threads)
    db_client = MongoClient(host=db_host, port=db_port)
    collection = db_client[db_name][collection_name]

    try:
        db_client.admin.command('ismaster')
    except ConnectionFailure:
        click.echo("{}:{} not available".format(db_host, db_port))
        raise

    if locations_file:
        locations = json.loads(
            locations_file.read()
        )['geometry']['coordinates']
        # geojson is lon,lat instead of lat,lon
        locations = [i[::-1] for i in locations]

    result = api_client.get_locations(locations, time)

    if save_to_db:
        click.echo("Saving to database")
        collection.insert_many(result)
    else:
        click.echo(result)

if __name__ == "__main__":
    cli()
