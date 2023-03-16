from Positioning import positioning_MTP, homing_MTP
from Siemens_PLC import fire_signal, sensor, MemorySpace
from Snapshot import snapshot


horizontal = 95
vertical = 0
sample_distance = 42
nikon_distance = 457


# homing_MTP()
positioning_MTP(vertical, horizontal)
sensor()
fire_signal()
# positioning_MTP(vertical, horizontal + sample_distance)
# sensor()
# fire_signal()
# positioning_MTP(vertical, nikon_distance)
# snapshot()
# positioning_MTP(vertical, nikon_distance + sample_distance)
# snapshot()

