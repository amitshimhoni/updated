import cv2
import os
from PIL import Image


def start(Name):
    print("check")
    cam = cv2.VideoCapture(0)

    cv2.namedWindow("take 5 photo of yourself")

    img_counter = 0
    path = os.path.join("/Users/amit/PycharmProjects/Lastproject/images/" + Name+"/")
    os.mkdir(path)
    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("take 5 photo of yourself", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:
            # SPACE pressed
            img_name = Name+"{}.png".format(img_counter)
            cv2.imwrite(os.path.join(path, img_name), frame)

            print("{} written!".format(img_name))
            img_counter += 1
        if img_counter == 5:
            break
    cam.release()

    cv2.destroyAllWindows()

