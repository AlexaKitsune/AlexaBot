import serial
import time
import json

ser = serial.Serial('COM4', 9600, write_timeout=1)

def send_data(data_):
    global ser
    try:
        data_ = json.dumps(data_, separators=(",", ":")) + "\n"
        ser.write(data_.encode("utf-8"))
        ser.flush()
        time.sleep(0.01)
    except serial.SerialTimeoutException as e:
        print("Excepción de tiempo de espera al escribir en el puerto serial:", str(e))
        ser.close()
        ser = serial.Serial('COM4', 9600, write_timeout=1)
        data_ = json.dumps({"READY": 1}, separators=(",", ":")) + "\n"
        ser.write(data_.encode("utf-8"))
        time.sleep(0.01)
    except Exception as e:
        print("Otra excepción al escribir en el puerto serial:", str(e))
        ser.close()
        ser = serial.Serial('COM4', 9600, write_timeout=1)
