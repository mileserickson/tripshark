CREATE VIEW _355_daily_stop_time_updates AS (
    SELECT DISTINCT ON (
        daily_trip_updates.service_date
    ,   daily_trip_updates.trip_id
    ,   _355_stop_time_updates.stop_id
    )
        daily_trip_updates.service_date
    ,   daily_trip_updates.trip_id AS trip_id
    ,   stop_time_updates.stop_id AS stop_id
    ,   stop_time_updates.departure_time AS dep_utc
    ,   to_number(
            to_char(
                to_timestamp(stop_time_updates.departure_time) - INTERVAL '7h'
            , 'SSSS')
        , '99999') AS dep
    FROM
        daily_trip_updates
    INNER JOIN
        stop_time_updates
    ON
        daily_trip_updates.trip_update_id = stop_time_updates.trip_update_id
    ORDER BY
        daily_trip_updates.service_date
    ,   daily_trip_updates.trip_id
    ,   stop_time_updates.stop_id
    ,   daily_trip_updates.utc_timestamp DESC
)
