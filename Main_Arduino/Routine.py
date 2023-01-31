import time

from Positioning import positioning_MTP, homing_MTP
from Trigger_InProcess_Input import microswitch
from Trigger_InProcess_Output import fire_signal
# from Camera import *
from single_snapshot import snapshot

horizontal = 50
vertical = 50
sample_distance = 32.5


sample_list = []
sample_list = [item for item in input("Enter the list items : ").split()]
image_index = 0

snapshot()
# homing_MTP()
# positioning_MTP(vertical, horizontal)
# microswitch()
# fire_signal()
# camera.capture_single_image(autofocus=True)
# positioning_MTP(vertical, horizontal + sample_distance)
# camera.capture_single_image(autofocus=True)
# positioning_MTP(vertical, horizontal + 2*sample_distance)
# camera.capture_single_image(autofocus=True)
# homing_MTP()
#
