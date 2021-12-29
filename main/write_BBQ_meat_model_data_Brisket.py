# Meat Model - Brisket: This module writes the projected temperature points over time (starting with the specified
# temperature) to an InfluxDB database.
# 0.0) Prerequisites
#    0.1) Python Dependencies:
#        0.1.a) Python package 'influxdb' shall be installed into the active Python environment (e.g., by running
#                'pip install influxdb' in the environment's terminal window).
#                 Tips: 'https://www.influxdata.com/blog/getting-started-python-influxdb/'
#        0.1.b) Python module 'init_influxdb.py' shall be present in the active Python environment path (possibly in
#                a Common directory, since this module is used in other unrelated Projects).
#    0.2) Configuration Dependencies:
#        0.2.a) InfluxDB shall be installed; InfluxDB shall be running (e.g., by running this in a terminal window:
#                'C:\Users\User\Downloads\00 Brewing\influxdb-1.5.2-1\influxd.exe'.
#                 For info on where InfluxDB writes data, see:
#                 'https://stackoverflow.com/questions/43644051/influxdb-storage-folder-windows'.
#        0.2.b) If a target InfluxDB schema does not already exist, then the optional 'reset_database' function must
#                first be executed stand-alone.
# 1.0) Run-time notes:
#   1.1) Usage:
#       1.1.1) standalone?: Yes.
#           >>> exec(open('write_BBQ_meat_model_data_Brisket.py').read())
#       1.1.2) call from another module?: No.
# 2.0) Changelog:
#       Version 1.0: Original version.
#       Version 2.1: Re-worked predictions based on the Hoggin'-dazs (2018-06-30) brisket data. This was a 16.4 lb
#                    brisket which took 15hr+58min to rise from 47°F to 203°F. This included two significant stalls:
#                    163-164°F for 54min, and 174-174°F for 53min.
#                       Relevant info:
#                           (a) other items in smoker: 7.5 lb pork shoulder, added 1h 50m after the brisket.
#                           (b) environment: outside temp was ~65°F. Wind = calm.
#                           (c) actions: wrapped brisket after 12h+5m (195°F)


# ******* SECTION 1 - Initialize InfluxDB session *******
import init_influxdb  # See Prerequisite 0.1.a and 0.1.b.
init_influxdb.init_influxdb(target_database='GURU1',host='localhost', port=8086)

# ******* SECTION 2 - initialize meat model values, where each value is recorded in one-minute intervals *******
import datetime                     # needed for current time
brisket_temps = [47,47,47,47,47,47,47,48,49,49,50,50,51,52,52,53,54,54,55,55,56,57,57,58,59,60,61,61,62,62,63,64,65,65,
                 66,66,67,68,68,69,70,71,71,72,72,74,74,75,76,77,77,78,79,80,81,81,82,83,83,85,86,86,86,87,88,89,90,91,
                 91,92,93,94,94,95,95,96,97,97,98,99,100,100,101,102,102,104,104,105,105,106,106,107,108,109,110,110,
                 111,111,113,113,114,115,115,116,117,118,118,119,120,120,121,123,123,124,124,124,125,125,125,126,127,
                 126,127,128,128,128,129,129,129,129,130,130,131,131,132,132,133,133,133,133,134,134,134,134,135,135,
                 135,135,136,136,137,137,137,138,138,138,138,138,139,139,139,139,139,140,140,140,140,141,141,141,141,
                 141,142,142,143,143,143,144,144,144,144,144,145,145,145,145,145,146,146,146,146,146,147,147,147,147,
                 147,148,148,148,148,148,148,148,149,149,149,149,149,150,150,150,150,150,150,151,152,151,151,151,152,
                 152,152,153,153,153,153,153,153,154,154,154,154,154,154,154,155,155,155,155,155,155,155,155,156,156,
                 156,156,156,156,156,156,156,157,157,157,157,157,157,157,157,157,157,158,158,158,158,158,158,158,158,
                 158,158,158,158,159,159,159,159,159,159,159,159,159,160,160,160,160,160,161,160,161,160,160,161,161,
                 161,161,162,162,162,162,162,162,162,162,162,162,162,162,162,162,162,162,162,162,163,162,163,163,163,
                 163,163,163,163,163,163,163,163,163,163,163,163,163,163,163,163,163,163,163,163,164,164,164,164,164,
                 164,164,164,164,164,164,164,164,164,164,164,164,164,164,164,164,164,164,164,164,164,164,164,164,164,
                 165,165,165,165,165,165,165,165,166,166,166,166,166,166,167,167,167,167,167,167,167,167,168,168,168,
                 168,169,168,168,168,168,168,169,169,169,169,170,170,169,169,170,169,169,170,169,170,170,170,170,170,
                 170,170,171,171,170,171,171,171,171,171,172,172,172,172,172,173,173,173,173,173,173,173,173,174,174,
                 174,174,174,174,174,174,174,174,174,174,174,174,174,174,174,174,174,174,174,174,174,174,174,174,174,
                 174,174,174,174,174,174,174,174,174,175,175,175,175,175,175,175,175,175,175,175,175,175,175,175,175,
                 175,176,176,176,176,176,176,176,176,176,176,176,176,176,176,176,177,177,177,177,177,177,177,177,177,
                 177,178,178,179,179,179,179,179,179,180,180,180,180,180,180,180,180,181,181,181,181,181,181,181,181,
                 181,181,181,181,181,181,181,181,181,181,181,181,181,181,181,182,182,182,182,182,182,182,182,182,182,
                 182,182,182,182,182,182,183,183,183,183,183,183,183,183,183,183,183,183,183,183,184,184,184,184,184,
                 184,184,184,184,184,184,184,184,184,185,185,185,185,185,185,185,185,185,185,185,185,185,185,185,185,
                 185,185,185,185,185,186,185,186,186,186,186,186,186,187,187,186,186,187,188,187,187,188,188,187,188,
                 188,188,188,188,188,189,189,189,189,189,189,189,189,189,189,189,190,190,190,190,190,190,190,190,190,
                 190,190,190,191,191,191,191,191,191,191,191,191,191,191,191,192,192,192,192,192,192,192,192,192,192,
                 193,193,193,193,193,193,193,193,193,193,194,194,194,194,194,194,194,194,195,195,195,195,195,195,195,
                 195,195,195,196,196,194,192,191,191,191,191,191,191,191,191,191,191,191,192,192,192,192,192,192,192,
                 193,193,193,193,193,193,194,194,194,194,194,194,194,194,195,195,195,195,195,195,195,195,195,195,196,
                 196,196,196,196,196,196,196,197,196,197,197,196,197,196,197,197,197,197,197,198,198,198,198,198,198,
                 198,198,198,198,198,198,198,198,198,198,198,198,198,198,198,199,199,199,199,199,199,199,199,199,199,
                 199,199,199,199,199,199,199,199,199,199,199,199,199,199,199,199,199,199,199,199,199,199,199,199,199,
                 199,199,199,199,199,199,199,199,199,199,199,199,199,199,199,199,199,199,199,199,199,200,199,199,199,
                 199,199,199,199,199,199,199,199,199,199,199,198,198,198,198,198,198,198,198,198,198,198,198,198,198,
                 198,198,198,198,198,198,198,199,198,199,199,199,199,199,199,199,199,199,199,199,199,199,200,200,200,
                 200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,201,201,201,201,201,201,201,
                 202,202,202,202,202,202,202,202,202,203,203,203,203]
offset_temperature = int(input("Enter the current brisket temperature measurement (between 47 and 203): "))   # stores the current measured meat temperature
offset_minutes = brisket_temps.index(int(offset_temperature))  # finds how many meat model elapsed minutes correspond to measured meat temperature
# The next line negatively time-shifts the time-now value (in GMT) by the number of minutes just found (to be added in
# later, effectively assigning time-now to the meat-model's temperature which corresponds to the actual measured
# temperature (so that we're starting from a common start point):
time_now_GMT = datetime.datetime.utcnow() - datetime.timedelta(minutes = offset_minutes)


# ******* SECTION 3 - build json object from meat model values and write to InfluxDB *******
brisket_json = []  # initialize empty json object
for index in range(len(brisket_temps)):  # for each value in in brisket_temps)...
    brisket_measurement = {              # ...create JSON object entry
        "measurement": "meat_model",
        "tags": {
            "tag_pitmaster": "Jon",
            "food": "Brisket",
            "type": "model"
            },
        "time": str(time_now_GMT + datetime.timedelta(minutes = index)),  # write the time (previously shifted) plus a delta corresponding to the index of the meat model (which is one index value per mintue).
        "fields": {
            "Brisket_temp": int(brisket_temps[index]) # write the meat model temp corresponding to the index of the meat model
            }
        }
    brisket_json.append(brisket_measurement)  # append the just-built json object to the list
init_influxdb.client.write_points(brisket_json)  # writes the JSON object to InfluxDB
print('I did it!')