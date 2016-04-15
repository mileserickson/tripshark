"""Request GTFS-realtime data."""

import time
from datetime import datetime
import os
import requests
import gtfs_realtime_pb2
from protobuf_to_dict import protobuf_to_dict

def oba_timestamp(dt):
    """Return a OneBusAway timestamp (milliseconds since the Unix Epoch).

    Parameters
    ----------
    dt : datetime

    Returns
    -------
    oba_ts : int
        Milliseconds since the Unix Epoch (01/01/1970 00:00:00)

    Examples
    --------
    >>> oba_timestamp()
    """
    t = time.mktime(dt.timetuple())  # Cast datetime to time
    return int(t)


def gtfsrt_to_dict(gtfsrt_raw):
    """Return a dictionary of the contents of a GTFS-Realtime feed.

    Parameters
    ----------
    gtfsrt_raw : string
        Raw GTFS-Realtime feed.

    Returns
    -------
    gtfsrt_dict : dict
    """
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(gtfsrt_raw)  # Parse GTFS-Realtime
    return protobuf_to_dict(feed)  # Return as dictionary
