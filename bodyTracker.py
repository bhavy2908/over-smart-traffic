import cv2
import mediapipe as mp
import time
import math


class poseDetector:

    def __init__(self, mode=False, upBody=False, smooth=True,
                 detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth,
                                     self.detectionCon, self.trackCon)

    def getPose(self, img, draw=False):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)
        return img

    def getPosition(self, img, draw=False):
        self.landmarkList = []
        if self.results.pose_landmarks:

            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.landmarkList.append([id, cx, cy])

        return self.landmarkList

    def getAngle(self, img, draw=True):

        x1, y1 = self.landmarkList[16][1:]
        x2, y2 = self.landmarkList[12][1:]
        x3, y3 = self.landmarkList[15][1:]
        if y3 < y1:
            x1, y1 = self.landmarkList[16][1:]
            x2, y2 = self.landmarkList[11][1:]
            x3, y3 = self.landmarkList[15][1:]
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                             math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360
        print(int(angle))
        cv2.putText(img, "Angle: " + str(int(angle)), (840, 565),
                    cv2.FONT_HERSHEY_PLAIN, 2, (220, 100, 0), 3)
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10, (220, 100, 0), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (220, 100, 0), 2)
            cv2.circle(img, (x2, y2), 10, (220, 100, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (220, 100, 0), 2)
            cv2.circle(img, (x3, y3), 10, (220, 100, 0), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (220, 100, 0), 2)
        return angle



def main():
    cap = cv2.VideoCapture(0)
    previousTime = 0
    detector = poseDetector()
    while True:
        success, img = cap.read()
        img = detector.getPose(img)
        landmarkList = detector.getPosition(img, draw=False)
        detector.getAngle(img)

        currentTime = time.time()
        fps = 1 / (currentTime - previousTime)
        previousTime = currentTime

        cv2.putText(img, str(int(fps)), (10, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

        cv2.imshow("Tracker", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
