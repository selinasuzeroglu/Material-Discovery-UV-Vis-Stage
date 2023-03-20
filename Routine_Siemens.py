from Positioning import positioning_MTP, homing_MTP
from Siemens_PLC import fire_signal, sensor1, sensor2, switch, IP, RACK, SLOT
from Snapshot import snapshot
import snap7


horizontal = 95
vertical = 0
sample_distance = 42
nikon_distance = 457


for i in range(10000):  # for test measurement runs, we chose to try 10000 subsequent runs.
    plc = snap7.client.Client()  # create client to communicate with PLC
    plc.connect(IP, RACK, SLOT)  # connect client to PLC
    homing_MTP()  # home vertical and horizontal Zaber stages
    positioning_MTP(vertical, horizontal)  # moving stages to 1st measurement position (1st sample)
    sensor1()  # check 1st measurement position with sensor switch
    fire_signal()  # fire data results from InProcess sample measurement
    positioning_MTP(vertical, horizontal + sample_distance)  # moving stages to 2nd measurement position (2nd sample in
    # in distance 42mm to  1st sample position)
    # sensor2() change switch to sensor2 as soon as 2nd sensor is wired up
    switch()  # for now, we used switch, because 2nd sensor wasn't build in
    fire_signal()  # fire data results from InProcess sample measurement
    positioning_MTP(vertical, nikon_distance)  # move stages to 1st photography position
    snapshot()  # 1st sample will be photographed
    positioning_MTP(vertical, nikon_distance + sample_distance)  # move stages to 2nd photography position
    snapshot()  # 2nd sample will be photographed
    plc.disconnect()  # disconnect the client from PLC
    plc.destroy()  # destroy the client communication to the PLC

