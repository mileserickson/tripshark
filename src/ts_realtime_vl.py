"""Realtime updater of GeoJSON vehicle location feed."""

import psycopg2
from ts_gtfs import GTFS
import geojson
from geojson import (Feature, Point, FeatureCollection as FC)
import boto3

s3client = boto3.client('s3')

def main():
    """Update GeoJSON vehicle location file every 30 seconds."""
    gtfs = GTFS()  # Initialize a GTFS object with a database connection
    while True:
        # Refresh vehicle locations
        rtvl = gtfs.get_vehicle_locations(time_window=600)
        # Create GeoJSON Feature Collection
        fc = FC([Feature(geometry=Point((v[2], v[1])), id=v[0]) for v in rtvl])
        # Serialize to string
        rtvl_geojson = geojson.dumps(fc)
        # Save to Amazon S3
        s3client.put_object(
            ACL='public-read',
            Body=rtvl_geojson,
            Bucket='static.tripshark.net',
            Key='test/rtvl.geojson',
        )
        

if __name__ == '__main__':
    main()
