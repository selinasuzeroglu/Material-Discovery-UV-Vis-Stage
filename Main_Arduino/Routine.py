import time

from Positioning import positioning_MTP, homing_MTP
from Trigger_InProcess_Input import microswitch
from Trigger_InProcess_Output import fire_signal
from Nikon_Remote_Control.single_snapshot import snapshot

horizontal = 50
vertical = 50
sample_distance = 32.5


homing_MTP()
positioning_MTP(vertical, horizontal)
time.sleep(1)
snapshot()
positioning_MTP(vertical, horizontal + sample_distance)
time.sleep(1)
snapshot()
positioning_MTP(vertical, horizontal + 2*sample_distance)
time.sleep(1)
snapshot()
homing_MTP()

