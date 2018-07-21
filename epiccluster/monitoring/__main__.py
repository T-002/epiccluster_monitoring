# !/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright (c) 2018 Christian Schwarz

"""This module starts all collectors in a separate thread."""

from claymore_collector import ClaymoreCollector
from ethermine_collector import EthermineCollector
from nvidia_collector import NvidiaCollector

import time

if __name__ == "__main__":
    print("Sleeping for 30 seconds.")
    time.sleep(30)

    collectors = list()
    collectors.append(ClaymoreCollector(5))
    collectors.append(EthermineCollector(7200))
    collectors.append(NvidiaCollector(5))

    for collector in collectors:
        collector.start()

    while True:
        time.sleep(30)
        running_collectors = list(filter(lambda c: c.should_run, collectors))
        running_collectors = [collector.__class__.__name__ for collector in running_collectors]
        print("Running Collectors: %s" % ", ".join(running_collectors))
