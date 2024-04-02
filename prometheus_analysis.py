#!/usr/bin/python3
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

def api(**kwargs):
    '''
      Gets alerts from the API
      Takes the API URL, any headers, the previous report,
      a prometheus endpoint and the desired output location.
      Returns nothing, does printing.
      We only do kwargs because 6 arguments is too many
    '''
    # Calculate dates for a delta and output timestamp:
    # Get the raw data with pagination
    raw_alerts = []
    api_url = kwargs['api_url']
    headers = kwargs['headers']
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
    # Get targets
    targets = core.get_prom_instances(get_json_object(f"{kwargs['prom_endpoint']}/targets"))
    rules = core.get_prom_rules(get_json_object(f"{kwargs['prom_endpoint']}/rules"))
    # nom nom data
    data = core.prom_data_conversion(raw_alerts, targets, rules)
    alerts = pd.DataFrame(data[0], columns=['Alert', 'Count'])
    instances = pd.DataFrame(data[1], columns=['Instance', 'Count'])
    # Now to generate a list of the old dataframes.
    core.generate_output(output=kwargs['output'], alerts=alerts,
                         diff=kwargs['diff'], instances=instances, period=kwargs['period'])

def csv(file, output, period):
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
    core.generate_output( output=output, alerts=alerts, diff=None,
                          instances=instances, period=period )
