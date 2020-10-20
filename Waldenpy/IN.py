#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 17:43:16 2020

@author: yan
"""


import Walden as w
import serial.tools.list_ports
import time

WPI = w.Get_WPI_12('/dev/ttyACM2')
    
#Variables
NumberIteration = 500
OUT_11 = 'UV'
OUT_12 = 'WX'

TreshLow = 90
TreshUp = 1000
def WPI_In(WPI,In):
    In = int(In)-1
    WPI.analog[In].enable_reporting()
    Pause_Time(.015)
    try:
        Temp = round(round(WPI.analog[In].read(),3)*100,1)
        if ((Temp >= TreshLow) & (Temp < TreshUp)):
            State = 0
        elif Temp == 100:
            State = 0  
        else:
            State = 1
    except:
        State = 0        
    return State


def Pause_Time(Seconds):
    time.sleep(Seconds)
    
#Program
for i in range(0, NumberIteration):
    # WPI_In(WPI, '1')
    # WPI_In(WPI, '2')
    
    # In3 = WPI_In(WPI,'1')
    if WPI_In(WPI,'1') == 1:
        print('1- si')
    else:
        print('1- no')
    
    # In2 = WPI_In(WPI,'2')
    if WPI_In(WPI,'2') == 1:
        print('2- si')
    else:
        print('2- no')
    

#%%-----------CLOSE WPI-----------------------------------------------------
w.Stop_WPI(WPI)