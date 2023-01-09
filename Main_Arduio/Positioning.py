import time

from zaber_motion import Units, Library
from zaber_motion.ascii import Connection
from Trigger_InProcess_Input import microswitch
from Trigger_InProcess_Output import fire_signal


def positioning(pos):
    Library.enable_device_db_store()

    with Connection.open_serial_port("COM7") as connection:
        device_list = connection.detect_devices()
        print("Found {} devices".format(len(device_list)))

        device1 = device_list[0]
        device2 = device_list[1]

        axis_1 = device1.get_axis(1)  # get axis (1 out of 1) for device_1
        axis_2 = device2.get_axis(1)  # get axis (1 out of 1) for device_2

        class Axis:
            def __init__(self, axis, position=0):
                self.axis = axis
                self.position = position

            def __mul__(self):
                zaber_position = self.position * 8063.0
                return zaber_position

            def __eq__(self):
                return True if self.axis.get_position() == self.position * 8063.0 else False

            def place_on_sample(self):
                self.axis.move_absolute(self.position, Units.LENGTH_MILLIMETRES, wait_until_idle=True)

            def place_off_sample(self):
                self.axis.home(wait_until_idle=False)

            def park(self):
                self.axis.park()

            def unpark(self):
                self.axis.unpark()

        def placing(axis_posn):
            for i in range(0, 3):
                if axis_posn.__eq__() is True:
                    axis_posn.park()
                    print("Sample is placed")
                else:
                    axis_posn.place_on_sample()
                    axis_posn.park()

        def unparking(axis_posn):
            axis_posn.unpark()

        axis1_pos = Axis(axis_1, pos)

        placing(axis1_pos)
        unparking(axis1_pos)


def homing_MTP():
    Library.enable_device_db_store()

    with Connection.open_serial_port("COM7") as connection:
        device_list = connection.detect_devices()
        print("Found {} devices".format(len(device_list)))

        device1 = device_list[0]
        device2 = device_list[1]

        axis_1 = device1.get_axis(1)  # get axis (1 out of 1) for device_1
        axis_2 = device2.get_axis(1)  # get axis (1 out of 1) for device_2

        def homing():
            for i in range(0, 3):
                if connection.home_all(wait_until_idle=True):  # home all devices or, alternatively, use same approach as for placing: for axis in axes_posn: axis.place_off_sample()
                    print("Axes are homed")
                    break  # has to go
                else:
                    connection.home_all(wait_until_idle=True)
                    break  # has to go

        homing()


time.sleep(2)
microswitch()
time.sleep(2)
fire_signal()
