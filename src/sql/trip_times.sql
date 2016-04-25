CREATE VIEW trip_times AS (
    SELECT
        routes.agency_id AS agency
    ,   routes.route_short_name AS route_num
    ,   stop_times.stop_id AS stop_id
    ,   stops.stop_name AS stop_name
    ,   stops.stop_lat AS stop_lat
    ,   stops.stop_lon AS stop_lon
    ,   stop_times.arrival_time AS arrival_time
    ,   to_number(
            to_char(
                to_timestamp(stop_times.arrival_time, 'HH24:MI:SS')
            , 'SSSS')
        , '99999') AS arr
    ,   stop_times.departure_time AS departure_time
    ,   to_number(
            to_char(
                to_timestamp(stop_times.departure_time, 'HH24:MI:SS')
            , 'SSSS')
        , '99999') AS dep
    ,   routes.route_id AS route_id
    ,   trips.trip_id AS trip_id
    ,   trips.shape_id AS shape_id
    ,   trips.service_id AS service_id
    ,   stop_times.stop_sequence AS stop_seq
    FROM
        trips
    INNER JOIN
        routes ON trips.route_id = routes.route_id
    INNER JOIN
        stop_times ON stop_times.trip_id = trips.trip_id
    INNER JOIN
        stops ON stop_times.stop_id = stops.stop_id
    ORDER BY
        routes.agency_id
    ,   routes.route_short_name
    ,   stop_times.trip_id
    ,   stop_times.stop_sequence
)
