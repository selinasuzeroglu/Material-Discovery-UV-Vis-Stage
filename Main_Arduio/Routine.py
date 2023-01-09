import time

from Positioning import positioning_MTP, homing_MTP
from Trigger_InProcess_Input import microswitch
from Trigger_InProcess_Output import fire_signal


homing_MTP()
positioning_MTP(20, 20)
time.sleep(2)
microswitch()
time.sleep(2)
fire_signal()
positioning_MTP(25, 0)
