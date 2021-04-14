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


|event_id|city|state|cluster|lon|lat|rad|
|-|-|-|-|-|-|-|

