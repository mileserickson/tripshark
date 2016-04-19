SELECT
    stop_id,
    trip_id,
    arr,
    dep
FROM 
    (SELECT
	    stop_id
	,   trip_id
	,   arrival_time AS arr
	,   departure_time as dep
	FROM
	    stop_times
	WHERE
	    stop_id = %s) AS st
INNER JOIN trips ON st.trip_id = trips.trip_id
INNER JOIN universal_calendar on trips.service_id = universal_calendar.service_id
WHERE
    universal_calendar.date = %s
ORDER BY
    st.dep

