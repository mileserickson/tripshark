SELECT DISTINCT
    retro_trip_times.service_date
,   retro_trip_times.trip_id
,   retro_trip_times.stop_seq
,   retro_trip_times.stop_id
,   retro_trip_times.stop_name
,   retro_trip_times.departure_time
,   (_355_stop_time_updates.dep - retro_trip_times.dep) AS delay
FROM
    _355_stop_time_updates
INNER JOIN
    retro_trip_times
ON
    retro_trip_times.service_date = _355_stop_time_updates.service_date
AND retro_trip_times.trip_id = _355_stop_time_updates.trip_id
AND retro_trip_times.stop_id = _355_stop_time_updates.stop_id
WHERE
    _355_stop_time_updates
ORDER BY
    retro_trip_times.trip_id
,   retro_trip_times.stop_seq
,   retro_trip_times.service_date
;
