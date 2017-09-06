# -*- coding: utf-8 -*-
"""
Created on Sun Aug 06 20:02:16 2017
@descrip : a GUI element to interact with user
    -Uses webcam analyzer to check webcam images
    -Also sets user states: ['dark', 'uknown', 'name1', 'name2', ...]
@author: mihir
"""
import Tkinter as tk
from webcamAnalyze import analyzer
import cv2
import speech_recognition as sr
import apiai
import os
import sys
import json

class interactor(tk.Frame):
    welcomeMessage = ""
    currentUserState = ""
    acceptedUsers = []
    
    userText = ""
    mirrorText = ""
    infoText = ""
    # use for speech recognition
    r = sr.Recognizer()
    device_id = 1 #index that selects mic
    
    #api ai
    CLIENT_ACCESS_TOKEN = '62d96cc2d6b347a2ac050a7afb1c0574'

    def __init__(self, root, acceptedUsers, vision = False, device_id = 1, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        
        if (vision):
            global eyes
            eyes = analyzer()
            global cap
            cap = cv2.VideoCapture(0)
        self.welcomeMessage = tk.StringVar()
        self.welcomeMessage.set("Welcome")
        self.acceptedUsers = acceptedUsers
        hello_label = tk.Label(self, textvariable = self.welcomeMessage, fg = "#ffffff", bg = "#000000", font = ("Arial", 36))
        
        self.infoText = tk.StringVar()
        info_label = tk.Label(self, textvariable = self.infoText, fg = "#ffffff", bg = "#000000", font = ("Arial", 12))
        
        self.userText = tk.StringVar()
        user_text_label = tk.Label(self, textvariable = self.userText, fg = "#ffffff", bg = "#000000", font = ("Arial", 14))
        
        self.mirrorText = tk.StringVar()
        mirror_text_label = tk.Label(self, textvariable = self.mirrorText, fg = "#ffffff", bg = "#000000", font = ("Arial", 16))
        
        hello_label.grid(row = 0, column = 0, sticky = "N")
        info_label.grid(row = 1, column = 0)
        user_text_label.grid(row = 2, column = 0)
        mirror_text_label.grid(row = 3, column = 0)
        
        self.device_id = device_id
        
        global ai
        ai = apiai.ApiAI(self.CLIENT_ACCESS_TOKEN)
        
        if (vision):
            print "Checking Webcam"
            self.checkWebcam(root)

    def checkWebcam(self, root):
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.currentUserState = eyes.analyze(frame)
        print self.currentUserState
        if (self.currentUserState == 'dark' or self.currentUserState == 'noface'):
            self.welcomeMessage.set("")
        elif (self.currentUserState == 'unknown'):
            self.welcomeMessage.set("Hello guest")
        else:
            self.welcomeMessage.set("Hello " + self.currentUserState.title())
            
        if self.currentUserState != 'noface' or self.currentUserState != 'dark':
            print self.currentUserState
            self.infoText.set("Listening...")
            root.after(50, self.listen, root)
        else:
            root.after(1000, self.checkWebcam, root)
    def listen(self, root):
        '''speech to text. Returns text'''
        #mic_list = sr.Microphone.list_microphone_names()
        #DOESNT WORK: subprocess.call(['aplay', '-nodisp', '-autoexit', 'C:/Users/mihir/beep1.wav'])
        #winsound.PlaySound('Tech Sample Pack/Designed/beep1.wav', winsound.SND_FILENAME)
    
        with sr.Microphone(device_index = self.device_id, sample_rate = 48000, chunk_size = 100) as source:		
            #r.adjust_for_ambient_noise(source, duration = 1)
            self.r.energy_threshold = 350
            self.r.non_speaking_duration = .5
            print(("listening... (" + str(self.r.energy_threshold) + ")"), "")
            audio = self.r.listen(source)
            self.infoText.set("")
        try:
            #result = r.recognize_sphinx(audio)
            result = self.r.recognize_google(audio)
            self.displayMessage("You: " + result, "")
            print result
            root.after(50, self.respondToUser, result)
            #return r.recognize_google_cloud(audio)
        except sr.UnknownValueError:
            self.infoText.set("Could not understand audio")
            print "dont understand"
        except sr.RequestError as e:
            self.infoText.set("Recog Error; {0}".format(e))
        root.after(250, self.checkWebcam, root)
        
    def displayMessage(self, userMessage, mirrorMessage):
        self.userText.set(userMessage)
        self.mirrorText.set("> " + mirrorMessage)
    
    def respondToUser(self, text):
        request = ai.text_request()
        request.query = text
        response = json.loads(request.getresponse().read())
        print (response)
        self.mirrorText.set(">" + str(response['result']['fulfillment']['speech']))
            

if __name__ == '__main__':
    root = tk.Tk()
    root.configure(bg = "#000000")
    # root.attributes("-fullscreen", True) #makes it fullscreen
    root.geometry("800x900")
    inter = interactor(root, ['mihir', 'avi'], vision = True, bg = "#000000")
    inter.grid(row = 0, column = 0, sticky = 'N')
    root.mainloop()
