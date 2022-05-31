import cv2
import numpy as np
import cvzone
import pickle

rectW,rectH=107,48

cap=cv2.VideoCapture('carPark.mp4')

output = cv2.VideoWriter("output.avi",cv2.VideoWriter_fourcc(*'MPEG'),30,(1080,1920))

with open('carParkPos','rb') as f:
    posList=pickle.load(f)
frame_counter = 0

def check(imgPro):
    spaceCount=0
    for pos in posList:
        x,y=pos
        crop=imgPro[y:y+rectH,x:x+rectW]
        count=cv2.countNonZero(crop)
        cvzone.putTextRect(img,str(count),(x,y+rectH-3),scale=1,thickness=2,offset=0,colorR=(255,0,255))
        if count<900:
            spaceCount+=1
            color=(0,255,0)
            thick=4
        else:
            color=(0,69,255)
            thick=2

        cv2.rectangle(img,pos,(x+rectW,y+rectH),color,thick)
    cv2.rectangle(img,(45,30),(640,75),(255,0,0),-1)
    cv2.putText(img,f'Available Space: {spaceCount}/{len(posList)}'f' long time : {len(posList)-spaceCount}',(50,60),cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,255,255),2)

while True:
    _,img=cap.read()
    if frame_counter == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        frame_counter = 0 #Or whatever as long as it is the same as next line
        cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, 0)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(gray,(3,3),1)
    Thre=cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)
    blur=cv2.medianBlur(Thre,5)
    kernel=np.ones((3,3),np.uint8)
    dilate=cv2.dilate(blur,kernel,iterations=1)
    check(dilate)
    output.write(frame_counter)
    cv2.imshow("output",frame_counter)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        break

    cv2.imshow("Image",img)
    cv2.waitKey(10)
