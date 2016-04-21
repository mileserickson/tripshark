"""Realtime updater of GeoJSON vehicle location feed."""

from ts_gtfs import GTFS
import threading
import geojson
from geojson import (Feature, Point, FeatureCollection as FC)
import boto3

s3client = boto3.client('s3')
gtfs = GTFS()  # Initialize a GTFS object with a database connection

def update_rtvl(interval=30.0):
    """Update real-time vehicle locations on a schedule."""
    # Schedule next update
    threading.Timer(interval, update_rtvl).start()
    # Refresh vehicle locations
    rtvl = gtfs.get_vehicle_locations(time_window=300)
    # Create GeoJSON Feature Collection
    fc = FC([Feature(geometry=Point((v[2], v[1])), id=v[0]) for v in rtvl])
    # Serialize to string
    rtvl_geojson = geojson.dumps(fc)
    # Save to Amazon S3
    try:
        s3client.put_object(
            ACL='public-read',
            Body=rtvl_geojson,
            Bucket='static.tripshark.net',
            Key='test/rtvl.geojson',
        )
        print("Saved s3://static.tripshark.net/test/rtvl.geojson")
    except:
        print("RTVL save failed")

if __name__ == '__main__':
    update_rtvl()
