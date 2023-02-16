import snap7
import serial
import time
from SQL_Plot_Results import fire_results



IP = '192.168.0.1'
RACK = 0
SLOT = 1

plc = snap7.client.Client()
plc.connect(IP, RACK, SLOT)
state = plc.get_cpu_state()
# print(f'State: {state}')

"""" 
We want to read/write datatype = bool (bit size = 1), because that allows us to read/write Digital Input/Output,
which operate either in ON(=TRUE/1) or OFF(=FALSE/O) mode.
Instead of directly operating with I/O of the PLC hardware, we create DataBlocks which represent the memory space inside 
the PLC. We use the DataBlocks for HMI communication (by way of Ethernet connection) to read/write memory space of/to 
I/O of the PLC hardware. By implementing condition statements between I/O and DataBlocks into TIA Program Blocks, 
we can control PLC I/O through Python.

Address Example for DataBlocks: DB1.DBX0.1
db_number = 1
start_offset = 0
bool_index = 1 (bool_index goes from 0 to 7, after 8 bits new byte starts (start_offset = 1)

reading memory bool:
client.db_read(db_number, start_offset, size)
size = 1 because we only need one byte for boolean (boolean bit_size = 1 but PLC operates with minimum of byte datasize)

client.db_read gives bytearray of one byte length, e.g. client.db_read = bytearray([0b00000001])
snap7.util.get_bool(bytearray_: bytearray, byte_index: int, bool_index: int) → bool
Get the boolean value from location in bytearray.
Location here is byte_index = 0.

writing memory bool:
snap7.util.set_bool(bytearray_: bytearray, byte_index: int, bool_index: int, value: bool)
Set boolean value on location in bytearray.
Value: 1=true, 0=false
 """

def read_bool(db_number, start_offset, bit_offset):
    reading = plc.db_read(db_number, start_offset, 1)
    bool = snap7.util.get_bool(reading, 0, bit_offset)
    return bool


def write_bool(db_number, start_offset, bit_offset, value):
    reading = plc.db_read(db_number, start_offset, 1)
    snap7.util.set_bool(reading, 0, bit_offset, value)
    plc.db_write(db_number, start_offset, reading)
    return None



def microswitch():
    IP = '192.168.0.1'
    RACK = 0
    SLOT = 1

    plc = snap7.client.Client()
    plc.connect(IP, RACK, SLOT)
    while True:
        try:
            db_number = 1
            start_offset = 0
            bit_offset = 0  # Microswitch
            if read_bool(db_number, start_offset, bit_offset):
                bit_offset = 1  # Zeiss_Input
                value = 1
                write_bool(db_number, start_offset, bit_offset, value)
                print("Sample Holder in Position")
                break
            else:
                print("Sample Holder NOT in Position")
        except:
            print("Interrupt")


def fire_signal():
    IP = '192.168.0.1'
    RACK = 0
    SLOT = 1

    plc = snap7.client.Client()
    plc.connect(IP, RACK, SLOT)
    while True:
        try:
            db_number = 1
            start_offset = 0
            bit_offset = 2  # Zeiss_Output
            if read_bool(db_number, start_offset, bit_offset):
                print("Measurement finished")
                time.sleep(30)
                fire_results()
                break
        except:
            print("Interrupt")

