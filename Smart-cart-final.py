from os import read
import cv2
from cv2 import data
from pyzbar import pyzbar
import pyrebase
import time
import numpy as np
import serial
import adafruit_us100

barcode_text=0
def read_barcode(frame):
    #Reading the frame from the camera and decoding it using Pyzbar python library
    barcodes=pyzbar.decode(frame)
    for barcode in barcodes:
        x, y, w, h=barcode.rect
        barcode_text=barcode.data.decode('utf-8')
        push_to_db(barcode_text)
        if barcode_text:
            break

def main():
    #Main function to activate the camera live feed using cv2 and send each frame to read_barcode function to decode it and identify barcodes
    camera=cv2.VideoCapture(0)
    ret, frame= camera.read()
    while ret:
        ret, frame=camera.read()
        read_barcode(frame)
        break
    camera.release()
    cv2.destroyAllWindows()




def push_to_db (barcode_text):
    firebaseConfig = {
    'apiKey': "AIzaSyDnJvvik1UPpFqEEaGFk68zQAMrf-WJX8k",
    'authDomain': "shopping-cart-1543f.firebaseapp.com",
    'databaseURL': "https://shopping-cart-1543f-default-rtdb.asia-southeast1.firebasedatabase.app",
    'projectId': "shopping-cart-1543f",
    'storageBucket': "shopping-cart-1543f.appspot.com",
    'messagingSenderId': "505850601943",
    'appId': "1:505850601943:web:9ad17cb4f8e10b21b4ab92",
    'measurementId': "G-V4E307VXS5"
    }
    #Firebase config to connect to the realtime database in Firebase
    firebase = pyrebase.initialize_app(firebaseConfig)
    db=firebase.database()
    db_size=db.child('ucart').get()
    db.child('ucart').child(np.size(db_size.val())).set(data)
    #Logic to find the index of cart in database and add the new barcode immediately after it


uart = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
us100 = adafruit_us100.US100(uart)
while True:
    if us100.distance<18:
        main()

#print("Distance: ", us100.distance)

#firebase = pyrebase.initialize_app(firebaseConfig)
#db=firebase.database()

#data={'id':12345}
#db.child(1).set(data)
