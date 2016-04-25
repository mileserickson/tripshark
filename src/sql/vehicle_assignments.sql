CREATE VIEW
    vehicle_assignments
AS (
    SELECT DISTINCT ON (vehicle_id)
        vehicle_id
    ,   route_id
    ,   route_num
    FROM
        trip_updates
    ORDER BY
        vehicle_id
    ,   timestamp DESC
    WHERE
        timestamp > extract(epoch from now()) - 600

/* or... */

CREATE VIEW vehicle_block_assignments AS ()
    SELECT DISTINCT ON (service_date, block_id)
        service_date
    ,   block_id
    ,   vehicle_id
    FROM
        universal_calenadar
    INNER JOIN blocks ON
        universal_calendar.service_id = blocks.service_id
    INNER JOIN trip_updates ON
        trip_updates.trip_id = blocks.trip_id
    ORDER BY
        trip_updates.timestamp DESC
