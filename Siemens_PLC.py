import snap7
import time
from SQL_plot_results import fire_results

IP = '192.168.0.1'
RACK = 0
SLOT = 1
plc = snap7.client.Client()


# state = plc.get_cpu_state()
# print(f'State: {state}')

class MemorySpace:
    def __init__(self, db_number, start_offset, bit_offset):
        self.db_number = db_number
        self.start_offset = start_offset
        self.bit_offset = bit_offset

    def read_bool(self):
        reading = plc.db_read(self.db_number, self.start_offset, 1)
        bool = snap7.util.get_bool(reading, 0, self.bit_offset)
        return bool

    def write_bool(self, value):
        reading = plc.db_read(self.db_number, self.start_offset, 1)
        snap7.util.set_bool(reading, 0, self.bit_offset, value)
        plc.db_write(self.db_number, self.start_offset, reading)
        return None

    def read_real(self):
        reading = plc.db_read(self.db_number, self.start_offset, 4)
        real = snap7.util.get_real(reading, 0)
        return real


Microswitch = MemorySpace(1, 8, 0)
ZeissTriggerIN = MemorySpace(1, 8, 1)
ZeissTriggerOUT = MemorySpace(1, 8, 2)
Sensor1 = MemorySpace(1, 4, 0)
Sensor2 = MemorySpace(1, 0, 0)


def microswitch():
    while True:
        if plc.get_connected():
            try:
                if Microswitch.read_bool():
                    ZeissTriggerIN.write_bool(1)
                    print("Sample Holder in Position")
                    time.sleep(2)
                    ZeissTriggerIN.write_bool(0)
                    break
                else:
                    ZeissTriggerIN.write_bool(0)
                    print("Sample Holder NOT in Position")
            except:
                continue
        if not plc.get_connected():
            try:
                print('not connected')
                plc.connect(IP, RACK, SLOT)
                time.sleep(0.2)
            except:
                continue


def fire_signal():
    while True:
        if plc.get_connected():
            try:
                if ZeissTriggerOUT.read_bool():
                    print("Measurement finished")
                    time.sleep(15)
                    fire_results()
                    break
                else:
                    print("Waiting for measurement to finish")
            except:
                continue
        if not plc.get_connected():
            try:
                plc.connect(IP, RACK, SLOT)
                print('not connected')
                time.sleep(0.2)
            except:
                continue


def switch():
    while True:
        if plc.get_connected():
            ZeissTriggerIN.write_bool(1)
            print("Sample Holder in Position")
            time.sleep(2)
            ZeissTriggerIN.write_bool(0)
            break
        if not plc.get_connected():
            try:
                plc.connect(IP, RACK, SLOT)
                print('not connected')
                time.sleep(0.2)
            except:
                continue


def sensor1():
    while True:
        if plc.get_connected():
            try:
                if Sensor1.read_real() > 0.025:
                    ZeissTriggerIN.write_bool(1)
                    print("Sample Holder in Position")
                    time.sleep(2)
                    ZeissTriggerIN.write_bool(0)
                    break
                else:
                    ZeissTriggerIN.write_bool(0)
                    print("Sample Holder NOT in Position")
            except:
                continue
        if not plc.get_connected():
            try:
                plc.connect(IP, RACK, SLOT)
                print('not connected')
                time.sleep(0.2)
            except:
                continue


def sensor2():
    while True:
        if plc.get_connected():
            try:
                if Sensor2.read_real() > 0.025:
                    ZeissTriggerIN.write_bool(1)
                    print("Sample Holder in Position")
                    time.sleep(2)
                    ZeissTriggerIN.write_bool(0)
                    break
                else:
                    ZeissTriggerIN.write_bool(0)
                    print("Sample Holder NOT in Position")
            except:
                continue
        if not plc.get_connected():
            try:
                plc.connect(IP, RACK, SLOT)
                print('not connected')
                time.sleep(0.2)
            except:
                continue

