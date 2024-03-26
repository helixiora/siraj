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

    # Results
    print(alerts)
    print(instances)
    time_stamp = core.get_timestamp()
    # Generate output:
    core.generate_output(
                          output=output,
                          time_stamp=time_stamp,
                          alerts=alerts,
                          instances=instances
                        )
