# Smokey Bot: This program gets status from the BBQ Guru API, formats it, writes it to an InfluxDB database (for external
# visualization (e.g., Grafana) and data-logging purposes), and live-tweets BBQ session info.
# 0.0) Prerequisites
#    0.1) Python Dependencies:
#        0.1.a) Python package 'influxdb' shall be installed into the active Python environment (e.g., by running
#                'pip install influxdb' in the environment's terminal window).
#                 Tips: 'https://www.influxdata.com/blog/getting-started-python-influxdb/'
#        0.1.b) Python module 'init_influxdb.py' shall be present in the active Python environment path (possibly in
#                a Common directory, since this module is used in other unrelated Projects).
#        0.1.c) Python package 'tweepy' shall be installed into the active Python environment (e.g., by running
#                'pip install tweepy' in the environment's terminal window). This is required for 'init_twitter_api.py'
#                and 'tweet.py'. Tweepy API definition: 'http://docs.tweepy.org/en/latest/api.html'
#        0.1.d) Python module 'init_twitter_api.py' shall be present in the active Python environment path (possibly in
#               a Common directory, since this module is used in other unrelated Projects). This module accepts
#               JSON-formatted Twitter credentials (key:values), and returns a usable Twitter API.
#        0.1.e) Python module 'tweet.py' shall be present in the active Python environment path (possibly in
#               a Common directory, since this module is used in other unrelated Projects). This module accepts
#               the 'api' object (returned by 'init_twitter_api.py) as a required argument, and it accepts N number of
#               additional string-formatted arguments. The 'tweet.py' module concatenates the string-formatted arguments
#               (so be careful about spaces/punctuation in the arguments) and tweets-out the result (using the passed
#               api.
#        0.1.f) Python module 'message_generator.py' shall be present in the active Python environment path (possibly
#               in a Common directory, since this module is used in other unrelated Projects).
#        0.1.g) Python package 'untangle' shall be installed into the active Python environment (e.g., by running
#               'pip install untangle' in the environment's terminal window).
#    0.2) Configuration Dependencies:
#        0.2.a) InfluxDB shall be installed; InfluxDB shall be running (e.g., by running this in a terminal window:
#                'C:\Program Files\InfluxDB\influxd.exe" run reporting-disabled'.
#                 For info on where InfluxDB writes data, see:
#                 'https://stackoverflow.com/questions/43644051/influxdb-storage-folder-windows'.
#        0.2.b) If a target InfluxDB schema does not already exist, then the optional 'reset_database' function must
#                first be executed stand-alone.
#        0.2.c) The BBQ Guru shall be accessible on the network at a known IP address (e.g., 'http://192.168.1.83').
#               The BBQ Guru web pages are '<IP_address>/all.xml', '<IP_address>/status.xml', and
#               '<IP_address>/config.xml'.
#               BBQ Guru 'STATUS' dictionary: 0 = 'OK' (applies to all), 1 = 'HIGH' (cook status only),
#               2 = 'LOW' (cook status only), 3 = 'DONE' (food status only), 4 = 'ERROR' (cook and food status only),
#               5 = 'HOLD' (timer status only), 6 = 'ALARM' (timer status only), and 7 = 'SHUTDOWN' (timer status only).
#        0.2.d) Grafana: Grafana shall be installed; Grafana server shall be running.
#                The Grafana UI is accessed via 'http://localhost:3000' (default user = admin; default pw = admin).
#        0.2.e) Twitter: The target Twitter account shall be properly setup for app access, with the proper access
#                credentials saved into a JSON-formatted file one directory level higher than this Python module
#                (e.g., '../''twitter_credentials_G2Chubby.json'). See these websites for tips/reference:
#                'http://stackabuse.com/accessing-the-twitter-api-with-python/',
#                'http://nodotcom.org/python-twitter-tutorial.html'.
# 1.0) Run-time notes:
#   1.1) Usage:
#       1.1.1) standalone?: Yes.
#           >>> 'exec(open('smokey_bot.py').read())'
#       1.1.2) call from another module?: No.
# 2.0) Changelog:
#       Version 1.0: Original version.
#       Version 1.1: Refactored InfluxDB writing so that there's flexibility for local or cloud instance usage.
#       Version 2.0 - 2020-11-25: Refactored entire program to leverage individual functions.
#       Version 2.01 - 2021-08-15: Cleaned-up some slop.
#       Versions 2.1 - 2021-11-14: Improved object handling and removed deprecated code.

#  ****** Section 0 - Import Modules ******
import init_influxdb  # See Prerequisite 0.1.a and 0.1.b.; used by configure_database().
import json  # required to parse Twitter credentials file; used by configure_twitter().
import init_twitter_api  # Prerequisite 0.1.d (Twitter API init module), 0.1.c ('tweepy' package), & 0.2.e (Twitter)
#                           used by configure_twitter().
import tweet  # See Prerequisite 0.1.e ('tweet.py' module); used by configure_message_generator().
import message_generator  # See Prerequisite 0.1.f ('message_generator' module); used by configure_message_generator().
from time import gmtime, strftime, sleep  # needed for processing GMT/current time and for loop delay (sleep)
import untangle  # See Prerequisite 0.1.g. (needed to parse the sloppy XML from the BBQ Guru).


def configure_program():
    """ Section 0 - Program Control: This function captures the essential configuration variables (static and dynamic)
     used to control program behavior, and stores them as a dictionary (smokey_config) to be read/updated by other
     functions."""
    smokey_config = {'tweet_enabled': False,  # when "True", program will attempt to Tweet status
                     'cloud_enabled': False,  # when "True", program writes data to Cloud instance of InfluxDB
                     'debug_enabled': False,  # when "True", program will print internal status messages to the screen
                     'message_debug_enabled': False,  # when "True", prints message_generator to screen every iteration.
                     'first_tweet_flag': 1,  # initialize first tweet flag for one-time-only tweeting (it later gets
                                             # set to 0 forever)
                     'loop_delay': 2,  # This dictates how many seconds to delay before looping back through the
                                       # program. This same number is used to set the initial value and decrement amount
                                       # for meat_tweet_delay and message_delay so that everything decrements in
                                       # lockstep with the loop delay.
                     'message_delay': 2,  # initially set random message delay (same as 'loop_delay'); this gets reset
                                          # to the 'static_message_generator_tweet_delay' value once it hits 0.
                     'meat_tweet_delay': 2,  # initially set meat tweet delay (same as 'loop_delay'); this gets reset to
                                             # the 'static_meat_tweet_delay' value once it hits 0.
                     'static_message_generator_tweet_delay': 450,  # Recommended value = 500 (in seconds, a.k.a. 8.3
                                                                   # minutes)
                     'static_meat_tweet_delay': 600,  # Recommended value = 600 (in seconds, a.k.a. 10 minutes)
                     'GURU_IP': 'http://192.168.1.83',  # Network IP for BBQ Guru (e.g., 'http://192.168.1.83')
                     'food_temp_init_counter': [10, 10, 10, 10],
                     # The above line initializes probe 0-3's reporting delay, activated when value changes from null
                     # to integer (first ~50 seconds of values are garbage when prob is first plugged in).
                     'food_temp_unplugged_counter': [10, 10, 10, 10],
                     # The above line initializes 'probe 0-3 unplugged' detector delay, activated when previous reading
                     # is very different than current reading (first ~10 seconds of readings are garbage).
                     'influx_target_db': 'GURU1',  # defines the target InfluxDB schema/instance.
                     'influx_target_host': 'localhost',  # defines the target InfluxDB IP (if not using cloud instance).
                     'influx_target_port': 8086  # defines the target InfluxDB port (if not using cloud instance).
                     }
    print(f"SmokeyBot config: tweet_enabled = {smokey_config['tweet_enabled']}, "
          f"cloud_enabled = {smokey_config['cloud_enabled']}")
    return smokey_config


def configure_database():
    """" Section 1 - Initialize InfluxDB session: This function initializes the InfluxDB instance (either local or
    cloud instance). """
    if smokey_config['cloud_enabled'] == False:  # if using LOCAL instance of InfluxDB
        init_influxdb.init_influxdb(target_database=smokey_config['influx_target_db'],
                                    host=smokey_config['influx_target_host'],
                                    port=smokey_config['influx_target_port'])
        instance = 'local'
        print(f"SmokeyBot config: Using {instance} instance of InfluxDB with "
              f"target_database = {smokey_config['influx_target_db']}, "
              f"host = {smokey_config['influx_target_host']}, and "
              f"port = {smokey_config['influx_target_port']}.")
    else:  # if using CLOUD instance of InfluxDB
        init_influxdb.init_influxdb_cloud()
        instance = 'cloud'
        print(f"smokey_bot.py: Using {instance} instance of InfluxDB.")
    return instance


def configure_twitter():
    """ SECTION 2 - Initialize Twitter API """
    with open('../twitter_credentials_G2Chubby.json') as file:  # Prerequisites 0.2.e (@G2ChubbySmoker's Twitter keys)
        twitter_credentials = json.load(file)
    api = init_twitter_api.init_twitter_api(twitter_credentials)  # create object ('api') portal to Twitter API
    return api  # used as twitter_api_config


def get_data_food():
    """ This function gets data from the BBQ Guru CyberQ's API (all.xml) and stores it into properly formatted
      lists, where index 0 = the pit temperature, index 1 = temperature probe 1, index 2 = temperature probe 2,
      and index 3 = temperature probe 3. Additionally, the function includes logic to correct/suppress error-conditions
      that occur when a temperature prop is inserted/removed during operation. """
    food_temp_previous = [None, None, None, None]
    food_temp = ['COOK_TEMP', 'FOOD1_TEMP', 'FOOD2_TEMP', 'FOOD3_TEMP']  # Required to build the string
    food_temp_meas = [None, None, None, None]
    food_set = ['COOK_SET', 'FOOD1_SET', 'FOOD2_SET', 'FOOD3_SET']  # Required to build the string
    food_set_meas = [None, None, None, None]
    food_status = ['COOK_STATUS', 'FOOD1_STATUS', 'FOOD2_STATUS', 'FOOD3_STATUS']  # Required to build the string
    food_status_meas = [None, None, None, None]
    twitter_food_temp = [None, None, None, None]
    twitter_food_set = [None, None, None, None]
    food_id = ['COOK', 'FOOD1', 'FOOD2', 'FOOD3']  # Required to build the string
    json_food_id = ['Pit_temp', 'Food1_temp', 'Food2_temp', 'Food3_temp']
    food_number = [0, 1, 2, 3]  # 0 = Pit probe, 1 = Probe1 (food1), 2 = Probe2 (food2), 3 = Probe3 (food3)
    try:
        o = untangle.parse(smokey_config['GURU_IP'] + '/all.xml')   # get all status from BBQ Guru and parse XML into
        #                                                           variable 'o'.
    except:  # Using bare except to catch all exceptions (i.e., 'except' clause w/o exceptions specified
        #      (vs. 'except TimeoutError:' (and the 'URLError' exception))
        print(f"{strftime('%Y-%m-%d %H:%M:%S')}: failed to get data from BBQ Guru; "
              f"sleeping for 30 seconds and retrying...")
        sleep(30)
        o = untangle.parse(smokey_config['GURU_IP'] + '/all.xml')
    for x in food_number:
        # print('debug: food_number is = ' + str(food_number))
        # print('debug: value of x variable is = ' + str(x))
        try:
            food_temp_previous[x] = float(json_body[0]['fields'][json_food_id[x]])  # for json_body_old()
            # food_temp_previous[x] = float(json_body[x]['fields'][json_food_id[x]])  # for refactored json_body()
            # print('debug: successfully read a float number from json_body for food_number = ' + str(x))
            # print('debug: food_temp_previous[' + str(x) + '] is a number (float) = ' + str(food_temp_previous[x]))
        except TypeError:
            food_temp_previous[x] = None
            # print(f"debug: food_temp_previous[{str(x)}] was not a number, has value = {str(food_temp_previous[x])}")
            pass
        except NameError:  # a 'NameError' exception occurs at first run b/c json_body does not yet exist
            food_temp_previous[x] = None
            # print(f"debug: {str(food_temp[x])} has never been measured (NameError exception)")  # (debug only)
        except KeyError:  # a 'KeyError' exception occurs at first run b/c json_body does not yet exist
            food_temp_previous[x] = None
            # print(f"debug: {str(food_temp[x])} has never been measured (KeyError exception)")  # (debug only)
        try:  # Try to convert PROBE 1 TEMP from string-formatted # to integer-formatted #
            food_temp_meas[x] = float(eval(str('o.nutcallstatus.' + food_id[x] + '.' + food_temp[x] + '.cdata'))) / 10
            # The above line converts the Guru's string-formatted value to float and divides by 10 (because Guru
            #    reports these numbers as string-formatted integers (e.g., 76.5 is reported as 765 text).
            #    Proper float-formatting is needed in order for Grafana to interpret the data.
            twitter_food_temp[x] = str(repr(round(food_temp_meas[x], 1)) + '\u00b0F')  # for Twitter: round to 1 decimal
            #                                                                           place, return to string,
            #                                                                           and append degF)
            # print(f"debug: {str(food_temp[x])} (food_temp[{str(x)}]) = {str(food_temp_meas[x])}")      # (debug only)
        except ValueError:  # if conversion fails (e.g., b/c it's not a string-formatted #), then...
            food_temp_meas[x] = None  # ...set value to null integer (for Grafana)...
            smokey_config['food_temp_init_counter'][x] = 60  # ...keep init counter at full value (60)...
            twitter_food_temp[x] = str('TBD')
            #       ...set value to food_temp[x]'s 'None' string (for Twitter) (i.e., '= str(food_temp[x])')...
            # print("debug: " + str(food_id[x]) + " Probe is in ValueError flow")  # (debug only)
            pass  # Using pass (vs. break) so the loop goes on to other inputs/values
        if isinstance(food_temp_meas[x], float) == True and smokey_config['food_temp_init_counter'][x] > 0:
            #       Detect if conversion has been successful for less than 60 seconds.
            # print(f"debug: found food_temp_meas[{str(x)}] is a float={str(food_temp_meas[x])} and "
            #       f"food_temp_init_counter[{str(x)}] is >0 = {str(smokey_config['food_temp_init_counter'][x])}")
            food_temp_meas[x] = None  # ...reset the probe value to None (b/c it will be bogus)
            smokey_config['food_temp_init_counter'][x] = smokey_config['food_temp_init_counter'][x] - 2
            #       ...and decrement counter by 2.
            print(f"{strftime('%Y-%m-%d %H:%M:%S')}: {str(food_id[x])} Probe initializing, begin measuring in"
                  f" {str(smokey_config['food_temp_init_counter'][x])} seconds")
            pass
        elif isinstance(food_temp_meas[x], float) == True and smokey_config['food_temp_init_counter'][x] <= 0:
            #       Detect if probe has been plugged in for more than 60 seconds. If true, then report data.
            #print(f"debug: found food_temp_meas[{str(x)}] is a number (float) & food_temp_init_counter[{str(x)}] <=0")
            if isinstance(food_temp_previous[x], float) == True:
                if abs(food_temp_previous[x] - (food_temp_meas[x])) > 20 and \
                        smokey_config['food_temp_unplugged_counter'][x] > 0:
                    print('debug: food_temp_previous = ' + str(food_temp_previous[x]) + ' for probe ' + str(x))
                    print('debug: food_temp_meas = ' + str(food_temp_meas[x]) + ' for probe ' + str(x))
                    print('debug: temp delta > 50, = ' + str(abs(food_temp_previous[x] - food_temp_meas[x])))
                    print('debug: resetting food_temp_meas[' + str(x) + '] = food_temp_previous[' + str(x) + ']')
                    food_temp_meas[x] = food_temp_previous[x]
                    smokey_config['food_temp_unplugged_counter'][x] = \
                        smokey_config['food_temp_unplugged_counter'][x] - 2
                    print('debug: new food_temp_unplugged_counter = ' +
                          str(smokey_config['food_temp_unplugged_counter']))
                else:
                    #print(f"debug: temp delta OK for probe[{str(x)}]: "
                    #      f"food_temp_previous = {str(food_temp_previous[x])}, "
                    #      f"food_temp = {str(food_temp_meas[x])}, "
                    #      f"delta = {str(abs(food_temp_previous[x] - food_temp_meas[x]))}")
                    food_temp_meas[x] = float(eval(str('o.nutcallstatus.' + food_id[x] + '.' + food_temp[x] + '.cdata'))) / 10
                    twitter_food_temp[x] = str(repr(round(food_temp_meas[x],1)) + '\u00b0F')
                    smokey_config['food_temp_unplugged_counter'][x] = 10
            else:
                food_temp_meas[x] = float(eval(str('o.nutcallstatus.' + food_id[x] + '.' + food_temp[x] + '.cdata'))) / 10  # for Grafana: convert string to float and divide by 10
                twitter_food_temp[x] = str(repr(round(food_temp_meas[x],1)) + '\u00b0F')  # for Twitter: round to 1 decimal place, return to string, & append degF)
                smokey_config['food_temp_unplugged_counter'][x] = 10
                print(f"{strftime('%Y-%m-%d %H:%M:%S')}: {str(food_id[x])} Probe (Probe {str(x)}) initialization "
                      f"complete, now posting data (first = {str(food_temp_meas[x])})")
            pass
        else:
            # print('debug: in this flow b/c food_temp_meas[' + str(x) + '] = ' + str(food_temp_meas[x]))
            pass
        try:  # Try to convert probe x SET-POINT from string-formatted value to float-formatted number
            food_set_meas[x] = float(eval(str('o.nutcallstatus.' + food_id[x] + '.' + food_set[x] + '.cdata'))) / 10
            # The above line converts the Guru's string-formatted value to float and divides by 10 (because Guru
            #    reports these numbers as string-formatted integers (e.g., 76.5 is reported as 765 text).
            #    Proper float-formatting is needed in order for Grafana to interpret the data.
            #print(f"debug: initial grab of food_set_meas[{str(x)}] = {str(food_set_meas[x])}; {str(food_set[x])}")
            twitter_food_set[x] = str(repr(round(food_set_meas[x], 1)) + '\u00b0F')  # for Twitter: round to 1 decimal
            #                                                                         place, return to string,
            #                                                                         and append degF)
            pass
        except ValueError:  # if conversion fails (e.g., b/c it's not a string-formatted #), then...
            food_set_meas[x] = None  # ...for Grafana: set value to null integer
            print('debug: ValueError in food_set_meas[x], setting to None')
            twitter_food_set[x] = str(food_set_meas[x])  # ...for Twitter: set value to 'None' string
            pass  # Using pass (vs. break) so the loop goes on to other inputs/values
        try:  # Try to convert probe x STATUS from string-formatted value to integer-formatted number
            food_status_meas[x] = int(eval(str('o.nutcallstatus.' + food_id[x] + '.' + food_status[x] + '.cdata')))
            # The above line converts the Guru's string-formatted value to float and divides by 10 (because Guru
            #    reports these numbers as string-formatted integers (e.g., 76.5 is reported as 765 text).
            #    Proper float-formatting is needed in order for Grafana to interpret the data.
            #print('debug: initial grab of '
            #      'food_status_meas[' + str(x) + '] = ' + str(food_set[x]) + ' = ' + str(food_status_meas[x]))
            pass
        except ValueError:  # if conversion fails (e.g., b/c it's not a string-formatted #), then...
            food_status_meas[x] = None  # ...set value to null integer (for Grafana)
            print('debug: ValueError in food_status_meas[x], setting to None')
            pass  # Using pass (vs. break) so the loop goes on to other inputs/values
    try:  # Try to convert fan output % from string-formatted value to integer-formatted number
        OUTPUT_PERCENT = int(o.nutcallstatus.OUTPUT_PERCENT.cdata)  # convert string to integer
        # print('debug - get_data_food(): fan OUTPUT_PERCENT = ' + str(OUTPUT_PERCENT))
        pass
    except ValueError:  # if conversion fails (e.g., b/c it's not a string-formatted value), then...
        OUTPUT_PERCENT = None  # ...set value to null integer (for Grafana)
        pass
    # print('debug - get_data_food(): food_temp_meas = ' + str(food_temp_meas))
    # print('debug - get_data_food(): food_set_meas = ' + str(food_set_meas))
    # print('debug - get_data_food(): food_status_meas = ' + str(food_status_meas))
    # print('debug - get_data_food(): twitter_food_temp = ' + str(twitter_food_temp))
    # print('debug - get_data_food(): twitter_food_set = ' + str(twitter_food_set))
    # print('debug - get_data_food(): food_temp_previous = ' + str(food_temp_previous))
    guru_data = {'food_temp_meas': food_temp_meas,  # store
                 'food_set_meas': food_set_meas,
                 'food_status_meas': food_status_meas,
                 'OUTPUT_PERCENT': OUTPUT_PERCENT,
                 'twitter_food_temp': twitter_food_temp,
                 'twitter_food_set': twitter_food_set,
                 'Cook_name': o.nutcallstatus.COOK.COOK_NAME.cdata,  # store Guru's cook name
                 'Food1_name': o.nutcallstatus.FOOD1.FOOD1_NAME.cdata,  # store Guru's probe 1 name
                 'Food2_name': o.nutcallstatus.FOOD2.FOOD2_NAME.cdata,  # store Guru's probe 2 name
                 'Food3_name': o.nutcallstatus.FOOD3.FOOD3_NAME.cdata,  # store Guru's probe 3 name
                 'Timer_current': o.nutcallstatus.TIMER_CURR.cdata  # store Guru's timer value
                 }
    return guru_data


def build_json_alternate(guru_data):  # experimental for use with cloud instance of InfluxDB / Grafana dashboard
    # print('debug - build_json_alternate(): food_temp_meas = ' + str(food_temp_meas))
    # print('debug - build_json_alternate(): food_set_meas = ' + str(food_set_meas))
    # print('debug - build_json_alternate(): food_status_meas = ' + str(food_status_meas))
    json_body = [  # build the JSON object to be written to InfluxDB
        {
            "measurement": "Cook_events",  # measurements for all cook/pit-level data
            "tags": {
                "tag_Cook_name": guru_data['Cook_name']  # used by Grafana (e.g., variable var_Cook_name)
            },
            "time": strftime("%Y-%m-%d %H:%M:%S", gmtime()),  # TESTING turns out this is required?
            "fields": {
                "Cook_name": guru_data['Cook_name'],  # store cook name #TESTING not using this
                "Pit_temp": guru_data['food_temp_meas'][0],  # store pit probe temperature
                "Pit_set": guru_data['food_set_meas'][0],  # store pit probe set-point
                "Pit_status": guru_data['food_status_meas'][0],  # store pit probe status
                "Output_percent": guru_data['OUTPUT_PERCENT'],  # store fan output %
                "Timer_current": guru_data['Timer_current']  # store timer value # Removed comma
                # "local_time": strftime("%Y-%m-%d %H:%M:%S")  # store current time  #TESTING not using this
            }
        },
        {
            "measurement": "Food1_events",  # measurements for all cook/pit-level data
            "tags": {
                "tag_Food1_name": guru_data['Food1_name']
                # used by Grafana (e.g., variable var_Food1_name)
            },
            "time": strftime("%Y-%m-%d %H:%M:%S", gmtime()),  # TESTING turns out this is required?
            "fields": {
                "Food1_name": guru_data['Food1_name'],  # stores probe 1 name
                "Food1_temp": guru_data['food_temp_meas'][1],  # store probe 1 temperature
                "Food1_set": guru_data['food_set_meas'][1],  # store probe 1 set-point
                "Food1_status": guru_data['food_status_meas'][1],  # store probe 1 status #TESTING removed comma
            }
        },
        {
            "measurement": "Food2_events",  # measurements for all cook/pit-level data
            "tags": {
                "tag_Food2_name": guru_data['Food2_name']
                # used by Grafana (e.g., variable var_Food2_name)
            },
            "time": strftime("%Y-%m-%d %H:%M:%S", gmtime()),  # TESTING turns out this is required?
            "fields": {
                "Food2_name": guru_data['Food2_name'],  # stores probe 2 name
                "Food2_temp": guru_data['food_temp_meas'][2],  # store probe 2 temperature
                "Food2_set": guru_data['food_set_meas'][2],  # store probe 2 set-point
                "Food2_status": guru_data['food_status_meas'][2],  # store probe 2 status #TESTING removed comma
            }
        },
        {
            "measurement": "Food3_events",  # measurements for all cook/pit-level data
            "tags": {
                "tag_Food3_name": guru_data['Food3_name']
                # used by Grafana (e.g., variable var_Food3_name)
            },
            "time": strftime("%Y-%m-%d %H:%M:%S", gmtime()),  # TESTING turns out this is required?
            "fields": {
                "Food3_name": guru_data['Food3_name'],  # store probe 3 name
                "Food3_temp": guru_data['food_temp_meas'][3],  # store probe 3 temperature
                "Food3_set": guru_data['food_set_meas'][3],  # store probe 3 set-point
                "Food3_status": guru_data['food_status_meas'][3],  # store probe 3 status #TESTING removed comma
            }
        }
    ]
    print('debug - build_json_alternate(): json_body = ' + str(json_body))
    return json_body


def build_json(guru_data):
    """ The function builds a JSON object from data extracted/conditioned from the BBQ Guru (extracted via function
    get_data_food). Note: this schema is my default schema that I use with the local instance of InfluxDB / Grafana.
    For alternate version (e.g., for experimental purposes when using an InfluxDB cloud instance),
    see build_jason_alternate."""
    json_body = [  # build the JSON object to be written to InfluxDB
        {
            "measurement": "GURU_events",  # measurements for all data
            "tags": {
                "tag_pitmaster": "Jon",
                "tag_Cook_name": guru_data['Cook_name'],  # for Grafana (e.g., variable var_Cook_name)
                "tag_Food1_name": guru_data['Food1_name'],  # for Grafana (e.g., variable var_Food1_name)
                "tag_Food2_name": guru_data['Food2_name'],  # for Grafana (e.g., variable var_Food2_name)
                "tag_Food3_name": guru_data['Food3_name']  # for Grafana (e.g., variable var_Food3_name)
            },
            "time": strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            "fields": {
                "Cook_name": guru_data['Cook_name'],  # store cook name
                "Pit_temp": guru_data['food_temp_meas'][0],  # store pit probe temperature
                "Pit_set": guru_data['food_set_meas'][0],  # store pit probe set-point
                "Pit_status": guru_data['food_status_meas'][0],  # store pit probe status
                "Food1_name": guru_data['Food1_name'],  # store probe 1 name
                "Food1_temp": guru_data['food_temp_meas'][1],  # store probe 1 temperature
                "Food1_set": guru_data['food_set_meas'][1],  # store probe 1 set-point
                "Food1_status": guru_data['food_status_meas'][1],  # store probe 1 status
                "Food2_name": guru_data['Food2_name'],  # store probe 2 name
                "Food2_temp": guru_data['food_temp_meas'][2],  # store probe 2 temperature
                "Food2_set": guru_data['food_set_meas'][2],  # store probe 2 set-point
                "Food2_status": guru_data['food_status_meas'][2],  # extract probe 2 status
                "Food3_name": guru_data['Food3_name'],  # store probe 3 name
                "Food3_temp": guru_data['food_temp_meas'][3],  # store probe 3 temperature
                "Food3_set": guru_data['food_set_meas'][3],  # store probe 3 set-point
                "Food3_status": guru_data['food_status_meas'][3],  # store probe 3 status
                "Output_percent": guru_data['OUTPUT_PERCENT'],  # store fan output %
                "Timer_current": guru_data['Timer_current'],  # store timer value
                "local_time": strftime("%Y-%m-%d %H:%M:%S")  # store current time
            }
        }
    ]
    # print('debug - build_json(): json_body = ' + str(json_body))
    return json_body


def write_to_influxdb(instance, json_body, smokey_config):
    """ This function writes the content of a JSON object to InfluxDB via the InfluxDB API. The API works differently
     depending on whether the InfluxDB instance type is cloud or local. """
    if smokey_config['cloud_enabled'] == True:
        try:
            init_influxdb.write_to_influxdb(instance, json_body)  # write the JSON object to InfluxDB for Grafana
            # print('debug (cloud): ' + str(json_body))  #debug only: enable this to check if json_body is valid here
        except TimeoutError:
            print(strftime("%Y-%m-%d %H:%M:%S") + ' - write to InfluxDB (cloud) failed; will try again')
            sleep(2)
        return
    if smokey_config['cloud_enabled'] == False:
        try:
            init_influxdb.client.write_points(json_body)  # write the JSON object to InfluxDB
            #print('debug (local influxdb): ' + str(json_body))  #debug only: displays if json_body is valid here
        except TimeoutError:
            print(strftime("%Y-%m-%d %H:%M:%S") + ' - write to InfluxDB (local) failed; will try again')
            sleep(2)
        return


def tweet_stuff(api, guru_data, smokey_config):
    """ Tweets messages to the Twitter API. """
    twitter_food_temp = guru_data['twitter_food_temp']
    twitter_food_set = guru_data['twitter_food_set']
    if smokey_config['tweet_enabled'] == True:
        if smokey_config['first_tweet_flag'] == 1:  # tweet the unique first tweet
            smokey_config['first_tweet_flag'] = 0  # reset first_tweet_flag to 0 to prevent repetition until program
            #                                        restarts.
            first_tweet_part_1 = 'Bleep Blorp. I am programed to smoke meats and to love. I am monitoring the ' \
                                 'temperature of'
            if guru_data['Food1_name'] == 'none':
                first_tweet_part_2 = ''
            else:
                first_tweet_part_2 = ' ...' + str(guru_data['Food1_name'])
            if guru_data['Food2_name'] == 'none':
                first_tweet_part_3 = ''
            else:
                first_tweet_part_3 = ' ...' + str(guru_data['Food2_name'])
            if guru_data['Food3_name'] == 'none':
                first_tweet_part_4 = ''
            else:
                first_tweet_part_4 = ' ...' + str(guru_data['Food3_name'])
            requested_tweet = first_tweet_part_1 + first_tweet_part_2 + first_tweet_part_3 + first_tweet_part_4
            tweet.post_tweet(api,requested_tweet)  # Tweet first message
            # print(f"debug: the tweet is '{requested_tweet}'")  # debug only: display what would be tweeted
        else:  # having already tweeted the first unique message, now tweet recurring messages
            if smokey_config['debug_enabled'] == True:
                print(f"debug: better not be first-tweeting because "
                      f"first_tweet_flag = {str(smokey_config['first_tweet_flag'])}")
            else:
                pass
        if smokey_config['meat_tweet_delay'] <= 0:  #  when timer reaches 0, tweet a message about meat
            smokey_config['meat_tweet_delay'] = smokey_config['static_meat_tweet_delay']
            #       Reset meat tweet delay to value specified in program control.
            tweet_part_1 = f"Current temperatures: Pit = {twitter_food_temp[0]} (target = {twitter_food_set[0]})"
            if guru_data['Food1_name'] == 'none':
                tweet_part_2 = ''
            else:
                tweet_part_2 = f"; {str(guru_data['Food1_name'])} = {twitter_food_temp[1]} " \
                               f"(target = {twitter_food_set[1]})"
                #  tweet_part_2 = f"; {str(guru_data['Food1_name'])} = DONE!"  # manually enable this to declare DONE
            if guru_data['Food2_name'] == 'none':
                tweet_part_3 = ''
            else:
                tweet_part_3 = f"; {str(guru_data['Food2_name'])} = {twitter_food_temp[2]} " \
                               f"(target = {twitter_food_set[2]})"
                #  tweet_part_3 = f"; {str(guru_data['Food2_name'])} = DONE!"  # manually enable this to declare DONE
            if guru_data['Food3_name'] == 'none':
                tweet_part_4 = ''
            else:
                tweet_part_4 = f"; {str(guru_data['Food3_name'])} = {twitter_food_temp[3]} " \
                               f"(target = {twitter_food_set[3]})"
            tweet_part_5 = ' #smokingmeat #bbq'
            requested_tweet = str(tweet_part_1) + str(tweet_part_2) + str(tweet_part_3) + str(tweet_part_4) + \
                              str(tweet_part_5)
            tweet.post_tweet(api, requested_tweet)  # Tweet about meat
            # print(f"debug: the tweet is '{requested_tweet}'")  # debug only: display what would be tweeted
        else:
            smokey_config['meat_tweet_delay'] = smokey_config['meat_tweet_delay'] - smokey_config['loop_delay']
            if smokey_config['debug_enabled'] == True:
                print('not supposed to meat tweet now because meat_tweet_delay is ' + str(smokey_config['meat_tweet_delay']))
            else:
                pass
        if smokey_config['message_delay'] <= 0:  # if delay has decremented to 0, then try tweeting (and reset delay)
            smokey_config['message_delay'] = smokey_config['static_message_generator_tweet_delay']
            #       Reset message delay to value specified in program control
            all_jobs = []
            words = message_generator.define_words()  # Initializes the word dictionary.
            all_jobs = message_generator.message(words)  # Builds list of jobs (w/o preamble) from random words
            #                                              in word dictionary
            requested_tweet = message_generator.respond_one(all_jobs)  # Returns a single randomly chosen message from
            #                                                            the message list (with default preamble)
            #                                                            and stores it in "message".
            tweet.post_tweet(api, requested_tweet)  # Tweet about nonsense
            # print(f"debug: the tweet is '{requested_tweet}'")  # debug only: display what would be tweeted
        else:
            if smokey_config['debug_enabled'] == True:
                print(f"not supposed to tweet message now because "
                      f"message_delay is {str(smokey_config['message_delay'])}")
            else:
                pass
            smokey_config['message_delay'] = smokey_config['message_delay'] - smokey_config['loop_delay']



def debug_functions(smokey_config, guru_data):
    """ Debug functions """
    if smokey_config['debug_enabled'] == True:
        print(f"Debug enabled...message_delay = {str(smokey_config['message_delay'])}")
        print(f"Debug enabled...meat-tweet_delay = {str(smokey_config['meat_tweet_delay'])}")
        print('debug: food_temp_init_counter = ' + str(smokey_config['food_temp_init_counter']))
        print('debug: food_temp_meas = ' + str(guru_data['food_temp_meas']))
        print('debug: food_set_meas = ' + str(guru_data['food_set_meas']))
        print('debug: food_status_meas = ' + str(guru_data['food_status_meas']))
        print('debug: json_body = ' + str(json_body))
    if smokey_config['message_debug_enabled'] == True:
        words = message_generator.define_words()  # Initializes the word dictionary.
        all_jobs = message_generator.message(words)  # Builds list of jobs (w/o preamble) from random words
        #                                              in word dictionary
        message = message_generator.respond_one(all_jobs)  # Returns a single randomly chosen message from
        #                                                    the message list (with default preamble)
        #                                                    and stores it in "message"
        print('Message debug enabled...message_generator screen-output (not to Twitter): ' + str(message))
    return


if __name__ == '__main__':
    """ Welcome to SmokeyBot. """
    smokey_config = configure_program()
    db_instance = configure_database()
    twitter_api_config = configure_twitter()
    while True:
        guru_data = get_data_food()  # Extracts/conditions data from Guru and stores into guru_data object.
        json_body = build_json(guru_data)  # Stores data from guru_data object into JSON object formatted for InfluxDB.
        # json_body = build_json_alternate()  # uses alternate json_body schema, for experimental purposes
        #                                      (e.g., w/ InfluxDB Cloud instance).
        write_to_influxdb(db_instance, json_body, smokey_config)  # Writes JSON object data to InfluxDB instance.
        tweet_stuff(twitter_api_config, guru_data, smokey_config)  # Tweets about cook and nonsense.
        debug_functions(smokey_config, guru_data)  # optionally, print verbose program output to screen
        sleep(smokey_config['loop_delay'])  # pause for duration of loop_delay (i.e., 2 sec); will then loop
