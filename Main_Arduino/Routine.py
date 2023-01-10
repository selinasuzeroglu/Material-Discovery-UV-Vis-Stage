import time

from Positioning import positioning_MTP, homing_MTP
from Trigger_InProcess_Input import microswitch
from Trigger_InProcess_Output import fire_signal

horizontal = 50
vertical = 50
sample_distance = 32.5


homing_MTP()
positioning_MTP(vertical, horizontal)
positioning_MTP(vertical, horizontal + sample_distance)
positioning_MTP(vertical, horizontal + 2*sample_distance)
homing_MTP()

