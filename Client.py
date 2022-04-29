import socket
import cv2
import protocol
import os
import subprocess
from PIL import ImageGrab
import PIL
from time import sleep
import threading

IP = socket.gethostbyname(socket.gethostname())
s = socket.socket()
PORT = 5566
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

def send_picture(client_socket):
    """The function sends the picture for identification """
    image_path = r"my-image.png"  # שמירת מיקומו של צילום המסך במשתנה
    send_file(client_socket, image_path)  # העברת צילום המסך
    os.remove("my-image.png")  # מחיקת התמונה מהמחשב עליו רץ השרת
def send_file(client_socket, file_path):
    """The function sends the file to the client"""

    file_size = os.path.getsize(file_path)  # קבלת גודל הקובץ/התמונה
    client_socket.send(protocol.create_msg(str(file_size)))  # שולח ללקוח את גודל הקובץ/התמונה

    with open(file_path, "rb") as f:
        total = 0
        while total < file_size:  # העברה בחלקים
            buffer = f.read(4096)
            client_socket.send(protocol.create_msg(buffer))
            print(buffer)
            total += len(buffer)
        f.close()
        print("done sending")

def save_picture(img_item, roi_gray,client):
    thread = threading.Thread(target=save_picture, args=(img_item, roi_gray))
    thread.start()
    cv2.imwrite(img_item, roi_gray)
    sleep(0.3)
    send_picture(client)



def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")

    connected = True
    while connected:
        import cv2
        import numpy as np

        cap = cv2.VideoCapture(0)
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default2.xml')
        while True:
            # capture frame by frame
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
            for (x, y, w, h) in faces:
                print(x, y, w, h)
                roi_gray = gray[y:y + h, x:x + w]
                roi_color = frame[y:y + h, x:x + w]
                img_item = "my-image.png"
                save_picture(img_item, roi_gray, client)




                color = (255, 0, 0)
                stroke = 2
                end_cord_x = x + w
                end_cord_y = y + h
                cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
            # Display the resulting frame
            cv2.imshow('frame', frame)
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break
            sleep(0.1)





if __name__ == "__main__":
    main()
