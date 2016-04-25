CREATE VIEW daily_vehicle_positions AS (
    SELECT
        to_date(
            to_char(to_timestamp(timestamp-(7*3600)), 'YYYY-MM-DD')
        , 'YYYY-MM-DD') AS service_date
    ,   vehicle_id
    ,   position_latitude AS lat
    ,   position_longitude AS lon
    ,   to_number(
            to_char(
                to_timestamp(
                    to_char(
                        to_timestamp(timestamp-(7*3600))
                    ,   'HH24:MI:SS')
                , 'HH24:MI:SS')
            , 'SSSS')
        , '99999') AS ts
    ,   timestamp AS utc_timestamp
    ,   oid AS vehicle_position_id
    FROM
        vehicle_positions
)
