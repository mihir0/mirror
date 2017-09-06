# -*- coding: utf-8 -*-
"""
Created on Sun Jul 30 00:22:05 2017

@author: mihir
@weather and time objects for mirror
Dark Sky API key: "2183a9b730d7b1fe85eee07601b0ccd9" 

"""
import requests
import json
import os
import Tkinter as tk
from PIL import ImageTk, Image
from datetime import datetime

class clockFrame(tk.Frame):
    strtime = ""
    strdate = ""
    tick = 12000 #update every 12 seconds
    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        # '%Y-%m-%d %H:%M:%S'
        # %I -> 12 hour time %p -> am/pm
        self.strtime = tk.StringVar()
        clock_label = tk.Label(self, textvariable = self.strtime, fg = "#ffffff", bg = "#000000", font = ("Arial", 36))
        clock_label.grid(row = 0, column = 0, sticky = "N")
        
        self.strdate = tk.StringVar()
        #self.strdate.set(datetime.now().strftime("%B, %d"))
        date_label = tk.Label(self, textvariable = self.strdate, fg = "#ffffff", bg = "#000000", font = ("Arial", 16))
        date_label.grid(row = 1, column = 0, sticky = "N")
        
        self.update(root)
    def update(self, root):
        '''updates time and date'''
        week = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        self.strtime.set(datetime.now().strftime('%I:%M %p'))
        self.strdate.set(week[datetime.today().weekday()] + datetime.now().strftime(", %B %d"))
        root.after(self.tick, self.update, root)

class currentWeatherFrame(tk.Frame):
    frameIndex = 0
    clockSpeed = 20 # ms of delay time before after animation method is called
    forecastRefresh = 600000 #refreshes forecast every 10 minutes
    darksky_key = "2183a9b730d7b1fe85eee07601b0ccd9"
    currentTemp = ""
    icon_name = "unknown"
    additionalInfo = ""
    summary = ""
    #stuff for weekly forecast:
    weeklyForecast = True
    weekdays = ['Mon','Tues','Wed','Thurs','Fri','Sat','Sun']
    weeklyDayLabels = []
    weeklyDayLabelsVars = []
    weeklyTempLabels = []
    weeklyTempLabelsVars = []
    weeklyIcons = []
    weeklyIconLabels = []
    weeklyFrameIndex = [0,0,0,0,0,0,0]
    
    
    def __init__(self, root, weeklyForecastBool, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.weeklyForecast = weeklyForecastBool
        global currentFrame
        currentFrame = ImageTk.PhotoImage(Image.open("/Users/Mihir/mirror/weather-icons/unknown/unknown.png"))
        self.framePaths = os.listdir("/Users/Mihir/mirror/weather-icons/")
        global icon_label
        icon_label = tk.Label(self, image = currentFrame, bg = "#000000")
        icon_label.image = currentFrame
        icon_label.grid(row = 0, column = 0, rowspan = 3)
        
        self.currentTemp = tk.StringVar()
        self.currentTemp.set("70")
        temp_label = tk.Label(self, textvariable=self.currentTemp,fg = "#ffffff", bg = "#000000", activebackground = "#000000", font=("Arial", 36))
        temp_label.grid(row = 0, column = 1)
                
        self.summary = tk.StringVar()
        summary_label = tk.Label(self, textvariable = self.summary, fg = "#ffffff", bg = "#000000", font = ("Arial", 16))
        summary_label.grid(row = 1, column = 1)
        
        self.additionalInfo = tk.StringVar()
        additional_info_label = tk.Label(self, textvariable = self.additionalInfo, fg = "#ffffff", bg = "#000000", font = ("Arial", 12))
        additional_info_label.grid(row = 2, column = 1)
        
        if self.weeklyForecast:
             weeklyFrame = tk.Frame(self, bg = "#000000")
             weeklyFrame.grid(row = 3, column = 1, pady = 30)
             #create 7 day labels and label vars, temp labels and temp vars
             for i in range(7):
                 self.weeklyDayLabelsVars.append(tk.StringVar())
                 self.weeklyDayLabels.append(tk.Label(weeklyFrame, textvariable = self.weeklyDayLabelsVars[i], fg = "#ffffff", bg = "#000000", font = ("Arial", 10)))
                 self.weeklyDayLabels[i].grid(row = 0 + i, column = 0)
                 
                 self.weeklyTempLabelsVars.append(tk.StringVar())
                 self.weeklyTempLabels.append(tk.Label(weeklyFrame, textvariable = self.weeklyTempLabelsVars[i], width = 12, fg = "#ffffff", bg = "#000000", font = ("Arial", 10)))
                 self.weeklyTempLabels[i].grid(row = 0 + i, column = 2)
                 
                 self.weeklyIcons.append("unknown")
                 self.weeklyIconLabels.append(tk.Label(weeklyFrame, image = currentFrame, bg = "#000000"))
                 self.weeklyIconLabels[i].image = currentFrame
                 self.weeklyIconLabels[i].grid(row = 0 + i, column = 1)
        self.update(root)
        self.updateIconFrame(root) # starts animations

    def updateIconFrame(self, root):
        ''' drives animation '''
        icon_path = "/Users/Mihir/mirror/weather-icons/" + self.icon_name + "/"
        #print self.icon_name
        frames = os.listdir(icon_path)
        currentFrame = ImageTk.PhotoImage(Image.open(icon_path + frames[self.frameIndex]).resize((100, 100), Image.ANTIALIAS).convert('RGB')) #update frame
        icon_label.config(image = currentFrame)
        icon_label.image = currentFrame
        if (self.frameIndex >= len(frames) - 1): #update index (which frame to show next)
            self.frameIndex = 0
        else:
            self.frameIndex = self.frameIndex + 1
            
        if (self.weeklyForecast):
            for i in range(7):
                icon_path = "/Users/Mihir/mirror/weather-icons/" + self.weeklyIcons[i] + "/"
                print icon_path
                frames = os.listdir(icon_path)
                pic = ImageTk.PhotoImage(Image.open(icon_path + frames[self.weeklyFrameIndex[i]]).resize((30, 30), Image.ANTIALIAS).convert('RGB'))
                #pic = ImageTk.PhotoImage(Image.open(icon_path + frames[self.weeklyFrameIndex[i]]))
                self.weeklyIconLabels[i].config(image = pic)
                self.weeklyIconLabels[i].image = pic
                if (self.weeklyFrameIndex[i] >= len(frames) - 1):
                    self.weeklyFrameIndex[i] = 0
                else:
                    self.weeklyFrameIndex[i] += 1
        root.after(self.clockSpeed, self.updateIconFrame, root)
    def getLocation(self):
        r = requests.get('http://freegeoip.net/json')
        j = json.loads(r.text)
        latitude = j['latitude']
        longitude = j['longitude']
        return (latitude, longitude)
    def getWeather(self, location):
        ''' updates current weather at your position
        @param location: a tuple containing latitude and longitude
        @return json object containing information '''
        exclude = "?exclude=minutely,hourly"
        if (not self.weeklyForecast):
            exclude += ",daily"
        query_url="https://api.darksky.net/forecast/%s/%.6f,%.6f" % (self.darksky_key, location[0], location[1]) + exclude
        r = requests.get(query_url)
        if r.status_code != 200:
            print "Error:", r.status_code
        return r.json()
    def update(self, root):
        ''' updates icons, and weather info '''
        j = self.getWeather(self.getLocation())
        temp = float(j['currently']['temperature'])
        symbol = u"\u00b0"
        line = "%.1f" %temp + symbol + 'F'
        self.currentTemp.set(line)
        new_icon = j['currently']['icon']
        if (new_icon != self.icon_name):
            self.frameIndex = 0 # reset frameIndex if icon is going to change
        self.icon_name = new_icon
        self.summary.set(j['currently']['summary'])
        precipChance = int(round(100 * float(j['currently']['precipProbability'])))
        if (precipChance != 0):
            self.additionalInfo.set(str(int(round(100 * float(j['currently']['precipProbability']))))
                + "% chance of " + j['currently']['precipType'] + ".")
        else:
            self.additionalInfo.set("No chance of precipitation.")
        #see if there are any alerts, and if so
        try: 
            self.additionalInfo.set(j['alerts']['severity'] + " : " + j['alerts']['title'])
        except KeyError:
            pass
        if (self.weeklyForecast): #if we have to get more info for weekly forecast...
            day = datetime.today().weekday() #returns int (Monday is 0)
            for i in range(7):
                if day == 6:
                    day = 0
                else:
                    day = day + 1
                self.weeklyDayLabelsVars[i].set(self.weekdays[day])
                
                mintemp = str(int(round(float(j['daily']['data'][i]['temperatureMin']))))
                maxtemp = str(int(round(float(j['daily']['data'][i]['temperatureMax']))))
                temp = mintemp + symbol + " - " + maxtemp + symbol
                self.weeklyTempLabelsVars[i].set(temp)
                new_icon = j['daily']['data'][i]['icon']
                if (new_icon != self.weeklyIcons[i]):
                    self.weeklyFrameIndex[i] = 0
                self.weeklyIcons[i] = new_icon
        root.after(self.forecastRefresh, self.update, root) #call next forecast refresh 

if __name__ == '__main__':
    root = tk.Tk()
    root.configure(bg = "#000000")
    # root.attributes("-fullscreen", True) #makes it fullscreens
    root.geometry("800x900")
    clock = clockFrame(root, bg = "#000000")
    clock.grid(row = 0, column = 0, sticky = 'N')
    weatherFrame = currentWeatherFrame(root, True, bg="#000000")
    weatherFrame.grid(row = 0, column = 1, sticky = 'NE')
    root.mainloop()