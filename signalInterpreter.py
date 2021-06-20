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

folderPath = "imgAssets"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

while True:
    success, img = cap.read()
    img = detector.getPose(img)
    landmarkList = detector.getPosition(img, draw=False)
    x10, y10 = landmarkList[10][1:]
    x11, y11 = landmarkList[11][1:]
    x12, y12 = landmarkList[12][1:]
    x13, y13 = landmarkList[13][1:]
    x14, y14 = landmarkList[14][1:]
    x15, y15 = landmarkList[15][1:]
    x16, y16 = landmarkList[16][1:]
    x23, y23 = landmarkList[23][1:]

    Angle = detector.getAngle(img)
    if y15 < y10 and y16 < y10 and 115 < Angle < 160:
        img[5:205, 5:205] = overlayList[0]
        cv2.putText(img, "HAND SIGNAL NO. 1", (390, 550), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)
    elif (y16 < y10 < y15 and y15 < (y11 +((y23-y11)/2)) and 120 < Angle < 180) or (y15 < y10 < y16 and y16 < (y11 +((y23-y11)/2)) and 120 < Angle < 180):
        img[5:205, 5:205] = overlayList[1]
        cv2.putText(img, "HAND SIGNAL NO. 2", (390, 550), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)
    elif (y16 > y14 and y10 < y15 and x15 > x13 and 220 < Angle < 250) or (
            y15 > y13 and y16 > y10 and x16 < x14 and 220 < Angle < 250):
        img[5:205, 5:205] = overlayList[2]
        cv2.putText(img, "HAND SIGNAL NO. 3", (390, 550), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)
    elif (y16 > y14 and y15 < y13 and y13 < y10 and 120 < Angle < 160) or (y15 > y13 and y16 < y14 and y14 < y10 and 120 < Angle < 160):
        img[5:205, 5:205] = overlayList[3]
        cv2.putText(img, "HAND SIGNAL NO. 4", (390, 550), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)
    elif (y16 < y10 < y15 and y15 < (y11 +((y23-y11)/2)) and 75 < Angle < 105) or (y15 < y10 < y16 and y16 < (y11 +((y23-y11)/2)) and 75 < Angle < 105):
        img[5:205, 5:205] = overlayList[4]
        cv2.putText(img, "HAND SIGNAL NO. 5", (390, 550), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)
    elif (y10 < y16 and y16 <y23 and y10 < y15 and y15 < y23  and 165 < Angle < 195):
        img[5:205, 5:205] = overlayList[5]
        cv2.putText(img, "HAND SIGNAL NO. 6", (390, 550), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)
    elif (y15 < y10 and y16 < y10 and 75 < Angle < 115):
        img[5:205, 5:205] = overlayList[6]
        cv2.putText(img, "HAND SIGNAL NO. 7", (390, 550), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)
    else :
        img[5:205, 5:205] = overlayList[7]
        cv2.putText(img, "NO VALID HAND SIGNAL", (387, 550), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)


    currentTime = time.time()
    fps = 1 / (currentTime - previousTime)
    previousTime = currentTime

    cv2.putText(img, "FPS: " + str(int(fps)), (5, 570), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
    cv2.putText(img, "github.com/bhavy2908", (830, 19), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)
    cv2.putText(img, "OVER SMART TRAFFIC", (390, 25), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)

    cv2.imshow("Over Smart Traffic - Bhavy", img)
    cv2.waitKey(1)
