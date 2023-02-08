import serial
import time


def microswitch():
    MicroSwitch = serial.Serial('COM6', 9600, timeout=1)
    InProcess = serial.Serial('COM9', 9600, timeout=1)
    time.sleep(2)
    MicroSwitch.flushInput()
    InProcess.flushInput()
    time.sleep(2)
    while True:
        try:
            Micro_bytes = MicroSwitch.readline()
            decoded_bytes = float(Micro_bytes[0:len(Micro_bytes) - 2].decode("utf-8"))
            if decoded_bytes == float(0.0):
                InProcess.write((bytes([0])))
                print("Sample Holder in Position")
                break

            else:
                print("Sample Holder NOT in Position")

        except:
            print("Interrupt")

    MicroSwitch.close()
    InProcess.close()



