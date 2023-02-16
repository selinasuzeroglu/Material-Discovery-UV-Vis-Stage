import snap7

IP = '192.168.0.1'
RACK = 0
SLOT = 1

plc = snap7.client.Client()
plc.connect(IP, RACK, SLOT)
state = plc.get_cpu_state()
print(f'State: {state}')

db_number = 1
start_offset = 0
bit_offset = 0
value = 1  # 1 = true | 0 = false

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
bool_index = 1

reading memory bool:
client.db_read(db_number, start_offset, size)
size = 1 because we only need one byte for boolean (boolean_bitsize = 1 but PLC operates with minimum of byte datasize)

client.db_read gives bytearray of one byte length, e.g. client.db_read = bytearray([0b00000001])
snap7.util.get_bool(bytearray_: bytearray, byte_index: int, bool_index: int) → bool
Get the boolean value from location in bytearray
 """
def write_bool(db_number, start_offset, bit_offset, value):
    reading = plc.db_read(db_number, start_offset, 1)
    snap7.util.set_bool(reading, 0, bit_offset, value)  # (value 1= true;0=false)
    plc.db_write(db_number, start_offset, reading)  # write back the bytearray and now the boolean value is changed in the PLC.
    return None


def read_bool(db_number, start_offset, bit_offset):
    reading = plc.db_read(db_number, start_offset, 1)
    bool = snap7.util.get_bool(reading, 0, bit_offset)
    return bool




write_bool(db_number, start_offset, 0, value)
read_bool(db_number, start_offset, 1)
