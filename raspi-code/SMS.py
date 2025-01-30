import threading
import RPi.GPIO as GPIO
import serial
import time

# Definiere das Lock
serial_lock = threading.Lock()

ser = serial.Serial("/dev/ttyAMA0", 115200)
ser.flushInput()

phone_number = '015733666642'  # Die Telefonnummer zum Senden der SMS
text_message = 'test'
power_key = 6

def send_at(command, back, timeout):
    print("command", command)
    rec_buff = ''
    ser.write((command+'\r\n').encode())
    time.sleep(timeout)
    if ser.inWaiting():
        time.sleep(0.01)
        rec_buff = ser.read(ser.inWaiting()).decode('utf-8')
    print("rec_buff", rec_buff)
    if back not in rec_buff:
        print(command + ' ERROR')
        print(command + ' back:\t' + rec_buff)
        return 0
    else:
        return 1

def SendShortMessage(phone_number, text_message):
    power_on(power_key)
    print("Setting SMS mode...")
    send_at("AT+CMGF=1", "OK", 1)
    print("Sending Short Message")
    answer = send_at("AT+CMGS=\""+phone_number+"\"", ">", 2)
    if 1 == answer:
        ser.write(text_message.encode())
        ser.write(b'\x1A')
        answer = send_at('', "OK", 20)
        if 1 == answer:
            print('send successfully')
        else:
            print('error')
    else:
        print('error%d' % answer)
    power_down(power_key)

def power_on(power_key):
    print('SIM7600X is starting:')
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(power_key, GPIO.OUT)
    time.sleep(0.1)
    GPIO.output(power_key, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(power_key, GPIO.LOW)
    time.sleep(20)
    ser.flushInput()
    print('SIM7600X is ready')

def power_down(power_key):
    print('SIM7600X is logging off:')
    GPIO.output(power_key, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(power_key, GPIO.LOW)
    time.sleep(18)
    print('Good bye')

# Thread-safe SMS senden
def send_message_thread(animal):
    with serial_lock:  # Lock wird verwendet, um den Zugriff zu synchronisieren
        SendShortMessage("015733666642", f"Ein {animal} wurde gesehen!")

# Test der Funktion im Hauptthread
if __name__ == "__main__":
    threading.Thread(target=send_message_thread, args=("Wolf",)).start()