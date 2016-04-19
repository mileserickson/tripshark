"""TripShark GTFS library"""

import psycopg2
import time


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
    SELECT DISTINCT
        vl.vehicle_id
    ,   vl.position_latitude
    ,   vl.position_longitude
    ,   vl.timestamp
    FROM
        (""" + QUERY_ACTIVE_VEHICLES + """) av
    INNER JOIN
        vehicle_positions vl
    ON
        av.id = vl.vehicle_id
    AND av.ts = vl.timestamp
    """

QUERY_POSITION_REPORTS = """
    SELECT
    DISTINCT ON (vl.vehicle_id, vl.timestamp)
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
    if conn is None:
        return None

    cur = conn.cursor()
    params = (when, when-time_window)
    cur.execute(QUERY_ACTIVE_VEHICLES, params)
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
    timestamp : long
        Time location reported by vehicle
    """
    if conn is None:
        return None
    query_vehicle_location = """
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
    with conn.cursor() as cur:
        params = (when, vehicle_id)
        cur.execute(query_vehicle_location, params)
        result = cur.fetchone()
    location = result[:2]
    timestamp = result[2]
    return location, timestamp


def get_vehicle_locations(when=time.time(), time_window=300, conn=None):
    """Return the location of all vehicles active within time_window."""
    if conn is None:
        return None
    with conn.cursor() as cur:
        params = (when, when-time_window)
        cur.execute(QUERY_ACTIVE_VEHICLE_LOCATIONS, params)
        result = cur.fetchall()
    return [r for r in result]

def get_position_reports(when=time.time(), time_window=86400, conn=None):
        """Return all position repors reported within time_window."""
        if conn is None:
            return None
        with conn.cursor() as cur:
            params = (when, when-time_window)
            cur.execute(QUERY_POSITION_REPORTS, params)
            result = cur.fetchall()
        return [r for r in result]
