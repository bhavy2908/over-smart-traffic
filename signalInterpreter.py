import cv2
import time
import bodyTracker
import os


wCam, hCam = 1920, 1080
cap = cv2.VideoCapture(0)
cap.set(4, wCam)
cap.set(3, hCam)
pTime = 0
detector = bodyTracker.poseDetector()
previousTime = 0



while True:
    success, img = cap.read()
    img = detector.getPose(img)
    landmarkList = detector.getPosition(img, draw=False)
    Angle = detector.getAngle(img)


    currentTime = time.time()
    fps = 1 / (currentTime - previousTime)
    previousTime = currentTime

    cv2.putText(img, "FPS: " + str(int(fps)), (5, 570), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
    cv2.putText(img, "github.com/bhavy2908", (830, 19), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)
    cv2.putText(img, "OVER SMART TRAFFIC", (390, 25), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)

    cv2.imshow("Over Smart Traffic - Bhavy", img)
    cv2.waitKey(1)