from zaber_motion import Units, Library
from zaber_motion.ascii import Connection

Library.enable_device_db_store()

with Connection.open_serial_port("COM7") as connection:
    device_list = connection.detect_devices()
    print("Found {} devices".format(len(device_list)))

    device_v = device_list[0]  # h = horizontal
    device_h = device_list[1]  # v = vertical

    axis_h = device_h.get_axis(1)  # get axis (1 out of 1) for device_v
    axis_v = device_v.get_axis(1)  # get axis (1 out of 1) for device_h

    h = 20
    v = 20


    # retries = 0
    # max_retries = 4

    def place_on_sample(h, v):
        axis_h.move_absolute(h, Units.LENGTH_MILLIMETRES, wait_until_idle=True)
        axis_v.move_absolute(v, Units.LENGTH_MILLIMETRES, wait_until_idle=True)


    # do we need that?
    def place_off_sample():
        axis_v.home(wait_until_idle=False)
        axis_h.home(wait_until_idle=False)


    position_h = 8063.0 * h  # 1mm gets 0.863mm as position
    position_v = 8063.0 * v


    def homing():
        for i in range(0, 3):
            if connection.home_all(wait_until_idle=True):
                print("Axes are homed")
                break  # has to go
            else:
                connection.home_all(wait_until_idle=True)
                break  # has to go


    def placing():
        for i in range(0, 3):
            if axis_h.get_position() == position_h and axis_v.get_position() == position_v:
                axis_h.park()
                axis_v.park()
                print("Sample is placed")
            else:
                place_on_sample(h, v)
                axis_h.park()
                axis_v.park()


    placing()

    print(axis_h.get_position())
    print(axis_v.get_position())
    axis_h.unpark()
    axis_v.unpark()


print("ok")