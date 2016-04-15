"""GTFS-Realtime Library"""
from __future__ import (division, print_function, absolute_import)

import os
import urllib
import gtfs_realtime_pb2
from protobuf_to_dict import protobuf_to_dict

feed_names = ('RTPOS', 'RTUPDATES', 'RTALERTS')
feed_urls = {name: os.environ[name] for name in feed_names}


def fetch_url(feed_url, filename):
    """Fetch HTTP content to a file.

    Parameters
    ----------
    url : string

    Examples
    --------
    >>> fetch_url_to_file('http://en.wikipedia.org/', 'fetch-wikipedia.tmp')
    >>> 'Wikipedia' in open('fetch_wikipedia.tmp').read()
    True
    >>> os.remove('fetch_wikipedia.tmp')
    """
    with open(filename) as f_out:
        pass


def fetch_rt(feed_url, as_dict=True):
    """Fetch gtfs_realtime data from a feed.

    Parameters
    ----------
    feed_url : string
        URL of gtfs_realtime feed, including any GET parameters.

    Returns
    -------
    feed : dictionary

    Examples
    --------
    >>> feed = fetch_rt('http://api.bart.gov/gtfsrt/tripupdate.aspx')
    >>> 'gtfs_realtime_version' in feed['header']
    True
    """
    response = urllib.urlopen(feed_url)  # Fetch feed with HTTP request
    feed = gtfs_realtime_pb2.FeedMessage()  # Protocol Buffer
    feed.ParseFromString(response.read())  # Parse GTFS-realtime feed
    return protobuf_to_dict(feed)  # Return as dictionary


def poll_feeds(feed_urls=feed_urls):
    """Poll multiple GTFS-Realtime feeds.

    Parameters
    ----------
    feed_urls : dict
        dict of strings: {feed_name: feed_url}

    Returns
    -------
    rt_feeds : dict
        dict of dicts: {feed_name: feed}
    """

    return {name: fetch_rt(url) for name, url in feed_urls.items()}
