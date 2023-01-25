import time

from Positioning import positioning_MTP, homing_MTP
from Trigger_InProcess_Input import microswitch
from Trigger_InProcess_Output import fire_signal
from Camera import *


horizontal = 50
vertical = 50
sample_distance = 32.5

camera_control_cmd_path = 'C:\\Program Files (x86)\\digiCamControl\\CameraControlCmd.exe'
camera = Camera(control_cmd_location=camera_control_cmd_path)


homing_MTP()
positioning_MTP(vertical, horizontal)
time.sleep(2)
microswitch()
time.sleep(2)
fire_signal()
camera.capture_single_image(autofocus=True)
# positioning_MTP(vertical, horizontal + sample_distance)
# camera.capture_single_image(autofocus=True)
# positioning_MTP(vertical, horizontal + 2*sample_distance)
# camera.capture_single_image(autofocus=True)
homing_MTP()

