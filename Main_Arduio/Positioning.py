from zaber_motion import Units, Library
from zaber_motion.ascii import Connection


def positioning_MTP(pos_1, pos_2):
    Library.enable_device_db_store()

    with Connection.open_serial_port("COM7") as connection:
        device_list = connection.detect_devices()

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

        def placing(axes_posn):
            for i in range(0, 3):
                if all(axis.__eq__() is True for axis in axes_posn):
                    for axis in axes_posn:
                        axis.park()
                        print("Sample is placed")
                else:
                    for axis in axes_posn:
                        axis.place_on_sample()
                        axis.park()

        def unparking(axes_posn):
            for axis in axes_posn:
                axis.unpark

        axis1_pos = Axis(axis_1, pos_1)
        axis2_pos = Axis(axis_2, pos_2)
        axes_pos = [axis1_pos, axis2_pos]

        placing(axes_pos)
        unparking(axes_pos)


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


