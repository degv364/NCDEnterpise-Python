#TODO the NCDEnterprise library requires the digi Xbee library from:
#https://github.com/digidotcom/python-xbee
# someday I may make an install package, but today is not that day.

import os
from datetime import datetime
from ncd_enterprise import NCDEnterprise

# TODO Change this line to your Serial Port
# SERIAL_PORT = "/dev/tty.usbserial-AC4CF4AA"
SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 115200
PREFIX = os.path.expanduser("~/exosense_data/")


def write_to(file_name, file_prefix, value, battery):
    file_path = file_prefix + file_name
    with open(file_path, "w") as archive:
        archive.write(str(value))
    with open(file_path + "_battery", "w") as archive:
        archive.write(str(battery))


# This is function is the callback that I pass into the NCDEnterprise
# module during instantiation. The module uses the Digi XBee module
# which runs on another thread.
def my_custom_callback(sensor_data):
    # time control for debug
    write_to("datetime", PREFIX, datetime.now().ctime(), 100)
    print(datetime.now().ctime())
    battery = sensor_data["battery_percent"]
    if sensor_data["sensor_type_id"] == 13:
        value = sensor_data["sensor_data"]["amps"]
        print("amps:", value)
        write_to("amps", PREFIX, value, battery)
    elif sensor_data["sensor_type_id"] == 52:
        value = sensor_data["sensor_data"]["adc"]
        print("adc:", value)
        write_to("adc", PREFIX, value, battery)
    else:
        print(sensor_data)


# Error callbacks are only supported for the vibration time series data sets currently
def error_callback(error_data):
    print('Error detected:')
    print(error_data)

#instantiate the NCDEnterprise Object and pass in the Serial Port, Baud Rate,
# and Function/Method object
# the error handler method MUST be keyed as error_handler.
ncdModem = NCDEnterprise(SERIAL_PORT, BAUD_RATE, my_custom_callback, {'error_handler': error_callback})
# print(ncdModem.device.serial_port.rts)
