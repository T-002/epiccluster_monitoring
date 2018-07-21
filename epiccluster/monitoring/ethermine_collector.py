# !/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright (c) 2018 Christian Schwarz

import datetime
import json
import requests
import time

import collector
from monitoring_configuration import ethereum_wallet_address

class EthermineCollector(collector.Collector):
    """The EthermineCollector uses the ethermine.org API to
    collect relevant runtime statistics about the workers status.
    """

    def __init__(self, update_interval=1):
        """Initializes the EthermineCollector.

        Args:
            update_interval (number): Time in seconds to wait between
                data collections.
        """
        super(EthermineCollector, self).__init__(
            measurement_name="ethermine.org",
            update_interval=update_interval)

        self.tags = ["hostname", "eth_pool"]

        self.eth_pool = "ethermine.org"
        self.ethereum_address = ethereum_wallet_address

        self.api_url = "https://api.ethermine.org/miner/%s/worker/%s/history" % (
            self.ethereum_address, self.hostname)

    def collect(self):
        """This method should be overwritten to implement the data
        collection logic.

        Return:
            list: Returns a list of statistics relevant for the analysis.
        """
        response = requests.get(self.api_url)
        response = json.loads(response.content.decode("utf-8"))

        if response["status"] != "OK":
            print("Could not collect data from ethermine.org.")
            print(response)
            return None

        ethermine_stats = response["data"]
        ethermine_stats = self.parse_stats(ethermine_stats)

        return ethermine_stats

    def parse_stats(self, statistics):
        """Parses the statistics output and returns a list of parsed dictionaries.

        Args:
            statistics (str): String containing the decoded output of the statistics.

        Returns:
            list: The list contains parsed statistic entries with the following keys:
                hostname, gpu_id, measurement, epoch, value.
        """
        parsed_statistics = []

        for stat in statistics:
            try:
                parsed_stat = {
                    "time": datetime.datetime.fromtimestamp(stat["time"]),
                    "eth_pool": self.eth_pool,
                    "hostname": self.hostname,
                    "average_hashrate": int(stat["averageHashrate"]) / 1000000.0,
                    "current_hashrate": int(stat["currentHashrate"]) / 1000000.0,
                    "reported_hashrate": int(stat["reportedHashrate"]) / 1000000.0,
                    "valid_shares": stat["validShares"],
                    "stale_shares": stat["staleShares"],
                    "invalid_shares": stat["invalidShares"]}
            except TypeError:
                continue
            else:
                parsed_statistics.append(parsed_stat)

        return parsed_statistics


def run_collector():
    """Runs the collector and stores the data into Grafana."""
    ethermine_collector = EthermineCollector(600)
    ethermine_collector.start()

    while ethermine_collector.should_run:
        print("[%s] [%s] running." % (datetime.datetime.now(), __file__))
        time.sleep(30)

    ethermine_collector.join()


if __name__ == "__main__":
    run_collector()
