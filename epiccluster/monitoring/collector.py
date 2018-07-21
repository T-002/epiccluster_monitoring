# !/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright (c) 2018 Christian Schwarz

import subprocess
import threading
import time

from influxdb import InfluxDBClient
from monitoring_configuration import influxdb_connection


class Collector(threading.Thread):
    """The Collector is the base class for all data collectors
    of the mining monitoring.

    The Collector is responsible to collect the data from the
    corresponding third-party tool and can be used to request the
    current status.
    """

    def __init__(self, measurement_name, update_interval=1):
        """Initializes the Collector.

        Args:
            measurement_name (str): Name of the measurement to be collected.
            update_interval (number): Time in seconds to wait between
                data collections.
            """
        super(Collector, self).__init__()

        self.update_interval = update_interval
        self.should_run = True

        self.hostname = subprocess.check_output("hostname").decode().replace("\n", "")
        self.measurement_name = measurement_name

        self.tags = []

        self.database = InfluxDBClient(**influxdb_connection)

    def stop(self):
        """Stops the Collector. This will stop the collection loop."""
        self.should_run = False

    def run(self):
        """The main collection loop of the Collector.

        This method is executed until Collector.stop() is called.
        """
        while self.should_run:
            stats = self.collect()
            time.sleep(self.update_interval)

            if stats is None:
                continue

            self.store_stats(stats)

    def collect(self):
        """This method should be overwritten to implement the data
        collection logic.

        Return:
            list: Returns a list of statistics relevant for the analysis.
        """
        raise NotImplementedError

    def store_stats(self, stats):
        """Stores the statistics into the backend.

        Args:
            stats (list): List of statistics to be stored into the backend.
        """
        influx_stats = []

        for stat in stats:
            fields = {}
            for key in stat:
                if key == "time":
                    continue

                if key in self.tags:
                    continue


                fields[key] = stat[key]

            tags = {}
            for key in self.tags:
                tags[key] = stat[key]

            influx_stats.append({
                "time": stat["time"],
                "measurement": self.measurement_name,
                "tags": tags,
                "fields": fields
            })

        self.database.write_points(influx_stats)
