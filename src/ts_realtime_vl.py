"""Realtime updater of GeoJSON vehicle location feed."""

import psycopg2
from ts_gtfs import GTFS
import geojson
from geojson import (Feature, Point, FeatureCollection as FC)
import boto3

# Set database name and DB username
DB_NAME = 'gtfs'
DB_USERNAME = 'ubuntu'

def main():
    """Update GeoJSON vehicle location file every 30 seconds."""

    gtfs = GTFS()

    while True:
        # Refresh vehicle locations
        vl = gtfs.get_vehicle_locations(time_window=600)
        # Create GeoJSON Feature Collection
        fc = FC([Feature(geometry=Point((v[2], v[1])), id=v[0]) for v in vl])
        # Serialize to string
        fc_s = geojson.dumps(fc)
        # Save to Amazon S3
