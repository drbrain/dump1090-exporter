"""
This module defines the metrics that will be exposed to Prometheus.

The metrics are grouped under two top level keys which represent the two data
files that the data is extracted from. Aircraft metrics are extracted from the
data/aircraft.json file. Statistics metrics are extracted from the
data/stats.json file.

Each metric specification item consists of a 3-tuple. The first element
represents a name used within the application to uniquely reference the metric
object. The next two elements represent the Prometheus metric label and its
help string.

When the application creates the actual Prometheus metrics labels it prefixes
`dump1090_` onto each label to namespace the metrics under a common name. In
the case of the stats group of metrics it also adds a `stats_` to the prefix
to group the stats with a common label prefix.

So an item listed under the aircraft section, for example the
'recent_aircraft_observed' item, will end up with a Prometheus metric label of:

.. code-block:: console

    dump1090_recent_aircraft_observed

An item listed under the stats section, for example the 'stats_messages_total'
item, will end up with a Prometheus metric label of:

.. code-block:: console

    dump1090_stats_messages_total

There are multiple sections in the dump1090 stats data file. The Prometheus
multi-dimensional metrics labels are used to expose these. So, to obtain the
stats metrics for the last1min group you would use a metrics label of:

.. code-block:: console

    dump1090_stats_messages_total{job="dump1090", time_period="last1min"}

To extract the totals since the dump1090 application started:

.. code-block:: console

    dump1090_stats_messages_total{job="dump1090", time_period="total"}

"""

Specs = {
    "aircraft": (
        (
            "observed",
            "recent_aircraft_observed",
            "Number of aircraft recently observed",
        ),
        (
            "observed_with_pos",
            "recent_aircraft_with_position",
            "Number of aircraft recently observed with position",
        ),
        (
            "observed_with_mlat",
            "recent_aircraft_with_multilateration",
            "Number of aircraft recently observed with multilateration",
        ),
        (
            "max_range",
            "recent_aircraft_max_range",
            "Maximum range of recently observed aircraft",
        ),
    ),
    "stats": {
        # top level items not in a sub-group are listed under this empty key.
        "": (
            (
                "counter",
                "total",
                "messages",
                "stats_messages_total",
                "Number of Mode-S messages processed",
            ),
            (
                "counter",
                "total",
                "messages_by_df",
                "stats_messages_by_df_total",
                "Number of messages processed by downlink format",
            ),
        ),
        "adaptive": (
            (
                "gauge",
                "last1min",
                "dynamic_range_limit_db",
                "stats_adaptive_dynamic_range_limit_dB",
                "Current dynamic range gain upper limit in dB",
            ),
            (
                "counter",
                "total",
                "gain_changes",
                "stats_adaptive_gain_changes",
                "Number of gain changes caused by adaptive gain control",
            ),
            (
                "gauge",
                "last1min",
                "gain_db",
                "stats_adaptive_gain_dB",
                "Current adaptive gain setting in dB",
            ),
            (
                "counter",
                "total",
                "gain_seconds",
                "stats_adaptive_gain_dB_seconds",
                "Adaptive gain dB by seconds at that level",
            ),
            (
                "counter",
                "total",
                "loud_decoded",
                "stats_adaptive_loud_decoded",
                "Number of loud decoded messages",
            ),
            (
                "counter",
                "total",
                "loud_undecoded",
                "stats_adaptive_loud_undecoded",
                "Number of loud undecoded bursts",
            ),
            (
                "gauge",
                "total",
                "noise_dbfs",
                "stats_adaptive_noise_level_dbFS",
                "Noise level dbFS",
            ),
        ),
        "cpr": (
            (
                "counter",
                "total",
                "airborne",
                "stats_cpr_airborne",
                "Number of airborne CPR messages received",
            ),
            (
                "counter",
                "total",
                "surface",
                "stats_cpr_surface",
                "Number of surface CPR messages received",
            ),
            (
                "counter",
                "total",
                "filtered",
                "stats_cpr_filtered",
                "Number of CPR messages ignored",
            ),
            (
                "counter",
                "total",
                "global_bad",
                "stats_cpr_global_bad",
                "Global positions that were rejected",
            ),
            (
                "counter",
                "total",
                "global_ok",
                "stats_cpr_global_ok",
                "Global positions successfully derived",
            ),
            (
                "counter",
                "total",
                "global_range",
                "stats_cpr_global_range",
                "Global positions rejected due to receiver max range check",
            ),
            (
                "counter",
                "total",
                "global_skipped",
                "stats_cpr_global_skipped",
                "Global position attempts skipped due to missing data",
            ),
            (
                "counter",
                "total",
                "global_speed",
                "stats_cpr_global_speed",
                "Global positions rejected due to speed check",
            ),
            (
                "counter",
                "total",
                "local_aircraft_relative",
                "stats_cpr_local_aircraft_relative",
                "Local positions found relative to a previous aircraft position",
            ),
            (
                "counter",
                "total",
                "local_ok",
                "stats_cpr_local_ok",
                "Local (relative) positions successfully found",
            ),
            (
                "counter",
                "total",
                "local_range",
                "stats_cpr_local_range",
                "Local positions rejected due to receiver max range check",
            ),
            (
                "counter",
                "total",
                "local_receiver_relative",
                "stats_cpr_local_receiver_relative",
                "Local positions found relative to the receiver position",
            ),
            (
                "counter",
                "total",
                "local_skipped",
                "stats_cpr_local_skipped",
                "Local (relative) positions skipped due to missing data",
            ),
            (
                "counter",
                "total",
                "local_speed",
                "stats_cpr_local_speed",
                "Local positions rejected due to speed check",
            ),
        ),
        "cpu": (
            (
                "counter",
                "total",
                "background",
                "stats_cpu_background_milliseconds",
                "Time spent in network I/O, processing and periodic tasks",
            ),
            (
                "counter",
                "total",
                "demod",
                "stats_cpu_demod_milliseconds",
                "Time spent demodulation and decoding data from SDR dongle",
            ),
            (
                "counter",
                "total",
                "reader",
                "stats_cpu_reader_milliseconds",
                "Time spent reading sample data from SDR dongle",
            ),
        ),
        "local": (
            (
                "counter",
                "total",
                "accepted",
                "stats_local_accepted",
                "Number of valid Mode S messages accepted with N-bit errors corrected",
            ),
            (
                "gauge",
                "last1min",
                "signal",
                "stats_local_signal_strength_dbFS",
                "Signal strength dbFS",
            ),
            (
                "gauge",
                "last1min",
                "peak_signal",
                "stats_local_peak_signal_strength_dbFS",
                "Peak signal strength dbFS",
            ),
            (
                "gauge",
                "last1min",
                "noise",
                "stats_local_noise_level_dbFS",
                "Noise level dbFS",
            ),
            (
                "counter",
                "total",
                "strong_signals",
                "stats_local_strong_signals",
                "Number of messages that had a signal power above -3dBFS",
            ),
            (
                "counter",
                "total",
                "bad",
                "stats_local_bad",
                "Number of Mode S preambles that didn't result in a valid message",
            ),
            (
                "counter",
                "total",
                "modes",
                "stats_local_modes",
                "Number of Mode S preambles received",
            ),
            (
                "counter",
                "total",
                "modeac",
                "stats_local_modeac",
                "Number of Mode A/C preambles decoded",
            ),
            (
                "counter",
                "total",
                "samples_dropped",
                "stats_local_samples_dropped",
                "Number of samples dropped",
            ),
            (
                "counter",
                "total",
                "samples_processed",
                "stats_local_samples_processed",
                "Number of samples processed",
            ),
            (
                "counter",
                "total",
                "unknown_icao",
                "stats_local_unknown_icao",
                "Number of Mode S preambles containing unrecognized ICAO",
            ),
        ),
        "remote": (
            (
                "counter",
                "total",
                "accepted",
                "stats_remote_accepted",
                "Number of valid Mode S messages accepted with N-bit errors corrected",
            ),
            (
                "counter",
                "total",
                "bad",
                "stats_remote_bad",
                "Number of Mode S preambles that didn't result in a valid message",
            ),
            (
                "counter",
                "total",
                "modeac",
                "stats_remote_modeac",
                "Number of Mode A/C preambles decoded",
            ),
            (
                "counter",
                "total",
                "modes",
                "stats_remote_modes",
                "Number of Mode S preambles received",
            ),
            (
                "counter",
                "total",
                "unknown_icao",
                "stats_remote_unknown_icao",
                "Number of Mode S preambles containing unrecognized ICAO",
            ),
        ),
        "tracks": (
            ("counter", "total", "all", "stats_tracks_all", "Number of tracks created"),
            (
                "counter",
                "total",
                "single_message",
                "stats_tracks_single_message",
                "Number of tracks consisting of only a single message",
            ),
            (
                "counter",
                "total",
                "unreliable",
                "stats_tracks_unreliable",
                "Number of unreliable tracks",
            ),
        ),
    },
}
