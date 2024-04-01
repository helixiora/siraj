'''
  Core functions
'''
from datetime import datetime
import os
import sys
import numpy as np
import pandas as pd


def get_prom_instances(prom_json):
    '''
       Returns list of all targets from prom api url endpoint
       Takes the json object from requests
    '''
    targets = []
    data = prom_json['data']['activeTargets']
    for target in data:
        instance = target['labels']['instance']
        targets.append(instance)

    return targets

def get_prom_rules(prom_json):
    '''
       Returns list of all configured alerts from prom api
       Takes json objects
    '''
    rules = []
    data = prom_json['data']['groups']
    for group in data:
        for rule in group['rules']:
            rules.append(rule['name'])

    return rules

def prom_csv_conversion(d_f):
    '''
      Returns cleaned up dataframe with colums for alert, instance and count, if source is CSV.
      Takes the dataframe itself.
      Note this relies on slicing so as to keep it offline, so it can have weird behavior
    '''
    a_df = d_f[["Message", "Count"]].copy()
    a_df["Alert"] = a_df["Message"].str.split(" ").str.get(2)
    # Determine if alert is for Disk, for some reason
    # opsgenie interprets the disc as the instance...
    a_df["DiskAlert"] = a_df["Alert"].str.contains("Disk")
    # Based on that we will choose a different field for the instance.
    # Slice me nice
    a_df["Instance"] = np.where(
                                 a_df["DiskAlert"] is False,
                                 a_df["Message"].str.split(" ").str.get(3),
                                 a_df["Message"].str.split(" ").str.get(5)
                               )
    a_df.drop(["Message", "DiskAlert"], axis=1, inplace=True)

    return a_df

def prom_data_conversion(data, targets, rules):
    '''
      Returns list of 2 lists, one containing the alerts, the other the naughty hosts
      Takes data (raw data from opsgenie), list of targets and list of rules.
    '''
    alerts = []
    naughty_hosts = []
    for val in data:
        raw_alert = dict((k, val[k]) for k in ['message', 'count']
                          if k in val)

        message = raw_alert['message']
        count = raw_alert['count']
        # Find out if our target is contained in the list of hosts
        # Somehow this doesn't work with any so using list comp...
        # This also mandates the if clause to skip unmatched targets.
        target = [ t for t in targets if t in message ]
        if len(target) < 1:
            continue
        instance = (target[0], count)
        naughty_hosts.append(instance)
        # List comprehension here again since any didn't work...
        # Crash out here as final check as obviously our source data
        # isn't purely prometheus. This needs to be changed when we add
        # more sources to simply skip over it (there can be mixed opsgenies)
        rule = [ r for r in rules if r in message ]
        if len(rule) < 1:
            sys.exit(f"{message} isn't configured in prometheus.")
        alert = (rule[0], count)
        alerts.append(alert)

    return([alerts, naughty_hosts])

def add_percentages(d_f):
    '''
       Takes a dataframe.
       Returns a dataframe with added percentages and sums.
    '''
    # Add sum
    sum_num = d_f.sum(numeric_only=True)['Count']
    a_sum = ('Total', sum_num)
    d_f.loc[len(d_f)] = a_sum
    # Calc percentage
    d_f['Percentage'] = (round((d_f["Count"] / sum_num), 4)) * 100

    return d_f

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

def generate_output(output, alerts, instances):
    '''
      Do final sorting of the dataframes.
      Generates html file output.
      Takes output path, alerts (dataframe) and instances (dataframe)
      If output isn't specified writes to current dir.
    '''
    alerts = get_counts(alerts, index="Alert")
    instances = get_counts(instances, index="Instance")
    alerts = add_percentages(alerts)
    instances = add_percentages(instances)
    time_stamp = get_timestamp()
    print(alerts)
    print(instances)
    if not output:
        output = os.getcwd() + "/ops_genie_analysis_" + time_stamp + ".html"
    # Consider using a template file and concatenate that.
    output_content_0 = f"<h2>Generated @ {time_stamp}</h2>"
    output_content_1 = "<h2> Alerts: </h2>" + "\n" + alerts.to_html(justify="center", index=False)
    output_content_2 = "\n" + "<h2> Naughty Hosts: </h2>" + "\n"
    output_content_3 = instances.to_html(justify="center", index=False)
    output_content = output_content_0 + output_content_1 + output_content_2 + output_content_3
    with open(output, 'w', encoding='UTF-8') as output_file:
        output_file.write(output_content)
