import snap7
import time
import struct
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

Address Example for DataBlocks: 
DB1.DBX4.1 (Boolean)
db_number = 1
start_offset = 4
bool_index = 1 (bool_index goes from 0 to 7, after 8 bits new byte starts (start_offset = 1)
Explanation: For boolean we only need one byte to read either 0 (=OFF) or 1 (=ON). 

DB1.DBD0 (Real)
db_number = 1
start_offset = 0
no bool_index necessary
Explanation: Reals are not read in single bytes. The whole 4 bytes are needed to read reals.


reading DataBase:
1) client.db_read(db_number, start_offset, size)
start_offset - start address (number of the byte which saves information about desired DataBase element)
size - size of information in bytes

boolean:
start_offset can be the same value for up to 8 booleans, because 8 bits are stored in one byte (0 to 7).
After that adjacent start_offset number starts.
size = 1 because we only need one byte for boolean (boolean bit_size = 1 but PLC operates with minimum of byte datasize)

real:
start_offset is individual for every real but at least 4 integers lie between start_offset of two reals or a real and
any other datatype, f.e. real_1 start_offset = 0 then real_2 start_offset = 4, or real_1 start_offset = 5 and 
bool start_offset = 9
Reason for that is that datatype real is represented in 4 bytes in the PLC, so size = 4.

client.db_read gives bytearray of byte length = size, e.g. client.db_read = bytearray([0b00000001]) one byte length 
for boolean.

2) 
snap7.util.get_bool(bytearray_: bytearray, byte_index: int, bool_index: int) → bool 
Get the boolean value from location in bytearray.
Beginning from byte_index = 0 (1st and only byte) and bool_index = 0, since bit starts at the right and refers to 0=OFF
or 1=ON, f.e. client.db_read = bytearray([0b00000001])

snap7.util.get_real(bytearray_: bytearray, byte_index: int) → float
Get the real value from reading the bytearray of size=4 beginning from byte_index = 0 (1st of 4 bytes).

3) (we don't write real value memory, so only datatype boolean is discussed here)
writing memory bool:
snap7.util.set_bool(bytearray_: bytearray, byte_index: int, bool_index: int, value: bool)
Set boolean value on location in bytearray.
Value: 1=true, 0=false
 """


class MemorySpace:
    def __init__(self, db_number, start_offset, bit_offset):
        self.db_number = db_number
        self.start_offset = start_offset
        self.bit_offset = bit_offset

    def read_bool(self):
        reading = plc.db_read(self.db_number, self.start_offset, 1)  # bool_size = 1 byte
        bool = snap7.util.get_bool(reading, 0, self.bit_offset)  # byte_index = 0 starting byte reading from beginning
        return bool

    def write_bool(self, value):
        reading = plc.db_read(self.db_number, self.start_offset, 1)
        snap7.util.set_bool(reading, 0, self.bit_offset, value)  # byte_index = 0, value = 1(=ON)/0(=OFF) for OUTPUT
        plc.db_write(self.db_number, self.start_offset, reading)
        return None

    def read_real(self):
        reading = plc.db_read(self.db_number, self.start_offset, 4)  # bool_size = 4 byte
        real = snap7.util.get_real(reading, 0)  # byte_index = 0 starting byte reading from beginning
        return real


Microswitch = MemorySpace(1, 8, 0)  # mechanical limit switch for sample position check
ZeissTriggerIN = MemorySpace(1, 8, 1)  # controlling relay connected to Zeiss device
ZeissTriggerOUT = MemorySpace(1, 8, 2)
Sensor1 = MemorySpace(1, 0, 0)  # 1st sensor limit switch for sample position check
Sensor2 = MemorySpace(1, 4, 0)  # 2nd sensor limit switch for sample position check


def microswitch():
    IP = '192.168.0.1'
    RACK = 0
    SLOT = 1
    plc = snap7.client.Client()
    plc.connect(IP, RACK, SLOT)   # connecting to PLC
    while True:
        if not plc.get_connected():
            try:
                print('not connected')
                plc.connect(IP, RACK, SLOT)
                time.sleep(0.2)
            except:
                continue
        else:
            try:
                if Microswitch.read_bool():  # if mechanical switch is triggered, signal will be sent to f.e. I0.0.
                    # for Input Signal ON(=1) → Microswitch.read_bool() = TRUE
                    # for Input I0.0 Signal OFF(=0) → Microswitch.read_bool() = FALSE
                    ZeissTriggerIN.write_bool(1)  # write Output signal to ON(=1), so relay will be turned ON.
                    # Signal will be sent to InProcess which is defined as DigitalIn Trigger and initiates measurement.
                    print("Sample Holder in Position")
                    time.sleep(2)
                    ZeissTriggerIN.write_bool(0)  # write Output signal to OFF(=0), so relay will be turned OFF and
                    # trigger for measurement start stops.
                    plc.disconnect()  # disconnecting from PLC
                    plc.destroy()  # deleting PLC memory
                    break
                else:
                    ZeissTriggerIN.write_bool(0)  # write Output signal to OFF, b.c. mechanical switch isn't triggered
                    print("Sample Holder NOT in Position")
            except:
                continue


def fire_signal():
    IP = '192.168.0.1'
    RACK = 0
    SLOT = 1
    plc = snap7.client.Client()
    plc.connect(IP, RACK, SLOT)
    while True:
        if not plc.get_connected():
            try:
                plc.connect(IP, RACK, SLOT)
                print('not connected')
                time.sleep(0.2)
            except:
                continue
        else:
            try:
                if ZeissTriggerOUT.read_bool():
                    print("Measurement finished")
                    time.sleep(30)
                    fire_results()
                    plc.disconnect()
                    plc.destroy()
                    break
                else:
                    print("Waiting for measurement to finish")
            except:
                continue


def switch():
    IP = '192.168.0.1'
    RACK = 0
    SLOT = 1
    plc = snap7.client.Client()
    plc.connect(IP, RACK, SLOT)
    while True:
        if not plc.get_connected():
            try:
                plc.connect(IP, RACK, SLOT)
                print('not connected')
                time.sleep(0.2)
            except:
                continue
        else:
            ZeissTriggerIN.write_bool(1)
            print("Sample Holder in Position")
            time.sleep(2)
            ZeissTriggerIN.write_bool(0)
            plc.disconnect()
            plc.destroy()
            break


def sensor1():
    IP = '192.168.0.1'
    RACK = 0
    SLOT = 1
    plc = snap7.client.Client()
    plc.connect(IP, RACK, SLOT)
    while True:
        if not plc.get_connected():
            try:
                plc.connect(IP, RACK, SLOT)
                print('not connected')
                time.sleep(0.2)
            except:
                continue
        else:
            try:
                if Sensor1.read_real() > 0.025:
                    ZeissTriggerIN.write_bool(1)
                    print("Sample Holder in Position")
                    time.sleep(2)
                    ZeissTriggerIN.write_bool(0)
                    plc.disconnect()
                    plc.destroy()
                    break
                else:
                    ZeissTriggerIN.write_bool(0)
                    print("Sample Holder NOT in Position")
            except:
                continue


def sensor2():
    IP = '192.168.0.1'
    RACK = 0
    SLOT = 1
    plc = snap7.client.Client()
    plc.connect(IP, RACK, SLOT)
    while True:
        if not plc.get_connected():
            try:
                plc.connect(IP, RACK, SLOT)
                print('not connected')
                time.sleep(0.2)
            except:
                continue
        else:
            try:
                if Sensor2.read_real() > 0.025:
                    ZeissTriggerIN.write_bool(1)
                    print("Sample Holder in Position")
                    time.sleep(2)
                    ZeissTriggerIN.write_bool(0)
                    plc.disconnect()
                    plc.destroy()
                    break
                else:
                    ZeissTriggerIN.write_bool(0)
                    print("Sample Holder NOT in Position")
            except:
                continue