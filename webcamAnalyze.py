# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 16:46:44 2017

@author: mihir
@description: objects that analyze camera feed

"""

import cv2
import numpy as np
import os

class analyzer():
    results = ['dark', 'face', 'unknown']
    cascadePath = "C:/Users/mihir/Haarcascades/haarcascade_frontalface_default.xml"
    recognition_conf_thresh = 50
    facesdir = "C:/Users/mihir/mirror/faces/"
    hashMapUsers = {} #key: hash(names), value: name string
    def __init__(self):
        global faceDetector
        faceDetector = cv2.CascadeClassifier(self.cascadePath)
        # used for face RECOGNITION
        global recognizer
        recognizer = cv2.createLBPHFaceRecognizer()  
        
        #train recognizer
        if not len(os.listdir(self.facesdir)) >= 1: # if no faces folders
            print ("Error: cannot train without face images")
            exit()
        # propogate image and name list
        faceFolders = os.listdir(self.facesdir)
        print faceFolders
        imageList = []
        nameList = []
        for folder in faceFolders:
            images = os.listdir(self.facesdir + folder + "/")
            self.hashMapUsers[hash(folder)] = folder
            for face in images:
                imageList.append(cv2.imread(self.facesdir + folder + "/" + face, 0))
                nameList.append(hash(folder))
        # print imageList
        # print nameList
        print self.hashMapUsers
        recognizer.train(imageList, np.array(nameList))
    def getFaceBox(self, image):
        '''uses faceDetector to check if a face is detected
        @param image
        @returns box(es) containing position of face(s) '''
        faces = faceDetector.detectMultiScale(image)
        boxes = []
        for (x, y, w, h) in faces:
            boxes.append((x, y, w, h))
        return boxes
    def expandDatabase(self, image, name):
        '''takes pictures and adds to database'''
        # 1 : capture pics
        # 2 : save in dir (might be added to preexisting folder)
        image = cv2.pyrDown(image)
        name = name.lower().strip()
        folder = self.facesdir + name  # path of folder containing facial images
        filenum = 0
        if not os.path.exists(folder):
            os.makedirs(folder)
        else:
            filenum = len(os.listdir(folder)) + 1 # tagged on the end of filename
            print "filenum: " + str(filenum)
        boxes = self.getFaceBox(image)
        if (len(boxes) == 1):
            box = boxes[0]
            cv2.rectangle(image, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]), (0, 0, 255), 2)
            cv2.imshow(name, image)
            #grayscale, crop, equalize hist, and save
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cropped = gray[box[1] : box[1] + box[3], box[0] : box[0] + box[2]]
            norm = cv2.equalizeHist(cropped)
            cv2.imwrite(folder + '/' + str(filenum) + '.jpg', norm)
            print ("Wrote file: " + folder +"/" + str(filenum) + ".jpg")
            cv2.imshow('Cropped', norm)
        else:
            print "Error: no face or too many faces "

    def analyze(self, image):
        ''' input grayscaled image'''
        image = cv2.pyrDown(image)
        #cv2.imshow('pyrdown image', image)
        retval, thresh = cv2.threshold(image, 50, 255, cv2.THRESH_BINARY)
        #cv2.imshow('thresh', thresh)
        height, width = thresh.shape[:2]
        if cv2.countNonZero(thresh) < (height * width)/5:
            return 'dark'
        else: #this establishes the image is not dark
            faces = self.getFaceBox(image)
            if len(faces) == 0:
                return 'noface'
            names = []
            for face in faces:
                cropped = cv2.equalizeHist(image[face[1] : face[1] + face[3], face[0] : face[0] + face[2]]) #crops and equalizes
                prediction, conf = recognizer.predict(cropped)
                if (conf < self.recognition_conf_thresh):
                    names.append(self.hashMapUsers[prediction])
                    print str(conf)
            if names == []:
                return "unknown"
            return names[0]

if __name__ == "__main__":
    import sys
    from time import sleep
    train_mode = False
    train_name = ""
    if (len(sys.argv) == 2):
        train_mode = True
        train_name = sys.argv[1].strip().lower()
    print train_mode
    cap = cv2.VideoCapture(0)   
    a = analyzer()
    while True:
        ret, frame = cap.read()
        # ******GATHERING DATA********
        if (train_mode):
            a.expandDatabase(frame, train_name)
            sleep(.1)
        # ******RECOGNITION***********
        else:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            print a.analyze(frame)
        if (cv2.waitKey(1) == 13):
            break
    cap.release()
    cv2.destroyAllWindows()