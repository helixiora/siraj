#!/usr/bin/python3
'''
  Does CSV analysis related functions
'''
from datetime import datetime
import pandas as pd
import core

# Argument parsing

def csv_analysis(file, output):
    '''
      Prints instances and alerts dataframes, generates output file.
    '''
    data = pd.read_csv(file)
    d_t = datetime.now()
    time_stamp = d_t.strftime("%d-%m-%Y_%H:%M:%S")

    # Actual data manipulation
    data = core.sanatize(data)
    alerts = core.get_counts(data, index="Alert")
    instances = core.get_counts(data, index="Instance")

    # Results
    print(alerts)
    print(instances)

    # Generate output:
    core.generate_output(
                          output=output,
                          time_stamp=time_stamp,
                          alerts=alerts,
                          instances=instances
                        )
