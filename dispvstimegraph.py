from collections import deque
#import numpy as np
import cv2
import math
import time
import matplotlib.pyplot as plt
import serial

ard=serial.Serial('COM7',9600,timeout=0.5)
ard.flush()
flag=0
pts = deque()
xaxis=deque()
yaxis=deque()
i=0
a=0
b=0
cap=cv2.VideoCapture(0) 
while True:
        ret,frame =cap.read()
 
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        
 
        mask = cv2.inRange(hsv, (29,66,25), (64,255,255))
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        
        if len(cnts) > 0:
                c = max(cnts, key=cv2.contourArea)
                ((r, t), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                pts.appendleft(center)
                if flag==0:
                        a,b=center
                        
                        flag+=1
                
                if(ard.read()):
                        data=ard.read()
                        
                        if(data=='a'):
                                c,d=center
                                x= math.sqrt((c-a)*(c-a)+(d-b)*(d-b))/2.0
                                x=x/37.795    #37.795 for pixels to cm
                                vel='Velocity='+repr(x)+' cm/sec'
                                print vel
                                a=c
                                b=d
                                i+=2   #time for graph
                                m,n=pts[-1]
                                cv2.circle(frame, (int(r), int(t)), int(radius),
                                (0, 120, 255), 2)
                        
                                for i in xrange(1, len(pts)):
                
                                        cv2.line(frame, pts[i - 1], pts[i], (0, 255, 0),2)

                                
                                y=math.sqrt((c-m)*(c-m)+(d-n)*(d-n))
                                xaxis.append(y)
                                yaxis.append(i)

                else:
                        cv2.circle(frame, (int(r), int(t)), int(radius),
                                (0, 120, 255), 2)
                        for i in xrange(1, len(pts)):
                
                                cv2.line(frame, pts[i - 1], pts[i], (0, 255, 0),2)

                        
        
               
                
                
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
 
        if key == ord("q"):
                break
yaxis.appendleft(0)
xaxis.appendleft(0)
plt.plot(yaxis,xaxis)
plt.ylabel('Disp(pixels)')
plt.xlabel('time')
plt.show()
