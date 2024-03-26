'''
  Core functions
'''
from datetime import datetime
import os
import numpy as np
import pandas as pd


def sanatize(d_f):
    '''
      Returns cleaned up dataframe with colums for alert, instance and count, if source is CSV.
      First arg is the dataframe itself.
      Here we can add data wrangling when source is != prometheus.
    '''
    a_df = d_f[["Message", "Count"]].copy()
    a_df["Alert"] = a_df["Message"].str.split(" ").str.get(2)
    # Determine if alert is for Disk, for some reason
    # opsgenie interprets the disc as the instance...
    a_df["DiskAlert"] = a_df["Alert"].str.contains("Disk")
    # Based on that we will choose a different field for the instance:
    a_df["Instance"] = np.where(
                                 a_df["DiskAlert"] is False,
                                 a_df["Message"].str.split(" ").str.get(3),
                                 a_df["Message"].str.split(" ").str.get(5)
                               )
    a_df.drop(["Message", "DiskAlert"], axis=1, inplace=True)

    return a_df

def ingest_api(data):
    '''
      Returns list of 2 elements: alerts and hosts data from
      provided source data from API. This also needs modification when source is != prometheus.
    '''
    alerts = []
    naughty_hosts = []
    for val in data:
        raw_alert = dict((k, val[k]) for k in ['message', 'count']
                          if k in val)

        # For some reason with disk full alerts it interprets the disk as the instance
        message = raw_alert['message']
        if "Disk" in message:
            split = 5
        else:
            split = 3

        instance = message.split(" ")[split]
        count = raw_alert['count']
        alert = { message.split(" ")[2]: count }
        host = { instance: count }
        alerts.append(alert)
        naughty_hosts.append(host)

    return([alerts, naughty_hosts])


def get_counts(d_f, index):
    '''
      Takes a dataframe and index.
      Returns a dataframe with sums of count by index.
    '''
    a_df = d_f.groupby(index)['Count'].sum()
    a_df = pd.DataFrame({index:a_df.index, 'Count':a_df.values})
    return a_df.sort_values('Count', ascending=False)

def get_timestamp():
    '''
      Returns timestamp string to be used in file naming
    '''
    d_t = datetime.now()
    time_stamp = d_t.strftime("%d-%m-%Y_%H:%M:%S")
    return time_stamp

def generate_output(output, time_stamp, alerts, instances):
    '''
      Generates html file output.
      Takes output path, time_stamp, alerts (dataframe) and instances (dataframe)
      If output isn't specified writes to current dir.
    '''
    if not output:
        output = os.getcwd() + "/ops_genie_analysis_" + time_stamp + ".html"
    # Consider using a template file and concatenate that.
    output_content_1 = "<h2> Alerts: </h2>" + "\n" + alerts.to_html(justify="center", index=False)
    output_content_2 = "\n" + "<h2> Naughty Hosts: </h2>" + "\n"
    output_content_3 = instances.to_html(justify="center", index=False)
    output_content = output_content_1 + output_content_2 + output_content_3
    with open(output, 'w', encoding='UTF-8') as output_file:
        output_file.write(output_content)
    output_file.close()
