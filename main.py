# -*- coding: utf-8 -*-
"""
Created on Wed Aug 09 13:04:33 2017

@author: mihir
@main.py
"""
from timeWeather import clockFrame, currentWeatherFrame
from interactor import interactor
import tkinter as tk
if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg = "#000000")
    # root.attributes("-fullscreen", True) #makes it fullscreen
    root.geometry("800x900")
    #set up interactor
    acceptedUsers = ['mihir', 'avi', 'ajay']
    inter = interactor(root, acceptedUsers, vision = True, bg = "#000000")
    inter.grid(row = 0, column = 0, sticky = 'N', columnspan = 2)

    #set up time/weather elements
    clock = clockFrame(root, bg = "#000000")
    clock.grid(row = 1, column = 0, sticky = 'NW')
    weatherFrame = currentWeatherFrame(root, True, bg="#000000")
    weatherFrame.grid(row = 1, column = 1, sticky = 'NE')
    
    root.mainloop()
    
