# SmokeyBot
This program gets status from the BBQ Guru API, formats it, writes it to an InfluxDB database (for external # visualization (e.g., Grafana) and data-logging purposes), and live-tweets BBQ session info.

# 0.0) Prerequisites
#   0.1) Python Dependencies:
       0.1.a) Python package 'influxdb' shall be installed into the active Python environment (e.g., by running
               'pip install influxdb' in the environment's terminal window).
                Tips: 'https://www.influxdata.com/blog/getting-started-python-influxdb/'
       0.1.b) Python module 'init_influxdb.py' shall be present in the active Python environment path (possibly in
               a Common directory, since this module is used in other unrelated Projects).
       0.1.c) Python package 'tweepy' shall be installed into the active Python environment (e.g., by running
               'pip install tweepy' in the environment's terminal window). This is required for 'init_twitter_api.py'
               and 'tweet.py'. Tweepy API definition: 'http://docs.tweepy.org/en/latest/api.html'
       0.1.d) Python module 'init_twitter_api.py' shall be present in the active Python environment path (possibly in
              a Common directory, since this module is used in other unrelated Projects). This module accepts
              JSON-formatted Twitter credentials (key:values), and returns a usable Twitter API.
       0.1.e) Python module 'tweet.py' shall be present in the active Python environment path (possibly in
              a Common directory, since this module is used in other unrelated Projects). This module accepts
              the 'api' object (returned by 'init_twitter_api.py) as a required argument, and it accepts N number of
              additional string-formatted arguments. The 'tweet.py' module concatenates the string-formatted arguments
              (so be careful about spaces/punctuation in the arguments) and tweets-out the result (using the passed
              api.
       0.1.f) Python module 'message_generator.py' shall be present in the active Python environment path (possibly
              in a Common directory, since this module is used in other unrelated Projects).
       0.1.g) Python package 'untangle' shall be installed into the active Python environment (e.g., by running
              'pip install untangle' in the environment's terminal window).
#   0.2) Configuration Dependencies:
      0.2.a) InfluxDB shall be installed; InfluxDB shall be running (e.g., by running this in a terminal window:
               'C:\Program Files\InfluxDB\influxd.exe" run reporting-disabled'.
                For info on where InfluxDB writes data, see:
                'https://stackoverflow.com/questions/43644051/influxdb-storage-folder-windows'.
       0.2.b) If a target InfluxDB schema does not already exist, then the optional 'reset_database' function must
               first be executed stand-alone.
       0.2.c) The BBQ Guru shall be accessible on the network at a known IP address (e.g., 'http://192.168.1.83').
              The BBQ Guru web pages are '<IP_address>/all.xml', '<IP_address>/status.xml', and
              '<IP_address>/config.xml'.
              BBQ Guru 'STATUS' dictionary: 0 = 'OK' (applies to all), 1 = 'HIGH' (cook status only),
              2 = 'LOW' (cook status only), 3 = 'DONE' (food status only), 4 = 'ERROR' (cook and food status only),
              5 = 'HOLD' (timer status only), 6 = 'ALARM' (timer status only), and 7 = 'SHUTDOWN' (timer status only).
       0.2.d) Grafana: Grafana shall be installed; Grafana server shall be running.
               The Grafana UI is accessed via 'http://localhost:3000' (default user = admin; default pw = admin).
       0.2.e) Twitter: The target Twitter account shall be properly setup for app access, with the proper access
               credentials saved into a JSON-formatted file one directory level higher than this Python module
               (e.g., '../''twitter_credentials_G2Chubby.json'). See these websites for tips/reference:
               'http://stackabuse.com/accessing-the-twitter-api-with-python/',
               'http://nodotcom.org/python-twitter-tutorial.html'.
# 1.0) Run-time notes:
#  1.1) Usage:
      1.1.1) standalone?: Yes.
          >>> 'exec(open('smokey_bot.py').read())'
      1.1.2) call from another module?: No.
# 2.0) Changelog:
      Version 1.0: Original version.
      Version 1.1: Refactored InfluxDB writing so that there's flexibility for local or cloud instance usage.
      Version 2.0 - 2020-11-25: Refactored entire program to leverage individual functions.
      Version 2.01 - 2021-08-15: Cleaned-up some slop.
      Versions 2.1 - 2021-11-14: Improved object handling and removed deprecated code.
