"""mGTFS library"""

import psycopg2
import time

""" TODO database connection
db_params = {
    'dbname': 'gtfs',
    'username': 'gtfs',
    }
conn = psycopg2.connect("dbname=gtfs user=ubuntu")
"""


def get_active_vehicles(when=time.time(), time_window=300, conn=None):
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
    return None if conn is None

    query_active_vehicles = """
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
    cur = conn.cursor()
    params = (when, when-time_window)
    cur.execute(query_active_vehicles, params)
    return [r[0] for r in cur.fetchall()]


def get_vehicle_location(vehicle_id, when=time.time(), conn=None):
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
    """
    return None if conn is None

    query_vehicle_location = """
        SELECT
            position_latitude
        ,   position_longitude
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
    cur = conn.cursor()
    params = (when, vehicle_id)
    cur.execute(query_vehicle_location, params)
    return cur.fetchone()


def get_vehicle_locations(when=time.time(), time_window=300, conn=None):
    """Return the location of all vehicles active within time_window."""
    return None if conn is None

