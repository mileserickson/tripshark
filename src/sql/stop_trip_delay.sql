SELECT DISTINCT
    daily_trip_times.service_date
,   daily_trip_times.trip_id
,   daily_trip_times.stop_seq
,   daily_trip_times.stop_id
,   daily_trip_times.stop_name
,   daily_trip_times.departure_time
,   (daily_stop_time_updates.dep - daily_trip_times.dep) AS delay
FROM
    daily_stop_time_updates
INNER JOIN
    daily_trip_times
ON
    daily_trip_times.service_date = daily_stop_time_updates.service_date
AND daily_trip_times.trip_id = daily_stop_time_updates.trip_id
AND daily_trip_times.stop_id = daily_stop_time_updates.stop_id
WHERE
    daily_stop_time_updates.stop_id = '5402'
ORDER BY
    daily_trip_times.trip_id
,   daily_trip_times.stop_seq
,   daily_trip_times.service_date
;
