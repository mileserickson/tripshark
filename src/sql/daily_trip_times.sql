CREATE VIEW daily_trip_times AS (
SELECT
    universal_calendar.date AS service_date,
    trip_times.*
FROM
    universal_calendar
INNER JOIN
    trip_times
ON
    universal_calendar.service_id = trip_times.service_id
);

CREATE MATERIALIZED VIEW retro_trip_times AS (
    SELECT * FROM daily_trip_times
);
