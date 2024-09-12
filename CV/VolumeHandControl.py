import numpy as np
import cv2
import HandTrackingModule as htm
import time
import math

cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)
handDetect = htm.handDetector()
pTime = 0
cTime = 0
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volrange = volume.GetVolumeRange()
volMin = volrange[0]
volMax = volrange[1]
vol = 0
volBar = 400
volPer = 0

while True:
    ret, img = cam.read()
    img = handDetect.findhands(img)
    lmlist = handDetect.findPosition(img)
    # if len(lmlist) != 0:
    #     print(lmlist[4], lmlist[8])
    if len(lmlist) != 0:
        x1,y1 = lmlist[4][1], lmlist[4][2]
        x2,y2 = lmlist[8][1], lmlist[8][2]
        cx, cy = (x2+x1) //2, (y2+y1) //2
        cv2.circle(img, (x1,y1), 8, (255,0, 255), -1)
        cv2.circle(img, (x2,y2), 8, (255,0,255), -1)
        cv2.line(img, (x1,y1), (x2,y2), (0,255,0), 2)
        cv2.circle(img, (cx, cy), 8, (255,0, 255), -1)
        length = math.sqrt((x2-x1) **2 + (y2-y1) **2)
        # print(length)
        if length < 50:
            cv2.circle(img, (cx, cy), 8, (255,127, 0), -1)
        # length_range: 50 - 250
        # vol_range: volMin - volMax
        vol = np.interp(length, [50,250], [volMin, volMax])
        volBar = np.interp(length, [50,250], [400, 150])
        volPer = np.interp(length, [50,250], [0, 100])
        volume.SetMasterVolumeLevel(vol, None)
    
    img = cv2.flip(img, 1)
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 2)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255,0,0), cv2.FILLED)
    cv2.putText(img, str(int(volPer)) + "%", (50, 430), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 2)
    cv2.putText(img, str(int(fps)), (10,30), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 2)
    cv2.imshow('Volume control', img)
    if cv2.waitKey(1) & 0xFF == 27:
        break
        

        