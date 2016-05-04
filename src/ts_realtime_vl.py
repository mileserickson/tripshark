"""Realtime updater of GeoJSON vehicle location feed."""

from ts_gtfs import GTFS
import geojson
from geojson import (Feature, Point, LineSting, FeatureCollection as FC)
import boto3
import time

print('# Connect to AWS')
session = boto3.Session(profile_name='tripshark_s3')
s3client = session.client('s3', region_name='us-west-2')

INTERVAL = 30  # Seconds between updates

gtfs = GTFS()  # Initialize a GTFS object with a database connection

def update_rtvl():
    """Update real-time vehicle locations to an S3 bucket."""
    print('# Refresh vehicle locations')
    rtvl = gtfs.get_vehicle_locations(when=time.time(), time_window=300)
    print('# Create GeoJSON Feature Collection')
    fc = FC([Feature(geometry=Point((v[2], v[1])), id=v[0],
                     properties={'ts': v[3]}) for v in rtvl])
    print('# Serialize to string')
    rtvl_geojson = geojson.dumps(fc)
    print('# Save to Amazon S3')
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


def repeat_fn(fn, interval):
    """Call fn() at interval (seconds), or as frequently as possible."""
    while True:
        starttime = time.time()
        fn()
        elapsed_time = time.time() - starttime
        if elapsed_time < INTERVAL:
            time.sleep(INTERVAL - elapsed_time)


if __name__ == '__main__':
    repeat_fn(update_rtvl, INTERVAL)
