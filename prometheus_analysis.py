#!/usr/bin/python3
# pylint: disable=no-member
'''
   Does API logs extraction and analysis
'''
import time
import pandas as pd
import requests
import core

def get_json_object(url):
    '''
       Returns json object from prom API
    '''
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        return data

    except requests.exceptions.RequestException as error:
        raise SystemExit(error) from None

def api(api_url, headers, prom_endpoint, output):
    '''
      Gets alerts from the API
    '''
    # Calculate dates for a delta and output timestamp:
    # Get the raw data with pagination
    raw_alerts = []

    while api_url:

        try:
            response = requests.get(api_url, headers=headers, timeout=10)

        except requests.exceptions.RequestException as error:

            raise SystemExit(error) from None

        if response.status_code == 200:
            alerts = response.json()
            raw_alerts.extend(alerts.get("data", []))
            paging = alerts['paging']
            try:
                api_url = paging['next']
                # Sleep here as API complains of too many requests
                time.sleep(2)
            except KeyError:
                api_url = None

        else:
            print(f"Error: {response.status_code}, {response.text}")
            break

    targets = core.get_prom_instances(get_json_object(f"{prom_endpoint}/targets"))
    rules = core.get_prom_rules(get_json_object(f"{prom_endpoint}/rules"))
    data = core.prom_data_conversion(raw_alerts, targets, rules)
    # Ingest_api returns a list with two elements, one for alerts the other for instances
    #alert_rows = [(key, value) for data[0] in data[0] for key, value in data[0].items()]
    #instance_rows = [(key, value) for data[1] in data[1] for key, value
    #                 in data[1].items()]
    alerts = pd.DataFrame(data[0], columns=['Alert', 'Count'])
    instances = pd.DataFrame(data[1], columns=['Instance', 'Count'])
    core.generate_output(output=output, alerts=alerts, instances=instances)

def csv(file, output):
    '''
       Takes input CSV file and output destination.
       This mode is to be used for offline data analysis and is unstable in terms of parsing.
    '''
    data = pd.read_csv(file)

    # Actual data manipulation
    data = core.prom_csv_conversion(data)
    alerts = core.get_counts(data, index="Alert")
    instances = core.get_counts(data, index="Instance")
    alerts = core.add_percentages(alerts)
    instances = core.add_percentages(instances)

    # Results
    core.generate_output( output=output, alerts=alerts, instances=instances )
