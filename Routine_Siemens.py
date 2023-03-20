from Positioning import positioning_MTP, homing_MTP
from Siemens_PLC import fire_signal, sensor1, switch, plc, IP, RACK, SLOT
from Snapshot import snapshot
import snap7


horizontal = 95
vertical = 0
sample_distance = 42
nikon_distance = 457


for i in range(10000):
    plc = snap7.client.Client()
    plc.connect(IP, RACK, SLOT)
    homing_MTP()
    positioning_MTP(vertical, horizontal)
    sensor1()
    fire_signal()
    positioning_MTP(vertical, horizontal + sample_distance)
    # sensor1()
    switch()
    fire_signal()
    positioning_MTP(vertical, nikon_distance)
    snapshot()
    positioning_MTP(vertical, nikon_distance + sample_distance)
    snapshot()
    plc.disconnect()
    plc.destroy()

