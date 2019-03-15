import cv2
import numpy as np
import  imutils
from picamera.array import PiRGBArray
from picamera import PiCamera
import datetime


camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 15
rawCapture = PiRGBArray(camera, size=(640, 480))

subtractor = cv2.createBackgroundSubtractorMOG2(history=150, varThreshold=25, detectShadows=True)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array

    mask = subtractor.apply(image)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:
        fecha = datetime.datetime.now().isoformat().replace(":", "_")
        if cv2.contourArea(c) < 5000:
            continue
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # cv2.imwrite("fuck/"+fecha+".jpg", img)
        print("foto tomada")

    rawCapture.truncate(0)
camera.release()
cv2.destroyAllWindows()