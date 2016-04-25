CREATE INDEX rtt_sd_idx ON retro_trip_times (service_date);
CREATE INDEX rtt_tid_idx ON retro_trip_times (trip_id);
CREATE INDEX rtt_sid_idx ON retro_trip_times (stop_id);
CREATE INDEX rtt_sts_idx ON retro_trip_times (service_date, trip_id, stop_id);

CREATE INDEX rstu_sd_idx ON retro_stop_time_updates (service_date);
CREATE INDEX rstu_tid_idx ON retro_stop_time_updates (trip_id);
CREATE INDEX rstu_sid_idx ON retro_stop_time_updates (stop_id);
CREATE INDEX rstu_sts_idx ON retro_stop_time_updates (service_date, trip_id, stop_id)
