from __future__ import (division, print_function, absolute_import)
import boto3
import json
from boto3.dynamodb.types import (Binary, Decimal)
from datetime import datetime

DEFAULT_TABLE = 'tripshark_gtfs_realtime'


def store_raw_data(raw_data, agency_id='TEST', table_name=DEFAULT_TABLE):
    """Store raw data in DynamoDB for subsequent processing.

    Parameters
    ----------
    raw_data : str
        Binary data to store in the database.
    agency_id : str
        Unique transit agency identifier.
    table_name : str
        Name of the DynamoDB table used to store the data.

    Returns
    -------
    response : dict
        {'ResponseMetadata': {'HTTPStatusCode': ..., 'RequestId': ...}}


    Examples
    --------
    >>> raw_data = open('../data/rtpos.gtfsrt').read()
    >>> result = store_raw_data(raw_data, agency_id='TEST')
    >>> result['ResponseMetadata']['HTTPStatusCode']
    200
    """
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table(table_name)
    now = datetime.now()
    ts = (now - datetime(1970, 1, 1)).total_seconds()
    response = table.put_item(Item={
            'agency_id': str(agency_id),
            'date_time': now.strftime("%Y-%m-%d %H:%M:%S"),
            'raw_data': Binary(raw_data)
            }
        )
    return response
