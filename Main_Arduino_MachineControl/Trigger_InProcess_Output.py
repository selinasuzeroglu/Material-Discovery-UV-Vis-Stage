import serial
import time
from SQL_Plot_Results import fire_results


def fire_signal():
    InProcessOutput = serial.Serial('COM13', 9600, timeout=1)
    time.sleep(2)
    InProcessOutput.flushInput()
    time.sleep(2)
    while True:
        try:
            Micro_bytes = InProcessOutput.readline()
            decoded_bytes = float(Micro_bytes[0:len(Micro_bytes) - 2].decode("utf-8"))
            if decoded_bytes == float(0.0):
                print("Measurement finished")
                time.sleep(30)
                fire_results()
                break
            else:
                print("Waiting for measurement to finish")

        except:
            print("Interrupt")

    InProcessOutput.close()

fire_signal()