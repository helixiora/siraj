# Siraj, OpsGenie alert analysis tool

Siraj (lamp light in Arabic) helps light (get it?) your way through your OpsGenie alert data.
As we strive to get more from our operations data a lot might get lost in the way. This tool aims to export the valuable information from your
alerts, so that you start seeing the big picture. It's in Arabic because Gennie comes from Jinn.

### Installation

As of right now you need to git clone the source code, I'm working on packaging it so as to distribute a .deb package.

### Requirements

Python > 3.10

Check requirements.txt for modules.

### Usage:

siraj.py [-h] -m {api,csv} [--file FILE] [--output OUTPUT] [--api_key API_KEY] [--days_back DAYS_BACK] [--prometheus]

Siraj, OpsGenie data analysis

options:
  -h, --help            show this help message and exit
  -m {api,csv}, --mode {api,csv}
                        Run mode
  --file FILE, -f FILE  Path to the file to use
  --output OUTPUT, -o OUTPUT
                        Path to output HTML file, if not specifed defaults to local_dir/ops_genie_analysis_TIMESTAMP.html
  --api_key API_KEY, -a API_KEY
                        Key to use
  --days_back DAYS_BACK, -d DAYS_BACK
                        How many days back to scrape
  --prometheus, -p      Additional data manipulation if prometheus was the data source

Note that --api_key, --days_back are REQUIRED when using the api mode.
When using csv mode --file is the only REQUIRED option.

### Examples:

#### API:
```
./siraj.py -m api -a $SOME_KEY -d 10
                           Alert  Count
5               DiskSpace10%Free   1524
9                HighMemoryUsage    228
10                  InstanceDown    148
16                   OutOfMemory    118
8                    HighCpuLoad    100
14               NodeMemoryUsage     88
3               ContextSwitching     48
0           ApacheTooManyWorkers     22
23          SystemdServiceFailed     16
13               MySQLNotRunning     10
2               BlackboxSlowPing      4
22  SslCertificateWillExpireSoon      4
21     ProbeFailedWebUnreachable      4
24                           has      3

                           Instance  Count
11                            host1    884
6                       other_host2    600
84              super_special_host3    316
87                         bad_host    222
83                         sad_host    186
..                              ...    ...
96               i.m.on.a.boat:2343      2
```
#### CSV:

```
./siraj.py -m csv -f /path/to/my/special.csv
                           Alert  Count
5               DiskSpace10%Free   1524
9                HighMemoryUsage    228
10                  InstanceDown    148
16                   OutOfMemory    118
8                    HighCpuLoad    100
14               NodeMemoryUsage     88
3               ContextSwitching     48
0           ApacheTooManyWorkers     22
23          SystemdServiceFailed     16
13               MySQLNotRunning     10
2               BlackboxSlowPing      4
22  SslCertificateWillExpireSoon      4
21     ProbeFailedWebUnreachable      4
24                           has      3

                           Instance  Count
11                            host1    884
6                       other_host2    600
84              super_special_host3    316
87                         bad_host    222
83                         sad_host    186
..                              ...    ...
96               i.m.on.a.boat:2343      2

```
### Alerts from CSV: 

You can use this to pull from a local CSV file if you don't have API access to your target instance.

Arguments: [-h] [--file FILE] [--prometheus]

OPS Genie CSV analyser

options:
  -h, --help            show this help message and exit
  --file FILE, -f FILE  Path to the file to use REQUIRED
  --output, -o          Path to output HTML file, if not specifed defaults to current_working_directory/ops_genie_analysis_$TIMESTAMP.html
  --prometheus, -p      Additional data manipulation if prometheus was the data source, defaults to true.


### Alerts from API:

If you do have API read access you can use this to pull realtime.

usage: alerts_from_api.py [-h] --api_key API_KEY --days_back DAYS_BACK [--output OUTPUT]

OPS Genie API alerts analyser

options:
  -h, --help            show this help message and exit
  --api_key API_KEY, -a API_KEY [REQUIRED]
                        Key to use
  --days_back DAYS_BACK, -d DAYS_BACK (Integer) [REQUIRED]
                        How many days back to scrape
  --output OUTPUT, -o OUTPUT
                        Path to output HTML file, if not specifed defaults to local_dir/ops_genie_analysis_TIMESTAMP.html


### Output and web:

What use is data if we don't have ways to see it?

As you've seen in the examples Siraj outputs data to stdout and it also generates an HTML file. By using the "--output" option you can modify the path and name of this file to be something of your choosing. This way you can either run the tool ad hoc or in some automated way. Then you can serve the file using **any** web server, heck you can even keep an archive of the things to show your progress.

### Limitations

Currently the output file format itself is not plugable/modifiable (see the TODO in core.py).
The only data I have available for it to work with in OpsGenie is Prometheus generated. If I can get my hands on something more I'll extend this so it can interpret that properly too.
I also need to work on building  a .deb package.

### Contributions

Any code contributions are welcome, I reserve the right to review and merge/not merge them. 
