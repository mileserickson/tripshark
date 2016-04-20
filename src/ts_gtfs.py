"""TripShark GTFS library"""

import psycopg2
import time

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
    SELECT DISTINCT ON (vehicle_id, vehicle_positions.timestamp)
        vehicle_id AS id
    ,   position_latitude AS lat
    ,   position_longitude AS lon
    ,   vehicle_positions.timestamp AS ts
    FROM
        vehicle_positions
    WHERE
        vehicle_positions.timestamp <= %s
    AND
        vehicle_positions.timestamp > %s
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
    """Return a database connection.

    Parameters
    ----------
    dbname : string
    user : string
        PostgreSQL database name and username.

    Returns
    -------
    conn : psycopg2.extensions.connection

    Examples
    --------
    >>> with get_db_connection() as conn:
    >>>     result = type(c), c.closed
    >>> result
    (psycopg2.extensions.connection, 0)
    """
    return psycopg2.connect("dbname={} user={}".format(DB_NAME, DB_USERNAME))


class GTFS(object):
    """GTFS database connection"""
    def __init__(self, conn=dbc()):
        """Initialize a new GTFS object."""
        self.conn = conn
        self.db = self.conn.dsn.split(" ")[0].split("=")[1]
        self.user = self.conn.dsn.split(" ")[1].split("=")[1]

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
            params = (when, when-time_window)
            cur.execute(QUERY_ACTIVE_VEHICLE_LOCATIONS, params)
        return cur.fetchall()

    def get_position_reports(self, when=time.time(), time_window=86400):
            """Return all position reports reported within time_window."""
            with self.conn.cursor() as cur:
                params = (when, when-time_window)
                cur.execute(QUERY_POSITION_REPORTS, params)
            return cur.fetchall()
