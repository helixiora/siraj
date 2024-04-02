#!/usr/bin/python3
'''
   Main entry point for OpsGenie alert analysis
'''
import argparse
import os
import sys
from datetime import date
from dateutil.relativedelta import relativedelta
import prometheus_analysis

def run():
    '''
     Lauft, lauft, lauft
    '''
    parser = argparse.ArgumentParser(description='Siraj, OpsGenie data analysis',
                                     epilog='Project details https://github.com/lutenica/siraj')
    parser.add_argument('-m','--mode', choices=['api', 'csv'], required=True, help='Run mode')
    parser.add_argument('-s','--source', choices=['prom'], required=True,
                        help='Source of the data in OpsGenie, e.g prometheus.')
    parser.add_argument('--file', '-f', help='Path to the file to use')
    parser.add_argument('--output', '-o',
                        help='Path to output HTML file, \
                        if not specifed defaults to local_dir/ops_genie_analysis_TIMESTAMP.html')
    parser.add_argument('--api_key', '-a', help='Opsgenie API key')
    parser.add_argument('--prometheus_api', '-p',
                        help='Prometheus API endpoint, e.g https://your_prom_instance/api/v1')
    parser.add_argument('--days_back', '-d', type=int, help='How many days back to scrape')
    parser.add_argument('--date_range', nargs=2,
                        help='Data-range for extraction, format should be dd-mm-YYYY dd-mm-YYYY')
    parser.add_argument('--diff', help='URL of previous report to compare to')
    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])
    # Cases for diffferent sources.
    match args.source:
        case "prom":
            if args.mode == 'api':
                # Since we can't mandate required=True from argparse yet...
                if not args.api_key:
                    sys.exit('Please specify API Key with -a option')
                elif not args.prometheus_api:
                    sys.exit('Please specify a prometheus api endpoint URL with -p option')
                elif not args.days_back and not args.date_range:
                    sys.exit('Please specify how far back with the -d option or --date_range')
                else:
                    # Generate date and API URL
                    api_main = "https://api.opsgenie.com/v2/alerts/?query="
                    if args.days_back:
                        raw_date = date.today() + relativedelta(days=-args.days_back)
                        t_date = raw_date.strftime("%d-%m-%Y")
                        period = f'For the last {args.days_back} days'
                        api_query = f'createdAt>{t_date}&limit=100'
                    if args.date_range:
                        s_date = args.date_range[0]
                        e_date = args.date_range[1]
                        period = f'For the {args.date_range[0]} - {args.date_range[1]} period'
                        api_query = f'createdAt%3E{s_date}%20AND%20createdAt%3C{e_date}&limit=100'
                    api = api_main + api_query
                    headers = {
                               "Content-Type": "application/json",
                               "Authorization": f"GenieKey {args.api_key}"
                              }
                    prometheus_analysis.api(
                                             api_url=api,
                                             headers=headers,
                                             prom_endpoint=args.prometheus_api,
                                             diff=args.diff,
                                             period=period,
                                             output=args.output
                                           )
            else:
                if args.file:
                    if os.path.exists(args.file):
                        prometheus_analysis.csv(
                                                 file=args.file,
                                                 output=args.output,
                                                 period="Unknown"
                                               )
        case _:
            print("Tool needs to be extended for additional data sources!")

if __name__ == "__main__":
    run()
