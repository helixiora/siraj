#!/usr/bin/python3
'''
   Does API logs extraction and analysis
'''
import pandas as pd
import requests
import core

def api_analysis(api_url, headers, output):
    '''
      Gets alerts from the API
    '''
    # Calculate dates for a delta and output timestamp:
    # Get the raw data with pagination
    raw_alerts = []

    while api_url:

        response = requests.get(api_url, headers=headers, timeout=10)

        if response.status_code == 200:
            alerts = response.json()
            raw_alerts.extend(alerts.get("data", []))
            paging = alerts['paging']
            try:
                api_url = paging['next']
            except KeyError:
                api_url = None

        else:
            print(f"Error: {response.status_code}, {response.text}")
            break

    data = core.ingest_api(raw_alerts)
    # Ingest_api returns a list with two elements, one for alerts the other for instances
    alert_rows = [(key, value) for data[0] in data[0] for key, value in data[0].items()]
    instance_rows = [(key, value) for data[1] in data[1] for key, value
                     in data[1].items()]
    alerts = pd.DataFrame(alert_rows, columns=['Alert', 'Count'])
    instances = pd.DataFrame(instance_rows, columns=['Instance', 'Count'])

    # Lastly sort and output
    alerts = core.get_counts(alerts, index="Alert")
    instances = core.get_counts(instances, index="Instance")

    print(alerts)
    print(instances)
    time_stamp = core.get_timestamp()
    core.generate_output(output=output, time_stamp=time_stamp, alerts=alerts, instances=instances)
