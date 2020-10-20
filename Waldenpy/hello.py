#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 23:42:11 2020

@author: yan
"""


"""
Walden Modular Equipment SAS
Input
2020
"""


import Walden as w

#Devices
# WPI = w.Get_WPI_12('COM7')

try:
    WPI = w.Get_WPI_12('/dev/ttyACM0')
        
except:
    WPI = w.Get_WPI_12('/dev/ttyACM1')

#Variables
SesionTime = 10

#Control
CounterTime = 0

#Program
TempTime = w.Get_Time()
while(CounterTime <= SesionTime):
    
    #Input Read - WPI_Out(WPI name, Input)
    Response = w.WPI_In(WPI,'1')
    
    #Print Time and input
    print(Response, round(CounterTime,2))
    
    #Time
    CounterTime = w.Timer(CounterTime,TempTime,.05)
    TempTime = w.Get_Time()
    
w.Stop_WPI(WPI)