# Note 1: run this within Python using: "exec(open('write_BBQ_meat_model_data_Chicken.py').read())"
#
from influxdb import InfluxDBClient
client = InfluxDBClient(host='localhost', port=8086)
#client.drop_database('GURU1')   # only do this if you want to eliminate the database before starting again
#client.create_database('GURU1')
#client.get_list_database()
client.switch_database('GURU1')
#
#
import datetime  # needed for current time
from time import gmtime, strftime # needed for current time
import time  # needed for current time
import json  # needed to manipulate the JSON message
#
#
# Configure Time offset: enable ONE of the following (both write all model points, but the second one offsets it to desired time):
# Option 1:
#time_now_GMT = datetime.datetime.utcnow()   # write all points starting from time-now
# Option 2:
time_now_GMT = datetime.datetime.utcnow() - datetime.timedelta(minutes = 20)    # change XX to equal the minutes that's closest to the current meat temp.
#
x = True
while x == True:  # this loops forever (until manually stopped), pausing 5 minutes in between loops
    json_body = [   # build the JSON object to be written to InfluxDB
	{
		"measurement": "meat_model",
		"tags": {
			"tag_pitmaster": "Jon",
                        "food": "Chicken",
                        "type": "model"
		},
		"time": str(time_now_GMT),
		"fields": {
                        "Chicken_temp": 40
		}
	},
        {
		"measurement": "meat_model",
		"tags": {
			"tag_pitmaster": "Jon",
                        "food": "Chicken",
                        "type": "model"
		},
		"time": str(time_now_GMT + datetime.timedelta(minutes = 5)),
		"fields": {
                        "Chicken_temp": 41
		}
	},
        {
		"measurement": "meat_model",
		"tags": {
			"tag_pitmaster": "Jon",
                        "food": "Chicken",
                        "type": "model"
		},
		"time": str(time_now_GMT + datetime.timedelta(minutes = 10)),
		"fields": {
                        "Chicken_temp": 46
		}
	},
        {
		"measurement": "meat_model",
		"tags": {
			"tag_pitmaster": "Jon",
                        "food": "Chicken",
                        "type": "model"
		},
		"time": str(time_now_GMT + datetime.timedelta(minutes = 15)),
		"fields": {
                        "Chicken_temp": 53
		}
	},
        {
		"measurement": "meat_model",
		"tags": {
			"tag_pitmaster": "Jon",
                        "food": "Chicken",
                        "type": "model"
		},
		"time": str(time_now_GMT + datetime.timedelta(minutes = 20)), #FILL IN TIME ater "= "
		"fields": {
                        "Chicken_temp": 60  #FILL IN TEMP after ": "
		}
	},
        {
		"measurement": "meat_model",
		"tags": {
			"tag_pitmaster": "Jon",
                        "food": "Chicken",
                        "type": "model"
		},
		"time": str(time_now_GMT + datetime.timedelta(minutes = 25)), #FILL IN TIME ater "= "
		"fields": {
                        "Chicken_temp": 69  #FILL IN TEMP after ": "
		}
	},
        {
		"measurement": "meat_model",
		"tags": {
			"tag_pitmaster": "Jon",
                        "food": "Chicken",
                        "type": "model"
		},
		"time": str(time_now_GMT + datetime.timedelta(minutes = 30)), #FILL IN TIME ater "= "
		"fields": {
                        "Chicken_temp": 75  #FILL IN TEMP after ": "
		}
	},
        {
		"measurement": "meat_model",
		"tags": {
			"tag_pitmaster": "Jon",
                        "food": "Chicken",
                        "type": "model"
		},
		"time": str(time_now_GMT + datetime.timedelta(minutes = 35)), #FILL IN TIME ater "= "
		"fields": {
                        "Chicken_temp": 84  #FILL IN TEMP after ": "
		}
	},
        {
		"measurement": "meat_model",
		"tags": {
			"tag_pitmaster": "Jon",
                        "food": "Chicken",
                        "type": "model"
		},
		"time": str(time_now_GMT + datetime.timedelta(minutes = 40)), #FILL IN TIME ater "= "
		"fields": {
                        "Chicken_temp": 92  #FILL IN TEMP after ": "
		}
	},
        {
		"measurement": "meat_model",
		"tags": {
			"tag_pitmaster": "Jon",
                        "food": "Chicken",
                        "type": "model"
		},
		"time": str(time_now_GMT + datetime.timedelta(minutes = 45)), #FILL IN TIME ater "= "
		"fields": {
                        "Chicken_temp": 102  #FILL IN TEMP after ": "
		}
	},
        {
		"measurement": "meat_model",
		"tags": {
			"tag_pitmaster": "Jon",
                        "food": "Chicken",
                        "type": "model"
		},
		"time": str(time_now_GMT + datetime.timedelta(minutes = 50)), #FILL IN TIME ater "= "
		"fields": {
                        "Chicken_temp": 111  #FILL IN TEMP after ": "
		}
	},
        {
		"measurement": "meat_model",
		"tags": {
			"tag_pitmaster": "Jon",
                        "food": "Chicken",
                        "type": "model"
		},
		"time": str(time_now_GMT + datetime.timedelta(minutes = 55)), #FILL IN TIME ater "= "
		"fields": {
                        "Chicken_temp": 118  #FILL IN TEMP after ": "
		}
	},
        {
		"measurement": "meat_model",
		"tags": {
			"tag_pitmaster": "Jon",
                        "food": "Chicken",
                        "type": "model"
		},
		"time": str(time_now_GMT + datetime.timedelta(minutes = 60)), #FILL IN TIME ater "= "
		"fields": {
                        "Chicken_temp": 126  #FILL IN TEMP after ": "
		}
	},
        {
		"measurement": "meat_model",
		"tags": {
			"tag_pitmaster": "Jon",
                        "food": "Chicken",
                        "type": "model"
		},
		"time": str(time_now_GMT + datetime.timedelta(minutes = 65)), #FILL IN TIME ater "= "
		"fields": {
                        "Chicken_temp": 134  #FILL IN TEMP after ": "
		}
	},
        {
		"measurement": "meat_model",
		"tags": {
			"tag_pitmaster": "Jon",
                        "food": "Chicken",
                        "type": "model"
		},
		"time": str(time_now_GMT + datetime.timedelta(minutes = 70)), #FILL IN TIME ater "= "
		"fields": {
                        "Chicken_temp": 139  #FILL IN TEMP after ": "
		}
	},
        {
		"measurement": "meat_model",
		"tags": {
			"tag_pitmaster": "Jon",
                        "food": "Chicken",
                        "type": "model"
		},
		"time": str(time_now_GMT + datetime.timedelta(minutes = 75)), #FILL IN TIME ater "= "
		"fields": {
                        "Chicken_temp": 143  #FILL IN TEMP after ": "
		}
	},
        {
		"measurement": "meat_model",
		"tags": {
			"tag_pitmaster": "Jon",
                        "food": "Chicken",
                        "type": "model"
		},
		"time": str(time_now_GMT + datetime.timedelta(minutes = 80)), #FILL IN TIME ater "= "
		"fields": {
                        "Chicken_temp": 145  #FILL IN TEMP after ": "
		}
	},
        {
		"measurement": "meat_model",
		"tags": {
			"tag_pitmaster": "Jon",
                        "food": "Chicken",
                        "type": "model"
		},
		"time": str(time_now_GMT + datetime.timedelta(minutes = 85)), #FILL IN TIME ater "= "
		"fields": {
                        "Chicken_temp": 148  #FILL IN TEMP after ": "
		}
	},
        {
		"measurement": "meat_model",
		"tags": {
			"tag_pitmaster": "Jon",
                        "food": "Chicken",
                        "type": "model"
		},
		"time": str(time_now_GMT + datetime.timedelta(minutes = 90)), #FILL IN TIME ater "= "
		"fields": {
                        "Chicken_temp": 149  #FILL IN TEMP after ": "
		}
	},
        {
		"measurement": "meat_model",
		"tags": {
			"tag_pitmaster": "Jon",
                        "food": "Chicken",
                        "type": "model"
		},
		"time": str(time_now_GMT + datetime.timedelta(minutes = 95)), #FILL IN TIME ater "= "
		"fields": {
                        "Chicken_temp": 151  #FILL IN TEMP after ": "
		}
	},
        {
		"measurement": "meat_model",
		"tags": {
			"tag_pitmaster": "Jon",
                        "food": "Chicken",
                        "type": "model"
		},
		"time": str(time_now_GMT + datetime.timedelta(minutes = 100)), #FILL IN TIME ater "= "
		"fields": {
                        "Chicken_temp": 152  #FILL IN TEMP after ": "
		}
	},
        {
		"measurement": "meat_model",
		"tags": {
			"tag_pitmaster": "Jon",
                        "food": "Chicken",
                        "type": "model"
		},
		"time": str(time_now_GMT + datetime.timedelta(minutes = 105)), #FILL IN TIME ater "= "
		"fields": {
                        "Chicken_temp": 152  #FILL IN TEMP after ": "
		}
	},
        {
		"measurement": "meat_model",
		"tags": {
			"tag_pitmaster": "Jon",
                        "food": "Chicken",
                        "type": "model"
		},
		"time": str(time_now_GMT + datetime.timedelta(minutes = 110)), #FILL IN TIME ater "= "
		"fields": {
                        "Chicken_temp": 153  #FILL IN TEMP after ": "
		}
	},
        {
		"measurement": "meat_model",
		"tags": {
			"tag_pitmaster": "Jon",
                        "food": "Chicken",
                        "type": "model"
		},
		"time": str(time_now_GMT + datetime.timedelta(minutes = 115)), #FILL IN TIME ater "= "
		"fields": {
                        "Chicken_temp": 154  #FILL IN TEMP after ": "
		}
	},
        {
		"measurement": "meat_model",
		"tags": {
			"tag_pitmaster": "Jon",
                        "food": "Chicken",
                        "type": "model"
		},
		"time": str(time_now_GMT + datetime.timedelta(minutes = 120)), #FILL IN TIME ater "= "
		"fields": {
                        "Chicken_temp": 155  #FILL IN TEMP after ": "
		}
	},
        {
		"measurement": "meat_model",
		"tags": {
			"tag_pitmaster": "Jon",
                        "food": "Chicken",
                        "type": "model"
		},
		"time": str(time_now_GMT + datetime.timedelta(minutes = 125)), #FILL IN TIME ater "= "
		"fields": {
                        "Chicken_temp": 156  #FILL IN TEMP after ": "
		}
	},
        {
		"measurement": "meat_model",
		"tags": {
			"tag_pitmaster": "Jon",
                        "food": "Chicken",
                        "type": "model"
		},
		"time": str(time_now_GMT + datetime.timedelta(minutes = 130)), #FILL IN TIME ater "= "
		"fields": {
                        "Chicken_temp": 158  #FILL IN TEMP after ": "
		}
	},
        {
		"measurement": "meat_model",
		"tags": {
			"tag_pitmaster": "Jon",
                        "food": "Chicken",
                        "type": "model"
		},
		"time": str(time_now_GMT + datetime.timedelta(minutes = 135)), #FILL IN TIME ater "= "
		"fields": {
                        "Chicken_temp": 159  #FILL IN TEMP after ": "
		}
	},
        {
		"measurement": "meat_model",
		"tags": {
			"tag_pitmaster": "Jon",
                        "food": "Chicken",
                        "type": "model"
		},
		"time": str(time_now_GMT + datetime.timedelta(minutes = 140)), #FILL IN TIME ater "= "
		"fields": {
                        "Chicken_temp": 159  #FILL IN TEMP after ": "
		}
	},
        {
		"measurement": "meat_model",
		"tags": {
			"tag_pitmaster": "Jon",
                        "food": "Chicken",
                        "type": "model"
		},
		"time": str(time_now_GMT + datetime.timedelta(minutes = 145)), #FILL IN TIME ater "= "
		"fields": {
                        "Chicken_temp": 159  #FILL IN TEMP after ": "
		}
	},
        {
		"measurement": "meat_model",
		"tags": {
			"tag_pitmaster": "Jon",
                        "food": "Chicken",
                        "type": "model"
		},
		"time": str(time_now_GMT + datetime.timedelta(minutes = 150)), #FILL IN TIME ater "= "
		"fields": {
                        "Chicken_temp": 160  #FILL IN TEMP after ": "
		}
	}
	]
    client.write_points(json_body)  # writes the JSON object to InfluxDB
    print('I did it!')
    x = False
    #time.sleep(10)   # delays for 2 seconds before looping
