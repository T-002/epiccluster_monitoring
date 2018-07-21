# !/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright (c) 2018 Christian Schwarz

import datetime
import json
import socket
import time
import os

import collector

class ClaymoreCollector(collector.Collector):
    """The ClaymoreCollector uses the Claymore miner interface to
    extract relevant runtime statistics about the workers status.
    """

    def __init__(self, update_interval=1):
        """Initializes the ClaymoreCollector.

        Args:
            update_interval (number): Time in seconds to wait between
                data collections.
        """
        super(ClaymoreCollector, self).__init__(
            measurement_name="eth_miner",
            update_interval=update_interval)

        self.tags = ["hostname", "gpu_id", "eth_pool", "claymore_version"]
        self.claymore_password = os.getenv("CLAYMORE_PASSWORD")

    def collect(self):
        """Collects the data for all GPUs.

        Return:
            list: Returns a list of statistics relevant for the analysis.
        """
        claymore_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        claymore_socket.connect(("localhost", 3333))

        claymore_socket.send(('{"id":0,"jsonrpc":"2.0","method":"miner_getstat1","psw":"%s"}' % self.claymore_password).encode("utf-8"))
        claymore_stats = claymore_socket.recv(2048)
        claymore_socket.close()
        claymore_stats = json.loads(claymore_stats.decode("utf-8"))

        if claymore_stats["error"]:
            return None

        claymore_stats = claymore_stats["result"]
        claymore_stats = self.parse_stats(claymore_stats)

        return claymore_stats

    def parse_stats(self, statistics):
        """Parses the statistics output and returns a list of parsed dictionaries.

        Args:
            statistics (str): String containing the decoded output of the statistics.

        Returns:
            list: The list contains parsed statistic entries with the following keys:
                hostname, gpu_id, claymore_version, eth_pool, time, hashrate.
        """
        # uptime = statistics[1]
        # total_hashrate, total_shares, rejected_shares = statistics[2].split(";")

        # gpu_temp_fanspeed = statistics[6].split(";")
        # eth_invalid_shares = statistics[8].split(";") # invalid eth, eth pool switches, invalid dcr, dcr pool switch

        epoch = time.time()
        parsed_statistics = []

        gpu_hashrates = statistics[3].split(";")
        for gpu_id in range(len(gpu_hashrates)):
            gpu_hashrate = gpu_hashrates[gpu_id]
            if gpu_hashrate == "off":
                gpu_hashrate = 0

            parsed_statistics.append({
                "hostname": self.hostname,
                "gpu_id": gpu_id,
                "claymore_version": statistics[0],
                "eth_pool": statistics[7],
                "time": datetime.datetime.now(),
                "hashrate": int(gpu_hashrate) / 1000.0
            })

        return parsed_statistics


def run_collector():
    """Runs the collector and stores the data into Grafana."""
    claymore_collector = ClaymoreCollector(5)
    claymore_collector.start()

    while claymore_collector.should_run:
        print("[%s] [%s] running." % (datetime.datetime.now(), __file__))
        time.sleep(5)

    claymore_collector.join()


if __name__ == "__main__":
    run_collector()
