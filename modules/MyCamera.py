# -*- coding: utf-8 -*-
"""
Created on Mon Sep 03 15:32:13 2018

"""
# -*- coding: utf-8 -*-

import cv2
from memory_profiler import profile

class CameraCapture(object):
    def __init__(self):
        self.my_camera = None
        self.my_camera_fps = 0
        self.my_camera_resolution=()

    @profile
    def isOpen(self):        
        if not self.my_camera is None:
            return self.my_camera.isOpened()
        else:
            return False

    @profile
    def open(self):
        self.my_camera=cv2.VideoCapture(0,cv2.CAP_DSHOW)
        self.my_camera_fps= self.my_camera.get(cv2.CAP_PROP_FPS)
        print('camera fps:',self.my_camera_fps)
        self.my_camera_resolution=(int(self.my_camera.get(cv2.CAP_PROP_FRAME_WIDTH)),int(self.my_camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        print('camera resolution:',self.my_camera_resolution)

    @profile
    def imageCapture(self,picName,frameNum):
        i=1
        while i<=frameNum:
            isSuccess,frame = self.my_camera.read()
            if isSuccess:
                #cv2.imshow("My Capture",frame)
                # flip_hv = cv2.flip(frame, 0)
                cv2.imwrite(picName+'_'+str(i)+'.jpg', frame)
            i+=1

    @profile
    def videoCapture(self,vidName,duration):
    
        self.my_camera.set(3,640)
        self.my_camera.set(4,480)
        self.my_camera.set(1,10.0)
        
        # fourcc=cv2.cv.CV_FOURCC('m','p','4','v')
        fourcc=cv2.VideoWriter_fourcc('I','4','2','0')
        # fourccs = cv2.imwrite('RGB.jpg', self.flip_hv)
        out = cv2.VideoWriter(vidName+'.avi',fourcc,30,(640,480))
        print(vidName)
        print(self.my_camera.isOpened())
        
        n=1
        framenumber=int(duration)*30
        while n<=framenumber:
            ret,frame = self.my_camera.read()
            # frame = cv2.flip(frame,0)
            if ret == True:
                out.write(frame)
                # cv2.imshow("frame",frame)
                #if cv2.waitKey(1) &0xFF == ord('q'):
                   #break
            else:
                break
            n+=1
        self.my_camera.release()
        out.release()
        #cv2.destroyAllWindows()

    @profile
    def close(self):
        if self.my_camera.isOpened():
            self.my_camera.release()
            #cv2.destroyAllWindows()


if __name__ == "__main__":
    
    cap = CameraCapture()
    cap.open()
    print(cap.isOpen())
    cap.imageCapture('cherry_test',3)
    cap.videoCapture('cherry_test',5)
    cap.close()
    #cap.videoCapture('cherry_video',1)


