#!/usr/bin/python3
'''
   Does API logs extraction and analysis
'''
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import requests
import core

def api_analysis(api_key, days_back, output):
    '''
      Gets alerts from the API
    '''
    # Calculate dates for a delta and output timestamp:
    days_back = int(days_back)
    raw_date = date.today() + relativedelta(days=-days_back)
    t_date = raw_date.strftime("%d-%m-%Y")
    d_t = datetime.now()
    time_stamp = d_t.strftime("%d-%m-%Y_%H:%M:%S")

    # I know this sucks but their api doesn't understand params when encoded...
    api_url = f"https://api.opsgenie.com/v2/alerts/?query=createdAt>{t_date}&limit=100"
    headers = {
               "Content-Type": "application/json",
               "Authorization": f"GenieKey {api_key}"
              }

    # Get the raw data with pagination
    raw_alerts = []

    while api_url:

        response = requests.get(api_url, headers=headers)

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
    alerts = data[0]
    naughty_hosts = data[1]
    #Create df from list comprehenisons
    alert_rows = [(key, value) for alerts in alerts for key, value in alerts.items()]
    instance_rows = [(key, value) for naughty_hosts in naughty_hosts for key, value
                     in naughty_hosts.items()]
    alert_df = pd.DataFrame(alert_rows, columns=['Alert', 'Count'])
    instance_df = pd.DataFrame(instance_rows, columns=['Instance', 'Count'])

    # Lastly sort and output
    alerts = core.get_counts(alert_df, index="Alert")
    instances = core.get_counts(instance_df, index="Instance")

    print(alerts)
    print(instances)

    core.generate_output(output=output, time_stamp=time_stamp, alerts=alerts, instances=instances)
