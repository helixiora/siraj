#!/usr/bin/python3
'''
   Main entry point for OpsGenie alert analysis
'''
import argparse
import os
import sys
from datetime import date
from dateutil.relativedelta import relativedelta
import alerts_from_api
import alerts_from_csv

def run():
    '''
     Lauft, lauft, lauft
    '''
    parser = argparse.ArgumentParser(description='Siraj, OpsGenie data analysis')
    parser.add_argument('-m','--mode', choices=['api', 'csv'], required=True, help='Run mode')
    parser.add_argument('--file', '-f', help='Path to the file to use')
    parser.add_argument('--output', '-o',
                        help='Path to output HTML file, \
                        if not specifed defaults to local_dir/ops_genie_analysis_TIMESTAMP.html')
    parser.add_argument('--api_key', '-a', help='Key to use')
    parser.add_argument('--days_back', '-d', type=int, help='How many days back to scrape')
    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

    if args.mode == 'api':
       # Since we can't mandate required=True from argparse yet...
        if not args.api_key:
            sys.exit('Please specify API Key with -a option')
        elif not args.days_back:
            sys.exit('Please specify how far back with the -d option')
        else:
            # Generate date and API URL
            raw_date = date.today() + relativedelta(days=-args.days_back)
            t_date = raw_date.strftime("%d-%m-%Y")
            api_url = f"https://api.opsgenie.com/v2/alerts/?query=createdAt>{t_date}&limit=100"
            headers = {
                       "Content-Type": "application/json",
                       "Authorization": f"GenieKey {args.api_key}"
                      }
            alerts_from_api.api_analysis(
                                          api_url=api_url,
                                          headers=headers,
                                          output=args.output
                                        )
    else:
        if args.file:
            if os.path.exists(args.file):
                alerts_from_csv.csv_analysis(
                                              file=args.file,
                                              output=args.output
                                            )
if __name__ == "__main__":
    run()
