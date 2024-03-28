#!/usr/bin/python3
'''
  Does CSV analysis related functions
'''
import pandas as pd
import core

# Argument parsing

def csv_analysis(file, output):
    '''
      Prints instances and alerts dataframes, generates output file.
    '''
    data = pd.read_csv(file)

    # Actual data manipulation
    data = core.sanatize(data)
    alerts = core.get_counts(data, index="Alert")
    instances = core.get_counts(data, index="Instance")
    alerts = core.add_percentages(alerts)
    instances = core.add_percentages(instances)

    # Results
    core.generate_output( output=output, alerts=alerts, instances=instances )
