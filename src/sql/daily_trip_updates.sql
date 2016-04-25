CREATE VIEW daily_trip_updates AS (
    SELECT
        to_date(
            to_char(
                to_timestamp(
                    extract(epoch from timestamp) - 7*3600
                )
            , 'YYYY-MM-DD')
        , 'YYYY-MM-DD') AS service_date
        ,   routes.route_short_name AS route_num
        ,   trip_updates.trip_id AS trip_id
        ,   trip_updates.vehicle_id AS vehicle_id
        ,   to_number(
                to_char(
                    to_timestamp(
                        to_char(
                            timestamp-to_timestamp(7*3600)
                        ,   'HH24:MI:SS')
                    , 'HH24:MI:SS')
                , 'SSSS')
            , '99999') AS ts
        ,   timestamp AS utc_timestamp
        ,   trip_updates.route_id AS route_id
        ,   oid AS trip_update_id
    FROM
        trip_updates
    INNER JOIN routes ON
        trip_updates.route_id = routes.route_id
);
