import snap7
from snap7.util import *
from snap7.types import *


def read_memory(plc, byte, bit, datatype):
    result = plc.read_area(areas['MK'], 0, byte, datatype)
    if datatype == S7WLBit:
        return get_bool(result, 0, 1)
    elif datatype == S7WLByte or datatype == S7WLWord:
        return get_int(result, 0)
    elif datatype == S7WLReal:
        return get_real(result, 0)
    elif datatype == S7WLDWord:
        return get_dword(result, 0)
    else:
        return None


def write_memory(plc, byte, bit, datatype, value):
    result = plc.read_area(areas['MK'], 0, byte, datatype)
    if datatype == S7WLBit:
        set_bool(result, 0, bit, value)
    elif datatype == S7WLByte or datatype == S7WLWord:
        set_int(result, 0, value)
    elif datatype == S7WLReal:
        set_real(result, 0, value)
    elif datatype == S7WLDWord:
        set_dword(result, 0, value)
    plc.write_area(areas['MK'], 0, byte, result)


IP = '192.168.0.1'
RACK = 0
SLOT = 1

plc = snap7.client.Client()
plc.connect(IP, RACK, SLOT)

while True:
    readbit = read_memory(plc, 0, 1, S7WLBit)
    print(readbit) #if readbit TRUE, initiate SQL process


#microswitch must be connected to PLC as INPUT. As soon as microawith INPUT is HIGH, OUTPUT to InProcess must be send. This can be arranged within the TIA system.
#Second INPUT from InProcess to PLC enables signal sending as sson as measurements are completed. ReadMemory at sepcific INPUT and for TRUE get (after 30s) SQL data.
# Source: https://www.youtube.com/watch?v=u1WQFP2l29k&ab_channel=EndrikaD.Marselino