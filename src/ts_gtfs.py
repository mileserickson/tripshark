"""TripShark GTFS library."""

import psycopg2
import time
from collections import defaultdict
import geojson
from geojson import Feature, FeatureCollection, Point, LineString
import boto3

# Set database name and DB username
DB_NAME = 'gtfs'
DB_USERNAME = 'ubuntu'

# Define SQL queries
QUERY_ACTIVE_VEHICLES = """
    SELECT
        vehicle_id AS id
    ,   Max(timestamp) AS ts
    FROM
        vehicle_positions
    WHERE
        timestamp <= %s
    AND
        timestamp > %s
    GROUP BY
        vehicle_id
    """

QUERY_ACTIVE_VEHICLE_LOCATIONS = """
    SELECT DISTINCT ON (vehicle_id)
        vehicle_positions.vehicle_id AS id
    ,   vehicle_positions.position_latitude AS lat
    ,   vehicle_positions.position_longitude AS lon
    ,   vehicle_positions.timestamp AS ts
    FROM
        vehicle_positions
    WHERE
        vehicle_positions.timestamp <= %s
    AND
        vehicle_positions.timestamp > %s
    ORDER BY
        vehicle_positions.vehicle_id,
        vehicle_positions.timestamp DESC
    """

QUERY_POSITION_REPORTS = """
    SELECT DISTINCT ON (vl.vehicle_id, vl.timestamp)
        vl.vehicle_id AS id
    ,   vl.position_latitude AS lat
    ,   vl.position_longitude AS lon
    ,   vl.timestamp AS ts
    FROM
        vehicle_positions vl
    WHERE
        vl.timestamp <= %s
    AND
        vl.timestamp > %s
    ORDER BY
        vl.timestamp
    """

QUERY_VEHICLE_LOCATION = """
    SELECT
        position_latitude
    ,   position_longitude
    ,   timestamp
    FROM
        vehicle_positions
    WHERE
        timestamp <= %s
    AND
        vehicle_id = %s
    ORDER BY
        timestamp DESC
    LIMIT 1
    """


def dbc(dbname=DB_NAME, user=DB_USERNAME):
    """Return a psql database connection.

    Examples
    --------
    >>> type(dbc())
    psycopg2.extensions.connection
    """
    return psycopg2.connect("dbname={} user={}".format(DB_NAME, DB_USERNAME))


class GTFS(object):
    """Model a transit system's GTFS & GTFS-RT feeds."""

    def __init__(self, conn=dbc()):
        """Initialize a new GTFS object."""
        self.conn = conn
        self.db = self.conn.dsn.split(" ")[0].split("=")[1]
        self.user = self.conn.dsn.split(" ")[1].split("=")[1]
        self.shapes = self.get_shapes()

    def __del__(self):
        """Destroy a GTFS object."""
        self.conn.close()

    def __repr__(self):
        """Return a string representation of self."""
        return "GTFS(dbc(dbname='{}', user='{}'))".format(self.db, self.user)

    def get_active_vehicles(self, when=time.time(), time_window=300):
        """Return a list of active vehicle IDs.

        Parameters
        ----------
        when : float
            Unix timestamp indicating the time to check (defaults to now).
        time_window : int (seconds)
            Include vehicles with latest position timestamp age < time_window.

        Returns
        -------
        active_vehicles : list
            List of vehicle IDs with locations reported within time_window.
        """
        with self.conn.cursor() as cur:
            params = (when, when-time_window)
            cur.execute(QUERY_ACTIVE_VEHICLES, params)
            result = cur.fetchall()
            return [r[0] for r in result]

    def get_vehicle_location(self, vehicle_id, when=time.time()):
        """Return the most recent location reported for a single vehicle.

        Parameters
        ----------
        vehicle_id : int
        agency_id : str
        when : float
            Unix timestamp indicating the time to query (defaults to now)

        Returns
        -------
        location : tuple
            (latitude, longitude) : (float, float)
        timestamp : long
            Time location reported by vehicle
        """
        with self.conn.cursor() as cur:
            params = (when, vehicle_id)
            cur.execute(QUERY_VEHICLE_LOCATION, params)
            result = cur.fetchone()
        location = result[:2]
        timestamp = result[2]
        return location, timestamp

    def get_vehicle_locations(self, when=time.time(), time_window=300):
        """Return the location of all vehicles active within time_window."""
        with self.conn.cursor() as cur:
            params = [when, when-time_window]
            cur.execute(QUERY_ACTIVE_VEHICLE_LOCATIONS, params)
            result = cur.fetchall()
            cur.close()
            return result

    def get_position_reports(self, when=time.time(), time_window=86400):
        """Return all position reports reported within time_window."""
        with self.conn.cursor() as cur:
            params = (when, when-time_window)
            cur.execute(QUERY_POSITION_REPORTS, params)
            return cur.fetchall()

    def get_shapes(self):
        """Return a dict of shapes as lists of points sorted in sequence."""
        QUERY_SHAPES = """
            SELECT
                shapes.shape_id
            ,   shapes.shape_pt_lat AS lat
            ,   shapes.shape_pt_lon AS lon
            ,   shapes.shape_pt_sequence AS seq
            ,   shapes.shape_dist_traveled AS dist
            FROM
                shapes
            ORDER BY
                shapes.shape_id
            ,   shapes.shape_pt_sequence
        """
        with self.conn.cursor() as cur:
            cur.execute(QUERY_SHAPES)
            result = cur.fetchall()
        shapes = defaultdict(list)
        for r in result:
            shapes[r[0]].append({'coordinates': {'lat': r[1], 'lng': r[2]},
                                'seq': r[3], 'dist': r[4]})
        return shapes

    def get_shape_feature(self, shape_id):
        """Return a GeoJSON feature for the given shape ID."""
        shape = self.shapes[shape_id]
        points = ((float(point['coordinates']['lng']),
                   float(point['coordinates']['lat'])) for point in shape)
        feature = Feature(geometry=LineString([p for p in points]),
                          id=shape_id,
                          className={'baseVal': 'bus_route'}
                          # properties={'route_num': #TODO}
                          )
        return feature

    def shapes_to_s3(self,
                     bucket_name='static.tripshark.net',
                     prefix='shapes/1/shape_'
                     ):
        """Export all GTFS shapes to an S3 bucket."""
        print('# Connect to AWS')
        session = boto3.Session(profile_name='tripshark_s3')
        s3client = session.client('s3', region_name='us-west-2')
        for shape_id in self.shapes.iterkeys():
            fc = FeatureCollection([self.get_shape_feature(shape_id)])
            keyname = prefix + str(shape_id) + ".geojson"
            geojson_text = geojson.dumps(fc)
            print('# Save to Amazon S3')
            try:
                s3client.put_object(
                    ACL='public-read',
                    Body=geojson_text,
                    Bucket=bucket_name,
                    Key=keyname,
                )
                print("Saved s3://static.tripshark.net/" + keyname)
            except:
                print("Shape save failed: " + keyname)

    def dump_location_points():
        """Dump all location points to a GeoJSON file."""
        features = [Feature(geometry=Point((v[2], v[1])), id=v[0]) for v in vl]
        fc = FeatureCollection(features)
        with open('../data/vl.geojson', 'w') as f_out:
            f_out.write(geojson.dumps(fc))
