# !/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright (c) 2018 Christian Schwarz

import subprocess
import time
import datetime
import collector


class NvidiaCollector(collector.Collector):
    """The NvidiaCollector is responsible to collect all GPU relevant information, such as temperature,
    powerlimit, fan speed, and more.

    Those data points are collected independently from the
    mined crypto currency.
    """

    def __init__(self, update_interval=1):
        """Initializes the NvidiaCollector.

        Args:
            update_interval (number): Time in seconds to wait between
                data collections.
        """
        super(NvidiaCollector, self).__init__(
            measurement_name="nvidia_gpu",
            update_interval=update_interval)

        self.tags = ["hostname", "gpu_id"]

    def collect(self):
        """Collects the data for all GPUs.

        Return:
            list: Returns a list of statistics relevant for the analysis.
        """
        nvidia_stats = subprocess.check_output(["nvidia-smi", "stats", "-c", "1"])
        nvidia_stats = nvidia_stats.decode()
        nvidia_stats = nvidia_stats.split("\n")
        nvidia_stats = nvidia_stats[:-1]
        nvidia_stats = self.parse_stats(nvidia_stats)
        nvidia_stats = self.aggregate_stats(nvidia_stats)

        return nvidia_stats

    def parse_stats(self, statistics):
        """Parses the statistics output and returns a list of parsed dictionaries.

        Args:
            statistics (str): String containing the decoded output of the statistics.

        Returns:
            list: The list contains parsed statistic entries with the following keys:
                hostname, gpu_id, measurement, epoch, value.
        """
        parsed_statistics = []

        for entry in statistics:
            entry = entry.split(",")
            parsed_statistics.append({
                "hostname": self.hostname,
                "gpu_id": int(entry[0].strip()),
                "measurement": entry[1].strip(),
                "epoch": int(entry[2].strip()),
                "value": int(entry[3].strip())
            })

        return parsed_statistics

    def aggregate_stats(self, statistics):
        """Aggregates the parsed stats to their average and returns the smoothed stats
        for the highest time stamp.

        Args:
            statistics (list): Parsed statistics containing the required information.

        Returns:
            list: Returns a list containing the aggregated stats for each GPU.
        """
        hostname = self.hostname
        gpu_ids = set([stat["gpu_id"] for stat in statistics])

        aggregated_statistics = []

        for gpu_id in gpu_ids:
            aggregated_stat = {
                "hostname": hostname,
                "gpu_id": gpu_id,
                "time": datetime.datetime.now()
            }

            gpu_measurements = list(filter(lambda s: s["gpu_id"] == gpu_id, statistics))
            measures = set([stat["measurement"] for stat in gpu_measurements])

            for measurement in measures:
                values = [stat["value"] for stat in filter(lambda s: s["measurement"] == measurement, gpu_measurements)]
                aggregated_stat[measurement] = int(sum(values) / len(values))

            aggregated_statistics.append(aggregated_stat)

        return aggregated_statistics


def run_collector():
    """Runs the collector and stores the data into Grafana."""
    nvidia_collector = NvidiaCollector(5)
    nvidia_collector.start()

    while nvidia_collector.should_run:
        print("[%s] [%s] running." % (datetime.datetime.now(), __file__))
        time.sleep(5)

    nvidia_collector.join()


if __name__ == "__main__":
    run_collector()
