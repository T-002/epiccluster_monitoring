# EPICCluster - Monitoring
The monitoring subpackage of the epiccluster suite contains many components to monitor the health of your mining rig.

This includes:
  - Temperature and fan monitoroing of NVidia cards
  - Claymore miner monitoring
  - Ethermine.org history data collection

In case you have questions or possible additions, please feel free to contact me.

## Requirements
In order to fully utilize the monitoring tools, you need to install influxDB and Grafana.
Afterwards, you can need to copy the configuration template
(epiccluster/monitoring/monitoring_configuration_template.py)
to a new file called monitoring_configuration in the same directory and configure your parameters.

Afterwards you are able to start the tools with

    python epiccluster/monitoring

All collected data will be inserted into influxDB afterwards and can be used for creating dashboards.

## Future Roadmap
*Weather*: A collector adding your local weather data. This will enable building correlations
between weather and your rig status, especially interesting if you have no AC available.

*External Temperature Sensors*: Collect additional temperature data from
CPU / mainboard / water cooling ĺoop for more detailed insights into your rigs health.

*XVG Miner*: Collect similar information for the XVG miner, as for the currently supported
Claymore version.

*AMD support*: As soon as I collect enough donations to get an actual AMD GPU, I will add support for
AMD as well. 

*Documentation*: As this readme is a little rough, I will add more detailed information and setup
instructions.

*Python Wheel*: A deployable version of the code to make it easier to use for non-developers.

*Docker support*: The creation of a docker container, reducing the setup effort.

*Tests*: A range of tests to ensure the stability of all components.


### Repository Health
[![Code Health](https://landscape.io/github/T-002/epiccluster_monitoring/develop/landscape.svg?style=flat)](https://landscape.io/github/T-002/epiccluster_monitoring/develop)
[![Build Status](https://travis-ci.org/T-002/epiccluster_monitoring.svg?branch=develop)](https://travis-ci.org/T-002/epiccluster_monitoring)

## Donate
If you like the tools and want to support future development, please feel free to donate to the following addresses:

  - BTC 1LJagFDDEvkBmZEryL91XfRdCGKnL99qza
  - ETH 0xE1DFadc976A1cbDE7A1B4A5910A1dF272B5Dba24
  - XVG DDExkAZf8STX9dp8m3ocisBNbXf9g5LpPP
  - BTG GfU5nY1A57DXbaTFVEBjKSb94hKH9fMkqx