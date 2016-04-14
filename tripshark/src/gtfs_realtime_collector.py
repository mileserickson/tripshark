"""GTFS-Realtime Library"""
from __future__ import (division, print_function, absolute_import)

import os
import urllib
import gtfs_realtime_pb2
from protobuf_to_dict import protobuf_to_dict

feed_names = ('RTPOS', 'RTUPDATES', 'RTALERTS')
feed_urls = {name: os.environ[name] for name in feed_names}

def fetch_gtfsrt_feed(feed_url, as_dict=True):
    """Fetch gtfs_realtime data from a feed.

    Parameters
    ----------
    feed_url : string
        URL of gtfs_realtime feed, including any GET parameters.

    Returns
    -------
    feed_dict : dictionary

    Examples
    --------
    >>> f = fetch_gtfsrt_feed('http://api.bart.gov/gtfsrt/tripupdate.aspx')
    >>> 'gtfs_realtime_version' in f['header']
    True
    """
    response = urllib.urlopen(feed_url)  # Fetch feed with HTTP request
    feed = gtfs_realtime_pb2.FeedMessage()  # Protocol Buffer
    feed.ParseFromString(response.read())  # Parse GTFS-realtime feed
    return protobuf_to_dict(feed)  # Return as dictionary
