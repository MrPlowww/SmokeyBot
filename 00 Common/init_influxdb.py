# InfluxDB Initializer: This module initializes the InfluxDB API so that the InfluxDB API can subsequently be used
# by another module.
# 0.0) Prerequisites
#    0.1) Python Dependencies:
#        0.1.a) Python package 'influxdb' shall be installed into the active Python environment (e.g., by running
#                'pip install influxdb' in the environment's terminal window).
#                 Tips: 'https://www.influxdata.com/blog/getting-started-python-influxdb/'.
#        0.1.b) "Microsoft Visual C++ 14.2 standalone: Build Tools for Visual Studio 2019
#               (x86, x64, ARM, ARM64)" shall be installed within Windows. This must be present in order to install
#               Python package 'influxdb-client' (see 0.1.c), in accordance with
#               "https://wiki.python.org/moin/WindowsCompilers" and
#               "https://www.visualstudio.com/downloads/#build-tools-for-visual-studio-2019", which specifies that
#               Build tools's C++ build tools is installed, while selecting the latest versions of
#               "MSVCv142 - VS 2019 C++ x64/x86 build tools" and "Windows 10 SDK".
# 1c. (DONE) installed new dependency "influxdb-client" dependency within Project SmokeyBot.
#        0.1.c) Python package 'influxdb-client' shall be installed into the active Python environment.
#    0.2) Configuration Dependency:
#        0.2.a) InfluxDB shall be installed; InfluxDB shall be running (e.g., in a terminal window, execute:
#                'C:\Users\User\Downloads\00 Brewing\influxdb-1.5.2-1\influxd.exe').
#                 For info on where InfluxDB writes data, see:
#                 'https://stackoverflow.com/questions/43644051/influxdb-storage-folder-windows'.
#        0.2.b) If a target InfluxDB schema does not already exist, then the optional 'reset_database' function must
#                first be executed stand-alone.
# 1.0) Run-time notes:
#   1.1) Usage:
#       1.1.1) standalone?: No.
#       1.1.2) call from another module?: Yes, if using a local instance:
#           >>> import init_influxdb
#           >>> init_influxdb.init_influxdb('<database_name>') # where <database_name> = an existing InfluxDB database,
#                                                              # such as GURU1, BCS5, etc..
#                                                              # If no other arguments are provided, the default host
#                                                              # ('localhost') and default port (8086) will be used.
#      OR if using a cloud instance:
#            >>> with open('<path>/<file>') as file:
#                   influxdb_cloud_credentials = json.load(file)     # where '<path>/<file>' is the location/file of the
#                                                             # JSON file containing the target Twitter account's creds
#                                                             # (e.g., '../influxdb_credentials_Chubby_Bucket1.json')
#           1.1.2.a) IF desired operation is to erase the specified InfluxDB database and re-create it, then:
#               >>> import init_influxdb
#               >>> init_influxdb.reset_database('<database_name>') # where <database_name> = an existing InfluxDB
#                                                                   # database that you wish to erase.
# 2.0) Changelog:
#       Version 1.0: created stand-alone module.
#       Version 2.0: added InfluxDB's cloud functionality. Relocated the data-writing functions from the individual
#           modules into this module (b/c the write is done differently when writing to the Cloud instance vs. when
#           writing to the local instance of InfluxDB.
#


def init_influxdb(target_database, host='localhost', port=8086):
    """ This function initializes the InfluxDB session. This assumes that the target database already exists. If it
    does not, then the 'reset_database' function must be executed first(see below).
        Usage ex: '>>> init_influxdb.init_influxdb(target_database='BCS5',host='localhost', port=8086)'
        The target_database key value shall be a string (I typically use GURU1 for BBQing and BCS5 for brewing).
        The host key value shall be a string and match the running InfluxDB session (default = 'localhost').
        The port key value shall be a integer and match the running InfluxDB session (default = 8086).
     """
    from influxdb import InfluxDBClient
    global client
    client = InfluxDBClient(host, port)  # For more info: https://influxdb-python.readthedocs.io/en/latest/examples.html
    client.switch_database(target_database)  # direct InfluxDB calls to the specified database
    print('init_influxdb.py: Setting InfluxDB database to: ' + str(target_database))
    return client


def reset_database(target_database, host='localhost', port=8086):
    """ CAUTION: This function will erase the specified Influx database and re-create it. Only call this function if
    that is the desired outcome."""
    from influxdb import InfluxDBClient
    client = InfluxDBClient(host, port)
    databases = str(client.get_list_database())  # get the list of databases.
    print('Prior to action taken, the current available databases are: ' + databases)
    confirmation = input('Are you sure you want to erase and reinitialize database ' + str(target_database) + '? (enter Y or N)')
    if confirmation == 'Y':
        client.drop_database(target_database)      # eliminates the specified database (and all data within)
        print('Database ' + target_database + ' erased.')
        databases = str(client.get_list_database())  # get the list of databases.
        print('The remaining databases are: ' + databases + '. Re-initializing database ' + target_database + '.')
        client.create_database(target_database)    # creates the specified database
        print('Database ' + target_database + ' re-initialized.')
        databases = str(client.get_list_database())  # get the list of databases.
        return print('After action taken, the curren tavailable databases are: ' + databases)
    else:
        return print('Aborted - no action taken')


def init_influxdb_cloud():   # could accept inputs as "(token,org,bucket)"
    #from datetime import datetime
    from influxdb_client import InfluxDBClient, Point, WritePrecision
    from influxdb_client.client.write_api import SYNCHRONOUS
    import json
    global client
    global write_api
    global org
    global bucket
    with open('../influxdb_credentials_Chubby_Bucket2.json') as file:  # see Prerequisites 1.1.2
        influxdb_cloud_credentials = json.load(file)
    token = influxdb_cloud_credentials['token']
    org = influxdb_cloud_credentials['org']
    bucket = influxdb_cloud_credentials['bucket']
    client = InfluxDBClient(url="https://us-west-2-1.aws.cloud2.influxdata.com", token=token)
    write_api = client.write_api(write_options=SYNCHRONOUS)  # added this line
    #print('debug: init_influxdb.init_influxdb_cloud(): Initialized InfluxDB Cloud session')
    return client


def write_to_influxdb(instance, data):
    #print('debug: init_influxdb.write_to_influxdb(): Using ' + instance + ' instance of InfluxDB.')
    if instance == 'local':  # if using InfluxDB LOCAL instance, writes the JSON object to InfluxDB
        client.write_points(data)
        #init_influxdb.client.write_points(data)  # depricated
        #print('debug: init_influxdb.write_to_influxdb(): I did it! - I wrote to ' + instance + ' instance!')
        #print('debug: init_influxdb.write_to_influxdb() in local flow')
    elif instance == 'cloud': # if using InfluxDB CLOUD instance, writes the JSON object to InfluxDB CLOUD
        init_influxdb_cloud().write_api().write(bucket, org, data)
        #init_influxdb.client.write_api().write(init_influxdb.bucket, init_influxdb.org,data)  # depricated
        #print('debug: init_influxdb.write_to_influxdb(): I did it! - I wrote to ' + instance + ' instance!')
        #print('debug: init_influxdb.write_to_influxdb() in cloud flow')
    else:
        print('init_influxdb.write_to_influxdb(): failed to specify cloud or local instance of InfluxDB')
        pass
