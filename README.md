# Immune Deficiency Foundation Walk for Primary Immunodeficiency Email Tool

This tool automates creation of segmented email lists for the IDF Walk for PI.

## Quick Start

1. Run `pip install -r requirements.txt` to ensure that you have all of the required packages.
2. Make sure that you have opened an ssh connection to the server.
3. Run `python report.py` to generate the report. You will be asked to enter the database password.
4. The report will be saved to the `output` folder.

## Configuration

Each year the walk team will need to update the `config.csv` file with the walks for the current year.
This file should be finalized before the walk season starts.
Any changes that are made to the `config.csv` file during the walk season can cause geographical boundaries to be redrawn and result in inconsistent email delivery.

The table below provides a few example rows from the `config.csv` file.

|event_id|city|state|cluster|lon|lat|rad|
|-|-|-|-|-|-|-|
|1142|Atlanta| GA|Stripes|-84.3879824|33.7489954|200|
|1143|Baltimore| MD|Blue|-76.6121893|39.2903848|100|
|1137|Boston| MA|Stripes|-71.0588801|42.3600825|60|
|1163|Charleston| SC|Blue|-79.9310512|32.7764749|200|
|1138|Chicago| IL|White|-87.6297982|41.8781136|100|
|1145|Cleveland| OH|Blue|-81.6943605|41.49932|150|

* `event_id` is the Civi Event ID for the walk.
* `city` is the city where the walk will occur.
* `state` is the state where the walk will occur.
* `lon` is the longitude of the walk location.
* `lat` is the latitude of the walk location.
* `rad` is the maximum radius, in miles, from the walk location that will be included in that walks geographical region.

