##### hand tracking basics:

import imp
import cv2 as cv
import mediapipe as mp
import time 
import numpy as np
import pycaw as pc


## system volume template code of pyCaw----> can be used to alter the system volume

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volume.GetMute()
volume.GetMasterVolumeLevel()
vr=volume.GetVolumeRange()
volume.SetMasterVolumeLevel(0.0, None)


mpHands=mp.solutions.hands
handobject=mpHands.Hands()
mpDraw=mp.solutions.drawing_utils



vid=cv.VideoCapture(0)


while True:
    status,img=vid.read()  #### read every frame of the video... status->boolean indicating success or failure and img is the actual frame
    

    ### handtracking code: (note-> mediapipe module works with rgb images but opencv images are by default bgr..thus we need to convert bgr to rgb)

    rgb_frame=cv.cvtColor(img,cv.COLOR_BGR2RGB)

    resulting_hand=handobject.process(rgb_frame)


    if resulting_hand.multi_hand_landmarks is not None:
        for hand_landmark in resulting_hand.multi_hand_landmarks:


            #### each palm is divided into 21 imp 3D labels.... track them,get their coordinates and print them and also detect the wrist of the palm
            lmlist=[]
            for id,lm in enumerate(hand_landmark.landmark):
                h,w,c=img.shape

                cx,cy=int(lm.x*w),int(lm.y*h)
                #print(id,cx,cy)
                
                temp=[]
                temp.append(id)
                temp.append(cx)
                temp.append(cy)
                lmlist.append(temp)
                temp=[]
                
                cx1=0
                cy1=0
                dx1=0
                dy1=0
                #print(lmlist)
               
                
                if id==0:
                    cv.circle(img,(cx,cy),30,(100,200,244),cv.FILLED)
                
                for i in range(len(lmlist)):
                    if lmlist[i][0]==4:
                        cx1=lmlist[i][1]
                        cy1=lmlist[i][2]
                    
                    if lmlist[i][0]==8:
                        dx1=lmlist[i][1]
                        dy1=lmlist[i][2]



                    
                
            cv.line(img,(cx1,cy1),(dx1,dy1),(10,200,100),2)

            length=np.hypot(dy1-cy1,dx1-cx1)

           


            mpDraw.draw_landmarks(img,hand_landmark,mpHands.HAND_CONNECTIONS)

        min=28.4
        max=370
        minvol=vr[0]
        maxvol=vr[1]

        vol=np.interp(length,[15,370],[minvol,maxvol])
        print(int(length),vol)
        volume.SetMasterVolumeLevel(vol, None)

    cv.imshow("capture",img)
    cv.waitKey(1)