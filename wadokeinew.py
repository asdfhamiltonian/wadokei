#clock app
# encoding: utf-8

#Concept for calculating sunrise and sunset from "Calulating sunrise and sunset in Python" by Michele Anders
#Reprogrammed from algorithm by NOAA, "NOAA_Solar_Calculations_year.xls"
#Accessed from http://www.esrl.noaa.gov/gmd/grad/solcalc/calcdetails.html


import math
import datetime
import time


from tkinter import *
from math import sin, cos, pi

from sun2 import Sun

#lat1 = 0.0
#lon1 = 0.0
#utcdisplacement = 0.0

print("Welcome to python wadokei!")

def mainmenu():
    while True:
        print("Would you like to (s)elect a city or (m)anually enter coordinates?")
        option = input("> ").lower()
        if option == "m":
            manualcoords()
            break
        if option == "s":
            select_coords()
            break

def manualcoords():
    global lat1
    global lon1
    global utcdisplacement
    while True:
        lat1 = float(input("Latitude (positive for north, negative for south)? "))
        lon1 = float(input("Longitude (positive for east, negative for west)? "))
        utcdisplacement = float(input("UTC displacement? "))
        if (-90.0 <= lat1) and (lat1 <= 90.0) and (-180.0 <= lon1) and (lon1 <= 180.0) and (utcdisplacement <= 12) and (-12 <= utcdisplacement):
            break
        else:
            continue

def select_coords():
    global lat1
    global lon1
    global utcdisplacement
    while True:
        cities = ["San Francisco", "Eugene", "Portland", "Salem", "Seattle", "St. Louis", "Chicago", "New York", "London", "Paris", "Moscow", "Kyoto", "Osaka", "Tokyo","Sydney", "Honolulu"]
        citydict = {"San Francisco":[37.774929,-122.419416,-7],
                    "Eugene":[44.052069, -123.086754, -7],
                    "Portland": [45.523062, -122.676482, -7],
                    "Salem": [44.942898, -123.035096, -7],
                    "Seattle" : [47.606209, -122.332071, -7],
                    "St. Louis":[38.647585, -90.300944, -5],
                    "Chicago" : [41.878114, -87.629798, -5],
                    "New York" : [40.712784, -74.005941, -4],
                    "London" : [51.507351, -0.127758, 0],
                    "Paris" : [48.856614, 2.352222, 1],
                    "Moscow" : [55.755826, 37.617300, 3],
                    "Kyoto" : [35.011636, 135.768029, 9],
                    "Osaka": [34.693738, 135.502165, 9],
                    "Tokyo": [35.689487, 139.691706, 9],
                    "Sydney": [-33.867487, 151.206990, 10], 
                    "Honolulu": [21.306944, -157.858333, -10]}
                    
        print("Select from the following cities:")
        for city in cities:
            print(city)
        print("Or type exit to exit")
        location = input("> ")
        if location in cities:
            lat1 = citydict[location][0]
            lon1 = citydict[location][1]
            utcdisplacement = citydict[location][2]
            break
        elif location == "exit":
            mainmenu()
        else:
            continue

def x_pos(r, rad):
    x_delta = r*cos(rad) #relative position from center, with total len r
    x = 300 + x_delta #have to convert this to position in the tkinter
    #Coordinate system. The top left corner is 0,0
    return x

def y_pos(r, rad):
    y_delta = r*sin(rad) #relative position from center, radius r
    y = 300 - y_delta
    return y

def Clock(a, time):
    
    zodiac = ["卯","辰","巳","午","未","申","酉","戌","亥","子","丑","寅"]
    num = ["六","五","四","九","八","七","六","五","四","九","八","七"]
    count = 0
    a.create_rectangle(0, 600, 600, 300, fill="grey",outline="grey")
    a.create_rectangle(0, 0, 600, 300, fill="white",outline="white")
    
    for char in zodiac:
        a.create_text(x_pos(260,pi-count*pi/6),y_pos(260,pi-count*pi/6), text= char,font=("Mincho",40), fill="black", state=NORMAL) #clock goes clockwise so have to subtract
        #each clock movement
        #The next line of code creates the divider lines between each clock symbol
        a.create_line(x_pos(180, pi-count*pi/6 + pi/12),y_pos(180, pi-count*pi/6+pi/12),x_pos(280, pi-count*pi/6 + pi/12), y_pos(280, pi-count*pi/6+pi/12), fill="black", width=1.0)
        #the following line of code creates the major score mark for each zodiac sign.
        a.create_line(x_pos(180, pi-count*pi/6),y_pos(180, pi-count*pi/6),x_pos(190, pi-count*pi/6), y_pos(190, pi-count*pi/6), fill="black", width=3.0)
        #the next two lines of code create the score marks for the clock.
        a.create_line(x_pos(180, pi-count*pi/6-pi/24),y_pos(180, pi-count*pi/6-pi/24),x_pos(190, pi-count*pi/6-pi/24), y_pos(190, pi-count*pi/6-pi/24), fill="black", width=1.0)
        a.create_line(x_pos(180, pi-count*pi/6+pi/24),y_pos(180, pi-count*pi/6+pi/24),x_pos(190, pi-count*pi/6+pi/24), y_pos(190, pi-count*pi/6+pi/24), fill="black", width=1.0)
        count += 1
    count = 0
    for char in num:
        a.create_text(x_pos(210, pi-count*pi/6),y_pos(210, pi-count*pi/6), text= char,font=("Mincho",40), fill="black", state=NORMAL)
        count += 1
    a.create_oval(300-180,300-180,300+180,300+180) #code for inner clock circle
    a.create_oval(300-280, 300-280,300+280, 300+280) #code for outer clock circle
    hand = a.create_line(300, 300,x_pos(180,pi-time*pi/6), y_pos(180, pi-time*pi/6), fill="black", width=7.0, arrow=LAST)
    a.create_oval(300-10, 300-10, 300+10, 300+10, fill="black") #clock hand circle

mainmenu()
sunrise_info = Sun(lat1, lon1, utcdisplacement)
time = sunrise_info.wadokei()[0]

def Clock1(a):
    a.delete(ALL) #deletes the old clock face so it can refresh
    time = sunrise_info.wadokei()[0] #recalculates the wadokei time
    #might be more efficient to calclulate this in a separate function that only has to calclulate
    #sunrise/sunset times once and goes from there... have to think about how to structure it.
    Clock(a, time) #creates a new instance of clock
    a.after(500, Clock1, a) #this sets the refresh rate in microseconds with the first number

master = Tk()
a = Canvas(master, width=600, height=600)
a.pack()

Clock1(a)

a.mainloop()
