# tripshark: transit performance monitoring

Miles Erickson
April 7, 2016

## Project Description

The Seattle area has many hundreds of bus routes in addition to multiple ferry routes and rail lines. Automated trip planning software helps transit riders navigate the transit system. Such software can recommend the fastest scheduled route between a given origin and destination at a given time of day.

An example of a trip plan is shown below. Generated by the <a href="tripplanner.kingcounty.gov/">King County Metro Trip Planner</a> web site, this shows the fastest scheduled route between Pioneer Square and Magnuson Park (in Northeast Seattle) at 10:00 p.m. on a weekday. Note that the trip involves catching a bus that is scheduled to arrive at Northgate Transit Center at 10:30 pm, then transferring to a bus that departs from that location five minutes later at 10:35 pm:

<img src='img/sample_trip_plan.png' alt='Sample trip plan from Galvanize Seattle Campus to Magnuson Park'>

Of course, buses often run behind schedule. Riders can benefit from having information about the <i>reliability</i> of recommended transfer connections.

### Example Questions
* How often does the 41 actually arrive in time to make the transfer connection to the 75 at Northgate Transit Center?
* On average, what percentage of transit trip plans result in an on-time arrival? Does this percentage vary according to day of week, time of day, etc.?

### Existing Conditions
* Currently, recommended transfer connections are based solely on <i>scheduled</i> arrival and departure times. The trip planner does not store information about the on-time performance of individual trips.
* Real-time vehicle location data is available via [Tracker](http://tripplanner.kingcounty.gov/hiwire?.a=iRealTimeDisplay) and [OneBusAway](http://pugetsound.onebusaway.org/where/standard/), but neither service provides archival on-time performance data.

### Opportunities
* Real-time vehicle location data is available to developers.
* Schedule deviations should be predictable to some extent. For example, the Friday afternoon bus schedule is the same as the Monday afternoon bus schedule, but freeway congestion is most severe on Friday afternoons.
* The use of archived vehicle location data should enable predictions about the reliability of transit connections.


## Data Sources
* [GTFS Data](http://www.soundtransit.org/Developer-resources/Data-downloads) representing transit routes, bus stop locations, and scheduled trips.
* [OneBusAway Real-Time API](http://developer.onebusaway.org/modules/onebusaway-application-modules/1.1.14/api/where/index.html) showing the real-time locations of all transit vehicles.
* [Archival GTFS-realtime data](https://groups.google.com/forum/#!topic/onebusaway-api/NMb0FQozqyU) showing historical vehicle locations.

## Prior Art
* The OneBusAway project provides open-source code that interprets GTFS-realtime data and translates it into projected bus arrival times at any bus stop.