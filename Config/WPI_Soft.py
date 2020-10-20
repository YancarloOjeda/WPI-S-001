#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 09:10:24 2020

@author: yan
"""
#%%-----------LIBRARIES--------------------------------------------------------
from tkinter import Button, Frame, INSERT, LEFT, RIGHT, Label
from tkinter import  Scrollbar, Text, Tk, TOP, X, Y, filedialog
from PIL import Image, ImageTk
import PIL.Image
from tkinter import *
import cv2
from screeninfo import get_monitors
import tkinter
import Walden as w
import os 
import serial.tools.list_ports
import time
import pyfirmata
from pyfirmata import Arduino, util


#%%-----------COLORS-----------------------------------------------------------
def Fun_Rgb(RGB):
    return "#%02x%02x%02x" % RGB  

C_White = (255,255,255)
C_Black = (0,0,0)
C_Red = (255,0,0)
C_Green = (0,255,0)
C_Blue = (0,0,255)
C_Pal1 = (0,0,0)
C_Pal2 = (70,75,80)
C_Pal3 = (30,40,40)
C_Pal4 = (200,200,200)
C_Pal5 = (255,255,255)
C_Pal6 = (245,245,245)
C_Pal7 = (70,90,90)
C_Pal8 = (235,235,235)
Font_CV = cv2.FONT_HERSHEY_SIMPLEX
Font_1 = 'Sans'


#%%-----------DIRECTORIES------------------------------------------------------
Dir_Config = '/home/yan/WPI-H-001/Config/'
Dir_Images = '/home/yan/WPI-H-001/Image/'
Dir_Projects = '/home/yan/WPI-H-001/Waldenpy/'


#%%-----------GLOBAL VARIABLES------------------------------------------------
global active_WPI_1, active_WPI_2, active_WPI_3, active_WPI_4, active_WPI_5, active_WPI_5
active_WPI_1 = 0
active_WPI_2 = 0
active_WPI_3 = 0
active_WPI_4 = 0
active_WPI_5 = 0
active_WPI_6 = 0


#%%-----------HEIGHT AND WEIGHT OF MONITOR------------------------------------
aux_monitor = 0

try:
    for monitor in get_monitors():
        aux_monitor += 1
        if aux_monitor == 1:
            monitor_size = monitor
            aux_string_monitor = str(monitor_size)
            aux_cortar = aux_string_monitor.split('Monitor(')
            aux_cortar = aux_cortar[1].split(')')
            parameters_monitor = aux_cortar[0].split('width=')
            parameters_monitor = parameters_monitor[1].split(', height=')
            width_monitor = int(parameters_monitor[0])
            parameters_monitor = parameters_monitor[1].split(', width_mm=')
            height_monitor = int(parameters_monitor[0])
    
        if aux_monitor == 2:
            monitor_size = monitor
            aux_string_monitor = str(monitor_size)
            aux_cortar = aux_string_monitor.split('Monitor(')
            aux_cortar = aux_cortar[1].split(')')
            parameters_monitor = aux_cortar[0].split('width=')
            parameters_monitor = parameters_monitor[1].split(', height=')
            width_monitor = int(parameters_monitor[0])
            parameters_monitor = parameters_monitor[1].split(', width_mm=')
            height_monitor = int(parameters_monitor[0])
     
    aux_size = .65
    
except:
    width_monitor = 1280
    height_monitor = 800
    aux_size = .75
    
    
aux_width_monitor = width_monitor/15 
aux_height_monitor = height_monitor/15   
Var_Tamaño_Lbl_X = int(((height_monitor/3)*2)-(aux_width_monitor*1.5))
Var_Tamaño_Lbl_Y = int(((height_monitor/3)*2)-(aux_width_monitor*1.5)) 


#%%-----------FUN SIZE---------------------------------------------------------
def Fun_Size(img, size):
    img = PIL.Image.open(img)
    size_1 = img.size
    width = int(size_1[0]*size)
    height = int(size_1[1]*size)
    img = img.resize((width, height))
    img = ImageTk.PhotoImage(img)
    return img


class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 20
        y = y + cy + self.widget.winfo_rooty() +20
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

#%%-----------PRINCIPAL WINDOW-------------------------------------------------
root = Tk()
root.title('WPI-S-001')
root.geometry(str(width_monitor)+'x'+str(height_monitor-100)+'+0+0') 
root.config(bg = Fun_Rgb(C_Pal3))
root.isStopped = False

def Detect_WPI():
    global WPI_1, WPI_2, WPI_3, WPI_4, WPI_5, WPI_6, active_WPI_1
    global active_WPI_2, active_WPI_3, active_WPI_4, active_WPI_5, active_WPI_6 
    aux_WPI_1 = 0
    aux_WPI_2 = 0
    aux_WPI_3 = 0
    aux_WPI_4 = 0
    aux_WPI_5 = 0
    aux_WPI_6 = 0
    
    
    
    ##Detecting WPI-1
    for i in range(20):
        try:
            # WPI_1 = Arduino('/dev/ttyACM'+str(i))
            WPI_1 = w.Get_WPI_12('/dev/ttyACM'+str(i))
            print('1', WPI_1)
            active_WPI_1 = 1
        except:
            text.insert(INSERT, '')
        if active_WPI_1 == 1:
            aux_WPI_1 = i
            break
        
    ##Detecting WPI-2
    for i in range(20):
        if i != aux_WPI_1:
            try:
                WPI_2 = w.Get_WPI_12('/dev/ttyACM'+str(i))
                print('2', WPI_1)
                active_WPI_2 = 1
            except:
                text.insert(INSERT, '')
            if active_WPI_2 == 1:
                aux_WPI_2 = i
                # print('aux_WPI_2', i)
                break
    
    ##Detecting WPI-3        
    for i in range(20):
        if i != aux_WPI_1 and i != aux_WPI_2:
            try:
                WPI_3 = w.Get_WPI_12('/dev/ttyACM'+str(i))
                print('3', WPI_3)
                active_WPI_3 = 1
            except:
                text.insert(INSERT, '')
            if active_WPI_3 == 1:
                aux_WPI_3 = i
                break
    
    ##Detecting WPI-4        
    for i in range(20):
        if i != aux_WPI_1 and i != aux_WPI_2 and i != aux_WPI_3:
            try:
                WPI_4 = w.Get_WPI_12('/dev/ttyACM'+str(i))
                print('4', WPI_4)
                active_WPI_4 = 1
            except:
                text.insert(INSERT, '')
            if active_WPI_4 == 1:
                aux_WPI_4 = i
                break
    
    ##Detecting WPI-5        
    for i in range(20):
        if i != aux_WPI_1 and i != aux_WPI_2 and i != aux_WPI_3 and i != aux_WPI_4:
            try:
                WPI_5 = w.Get_WPI_12('/dev/ttyACM'+str(i))
                print('5', WPI_5)
                active_WPI_5 = 1
            except:
                text.insert(INSERT, '')
            if active_WPI_5 == 1:
                aux_WPI_5 = i
                break
     
    ##Detecting WPI-6
    for i in range(20):
        if i != aux_WPI_1 and i != aux_WPI_2 and i != aux_WPI_3 and i != aux_WPI_4 and i != aux_WPI_5:
            try:
                WPI_6 = w.Get_WPI_12('/dev/ttyACM'+str(i))
                print('6', WPI_6)
                active_WPI_6 = 1
            except:
                text.insert(INSERT, '')
            if active_WPI_6 == 1:
                aux_WPI_6 = i
                break
            
    
        
    if active_WPI_1 == 0: 
        text.insert(INSERT, 'WPI not found \n')
    else:
        text.insert(INSERT, str(WPI_1) +'\n')
    
    if active_WPI_2 == 0: 
        text.insert(INSERT, '')
    else:
        text.insert(INSERT, str(WPI_2) +'\n')
        
    if active_WPI_3 == 0: 
        text.insert(INSERT, '')
    else:
        text.insert(INSERT, str(WPI_3) +'\n')
    
    if active_WPI_4 == 0: 
        text.insert(INSERT, '')
    else:
        text.insert(INSERT, str(WPI_4) +'\n')
        
    if active_WPI_5 == 0: 
        text.insert(INSERT, '')
    else:
        text.insert(INSERT, str(WPI_5) +'\n')
        
    if active_WPI_6 == 0: 
        text.insert(INSERT, '')
    else:
        text.insert(INSERT, str(WPI_6) +'\n')
            
    
    
def close_WPI_Connection():
    global active_WPI_1, active_WPI_2, active_WPI_3, active_WPI_4, active_WPI_5, active_WPI_6
    if active_WPI_1 == 1:
        w.Stop_WPI(WPI_1)
        active_WPI_1 = 0 
        text.insert(INSERT, 'WPI-1 stopped correctly \n')
    else:
        text.insert(INSERT, 'Error. Not WPI-1 found \n')
    
    if active_WPI_2 == 1:
        w.Stop_WPI(WPI_2)
        active_WPI_2 = 0 
        text.insert(INSERT, 'WPI-2 stopped correctly \n')
    else:
        text.insert(INSERT, '')
        
    if active_WPI_3 == 1:
        w.Stop_WPI(WPI_3)
        active_WPI_3 = 0 
        text.insert(INSERT, 'WPI-3 stopped correctly \n')
    else:
        text.insert(INSERT, '')
        
    if active_WPI_4 == 1:
        w.Stop_WPI(WPI_4)
        active_WPI_4 = 0 
        text.insert(INSERT, 'WPI-4 stopped correctly \n')
    else:
        text.insert(INSERT, '')
        
    if active_WPI_5 == 1:
        w.Stop_WPI(WPI_5)
        active_WPI_5 = 0 
        text.insert(INSERT, 'WPI-5 stopped correctly \n')
    else:
        text.insert(INSERT, '')
        
    if active_WPI_6 == 1:
        w.Stop_WPI(WPI_6)
        active_WPI_6 = 0 
        text.insert(INSERT, 'WPI-6 stopped correctly \n')
    else:
        text.insert(INSERT, '')
        
    


def read_File():
    path_file = filedialog.askopenfilename(initialdir=Dir_Projects,
                                                     title="Select file",
                                                     filetypes=(("py files","*.py"),
                                                     ("all files","*.*")))
    
    os.system(path_file)


def show_text(state):
    print(state)
    text.insert(INSERT, state)


def stop_check_Input():
    global stop
    stop = True
    
def stop_check_Input_2():
    global stop_2
    stop_2 = True
    
def stop_check_Input_3():
    global stop_3
    stop_3 = True
    

    

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

def check_Input_1():
    global active_WPI_1, stop, WPI_1
    stop = False
    if active_WPI_1 == 0:
        text.insert(INSERT, 'Error. Not WPI found \n')
    else:
        text.insert(INSERT, 'Please press Stop Check button when checking has finished \n')
        
        while True:
            if WPI_In(WPI_1,'1') == 1:
                IN_1_WPI_1.set(True)
                root.update()
            else:
                IN_1_WPI_1.set(False)
                root.update()
            
            if WPI_In(WPI_1,'2') == 1:
                IN_2_WPI_1.set(True)
                root.update()
            else:
                IN_2_WPI_1.set(False)
                root.update()
            
            if WPI_In(WPI_1,'3') == 1:
                IN_3_WPI_1.set(True)
                root.update()
            else:
                IN_3_WPI_1.set(False)
                root.update()
                
            if WPI_In(WPI_1,'4') == 1:
                IN_4_WPI_1.set(True)
                root.update()
            else:
                IN_4_WPI_1.set(False)
                root.update()
            
            if WPI_In(WPI_1,'5') == 1:
                IN_5_WPI_1.set(True)
                root.update()
            else:
                IN_5_WPI_1.set(False)
                root.update()
                
            if WPI_In(WPI_1,'6') == 1:
                IN_6_WPI_1.set(True)
                root.update()
            else:
                IN_6_WPI_1.set(False)
                root.update()
            
            if WPI_In(WPI_1,'7') == 1:
                IN_7_WPI_1.set(True)
                root.update()
            else:
                IN_7_WPI_1.set(False)
                root.update()
            
            if WPI_In(WPI_1,'8') == 1:
                IN_8_WPI_1.set(True)
                root.update()
            else:
                IN_8_WPI_1.set(False)
                root.update()
            
            if WPI_In(WPI_1,'9') == 1:
                IN_9_WPI_1.set(True)
                root.update()
            else:
                IN_9_WPI_1.set(False)
                root.update()
            
            if WPI_In(WPI_1,'10') == 1:
                IN_10_WPI_1.set(True)
                root.update()
            else:
                IN_10_WPI_1.set(False)
                root.update()
            
            if WPI_In(WPI_1,'11') == 1:
                IN_11_WPI_1.set(True)
                root.update()
            else:
                IN_11_WPI_1.set(False)
                root.update()
            
            if WPI_In(WPI_1,'12') == 1:
                IN_12_WPI_1.set(True)
                root.update()
            else:
                IN_12_WPI_1.set(False)
                root.update()
            
            if stop == True:
                text.insert(INSERT, 'Checking has finished \n')
                break



def check_Input_2():
    global active_WPI_2, stop, WPI_2
    stop = False
    if active_WPI_2 == 0:
        text.insert(INSERT, 'Error. Not WPI found \n')
    else:
        text.insert(INSERT, 'Please press Stop Check button when checking has finished \n')
        
        while True:
            if WPI_In(WPI_2,'1') == 1:
                IN_1_WPI_2.set(True)
                root.update()
            else:
                IN_1_WPI_2.set(False)
                root.update()
            
            if WPI_In(WPI_2,'2') == 1:
                IN_2_WPI_2.set(True)
                root.update()
            else:
                IN_2_WPI_2.set(False)
                root.update()
            
            if WPI_In(WPI_2,'3') == 1:
                IN_3_WPI_2.set(True)
                root.update()
            else:
                IN_3_WPI_2.set(False)
                root.update()
                
            if WPI_In(WPI_2,'4') == 1:
                IN_4_WPI_2.set(True)
                root.update()
            else:
                IN_4_WPI_2.set(False)
                root.update()
            
            if WPI_In(WPI_2,'5') == 1:
                IN_5_WPI_2.set(True)
                root.update()
            else:
                IN_5_WPI_2.set(False)
                root.update()
                
            if WPI_In(WPI_2,'6') == 1:
                IN_6_WPI_2.set(True)
                root.update()
            else:
                IN_6_WPI_2.set(False)
                root.update()
            
            if WPI_In(WPI_2,'7') == 1:
                IN_7_WPI_2.set(True)
                root.update()
            else:
                IN_7_WPI_2.set(False)
                root.update()
            
            if WPI_In(WPI_2,'8') == 1:
                IN_8_WPI_2.set(True)
                root.update()
            else:
                IN_8_WPI_2.set(False)
                root.update()
            
            if WPI_In(WPI_2,'9') == 1:
                IN_9_WPI_2.set(True)
                root.update()
            else:
                IN_9_WPI_2.set(False)
                root.update()
            
            if WPI_In(WPI_2,'10') == 1:
                IN_10_WPI_2.set(True)
                root.update()
            else:
                IN_10_WPI_2.set(False)
                root.update()
            
            if WPI_In(WPI_2,'11') == 1:
                IN_11_WPI_2.set(True)
                root.update()
            else:
                IN_11_WPI_2.set(False)
                root.update()
            
            if WPI_In(WPI_2,'12') == 1:
                IN_12_WPI_2.set(True)
                root.update()
            else:
                IN_12_WPI_2.set(False)
                root.update()
            
            if stop == True:
                text.insert(INSERT, 'Checking has finished \n')
                break
                


def check_Input_3():
    global active_WPI_3, stop, WPI_3
    stop = False
    if active_WPI_3 == 0:
        text.insert(INSERT, 'Error. Not WPI found \n')
    else:
        text.insert(INSERT, 'Please press Stop Check button when checking has finished \n')
        
        while True:
            if WPI_In(WPI_3,'1') == 1:
                IN_1_WPI_3.set(True)
                root.update()
            else:
                IN_1_WPI_3.set(False)
                root.update()
            
            if WPI_In(WPI_3,'2') == 1:
                IN_2_WPI_3.set(True)
                root.update()
            else:
                IN_2_WPI_3.set(False)
                root.update()
            
            if WPI_In(WPI_3,'3') == 1:
                IN_3_WPI_3.set(True)
                root.update()
            else:
                IN_3_WPI_3.set(False)
                root.update()
                
            if WPI_In(WPI_3,'4') == 1:
                IN_4_WPI_3.set(True)
                root.update()
            else:
                IN_4_WPI_3.set(False)
                root.update()
            
            if WPI_In(WPI_3,'5') == 1:
                IN_5_WPI_3.set(True)
                root.update()
            else:
                IN_5_WPI_3.set(False)
                root.update()
                
            if WPI_In(WPI_3,'6') == 1:
                IN_6_WPI_3.set(True)
                root.update()
            else:
                IN_6_WPI_3.set(False)
                root.update()
            
            if WPI_In(WPI_3,'7') == 1:
                IN_7_WPI_3.set(True)
                root.update()
            else:
                IN_7_WPI_3.set(False)
                root.update()
            
            if WPI_In(WPI_3,'8') == 1:
                IN_8_WPI_3.set(True)
                root.update()
            else:
                IN_8_WPI_3.set(False)
                root.update()
            
            if WPI_In(WPI_3,'9') == 1:
                IN_9_WPI_3.set(True)
                root.update()
            else:
                IN_9_WPI_3.set(False)
                root.update()
            
            if WPI_In(WPI_3,'10') == 1:
                IN_10_WPI_3.set(True)
                root.update()
            else:
                IN_10_WPI_3.set(False)
                root.update()
            
            if WPI_In(WPI_3,'11') == 1:
                IN_11_WPI_3.set(True)
                root.update()
            else:
                IN_11_WPI_3.set(False)
                root.update()
            
            if WPI_In(WPI_3,'12') == 1:
                IN_12_WPI_3.set(True)
                root.update()
            else:
                IN_12_WPI_3.set(False)
                root.update()
            
            if stop == True:
                text.insert(INSERT, 'Checking has finished \n')
                break
                    
                

def check_Input_4():
    global active_WPI_4, stop, WPI_4
    stop = False
    if active_WPI_4 == 0:
        text.insert(INSERT, 'Error. Not WPI found \n')
    else:
        text.insert(INSERT, 'Please press Stop Check button when checking has finished \n')
        
        while True:
            if WPI_In(WPI_4,'1') == 1:
                IN_1_WPI_4.set(True)
                root.update()
            else:
                IN_1_WPI_4.set(False)
                root.update()
        
            if WPI_In(WPI_4,'2') == 1:
                IN_2_WPI_4.set(True)
                root.update()
            else:
                IN_2_WPI_4.set(False)
                root.update()
            
            if WPI_In(WPI_4,'3') == 1:
                IN_3_WPI_4.set(True)
                root.update()
            else:
                IN_3_WPI_4.set(False)
                root.update()
                
            if WPI_In(WPI_4,'4') == 1:
                IN_4_WPI_4.set(True)
                root.update()
            else:
                IN_4_WPI_4.set(False)
                root.update()
            
            if WPI_In(WPI_4,'5') == 1:
                IN_5_WPI_4.set(True)
                root.update()
            else:
                IN_5_WPI_4.set(False)
                root.update()
                
            if WPI_In(WPI_4,'6') == 1:
                IN_6_WPI_4.set(True)
                root.update()
            else:
                IN_6_WPI_4.set(False)
                root.update()
            
            if WPI_In(WPI_4,'7') == 1:
                IN_7_WPI_4.set(True)
                root.update()
            else:
                IN_7_WPI_4.set(False)
                root.update()
            
            if WPI_In(WPI_4,'8') == 1:
                IN_8_WPI_4.set(True)
                root.update()
            else:
                IN_8_WPI_4.set(False)
                root.update()
            
            if WPI_In(WPI_4,'9') == 1:
                IN_9_WPI_4.set(True)
                root.update()
            else:
                IN_9_WPI_4.set(False)
                root.update()
            
            if WPI_In(WPI_4,'10') == 1:
                IN_10_WPI_4.set(True)
                root.update()
            else:
                IN_10_WPI_4.set(False)
                root.update()
            
            if WPI_In(WPI_4,'11') == 1:
                IN_11_WPI_4.set(True)
                root.update()
            else:
                IN_11_WPI_4.set(False)
                root.update()
            
            if WPI_In(WPI_4,'12') == 1:
                IN_12_WPI_4.set(True)
                root.update()
            else:
                IN_12_WPI_4.set(False)
                root.update()
            
            if stop == True:
                text.insert(INSERT, 'Checking has finished \n')
                break


def check_Input_5():
    global active_WPI_5, stop, WPI_5
    stop = False
    if active_WPI_5 == 0:
        text.insert(INSERT, 'Error. Not WPI found \n')
    else:
        text.insert(INSERT, 'Please press Stop Check button when checking has finished \n')
        
        while True:
            if WPI_In(WPI_5,'1') == 1:
                IN_1_WPI_5.set(True)
                root.update()
            else:
                IN_1_WPI_5.set(False)
                root.update()
            
            if WPI_In(WPI_5,'2') == 1:
                IN_2_WPI_5.set(True)
                root.update()
            else:
                IN_2_WPI_5.set(False)
                root.update()
            
            if WPI_In(WPI_5,'3') == 1:
                IN_3_WPI_5.set(True)
                root.update()
            else:
                IN_3_WPI_5.set(False)
                root.update()
                
            if WPI_In(WPI_5,'4') == 1:
                IN_4_WPI_5.set(True)
                root.update()
            else:
                IN_4_WPI_5.set(False)
                root.update()
            
            if WPI_In(WPI_5,'5') == 1:
                IN_5_WPI_5.set(True)
                root.update()
            else:
                IN_5_WPI_5.set(False)
                root.update()
                
            if WPI_In(WPI_5,'6') == 1:
                IN_6_WPI_5.set(True)
                root.update()
            else:
                IN_6_WPI_5.set(False)
                root.update()
            
            if WPI_In(WPI_5,'7') == 1:
                IN_7_WPI_5.set(True)
                root.update()
            else:
                IN_7_WPI_5.set(False)
                root.update()
            
            if WPI_In(WPI_5,'8') == 1:
                IN_8_WPI_5.set(True)
                root.update()
            else:
                IN_8_WPI_5.set(False)
                root.update()
            
            if WPI_In(WPI_5,'9') == 1:
                IN_9_WPI_5.set(True)
                root.update()
            else:
                IN_9_WPI_5.set(False)
                root.update()
            
            if WPI_In(WPI_5,'10') == 1:
                IN_10_WPI_5.set(True)
                root.update()
            else:
                IN_10_WPI_5.set(False)
                root.update()
            
            if WPI_In(WPI_5,'11') == 1:
                IN_11_WPI_5.set(True)
                root.update()
            else:
                IN_11_WPI_5.set(False)
                root.update()
            
            if WPI_In(WPI_5,'12') == 1:
                IN_12_WPI_5.set(True)
                root.update()
            else:
                IN_12_WPI_5.set(False)
                root.update()
            
            if stop == True:
                text.insert(INSERT, 'Checking has finished \n')
                break


def check_Input_6():
    global active_WPI_6, stop, WPI_6
    stop = False
    if active_WPI_6 == 0:
        text.insert(INSERT, 'Error. Not WPI found \n')
    else:
        text.insert(INSERT, 'Please press Stop Check button when checking has finished \n')
        
        while True: 
            if WPI_In(WPI_6,'1') == 1:
                IN_1_WPI_6.set(True)
                root.update()
            else:
                IN_1_WPI_6.set(False)
                root.update()
            
            if WPI_In(WPI_6,'2') == 1:
                IN_2_WPI_6.set(True)
                root.update()
            else:
                IN_2_WPI_6.set(False)
                root.update()
            
            if WPI_In(WPI_6,'3') == 1:
                IN_3_WPI_6.set(True)
                root.update()
            else:
                IN_3_WPI_6.set(False)
                root.update()
                
            if WPI_In(WPI_6,'4') == 1:
                IN_4_WPI_6.set(True)
                root.update()
            else:
                IN_4_WPI_6.set(False)
                root.update()
            
            if WPI_In(WPI_6,'5') == 1:
                IN_5_WPI_6.set(True)
                root.update()
            else:
                IN_5_WPI_6.set(False)
                root.update()
                
            if WPI_In(WPI_6,'6') == 1:
                IN_6_WPI_6.set(True)
                root.update()
            else:
                IN_6_WPI_6.set(False)
                root.update()
            
            if WPI_In(WPI_6,'7') == 1:
                IN_7_WPI_6.set(True)
                root.update()
            else:
                IN_7_WPI_6.set(False)
                root.update()
            
            if WPI_In(WPI_6,'8') == 1:
                IN_8_WPI_6.set(True)
                root.update()
            else:
                IN_8_WPI_6.set(False)
                root.update()
            
            if WPI_In(WPI_6,'9') == 1:
                IN_9_WPI_6.set(True)
                root.update()
            else:
                IN_9_WPI_6.set(False)
                root.update()
            
            if WPI_In(WPI_6,'10') == 1:
                IN_10_WPI_6.set(True)
                root.update()
            else:
                IN_10_WPI_6.set(False)
                root.update()
            
            if WPI_In(WPI_6,'11') == 1:
                IN_11_WPI_6.set(True)
                root.update()
            else:
                IN_11_WPI_6.set(False)
                root.update()
            
            if WPI_In(WPI_6,'12') == 1:
                IN_12_WPI_6.set(True)
                root.update()
            else:
                IN_12_WPI_6.set(False)
                root.update()
            
            if stop == True:
                text.insert(INSERT, 'Checking has finished \n')
                break
            
    
def Fun_Lincense():
    messagebox.showinfo('License A0001.WPI.0.00.1','A0001.WPI.0.00.1')

def Fun_WTS():
    messagebox.showinfo('Walden Programming Interface',"Version: 0.00.1")

def exitApp():
    root.destroy()
    
    
#%%-----------TOOLBAR AND MENU-------------------------------------------------
toolbar = Frame(root)

img1 = PIL.Image.open(Dir_Images+'LoadIcon.png')
useImg1 = ImageTk.PhotoImage(img1)
img2 = PIL.Image.open(Dir_Images+'NewIcon.png')
useImg2 = ImageTk.PhotoImage(img2)
img3 = PIL.Image.open(Dir_Images+'SaveIcon.png')
useImg3 = ImageTk.PhotoImage(img3)
img4 = PIL.Image.open(Dir_Images+'QuitButton.png')
useImg4 = ImageTk.PhotoImage(img4)
img5 = PIL.Image.open(Dir_Images+'checkInput.jpg')
useImg5 = ImageTk.PhotoImage(img5)
img6 = PIL.Image.open(Dir_Images+'stopCheckInput.jpg')
useImg6 = ImageTk.PhotoImage(img6)


activeWPIConnection = Button(toolbar, image=useImg1, text="new", width=20, 
           command=Detect_WPI)
activeWPIConnection.pack(side=LEFT, padx=2, pady=2)
CreateToolTip(activeWPIConnection, text = 'Create WPI connection')

openFile = Button(toolbar, image=useImg2, text="open", width=20, command=read_File)
openFile.pack(side=LEFT, padx=2, pady=2)
CreateToolTip(openFile, text = 'Open file')

saveButton = Button(toolbar, image=useImg3, text="save", width=20, command=Detect_WPI)
saveButton.pack(side=LEFT, padx=2, pady=2)
CreateToolTip(saveButton, text = 'In construction')

closeButton = Button(toolbar, image=useImg4, text="close", width=20, 
                     command=close_WPI_Connection)
closeButton.pack(side=LEFT, padx=2, pady=2)
CreateToolTip(closeButton, text = 'Close WPI connection')

# checkInputButton = Button(toolbar, image=useImg5, text="Check Inputs WPI-1", width=20, 
#                      command=check_Input_1)
# checkInputButton.pack(side=LEFT, padx=2, pady=2)
# CreateToolTip(checkInputButton, text = 'Start Input checking')

checkStopInputButton = Button(toolbar, image=useImg6, text="Stop check Inputs WPI-1", width=20, 
                     command=stop_check_Input)
checkStopInputButton.pack(side=LEFT, padx=2, pady=2)
CreateToolTip(checkStopInputButton, text = 'Stop Input checking')

toolbar.pack(side=TOP, fill=X)



ventanaInicio_Menu = tkinter.Menu(root)
root.config(menu=ventanaInicio_Menu)

ventanaInicio_Menu_Opc1 = tkinter.Menu(ventanaInicio_Menu, bg=Fun_Rgb(C_Pal5), fg=Fun_Rgb(C_Black),
                             activebackground=Fun_Rgb(C_Pal4), activeforeground=Fun_Rgb(C_Black),
                             tearoff=0)                         
ventanaInicio_Menu.add_cascade(label="File", menu=ventanaInicio_Menu_Opc1)
ventanaInicio_Menu_Opc1.add_command(label='Open file', command=read_File) 
ventanaInicio_Menu_Opc1.add_command(label='Detect WPI port', command=Detect_WPI) 
ventanaInicio_Menu_Opc1.add_command(label='Stop WPI connection', command=close_WPI_Connection) 
ventanaInicio_Menu_Opc1.add_command(label='Check Inputs WPI-1', command=check_Input_1)
ventanaInicio_Menu_Opc1.add_command(label='Check Inputs WPI-2', command=check_Input_2)
ventanaInicio_Menu_Opc1.add_command(label='Check Inputs WPI-3', command=check_Input_3)
ventanaInicio_Menu_Opc1.add_command(label='Check Inputs WPI-4', command=check_Input_4)
ventanaInicio_Menu_Opc1.add_command(label='Check Inputs WPI-5', command=check_Input_5)
ventanaInicio_Menu_Opc1.add_command(label='Check Inputs WPI-6', command=check_Input_6)
ventanaInicio_Menu_Opc1.add_command(label='Stop check Inputs', command=stop_check_Input)
ventanaInicio_Menu_Opc1.add_command(label='License', command=Fun_Lincense)  
ventanaInicio_Menu_Opc1.add_command(label='Information', command=Fun_WTS) 
ventanaInicio_Menu_Opc1.add_command(label='Exit', command=exitApp)


#%%------------BUTTONS CHECK INPUTS--------------------------------------------
Btn_check_Input_1 = tkinter.Button(root,  bd=0, fg = Fun_Rgb(C_Pal5),
                                  bg = Fun_Rgb(C_Pal2), activebackground=Fun_Rgb(C_Pal4),
                                  highlightbackground=Fun_Rgb(C_Pal5),
                                  text = 'Proof In', command = check_Input_1)
Btn_check_Input_1.config(font = (Font_1,15))
Btn_check_Input_1.place(x=aux_width_monitor*4.5, y=aux_height_monitor*1.7)

Btn_check_Input_2 = tkinter.Button(root,  bd=0, fg = Fun_Rgb(C_Pal5),
                                  bg = Fun_Rgb(C_Pal2), activebackground=Fun_Rgb(C_Pal4),
                                  highlightbackground=Fun_Rgb(C_Pal5),
                                  text = 'Proof In', command = check_Input_2)
Btn_check_Input_2.config(font = (Font_1,15))
Btn_check_Input_2.place(x=aux_width_monitor*4.5, y=aux_height_monitor*3.7)

Btn_check_Input_3 = tkinter.Button(root,  bd=0, fg = Fun_Rgb(C_Pal5),
                                  bg = Fun_Rgb(C_Pal2), activebackground=Fun_Rgb(C_Pal4),
                                  highlightbackground=Fun_Rgb(C_Pal5),
                                  text = 'Proof In', command = check_Input_3)
Btn_check_Input_3.config(font = (Font_1,15))
Btn_check_Input_3.place(x=aux_width_monitor*4.5, y=aux_height_monitor*5.7)

Btn_check_Input_4 = tkinter.Button(root,  bd=0, fg = Fun_Rgb(C_Pal5),
                                  bg = Fun_Rgb(C_Pal2), activebackground=Fun_Rgb(C_Pal4),
                                  highlightbackground=Fun_Rgb(C_Pal5),
                                  text = 'Proof In', command = check_Input_4)
Btn_check_Input_4.config(font = (Font_1,15))
Btn_check_Input_4.place(x=aux_width_monitor*4.5, y=aux_height_monitor*7.7)

Btn_check_Input_5 = tkinter.Button(root,  bd=0, fg = Fun_Rgb(C_Pal5),
                                  bg = Fun_Rgb(C_Pal2), activebackground=Fun_Rgb(C_Pal4),
                                  highlightbackground=Fun_Rgb(C_Pal5),
                                  text = 'Proof In', command = check_Input_5)
Btn_check_Input_5.config(font = (Font_1,15))
Btn_check_Input_5.place(x=aux_width_monitor*4.5, y=aux_height_monitor*9.7)

Btn_check_Input_6 = tkinter.Button(root,  bd=0, fg = Fun_Rgb(C_Pal5),
                                  bg = Fun_Rgb(C_Pal2), activebackground=Fun_Rgb(C_Pal4),
                                  highlightbackground=Fun_Rgb(C_Pal5),
                                  text = 'Proof In', command = check_Input_6)
Btn_check_Input_6.config(font = (Font_1,15))
Btn_check_Input_6.place(x=aux_width_monitor*4.5, y=aux_height_monitor*11.7)


#%%------------IMAGE WALDEN----------------------------------------------------------
Img_ventanaInicio_1 = Fun_Size(Dir_Images + '/' +'interfaz-01.png',.4*aux_size)
Lbl_ventanaInicio_1 = Label(root, bg = Fun_Rgb(C_Pal3), 
                                    image = Img_ventanaInicio_1)
Lbl_ventanaInicio_1.place(x=aux_width_monitor*13,y=aux_height_monitor*10.5)


#%%------------RADIOBUTTON-----------------------------------------------------
def OUT_WPI_1():
    if active_WPI_1 == 0:
        text.insert(INSERT, 'Error. Select a WPI-1 is not available\n')
    else:    
        if OUT_1_WPI_1.get() == 1:
            w.WPI_Out(WPI_1,'AB','On')
        else:
            w.WPI_Out(WPI_1,'AB','Off')
        
        if OUT_2_WPI_1.get() == 1:
            w.WPI_Out(WPI_1,'CD','On')
        else:
            w.WPI_Out(WPI_1,'CD','Off')
        
        if OUT_3_WPI_1.get() == 1:
            w.WPI_Out(WPI_1,'EF','On')
        else:
            w.WPI_Out(WPI_1,'EF','Off')
            
        if OUT_4_WPI_1.get() == 1:
            w.WPI_Out(WPI_1,'GH','On')
        else:
            w.WPI_Out(WPI_1,'GH','Off')
            
        if OUT_5_WPI_1.get() == 1:
            w.WPI_Out(WPI_1,'IJ','On')
        else:
            w.WPI_Out(WPI_1,'IJ','Off')
            
        if OUT_6_WPI_1.get() == 1:
            w.WPI_Out(WPI_1,'KL','On')
        else:
            w.WPI_Out(WPI_1,'KL','Off')
            
        if OUT_7_WPI_1.get() == 1:
            w.WPI_Out(WPI_1,'MN','On')
        else:
            w.WPI_Out(WPI_1,'MN','Off') 
            
        if OUT_8_WPI_1.get() == 1:
            w.WPI_Out(WPI_1,'OP','On')
        else:
            w.WPI_Out(WPI_1,'OP','Off')
            
        if OUT_9_WPI_1.get() == 1:
            w.WPI_Out(WPI_1,'QR','On')
        else:
            w.WPI_Out(WPI_1,'QR','Off')
            
        if OUT_10_WPI_1.get() == 1:
            w.WPI_Out(WPI_1,'ST','On')
        else:
            w.WPI_Out(WPI_1,'ST','Off')
            
        if OUT_11_WPI_1.get() == 1:
            w.WPI_Out(WPI_1,'UV','On')
        else:
            w.WPI_Out(WPI_1,'UV','Off')
            
        if OUT_12_WPI_1.get() == 1:
            w.WPI_Out(WPI_1,'WX','On')
        else:
            w.WPI_Out(WPI_1,'WX','Off')
        
def OUT_WPI_2():        
    if active_WPI_2 == 0:
        text.insert(INSERT, 'Error. Select a WPI-2 is not available\n')
    else:    
        if OUT_1_WPI_2.get() == 1:
            w.WPI_Out(WPI_2,'AB','On')
        else:
            w.WPI_Out(WPI_2,'AB','Off')
        
        if OUT_2_WPI_2.get() == 1:
            w.WPI_Out(WPI_2,'CD','On')
        else:
            w.WPI_Out(WPI_2,'CD','Off')
        
        if OUT_3_WPI_2.get() == 1:
            w.WPI_Out(WPI_2,'EF','On')
        else:
            w.WPI_Out(WPI_2,'EF','Off')
            
        if OUT_4_WPI_2.get() == 1:
            w.WPI_Out(WPI_2,'GH','On')
        else:
            w.WPI_Out(WPI_2,'GH','Off')
            
        if OUT_5_WPI_2.get() == 1:
            w.WPI_Out(WPI_2,'IJ','On')
        else:
            w.WPI_Out(WPI_2,'IJ','Off')
            
        if OUT_6_WPI_2.get() == 1:
            w.WPI_Out(WPI_2,'KL','On')
        else:
            w.WPI_Out(WPI_2,'KL','Off')
            
        if OUT_7_WPI_2.get() == 1:
            w.WPI_Out(WPI_2,'MN','On')
        else:
            w.WPI_Out(WPI_2,'MN','Off') 
            
        if OUT_8_WPI_2.get() == 1:
            w.WPI_Out(WPI_2,'OP','On')
        else:
            w.WPI_Out(WPI_2,'OP','Off')
            
        if OUT_9_WPI_2.get() == 1:
            w.WPI_Out(WPI_2,'QR','On')
        else:
            w.WPI_Out(WPI_2,'QR','Off')
            
        if OUT_10_WPI_2.get() == 1:
            w.WPI_Out(WPI_2,'ST','On')
        else:
            w.WPI_Out(WPI_2,'ST','Off')
            
        if OUT_11_WPI_2.get() == 1:
            w.WPI_Out(WPI_2,'UV','On')
        else:
            w.WPI_Out(WPI_2,'UV','Off')
            
        if OUT_12_WPI_2.get() == 1:
            w.WPI_Out(WPI_2,'WX','On')
        else:
            w.WPI_Out(WPI_2,'WX','Off')
    
def OUT_WPI_3():        
    if active_WPI_3 == 0:
        text.insert(INSERT, 'Error. Select a WPI-3 is not available\n')
    else:    
        if OUT_1_WPI_3.get() == 1:
            w.WPI_Out(WPI_3,'AB','On')
        else:
            w.WPI_Out(WPI_3,'AB','Off')
        
        if OUT_2_WPI_3.get() == 1:
            w.WPI_Out(WPI_3,'CD','On')
        else:
            w.WPI_Out(WPI_3,'CD','Off')
        
        if OUT_3_WPI_3.get() == 1:
            w.WPI_Out(WPI_3,'EF','On')
        else:
            w.WPI_Out(WPI_3,'EF','Off')
            
        if OUT_4_WPI_3.get() == 1:
            w.WPI_Out(WPI_3,'GH','On')
        else:
            w.WPI_Out(WPI_3,'GH','Off')
            
        if OUT_5_WPI_3.get() == 1:
            w.WPI_Out(WPI_3,'IJ','On')
        else:
            w.WPI_Out(WPI_3,'IJ','Off')
            
        if OUT_6_WPI_3.get() == 1:
            w.WPI_Out(WPI_3,'KL','On')
        else:
            w.WPI_Out(WPI_3,'KL','Off')
            
        if OUT_7_WPI_3.get() == 1:
            w.WPI_Out(WPI_3,'MN','On')
        else:
            w.WPI_Out(WPI_3,'MN','Off') 
            
        if OUT_8_WPI_3.get() == 1:
            w.WPI_Out(WPI_3,'OP','On')
        else:
            w.WPI_Out(WPI_3,'OP','Off')
            
        if OUT_9_WPI_3.get() == 1:
            w.WPI_Out(WPI_3,'QR','On')
        else:
            w.WPI_Out(WPI_3,'QR','Off')
            
        if OUT_10_WPI_3.get() == 1:
            w.WPI_Out(WPI_3,'ST','On')
        else:
            w.WPI_Out(WPI_3,'ST','Off')
            
        if OUT_11_WPI_3.get() == 1:
            w.WPI_Out(WPI_3,'UV','On')
        else:
            w.WPI_Out(WPI_3,'UV','Off')
            
        if OUT_12_WPI_3.get() == 1:
            w.WPI_Out(WPI_3,'WX','On')
        else:
            w.WPI_Out(WPI_3,'WX','Off')
        

def OUT_WPI_4():        
    if active_WPI_4 == 0:
        text.insert(INSERT, 'Error. Select a WPI-4 is not available\n')
    else:    
        if OUT_1_WPI_4.get() == 1:
            w.WPI_Out(WPI_4,'AB','On')
        else:
            w.WPI_Out(WPI_4,'AB','Off')
        
        if OUT_2_WPI_4.get() == 1:
            w.WPI_Out(WPI_4,'CD','On')
        else:
            w.WPI_Out(WPI_4,'CD','Off')
        
        if OUT_3_WPI_4.get() == 1:
            w.WPI_Out(WPI_4,'EF','On')
        else:
            w.WPI_Out(WPI_4,'EF','Off')
            
        if OUT_4_WPI_4.get() == 1:
            w.WPI_Out(WPI_4,'GH','On')
        else:
            w.WPI_Out(WPI_4,'GH','Off')
            
        if OUT_5_WPI_4.get() == 1:
            w.WPI_Out(WPI_4,'IJ','On')
        else:
            w.WPI_Out(WPI_4,'IJ','Off')
            
        if OUT_6_WPI_4.get() == 1:
            w.WPI_Out(WPI_4,'KL','On')
        else:
            w.WPI_Out(WPI_4,'KL','Off')
            
        if OUT_7_WPI_4.get() == 1:
            w.WPI_Out(WPI_4,'MN','On')
        else:
            w.WPI_Out(WPI_4,'MN','Off') 
            
        if OUT_8_WPI_4.get() == 1:
            w.WPI_Out(WPI_4,'OP','On')
        else:
            w.WPI_Out(WPI_4,'OP','Off')
            
        if OUT_9_WPI_4.get() == 1:
            w.WPI_Out(WPI_4,'QR','On')
        else:
            w.WPI_Out(WPI_4,'QR','Off')
            
        if OUT_10_WPI_4.get() == 1:
            w.WPI_Out(WPI_4,'ST','On')
        else:
            w.WPI_Out(WPI_4,'ST','Off')
            
        if OUT_11_WPI_4.get() == 1:
            w.WPI_Out(WPI_4,'UV','On')
        else:
            w.WPI_Out(WPI_4,'UV','Off')
            
        if OUT_12_WPI_4.get() == 1:
            w.WPI_Out(WPI_4,'WX','On')
        else:
            w.WPI_Out(WPI_4,'WX','Off')    
    

def OUT_WPI_5():        
    if active_WPI_5 == 0:
        text.insert(INSERT, 'Error. Select a WPI-5 is not available\n')
    else:    
        if OUT_1_WPI_5.get() == 1:
            w.WPI_Out(WPI_5,'AB','On')
        else:
            w.WPI_Out(WPI_5,'AB','Off')
        
        if OUT_2_WPI_5.get() == 1:
            w.WPI_Out(WPI_5,'CD','On')
        else:
            w.WPI_Out(WPI_5,'CD','Off')
        
        if OUT_3_WPI_5.get() == 1:
            w.WPI_Out(WPI_5,'EF','On')
        else:
            w.WPI_Out(WPI_5,'EF','Off')
            
        if OUT_4_WPI_5.get() == 1:
            w.WPI_Out(WPI_5,'GH','On')
        else:
            w.WPI_Out(WPI_5,'GH','Off')
            
        if OUT_5_WPI_5.get() == 1:
            w.WPI_Out(WPI_5,'IJ','On')
        else:
            w.WPI_Out(WPI_5,'IJ','Off')
            
        if OUT_6_WPI_5.get() == 1:
            w.WPI_Out(WPI_5,'KL','On')
        else:
            w.WPI_Out(WPI_5,'KL','Off')
            
        if OUT_7_WPI_5.get() == 1:
            w.WPI_Out(WPI_5,'MN','On')
        else:
            w.WPI_Out(WPI_5,'MN','Off') 
            
        if OUT_8_WPI_5.get() == 1:
            w.WPI_Out(WPI_5,'OP','On')
        else:
            w.WPI_Out(WPI_5,'OP','Off')
            
        if OUT_9_WPI_5.get() == 1:
            w.WPI_Out(WPI_5,'QR','On')
        else:
            w.WPI_Out(WPI_5,'QR','Off')
            
        if OUT_10_WPI_5.get() == 1:
            w.WPI_Out(WPI_5,'ST','On')
        else:
            w.WPI_Out(WPI_5,'ST','Off')
            
        if OUT_11_WPI_5.get() == 1:
            w.WPI_Out(WPI_5,'UV','On')
        else:
            w.WPI_Out(WPI_5,'UV','Off')
            
        if OUT_12_WPI_5.get() == 1:
            w.WPI_Out(WPI_5,'WX','On')
        else:
            w.WPI_Out(WPI_5,'WX','Off')
            

def OUT_WPI_6():        
    if active_WPI_6 == 0:
        text.insert(INSERT, 'Error. Select a WPI-6 is not available\n')
    else:    
        if OUT_1_WPI_6.get() == 1:
            w.WPI_Out(WPI_6,'AB','On')
        else:
            w.WPI_Out(WPI_6,'AB','Off')
        
        if OUT_2_WPI_6.get() == 1:
            w.WPI_Out(WPI_6,'CD','On')
        else:
            w.WPI_Out(WPI_6,'CD','Off')
        
        if OUT_3_WPI_6.get() == 1:
            w.WPI_Out(WPI_6,'EF','On')
        else:
            w.WPI_Out(WPI_6,'EF','Off')
            
        if OUT_4_WPI_6.get() == 1:
            w.WPI_Out(WPI_6,'GH','On')
        else:
            w.WPI_Out(WPI_6,'GH','Off')
            
        if OUT_5_WPI_6.get() == 1:
            w.WPI_Out(WPI_6,'IJ','On')
        else:
            w.WPI_Out(WPI_6,'IJ','Off')
            
        if OUT_6_WPI_6.get() == 1:
            w.WPI_Out(WPI_6,'KL','On')
        else:
            w.WPI_Out(WPI_6,'KL','Off')
            
        if OUT_7_WPI_6.get() == 1:
            w.WPI_Out(WPI_6,'MN','On')
        else:
            w.WPI_Out(WPI_6,'MN','Off') 
            
        if OUT_8_WPI_6.get() == 1:
            w.WPI_Out(WPI_6,'OP','On')
        else:
            w.WPI_Out(WPI_6,'OP','Off')
            
        if OUT_9_WPI_6.get() == 1:
            w.WPI_Out(WPI_6,'QR','On')
        else:
            w.WPI_Out(WPI_6,'QR','Off')
            
        if OUT_10_WPI_6.get() == 1:
            w.WPI_Out(WPI_6,'ST','On')
        else:
            w.WPI_Out(WPI_6,'ST','Off')
            
        if OUT_11_WPI_6.get() == 1:
            w.WPI_Out(WPI_6,'UV','On')
        else:
            w.WPI_Out(WPI_6,'UV','Off')
            
        if OUT_12_WPI_6.get() == 1:
            w.WPI_Out(WPI_6,'WX','On')
        else:
            w.WPI_Out(WPI_6,'WX','Off')


#%%------------DECLARATION OF INPUTS AND OUTPUTS-------------------------------    
OUT_1_WPI_1 = tkinter.IntVar()
OUT_2_WPI_1 = tkinter.IntVar()
OUT_3_WPI_1 = tkinter.IntVar()
OUT_4_WPI_1 = tkinter.IntVar()
OUT_5_WPI_1 = tkinter.IntVar()
OUT_6_WPI_1 = tkinter.IntVar()
OUT_7_WPI_1 = tkinter.IntVar()
OUT_8_WPI_1 = tkinter.IntVar()
OUT_9_WPI_1 = tkinter.IntVar()
OUT_10_WPI_1 = tkinter.IntVar()
OUT_11_WPI_1 = tkinter.IntVar()
OUT_12_WPI_1 = tkinter.IntVar()

IN_1_WPI_1 = tkinter.IntVar()
IN_2_WPI_1 = tkinter.IntVar()
IN_3_WPI_1 = tkinter.IntVar()
IN_4_WPI_1 = tkinter.IntVar()
IN_5_WPI_1 = tkinter.IntVar()
IN_6_WPI_1 = tkinter.IntVar()
IN_7_WPI_1 = tkinter.IntVar()
IN_8_WPI_1 = tkinter.IntVar()
IN_9_WPI_1 = tkinter.IntVar()
IN_10_WPI_1 = tkinter.IntVar()
IN_11_WPI_1 = tkinter.IntVar()
IN_12_WPI_1 = tkinter.IntVar()



OUT_1_WPI_2 = tkinter.IntVar()
OUT_2_WPI_2 = tkinter.IntVar()
OUT_3_WPI_2 = tkinter.IntVar()
OUT_4_WPI_2 = tkinter.IntVar()
OUT_5_WPI_2 = tkinter.IntVar()
OUT_6_WPI_2 = tkinter.IntVar()
OUT_7_WPI_2 = tkinter.IntVar()
OUT_8_WPI_2 = tkinter.IntVar()
OUT_9_WPI_2 = tkinter.IntVar()
OUT_10_WPI_2 = tkinter.IntVar()
OUT_11_WPI_2 = tkinter.IntVar()
OUT_12_WPI_2 = tkinter.IntVar()

IN_1_WPI_2 = tkinter.IntVar()
IN_2_WPI_2 = tkinter.IntVar()
IN_3_WPI_2 = tkinter.IntVar()
IN_4_WPI_2 = tkinter.IntVar()
IN_5_WPI_2 = tkinter.IntVar()
IN_6_WPI_2 = tkinter.IntVar()
IN_7_WPI_2 = tkinter.IntVar()
IN_8_WPI_2 = tkinter.IntVar()
IN_9_WPI_2 = tkinter.IntVar()
IN_10_WPI_2 = tkinter.IntVar()
IN_11_WPI_2 = tkinter.IntVar()
IN_12_WPI_2 = tkinter.IntVar()



OUT_1_WPI_3 = tkinter.IntVar()
OUT_2_WPI_3 = tkinter.IntVar()
OUT_3_WPI_3 = tkinter.IntVar()
OUT_4_WPI_3 = tkinter.IntVar()
OUT_5_WPI_3 = tkinter.IntVar()
OUT_6_WPI_3 = tkinter.IntVar()
OUT_7_WPI_3 = tkinter.IntVar()
OUT_8_WPI_3 = tkinter.IntVar()
OUT_9_WPI_3 = tkinter.IntVar()
OUT_10_WPI_3 = tkinter.IntVar()
OUT_11_WPI_3 = tkinter.IntVar()
OUT_12_WPI_3 = tkinter.IntVar()

IN_1_WPI_3 = tkinter.IntVar()
IN_2_WPI_3 = tkinter.IntVar()
IN_3_WPI_3 = tkinter.IntVar()
IN_4_WPI_3 = tkinter.IntVar()
IN_5_WPI_3 = tkinter.IntVar()
IN_6_WPI_3 = tkinter.IntVar()
IN_7_WPI_3 = tkinter.IntVar()
IN_8_WPI_3 = tkinter.IntVar()
IN_9_WPI_3 = tkinter.IntVar()
IN_10_WPI_3 = tkinter.IntVar()
IN_11_WPI_3 = tkinter.IntVar()
IN_12_WPI_3 = tkinter.IntVar()


OUT_1_WPI_4 = tkinter.IntVar()
OUT_2_WPI_4 = tkinter.IntVar()
OUT_3_WPI_4 = tkinter.IntVar()
OUT_4_WPI_4 = tkinter.IntVar()
OUT_5_WPI_4 = tkinter.IntVar()
OUT_6_WPI_4 = tkinter.IntVar()
OUT_7_WPI_4 = tkinter.IntVar()
OUT_8_WPI_4 = tkinter.IntVar()
OUT_9_WPI_4 = tkinter.IntVar()
OUT_10_WPI_4 = tkinter.IntVar()
OUT_11_WPI_4 = tkinter.IntVar()
OUT_12_WPI_4 = tkinter.IntVar()

IN_1_WPI_4 = tkinter.IntVar()
IN_2_WPI_4 = tkinter.IntVar()
IN_3_WPI_4 = tkinter.IntVar()
IN_4_WPI_4 = tkinter.IntVar()
IN_5_WPI_4 = tkinter.IntVar()
IN_6_WPI_4 = tkinter.IntVar()
IN_7_WPI_4 = tkinter.IntVar()
IN_8_WPI_4 = tkinter.IntVar()
IN_9_WPI_4 = tkinter.IntVar()
IN_10_WPI_4 = tkinter.IntVar()
IN_11_WPI_4 = tkinter.IntVar()
IN_12_WPI_4 = tkinter.IntVar()


OUT_1_WPI_5 = tkinter.IntVar()
OUT_2_WPI_5 = tkinter.IntVar()
OUT_3_WPI_5 = tkinter.IntVar()
OUT_4_WPI_5 = tkinter.IntVar()
OUT_5_WPI_5 = tkinter.IntVar()
OUT_6_WPI_5 = tkinter.IntVar()
OUT_7_WPI_5 = tkinter.IntVar()
OUT_8_WPI_5 = tkinter.IntVar()
OUT_9_WPI_5 = tkinter.IntVar()
OUT_10_WPI_5 = tkinter.IntVar()
OUT_11_WPI_5 = tkinter.IntVar()
OUT_12_WPI_5 = tkinter.IntVar()

IN_1_WPI_5 = tkinter.IntVar()
IN_2_WPI_5 = tkinter.IntVar()
IN_3_WPI_5 = tkinter.IntVar()
IN_4_WPI_5 = tkinter.IntVar()
IN_5_WPI_5 = tkinter.IntVar()
IN_6_WPI_5 = tkinter.IntVar()
IN_7_WPI_5 = tkinter.IntVar()
IN_8_WPI_5 = tkinter.IntVar()
IN_9_WPI_5 = tkinter.IntVar()
IN_10_WPI_5 = tkinter.IntVar()
IN_11_WPI_5 = tkinter.IntVar()
IN_12_WPI_5 = tkinter.IntVar()


OUT_1_WPI_6 = tkinter.IntVar()
OUT_2_WPI_6 = tkinter.IntVar()
OUT_3_WPI_6 = tkinter.IntVar()
OUT_4_WPI_6 = tkinter.IntVar()
OUT_5_WPI_6 = tkinter.IntVar()
OUT_6_WPI_6 = tkinter.IntVar()
OUT_7_WPI_6 = tkinter.IntVar()
OUT_8_WPI_6 = tkinter.IntVar()
OUT_9_WPI_6 = tkinter.IntVar()
OUT_10_WPI_6 = tkinter.IntVar()
OUT_11_WPI_6 = tkinter.IntVar()
OUT_12_WPI_6 = tkinter.IntVar()

IN_1_WPI_6 = tkinter.IntVar()
IN_2_WPI_6 = tkinter.IntVar()
IN_3_WPI_6 = tkinter.IntVar()
IN_4_WPI_6 = tkinter.IntVar()
IN_5_WPI_6 = tkinter.IntVar()
IN_6_WPI_6 = tkinter.IntVar()
IN_7_WPI_6 = tkinter.IntVar()
IN_8_WPI_6 = tkinter.IntVar()
IN_9_WPI_6 = tkinter.IntVar()
IN_10_WPI_6 = tkinter.IntVar()
IN_11_WPI_6 = tkinter.IntVar()
IN_12_WPI_6 = tkinter.IntVar()

#%%------------OUT CHECKBUTTONS WPI-1-----------------------------------------------    
checkOUT_1_WPI_1 = tkinter.Checkbutton(root, variable=OUT_1_WPI_1,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_1)
checkOUT_1_WPI_1.config(font = (Font_1,10))
checkOUT_1_WPI_1.place(x=aux_width_monitor, y=aux_height_monitor*1.55)

checkOUT_2_WPI_1 = tkinter.Checkbutton(root, variable=OUT_2_WPI_1,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_1)
checkOUT_2_WPI_1.config(font = (Font_1,10))
checkOUT_2_WPI_1.place(x=aux_width_monitor*1.25, y=aux_height_monitor*1.55)

checkOUT_3_WPI_1 = tkinter.Checkbutton(root, variable=OUT_3_WPI_1,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_1)
checkOUT_3_WPI_1.config(font = (Font_1,10))
checkOUT_3_WPI_1.place(x=aux_width_monitor*1.5, y=aux_height_monitor*1.55)

checkOUT_4_WPI_1 = tkinter.Checkbutton(root, variable=OUT_4_WPI_1,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_1)
checkOUT_4_WPI_1.config(font = (Font_1,10))
checkOUT_4_WPI_1.place(x=aux_width_monitor*1.75, y=aux_height_monitor*1.55)

checkOUT_5_WPI_1 = tkinter.Checkbutton(root, variable=OUT_5_WPI_1,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_1)
checkOUT_5_WPI_1.config(font = (Font_1,10))
checkOUT_5_WPI_1.place(x=aux_width_monitor*2, y=aux_height_monitor*1.55)

checkOUT_6_WPI_1 = tkinter.Checkbutton(root, variable=OUT_6_WPI_1,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_1)
checkOUT_6_WPI_1.config(font = (Font_1,10))
checkOUT_6_WPI_1.place(x=aux_width_monitor*2.25, y=aux_height_monitor*1.55)

checkOUT_7_WPI_1 = tkinter.Checkbutton(root, variable=OUT_7_WPI_1,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_1)
checkOUT_7_WPI_1.config(font = (Font_1,10))
checkOUT_7_WPI_1.place(x=aux_width_monitor*2.5, y=aux_height_monitor*1.55)

checkOUT_8_WPI_1 = tkinter.Checkbutton(root, variable=OUT_8_WPI_1,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_1)
checkOUT_8_WPI_1.config(font = (Font_1,10))
checkOUT_8_WPI_1.place(x=aux_width_monitor*2.75, y=aux_height_monitor*1.55)

checkOUT_9_WPI_1 = tkinter.Checkbutton(root, variable=OUT_9_WPI_1,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_1)
checkOUT_9_WPI_1.config(font = (Font_1,10))
checkOUT_9_WPI_1.place(x=aux_width_monitor*3, y=aux_height_monitor*1.55)

checkOUT_10_WPI_1 = tkinter.Checkbutton(root, variable=OUT_10_WPI_1,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_1)
checkOUT_10_WPI_1.config(font = (Font_1,10))
checkOUT_10_WPI_1.place(x=aux_width_monitor*3.25, y=aux_height_monitor*1.55)

checkOUT_11_WPI_1 = tkinter.Checkbutton(root, variable=OUT_11_WPI_1,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_1)
checkOUT_11_WPI_1.config(font = (Font_1,10))
checkOUT_11_WPI_1.place(x=aux_width_monitor*3.5, y=aux_height_monitor*1.55)

checkOUT_12_WPI_1 = tkinter.Checkbutton(root, variable=OUT_12_WPI_1,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_1)
checkOUT_12_WPI_1.config(font = (Font_1,10))
checkOUT_12_WPI_1.place(x=aux_width_monitor*3.75, y=aux_height_monitor*1.55)


#%%------------OUT CHECKBUTTONS WPI-2-----------------------------------------------    
checkOUT_1_WPI_2 = tkinter.Checkbutton(root, variable=OUT_1_WPI_2,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_2)
checkOUT_1_WPI_2.config(font = (Font_1,10))
checkOUT_1_WPI_2.place(x=aux_width_monitor, y=aux_height_monitor*3.55)

checkOUT_2_WPI_2 = tkinter.Checkbutton(root, variable=OUT_2_WPI_2,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_2)
checkOUT_2_WPI_2.config(font = (Font_1,10))
checkOUT_2_WPI_2.place(x=aux_width_monitor*1.25, y=aux_height_monitor*3.55)

checkOUT_3_WPI_2 = tkinter.Checkbutton(root, variable=OUT_3_WPI_2,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_2)
checkOUT_3_WPI_2.config(font = (Font_1,10))
checkOUT_3_WPI_2.place(x=aux_width_monitor*1.5, y=aux_height_monitor*3.55)

checkOUT_4_WPI_2 = tkinter.Checkbutton(root, variable=OUT_4_WPI_2,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_2)
checkOUT_4_WPI_2.config(font = (Font_1,10))
checkOUT_4_WPI_2.place(x=aux_width_monitor*1.75, y=aux_height_monitor*3.55)

checkOUT_5_WPI_2 = tkinter.Checkbutton(root, variable=OUT_5_WPI_2,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_2)
checkOUT_5_WPI_2.config(font = (Font_1,10))
checkOUT_5_WPI_2.place(x=aux_width_monitor*2, y=aux_height_monitor*3.55)

checkOUT_6_WPI_2 = tkinter.Checkbutton(root, variable=OUT_6_WPI_2,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_2)
checkOUT_6_WPI_2.config(font = (Font_1,10))
checkOUT_6_WPI_2.place(x=aux_width_monitor*2.25, y=aux_height_monitor*3.55)

checkOUT_7_WPI_2 = tkinter.Checkbutton(root, variable=OUT_7_WPI_2,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_2)
checkOUT_7_WPI_2.config(font = (Font_1,10))
checkOUT_7_WPI_2.place(x=aux_width_monitor*2.5, y=aux_height_monitor*3.55)

checkOUT_8_WPI_2 = tkinter.Checkbutton(root, variable=OUT_8_WPI_2,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_2)
checkOUT_8_WPI_2.config(font = (Font_1,10))
checkOUT_8_WPI_2.place(x=aux_width_monitor*2.75, y=aux_height_monitor*3.55)

checkOUT_9_WPI_2 = tkinter.Checkbutton(root, variable=OUT_9_WPI_2,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_2)
checkOUT_9_WPI_2.config(font = (Font_1,10))
checkOUT_9_WPI_2.place(x=aux_width_monitor*3, y=aux_height_monitor*3.55)

checkOUT_10_WPI_2 = tkinter.Checkbutton(root, variable=OUT_10_WPI_2,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_2)
checkOUT_10_WPI_2.config(font = (Font_1,10))
checkOUT_10_WPI_2.place(x=aux_width_monitor*3.25, y=aux_height_monitor*3.55)

checkOUT_11_WPI_2 = tkinter.Checkbutton(root, variable=OUT_11_WPI_2,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_2)
checkOUT_11_WPI_2.config(font = (Font_1,10))
checkOUT_11_WPI_2.place(x=aux_width_monitor*3.5, y=aux_height_monitor*3.55)

checkOUT_12_WPI_2 = tkinter.Checkbutton(root, variable=OUT_12_WPI_2,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_2)
checkOUT_12_WPI_2.config(font = (Font_1,10))
checkOUT_12_WPI_2.place(x=aux_width_monitor*3.75, y=aux_height_monitor*3.55)


#%%------------OUT CHECKBUTTONS WPI-3-----------------------------------------------    
checkOUT_1_WPI_3 = tkinter.Checkbutton(root, variable=OUT_1_WPI_3,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_3)
checkOUT_1_WPI_3.config(font = (Font_1,10))
checkOUT_1_WPI_3.place(x=aux_width_monitor, y=aux_height_monitor*5.55)

checkOUT_2_WPI_3 = tkinter.Checkbutton(root, variable=OUT_2_WPI_3,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_3)
checkOUT_2_WPI_3.config(font = (Font_1,10))
checkOUT_2_WPI_3.place(x=aux_width_monitor*1.25, y=aux_height_monitor*5.55)

checkOUT_3_WPI_3 = tkinter.Checkbutton(root, variable=OUT_3_WPI_3,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_3)
checkOUT_3_WPI_3.config(font = (Font_1,10))
checkOUT_3_WPI_3.place(x=aux_width_monitor*1.5, y=aux_height_monitor*5.55)

checkOUT_4_WPI_3 = tkinter.Checkbutton(root, variable=OUT_4_WPI_3,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_3)
checkOUT_4_WPI_3.config(font = (Font_1,10))
checkOUT_4_WPI_3.place(x=aux_width_monitor*1.75, y=aux_height_monitor*5.55)

checkOUT_5_WPI_3 = tkinter.Checkbutton(root, variable=OUT_5_WPI_3,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_3)
checkOUT_5_WPI_3.config(font = (Font_1,10))
checkOUT_5_WPI_3.place(x=aux_width_monitor*2, y=aux_height_monitor*5.55)

checkOUT_6_WPI_3 = tkinter.Checkbutton(root, variable=OUT_6_WPI_3,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_3)
checkOUT_6_WPI_3.config(font = (Font_1,10))
checkOUT_6_WPI_3.place(x=aux_width_monitor*2.25, y=aux_height_monitor*5.55)

checkOUT_7_WPI_3 = tkinter.Checkbutton(root, variable=OUT_7_WPI_3,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_3)
checkOUT_7_WPI_3.config(font = (Font_1,10))
checkOUT_7_WPI_3.place(x=aux_width_monitor*2.5, y=aux_height_monitor*5.55)

checkOUT_8_WPI_3 = tkinter.Checkbutton(root, variable=OUT_8_WPI_3,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_3)
checkOUT_8_WPI_3.config(font = (Font_1,10))
checkOUT_8_WPI_3.place(x=aux_width_monitor*2.75, y=aux_height_monitor*5.55)

checkOUT_9_WPI_3 = tkinter.Checkbutton(root, variable=OUT_9_WPI_3,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_3)
checkOUT_9_WPI_3.config(font = (Font_1,10))
checkOUT_9_WPI_3.place(x=aux_width_monitor*3, y=aux_height_monitor*5.55)

checkOUT_10_WPI_3 = tkinter.Checkbutton(root, variable=OUT_10_WPI_3,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_3)
checkOUT_10_WPI_3.config(font = (Font_1,10))
checkOUT_10_WPI_3.place(x=aux_width_monitor*3.25, y=aux_height_monitor*5.55)

checkOUT_11_WPI_3 = tkinter.Checkbutton(root, variable=OUT_11_WPI_3,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_3)
checkOUT_11_WPI_3.config(font = (Font_1,10))
checkOUT_11_WPI_3.place(x=aux_width_monitor*3.5, y=aux_height_monitor*5.55)

checkOUT_12_WPI_3 = tkinter.Checkbutton(root, variable=OUT_12_WPI_3,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_3)
checkOUT_12_WPI_3.config(font = (Font_1,10))
checkOUT_12_WPI_3.place(x=aux_width_monitor*3.75, y=aux_height_monitor*5.55)



#%%------------OUT CHECKBUTTONS WPI-4-----------------------------------------------    
checkOUT_1_WPI_4 = tkinter.Checkbutton(root, variable=OUT_1_WPI_4,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_4)
checkOUT_1_WPI_4.config(font = (Font_1,10))
checkOUT_1_WPI_4.place(x=aux_width_monitor, y=aux_height_monitor*7.55)

checkOUT_2_WPI_4 = tkinter.Checkbutton(root, variable=OUT_2_WPI_4,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_4)
checkOUT_2_WPI_4.config(font = (Font_1,10))
checkOUT_2_WPI_4.place(x=aux_width_monitor*1.25, y=aux_height_monitor*7.55)

checkOUT_3_WPI_4 = tkinter.Checkbutton(root, variable=OUT_3_WPI_4,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_4)
checkOUT_3_WPI_4.config(font = (Font_1,10))
checkOUT_3_WPI_4.place(x=aux_width_monitor*1.5, y=aux_height_monitor*7.55)

checkOUT_4_WPI_4 = tkinter.Checkbutton(root, variable=OUT_4_WPI_4,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_4)
checkOUT_4_WPI_4.config(font = (Font_1,10))
checkOUT_4_WPI_4.place(x=aux_width_monitor*1.75, y=aux_height_monitor*7.55)

checkOUT_5_WPI_4 = tkinter.Checkbutton(root, variable=OUT_5_WPI_4,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_4)
checkOUT_5_WPI_4.config(font = (Font_1,10))
checkOUT_5_WPI_4.place(x=aux_width_monitor*2, y=aux_height_monitor*7.55)

checkOUT_6_WPI_4 = tkinter.Checkbutton(root, variable=OUT_6_WPI_4,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_4)
checkOUT_6_WPI_4.config(font = (Font_1,10))
checkOUT_6_WPI_4.place(x=aux_width_monitor*2.25, y=aux_height_monitor*7.55)

checkOUT_7_WPI_4 = tkinter.Checkbutton(root, variable=OUT_7_WPI_4,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_4)
checkOUT_7_WPI_4.config(font = (Font_1,10))
checkOUT_7_WPI_4.place(x=aux_width_monitor*2.5, y=aux_height_monitor*7.55)

checkOUT_8_WPI_4 = tkinter.Checkbutton(root, variable=OUT_8_WPI_4,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_4)
checkOUT_8_WPI_4.config(font = (Font_1,10))
checkOUT_8_WPI_4.place(x=aux_width_monitor*2.75, y=aux_height_monitor*7.55)

checkOUT_9_WPI_4 = tkinter.Checkbutton(root, variable=OUT_9_WPI_4,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_4)
checkOUT_9_WPI_4.config(font = (Font_1,10))
checkOUT_9_WPI_4.place(x=aux_width_monitor*3, y=aux_height_monitor*7.55)

checkOUT_10_WPI_4 = tkinter.Checkbutton(root, variable=OUT_10_WPI_4,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_4)
checkOUT_10_WPI_4.config(font = (Font_1,10))
checkOUT_10_WPI_4.place(x=aux_width_monitor*3.25, y=aux_height_monitor*7.55)

checkOUT_11_WPI_4 = tkinter.Checkbutton(root, variable=OUT_11_WPI_4,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_4)
checkOUT_11_WPI_4.config(font = (Font_1,10))
checkOUT_11_WPI_4.place(x=aux_width_monitor*3.5, y=aux_height_monitor*7.55)

checkOUT_12_WPI_4 = tkinter.Checkbutton(root, variable=OUT_12_WPI_4,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_4)
checkOUT_12_WPI_4.config(font = (Font_1,10))
checkOUT_12_WPI_4.place(x=aux_width_monitor*3.75, y=aux_height_monitor*7.55)



#%%------------OUT CHECKBUTTONS WPI-5-----------------------------------------------    
checkOUT_1_WPI_5 = tkinter.Checkbutton(root, variable=OUT_1_WPI_5,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_5)
checkOUT_1_WPI_5.config(font = (Font_1,10))
checkOUT_1_WPI_5.place(x=aux_width_monitor, y=aux_height_monitor*9.55)

checkOUT_2_WPI_5 = tkinter.Checkbutton(root, variable=OUT_2_WPI_5,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_5)
checkOUT_2_WPI_5.config(font = (Font_1,10))
checkOUT_2_WPI_5.place(x=aux_width_monitor*1.25, y=aux_height_monitor*9.55)

checkOUT_3_WPI_5 = tkinter.Checkbutton(root, variable=OUT_3_WPI_5,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_5)
checkOUT_3_WPI_5.config(font = (Font_1,10))
checkOUT_3_WPI_5.place(x=aux_width_monitor*1.5, y=aux_height_monitor*9.55)

checkOUT_4_WPI_5 = tkinter.Checkbutton(root, variable=OUT_4_WPI_5,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_5)
checkOUT_4_WPI_5.config(font = (Font_1,10))
checkOUT_4_WPI_5.place(x=aux_width_monitor*1.75, y=aux_height_monitor*9.55)

checkOUT_5_WPI_5 = tkinter.Checkbutton(root, variable=OUT_5_WPI_5,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_5)
checkOUT_5_WPI_5.config(font = (Font_1,10))
checkOUT_5_WPI_5.place(x=aux_width_monitor*2, y=aux_height_monitor*9.55)

checkOUT_6_WPI_5 = tkinter.Checkbutton(root, variable=OUT_6_WPI_5,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_5)
checkOUT_6_WPI_5.config(font = (Font_1,10))
checkOUT_6_WPI_5.place(x=aux_width_monitor*2.25, y=aux_height_monitor*9.55)

checkOUT_7_WPI_5 = tkinter.Checkbutton(root, variable=OUT_7_WPI_5,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_5)
checkOUT_7_WPI_5.config(font = (Font_1,10))
checkOUT_7_WPI_5.place(x=aux_width_monitor*2.5, y=aux_height_monitor*9.55)

checkOUT_8_WPI_5 = tkinter.Checkbutton(root, variable=OUT_8_WPI_5,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_5)
checkOUT_8_WPI_5.config(font = (Font_1,10))
checkOUT_8_WPI_5.place(x=aux_width_monitor*2.75, y=aux_height_monitor*9.55)

checkOUT_9_WPI_5 = tkinter.Checkbutton(root, variable=OUT_9_WPI_5,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_5)
checkOUT_9_WPI_5.config(font = (Font_1,10))
checkOUT_9_WPI_5.place(x=aux_width_monitor*3, y=aux_height_monitor*9.55)

checkOUT_10_WPI_5 = tkinter.Checkbutton(root, variable=OUT_10_WPI_5,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_5)
checkOUT_10_WPI_5.config(font = (Font_1,10))
checkOUT_10_WPI_5.place(x=aux_width_monitor*3.25, y=aux_height_monitor*9.55)

checkOUT_11_WPI_5 = tkinter.Checkbutton(root, variable=OUT_11_WPI_5,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_5)
checkOUT_11_WPI_5.config(font = (Font_1,10))
checkOUT_11_WPI_5.place(x=aux_width_monitor*3.5, y=aux_height_monitor*9.55)

checkOUT_12_WPI_5 = tkinter.Checkbutton(root, variable=OUT_12_WPI_5,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_5)
checkOUT_12_WPI_5.config(font = (Font_1,10))
checkOUT_12_WPI_5.place(x=aux_width_monitor*3.75, y=aux_height_monitor*9.55)



#%%------------OUT CHECKBUTTONS WPI-6-----------------------------------------------    
checkOUT_1_WPI_6 = tkinter.Checkbutton(root, variable=OUT_1_WPI_6,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_6)
checkOUT_1_WPI_6.config(font = (Font_1,10))
checkOUT_1_WPI_6.place(x=aux_width_monitor, y=aux_height_monitor*11.55)

checkOUT_2_WPI_6 = tkinter.Checkbutton(root, variable=OUT_2_WPI_6,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_6)
checkOUT_2_WPI_6.config(font = (Font_1,10))
checkOUT_2_WPI_6.place(x=aux_width_monitor*1.25, y=aux_height_monitor*11.55)

checkOUT_3_WPI_6 = tkinter.Checkbutton(root, variable=OUT_3_WPI_6,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_6)
checkOUT_3_WPI_6.config(font = (Font_1,10))
checkOUT_3_WPI_6.place(x=aux_width_monitor*1.5, y=aux_height_monitor*11.55)

checkOUT_4_WPI_6 = tkinter.Checkbutton(root, variable=OUT_4_WPI_6,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_6)
checkOUT_4_WPI_6.config(font = (Font_1,10))
checkOUT_4_WPI_6.place(x=aux_width_monitor*1.75, y=aux_height_monitor*11.55)

checkOUT_5_WPI_6 = tkinter.Checkbutton(root, variable=OUT_5_WPI_6,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_6)
checkOUT_5_WPI_6.config(font = (Font_1,10))
checkOUT_5_WPI_6.place(x=aux_width_monitor*2, y=aux_height_monitor*11.55)

checkOUT_6_WPI_6 = tkinter.Checkbutton(root, variable=OUT_6_WPI_6,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_6)
checkOUT_6_WPI_6.config(font = (Font_1,10))
checkOUT_6_WPI_6.place(x=aux_width_monitor*2.25, y=aux_height_monitor*11.55)

checkOUT_7_WPI_6 = tkinter.Checkbutton(root, variable=OUT_7_WPI_6,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_6)
checkOUT_7_WPI_6.config(font = (Font_1,10))
checkOUT_7_WPI_6.place(x=aux_width_monitor*2.5, y=aux_height_monitor*11.55)

checkOUT_8_WPI_6 = tkinter.Checkbutton(root, variable=OUT_8_WPI_6,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_6)
checkOUT_8_WPI_6.config(font = (Font_1,10))
checkOUT_8_WPI_6.place(x=aux_width_monitor*2.75, y=aux_height_monitor*11.55)

checkOUT_9_WPI_6 = tkinter.Checkbutton(root, variable=OUT_9_WPI_6,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_6)
checkOUT_9_WPI_6.config(font = (Font_1,10))
checkOUT_9_WPI_6.place(x=aux_width_monitor*3, y=aux_height_monitor*11.55)

checkOUT_10_WPI_6 = tkinter.Checkbutton(root, variable=OUT_10_WPI_6,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_6)
checkOUT_10_WPI_6.config(font = (Font_1,10))
checkOUT_10_WPI_6.place(x=aux_width_monitor*3.25, y=aux_height_monitor*11.55)

checkOUT_11_WPI_6 = tkinter.Checkbutton(root, variable=OUT_11_WPI_6,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_6)
checkOUT_11_WPI_6.config(font = (Font_1,10))
checkOUT_11_WPI_6.place(x=aux_width_monitor*3.5, y=aux_height_monitor*11.55)

checkOUT_12_WPI_6 = tkinter.Checkbutton(root, variable=OUT_12_WPI_6,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3),
                            command=OUT_WPI_6)
checkOUT_12_WPI_6.config(font = (Font_1,10))
checkOUT_12_WPI_6.place(x=aux_width_monitor*3.75, y=aux_height_monitor*11.55)



#%%------------INPUTS CHECKBUTTONS WPI-1--------------------------------------------
checkIN_1_WPI_1 = tkinter.Checkbutton(root, variable=IN_1_WPI_1,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_1_WPI_1.config(font = (Font_1,10))
checkIN_1_WPI_1.place(x=aux_width_monitor, y=aux_height_monitor*2.05)

checkIN_2_WPI_1 = tkinter.Checkbutton(root, variable=IN_2_WPI_1,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_2_WPI_1.config(font = (Font_1,10))
checkIN_2_WPI_1.place(x=aux_width_monitor*1.25, y=aux_height_monitor*2.05)

checkIN_3_WPI_1 = tkinter.Checkbutton(root, variable=IN_3_WPI_1,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_3_WPI_1.config(font = (Font_1,10))
checkIN_3_WPI_1.place(x=aux_width_monitor*1.5, y=aux_height_monitor*2.05)

checkIN_4_WPI_1 = tkinter.Checkbutton(root, variable=IN_4_WPI_1,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_4_WPI_1.config(font = (Font_1,10))
checkIN_4_WPI_1.place(x=aux_width_monitor*1.75, y=aux_height_monitor*2.05)

checkIN_5_WPI_1 = tkinter.Checkbutton(root, variable=IN_5_WPI_1,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_5_WPI_1.config(font = (Font_1,10))
checkIN_5_WPI_1.place(x=aux_width_monitor*2, y=aux_height_monitor*2.05)

checkIN_6_WPI_1 = tkinter.Checkbutton(root, variable=IN_6_WPI_1,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_6_WPI_1.config(font = (Font_1,10))
checkIN_6_WPI_1.place(x=aux_width_monitor*2.25, y=aux_height_monitor*2.05)

checkIN_7_WPI_1 = tkinter.Checkbutton(root, variable=IN_7_WPI_1,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_7_WPI_1.config(font = (Font_1,10))
checkIN_7_WPI_1.place(x=aux_width_monitor*2.5, y=aux_height_monitor*2.05)

checkIN_8_WPI_1 = tkinter.Checkbutton(root, variable=IN_8_WPI_1,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_8_WPI_1.config(font = (Font_1,10))
checkIN_8_WPI_1.place(x=aux_width_monitor*2.75, y=aux_height_monitor*2.05)

checkIN_9_WPI_1 = tkinter.Checkbutton(root, variable=IN_9_WPI_1,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_9_WPI_1.config(font = (Font_1,10))
checkIN_9_WPI_1.place(x=aux_width_monitor*3, y=aux_height_monitor*2.05)

checkIN_10_WPI_1 = tkinter.Checkbutton(root, variable=IN_10_WPI_1,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_10_WPI_1.config(font = (Font_1,10))
checkIN_10_WPI_1.place(x=aux_width_monitor*3.25, y=aux_height_monitor*2.05)

checkIN_11_WPI_1 = tkinter.Checkbutton(root, variable=IN_11_WPI_1,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_11_WPI_1.config(font = (Font_1,10))
checkIN_11_WPI_1.place(x=aux_width_monitor*3.5, y=aux_height_monitor*2.05)

checkIN_12_WPI_1 = tkinter.Checkbutton(root, variable=IN_12_WPI_1,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_12_WPI_1.config(font = (Font_1,10))
checkIN_12_WPI_1.place(x=aux_width_monitor*3.75, y=aux_height_monitor*2.05)


#%%------------INPUTS CHECKBUTTONS WPI-2--------------------------------------------
checkIN_1_WPI_2 = tkinter.Checkbutton(root, variable=IN_1_WPI_2,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_1_WPI_2.config(font = (Font_1,10))
checkIN_1_WPI_2.place(x=aux_width_monitor, y=aux_height_monitor*4.05)

checkIN_2_WPI_2 = tkinter.Checkbutton(root, variable=IN_2_WPI_2,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_2_WPI_2.config(font = (Font_1,10))
checkIN_2_WPI_2.place(x=aux_width_monitor*1.25, y=aux_height_monitor*4.05)

checkIN_3_WPI_2 = tkinter.Checkbutton(root, variable=IN_3_WPI_2,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_3_WPI_2.config(font = (Font_1,10))
checkIN_3_WPI_2.place(x=aux_width_monitor*1.5, y=aux_height_monitor*4.05)

checkIN_4_WPI_2 = tkinter.Checkbutton(root, variable=IN_4_WPI_2,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_4_WPI_2.config(font = (Font_1,10))
checkIN_4_WPI_2.place(x=aux_width_monitor*1.75, y=aux_height_monitor*4.05)

checkIN_5_WPI_2 = tkinter.Checkbutton(root, variable=IN_5_WPI_2,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_5_WPI_2.config(font = (Font_1,10))
checkIN_5_WPI_2.place(x=aux_width_monitor*2, y=aux_height_monitor*4.05)

checkIN_6_WPI_2 = tkinter.Checkbutton(root, variable=IN_6_WPI_2,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_6_WPI_2.config(font = (Font_1,10))
checkIN_6_WPI_2.place(x=aux_width_monitor*2.25, y=aux_height_monitor*4.05)

checkIN_7_WPI_2 = tkinter.Checkbutton(root, variable=IN_7_WPI_2,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_7_WPI_2.config(font = (Font_1,10))
checkIN_7_WPI_2.place(x=aux_width_monitor*2.5, y=aux_height_monitor*4.05)

checkIN_8_WPI_2 = tkinter.Checkbutton(root, variable=IN_8_WPI_2,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_8_WPI_2.config(font = (Font_1,10))
checkIN_8_WPI_2.place(x=aux_width_monitor*2.75, y=aux_height_monitor*4.05)

checkIN_9_WPI_2 = tkinter.Checkbutton(root, variable=IN_9_WPI_2,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_9_WPI_2.config(font = (Font_1,10))
checkIN_9_WPI_2.place(x=aux_width_monitor*3, y=aux_height_monitor*4.05)

checkIN_10_WPI_2 = tkinter.Checkbutton(root, variable=IN_10_WPI_2,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_10_WPI_2.config(font = (Font_1,10))
checkIN_10_WPI_2.place(x=aux_width_monitor*3.25, y=aux_height_monitor*4.05)

checkIN_11_WPI_2 = tkinter.Checkbutton(root, variable=IN_11_WPI_2,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_11_WPI_2.config(font = (Font_1,10))
checkIN_11_WPI_2.place(x=aux_width_monitor*3.5, y=aux_height_monitor*4.05)

checkIN_12_WPI_2 = tkinter.Checkbutton(root, variable=IN_12_WPI_2,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_12_WPI_2.config(font = (Font_1,10))
checkIN_12_WPI_2.place(x=aux_width_monitor*3.75, y=aux_height_monitor*4.05)


#%%------------INPUTS CHECKBUTTONS WPI-3--------------------------------------------
checkIN_1_WPI_3 = tkinter.Checkbutton(root, variable=IN_1_WPI_3,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_1_WPI_3.config(font = (Font_1,10))
checkIN_1_WPI_3.place(x=aux_width_monitor, y=aux_height_monitor*6.05)

checkIN_2_WPI_3 = tkinter.Checkbutton(root, variable=IN_2_WPI_3,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_2_WPI_3.config(font = (Font_1,10))
checkIN_2_WPI_3.place(x=aux_width_monitor*1.25, y=aux_height_monitor*6.05)

checkIN_3_WPI_3 = tkinter.Checkbutton(root, variable=IN_3_WPI_3,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_3_WPI_3.config(font = (Font_1,10))
checkIN_3_WPI_3.place(x=aux_width_monitor*1.5, y=aux_height_monitor*6.05)

checkIN_4_WPI_3 = tkinter.Checkbutton(root, variable=IN_4_WPI_3,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_4_WPI_3.config(font = (Font_1,10))
checkIN_4_WPI_3.place(x=aux_width_monitor*1.75, y=aux_height_monitor*6.05)

checkIN_5_WPI_3 = tkinter.Checkbutton(root, variable=IN_5_WPI_3,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_5_WPI_3.config(font = (Font_1,10))
checkIN_5_WPI_3.place(x=aux_width_monitor*2, y=aux_height_monitor*6.05)

checkIN_6_WPI_3 = tkinter.Checkbutton(root, variable=IN_6_WPI_3,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_6_WPI_3.config(font = (Font_1,10))
checkIN_6_WPI_3.place(x=aux_width_monitor*2.25, y=aux_height_monitor*6.05)

checkIN_7_WPI_3 = tkinter.Checkbutton(root, variable=IN_7_WPI_3,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_7_WPI_3.config(font = (Font_1,10))
checkIN_7_WPI_3.place(x=aux_width_monitor*2.5, y=aux_height_monitor*6.05)

checkIN_8_WPI_3 = tkinter.Checkbutton(root, variable=IN_8_WPI_3,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_8_WPI_3.config(font = (Font_1,10))
checkIN_8_WPI_3.place(x=aux_width_monitor*2.75, y=aux_height_monitor*6.05)

checkIN_9_WPI_3 = tkinter.Checkbutton(root, variable=IN_9_WPI_3,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_9_WPI_3.config(font = (Font_1,10))
checkIN_9_WPI_3.place(x=aux_width_monitor*3, y=aux_height_monitor*6.05)

checkIN_10_WPI_3 = tkinter.Checkbutton(root, variable=IN_10_WPI_3,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_10_WPI_3.config(font = (Font_1,10))
checkIN_10_WPI_3.place(x=aux_width_monitor*3.25, y=aux_height_monitor*6.05)

checkIN_11_WPI_3 = tkinter.Checkbutton(root, variable=IN_11_WPI_3,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_11_WPI_3.config(font = (Font_1,10))
checkIN_11_WPI_3.place(x=aux_width_monitor*3.5, y=aux_height_monitor*6.05)

checkIN_12_WPI_3 = tkinter.Checkbutton(root, variable=IN_12_WPI_3,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_12_WPI_3.config(font = (Font_1,10))
checkIN_12_WPI_3.place(x=aux_width_monitor*3.75, y=aux_height_monitor*6.05)


#%%------------INPUTS CHECKBUTTONS WPI-4--------------------------------------------
checkIN_1_WPI_4 = tkinter.Checkbutton(root, variable=IN_1_WPI_4,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_1_WPI_4.config(font = (Font_1,10))
checkIN_1_WPI_4.place(x=aux_width_monitor, y=aux_height_monitor*8.05)

checkIN_2_WPI_4 = tkinter.Checkbutton(root, variable=IN_2_WPI_4,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_2_WPI_4.config(font = (Font_1,10))
checkIN_2_WPI_4.place(x=aux_width_monitor*1.25, y=aux_height_monitor*8.05)

checkIN_3_WPI_4 = tkinter.Checkbutton(root, variable=IN_3_WPI_4,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_3_WPI_4.config(font = (Font_1,10))
checkIN_3_WPI_4.place(x=aux_width_monitor*1.5, y=aux_height_monitor*8.05)

checkIN_4_WPI_4 = tkinter.Checkbutton(root, variable=IN_4_WPI_4,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_4_WPI_4.config(font = (Font_1,10))
checkIN_4_WPI_4.place(x=aux_width_monitor*1.75, y=aux_height_monitor*8.05)

checkIN_5_WPI_4 = tkinter.Checkbutton(root, variable=IN_5_WPI_4,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_5_WPI_4.config(font = (Font_1,10))
checkIN_5_WPI_4.place(x=aux_width_monitor*2, y=aux_height_monitor*8.05)

checkIN_6_WPI_4 = tkinter.Checkbutton(root, variable=IN_6_WPI_4,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_6_WPI_4.config(font = (Font_1,10))
checkIN_6_WPI_4.place(x=aux_width_monitor*2.25, y=aux_height_monitor*8.05)

checkIN_7_WPI_4 = tkinter.Checkbutton(root, variable=IN_7_WPI_4,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_7_WPI_4.config(font = (Font_1,10))
checkIN_7_WPI_4.place(x=aux_width_monitor*2.5, y=aux_height_monitor*8.05)

checkIN_8_WPI_4 = tkinter.Checkbutton(root, variable=IN_8_WPI_4,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_8_WPI_4.config(font = (Font_1,10))
checkIN_8_WPI_4.place(x=aux_width_monitor*2.75, y=aux_height_monitor*8.05)

checkIN_9_WPI_4 = tkinter.Checkbutton(root, variable=IN_9_WPI_4,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_9_WPI_4.config(font = (Font_1,10))
checkIN_9_WPI_4.place(x=aux_width_monitor*3, y=aux_height_monitor*8.05)

checkIN_10_WPI_4 = tkinter.Checkbutton(root, variable=IN_10_WPI_4,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_10_WPI_4.config(font = (Font_1,10))
checkIN_10_WPI_4.place(x=aux_width_monitor*3.25, y=aux_height_monitor*8.05)

checkIN_11_WPI_4 = tkinter.Checkbutton(root, variable=IN_11_WPI_4,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_11_WPI_4.config(font = (Font_1,10))
checkIN_11_WPI_4.place(x=aux_width_monitor*3.5, y=aux_height_monitor*8.05)

checkIN_12_WPI_4 = tkinter.Checkbutton(root, variable=IN_12_WPI_4,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_12_WPI_4.config(font = (Font_1,10))
checkIN_12_WPI_4.place(x=aux_width_monitor*3.75, y=aux_height_monitor*8.05)


#%%------------INPUTS CHECKBUTTONS WPI-5--------------------------------------------
checkIN_1_WPI_5 = tkinter.Checkbutton(root, variable=IN_1_WPI_5,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_1_WPI_5.config(font = (Font_1,10))
checkIN_1_WPI_5.place(x=aux_width_monitor, y=aux_height_monitor*10.05)

checkIN_2_WPI_5 = tkinter.Checkbutton(root, variable=IN_2_WPI_5,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_2_WPI_5.config(font = (Font_1,10))
checkIN_2_WPI_5.place(x=aux_width_monitor*1.25, y=aux_height_monitor*10.05)

checkIN_3_WPI_5 = tkinter.Checkbutton(root, variable=IN_3_WPI_5,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_3_WPI_5.config(font = (Font_1,10))
checkIN_3_WPI_5.place(x=aux_width_monitor*1.5, y=aux_height_monitor*10.05)

checkIN_4_WPI_5 = tkinter.Checkbutton(root, variable=IN_4_WPI_5,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_4_WPI_5.config(font = (Font_1,10))
checkIN_4_WPI_5.place(x=aux_width_monitor*1.75, y=aux_height_monitor*10.05)

checkIN_5_WPI_5 = tkinter.Checkbutton(root, variable=IN_5_WPI_5,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_5_WPI_5.config(font = (Font_1,10))
checkIN_5_WPI_5.place(x=aux_width_monitor*2, y=aux_height_monitor*10.05)

checkIN_6_WPI_5 = tkinter.Checkbutton(root, variable=IN_6_WPI_5,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_6_WPI_5.config(font = (Font_1,10))
checkIN_6_WPI_5.place(x=aux_width_monitor*2.25, y=aux_height_monitor*10.05)

checkIN_7_WPI_5 = tkinter.Checkbutton(root, variable=IN_7_WPI_5,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_7_WPI_5.config(font = (Font_1,10))
checkIN_7_WPI_5.place(x=aux_width_monitor*2.5, y=aux_height_monitor*10.05)

checkIN_8_WPI_5 = tkinter.Checkbutton(root, variable=IN_8_WPI_5,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_8_WPI_5.config(font = (Font_1,10))
checkIN_8_WPI_5.place(x=aux_width_monitor*2.75, y=aux_height_monitor*10.05)

checkIN_9_WPI_5 = tkinter.Checkbutton(root, variable=IN_9_WPI_5,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_9_WPI_5.config(font = (Font_1,10))
checkIN_9_WPI_5.place(x=aux_width_monitor*3, y=aux_height_monitor*10.05)

checkIN_10_WPI_5 = tkinter.Checkbutton(root, variable=IN_10_WPI_5,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_10_WPI_5.config(font = (Font_1,10))
checkIN_10_WPI_5.place(x=aux_width_monitor*3.25, y=aux_height_monitor*10.05)

checkIN_11_WPI_5 = tkinter.Checkbutton(root, variable=IN_11_WPI_5,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_11_WPI_5.config(font = (Font_1,10))
checkIN_11_WPI_5.place(x=aux_width_monitor*3.5, y=aux_height_monitor*10.05)

checkIN_12_WPI_5 = tkinter.Checkbutton(root, variable=IN_12_WPI_5,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_12_WPI_5.config(font = (Font_1,10))
checkIN_12_WPI_5.place(x=aux_width_monitor*3.75, y=aux_height_monitor*10.05)


#%%------------INPUTS CHECKBUTTONS WPI-6--------------------------------------------
checkIN_1_WPI_6 = tkinter.Checkbutton(root, variable=IN_1_WPI_6,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_1_WPI_6.config(font = (Font_1,10))
checkIN_1_WPI_6.place(x=aux_width_monitor, y=aux_height_monitor*12.05)

checkIN_2_WPI_6 = tkinter.Checkbutton(root, variable=IN_2_WPI_6,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_2_WPI_6.config(font = (Font_1,10))
checkIN_2_WPI_6.place(x=aux_width_monitor*1.25, y=aux_height_monitor*12.05)

checkIN_3_WPI_6 = tkinter.Checkbutton(root, variable=IN_3_WPI_6,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_3_WPI_6.config(font = (Font_1,10))
checkIN_3_WPI_6.place(x=aux_width_monitor*1.5, y=aux_height_monitor*12.05)

checkIN_4_WPI_6 = tkinter.Checkbutton(root, variable=IN_4_WPI_6,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_4_WPI_6.config(font = (Font_1,10))
checkIN_4_WPI_6.place(x=aux_width_monitor*1.75, y=aux_height_monitor*12.05)

checkIN_5_WPI_6 = tkinter.Checkbutton(root, variable=IN_5_WPI_6,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_5_WPI_6.config(font = (Font_1,10))
checkIN_5_WPI_6.place(x=aux_width_monitor*2, y=aux_height_monitor*12.05)

checkIN_6_WPI_6 = tkinter.Checkbutton(root, variable=IN_6_WPI_6,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_6_WPI_6.config(font = (Font_1,10))
checkIN_6_WPI_6.place(x=aux_width_monitor*2.25, y=aux_height_monitor*12.05)

checkIN_7_WPI_6 = tkinter.Checkbutton(root, variable=IN_7_WPI_6,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_7_WPI_6.config(font = (Font_1,10))
checkIN_7_WPI_6.place(x=aux_width_monitor*2.5, y=aux_height_monitor*12.05)

checkIN_8_WPI_6 = tkinter.Checkbutton(root, variable=IN_8_WPI_6,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_8_WPI_6.config(font = (Font_1,10))
checkIN_8_WPI_6.place(x=aux_width_monitor*2.75, y=aux_height_monitor*12.05)

checkIN_9_WPI_6 = tkinter.Checkbutton(root, variable=IN_9_WPI_6,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_9_WPI_6.config(font = (Font_1,10))
checkIN_9_WPI_6.place(x=aux_width_monitor*3, y=aux_height_monitor*12.05)

checkIN_10_WPI_6 = tkinter.Checkbutton(root, variable=IN_10_WPI_6,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_10_WPI_6.config(font = (Font_1,10))
checkIN_10_WPI_6.place(x=aux_width_monitor*3.25, y=aux_height_monitor*12.05)

checkIN_11_WPI_6 = tkinter.Checkbutton(root, variable=IN_11_WPI_6,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_11_WPI_6.config(font = (Font_1,10))
checkIN_11_WPI_6.place(x=aux_width_monitor*3.5, y=aux_height_monitor*12.05)

checkIN_12_WPI_6 = tkinter.Checkbutton(root, variable=IN_12_WPI_6,
                            bd=0, bg = Fun_Rgb(C_Pal3), 
                            activebackground=Fun_Rgb(C_Pal8),
                            highlightbackground=Fun_Rgb(C_Pal3))
checkIN_12_WPI_6.config(font = (Font_1,10))
checkIN_12_WPI_6.place(x=aux_width_monitor*3.75, y=aux_height_monitor*12.05)


#%%------------LABELS FOR COMS PORTS-------------------------------------------
Lbl= Label(root, bg = Fun_Rgb(C_Pal3),text = "WPI-1", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl.config(font = (Font_1,20))
Lbl.place(x=aux_width_monitor/2,y=aux_height_monitor*.5)

Lbl= Label(root, bg = Fun_Rgb(C_Pal3),text = "WPI-2", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl.config(font = (Font_1,20))
Lbl.place(x=aux_width_monitor/2,y=aux_height_monitor*2.5)

Lbl= Label(root, bg = Fun_Rgb(C_Pal3),text = "WPI-3", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl.config(font = (Font_1,20))
Lbl.place(x=aux_width_monitor/2,y=aux_height_monitor*4.5)

Lbl= Label(root, bg = Fun_Rgb(C_Pal3),text = "WPI-4", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl.config(font = (Font_1,20))
Lbl.place(x=aux_width_monitor/2,y=aux_height_monitor*6.5)

Lbl= Label(root, bg = Fun_Rgb(C_Pal3),text = "WPI-5", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl.config(font = (Font_1,20))
Lbl.place(x=aux_width_monitor/2,y=aux_height_monitor*8.5)

Lbl= Label(root, bg = Fun_Rgb(C_Pal3),text = "WPI-6", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl.config(font = (Font_1,20))
Lbl.place(x=aux_width_monitor/2,y=aux_height_monitor*10.5)


#%%------------LABELS FOR OUTPUTS----------------------------------------------
Lbl_OUT_WPI_1= Label(root, bg = Fun_Rgb(C_Pal3),text = "Out", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_OUT_WPI_1.config(font = (Font_1,14))
Lbl_OUT_WPI_1.place(x=aux_width_monitor/2,y=aux_height_monitor*1.5)

Lbl_OUT_WPI_2= Label(root, bg = Fun_Rgb(C_Pal3),text = "Out", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_OUT_WPI_2.config(font = (Font_1,14))
Lbl_OUT_WPI_2.place(x=aux_width_monitor/2,y=aux_height_monitor*3.5)

Lbl_OUT_WPI_3= Label(root, bg = Fun_Rgb(C_Pal3),text = "Out", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_OUT_WPI_3.config(font = (Font_1,14))
Lbl_OUT_WPI_3.place(x=aux_width_monitor/2,y=aux_height_monitor*5.5)

Lbl_OUT_WPI_4= Label(root, bg = Fun_Rgb(C_Pal3),text = "Out", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_OUT_WPI_4.config(font = (Font_1,14))
Lbl_OUT_WPI_4.place(x=aux_width_monitor/2,y=aux_height_monitor*7.5)

Lbl_OUT_WPI_5= Label(root, bg = Fun_Rgb(C_Pal3),text = "Out", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_OUT_WPI_5.config(font = (Font_1,14))
Lbl_OUT_WPI_5.place(x=aux_width_monitor/2,y=aux_height_monitor*9.5)

Lbl_OUT_WPI_6= Label(root, bg = Fun_Rgb(C_Pal3),text = "Out", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_OUT_WPI_6.config(font = (Font_1,14))
Lbl_OUT_WPI_6.place(x=aux_width_monitor/2,y=aux_height_monitor*11.5)


#%%------------LABELS FOR INPUTS-----------------------------------------------
Lbl_OUT_WPI_1= Label(root, bg = Fun_Rgb(C_Pal3),text = "In", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_OUT_WPI_1.config(font = (Font_1,14))
Lbl_OUT_WPI_1.place(x=aux_width_monitor/2,y=aux_height_monitor*2)

Lbl_OUT_WPI_2= Label(root, bg = Fun_Rgb(C_Pal3),text = "In", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_OUT_WPI_2.config(font = (Font_1,14))
Lbl_OUT_WPI_2.place(x=aux_width_monitor/2,y=aux_height_monitor*4)

Lbl_OUT_WPI_3= Label(root, bg = Fun_Rgb(C_Pal3),text = "In", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_OUT_WPI_3.config(font = (Font_1,14))
Lbl_OUT_WPI_3.place(x=aux_width_monitor/2,y=aux_height_monitor*6)

Lbl_OUT_WPI_4= Label(root, bg = Fun_Rgb(C_Pal3),text = "In", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_OUT_WPI_4.config(font = (Font_1,14))
Lbl_OUT_WPI_4.place(x=aux_width_monitor/2,y=aux_height_monitor*8)

Lbl_OUT_WPI_5= Label(root, bg = Fun_Rgb(C_Pal3),text = "In", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_OUT_WPI_5.config(font = (Font_1,14))
Lbl_OUT_WPI_5.place(x=aux_width_monitor/2,y=aux_height_monitor*10)

Lbl_OUT_WPI_6= Label(root, bg = Fun_Rgb(C_Pal3),text = "In", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_OUT_WPI_6.config(font = (Font_1,14))
Lbl_OUT_WPI_6.place(x=aux_width_monitor/2,y=aux_height_monitor*12)




#%%------------LABELS FOR USB LETTERS WPI-1------------------------------------
Lbl_AB_WPI_1= Label(root, bg = Fun_Rgb(C_Pal3),text = "AB", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_AB_WPI_1.config(font = (Font_1,11))
Lbl_AB_WPI_1.place(x=aux_width_monitor,y=aux_height_monitor*1.2)

Lbl_CD_WPI_1= Label(root, bg = Fun_Rgb(C_Pal3),text = "CD", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_CD_WPI_1.config(font = (Font_1,11))
Lbl_CD_WPI_1.place(x=aux_width_monitor*1.25,y=aux_height_monitor*1.2)

Lbl_EF_WPI_1= Label(root, bg = Fun_Rgb(C_Pal3),text = "EF", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_EF_WPI_1.config(font = (Font_1,11))
Lbl_EF_WPI_1.place(x=aux_width_monitor*1.5,y=aux_height_monitor*1.2)

Lbl_GH_WPI_1= Label(root, bg = Fun_Rgb(C_Pal3),text = "GH", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_GH_WPI_1.config(font = (Font_1,11))
Lbl_GH_WPI_1.place(x=aux_width_monitor*1.75,y=aux_height_monitor*1.2)

Lbl_IJ_WPI_1= Label(root, bg = Fun_Rgb(C_Pal3),text = "IJ", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_IJ_WPI_1.config(font = (Font_1,11))
Lbl_IJ_WPI_1.place(x=aux_width_monitor*2,y=aux_height_monitor*1.2)

Lbl_KL_WPI_1= Label(root, bg = Fun_Rgb(C_Pal3),text = "KL", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_KL_WPI_1.config(font = (Font_1,11))
Lbl_KL_WPI_1.place(x=aux_width_monitor*2.25,y=aux_height_monitor*1.2)

Lbl_MN_WPI_1= Label(root, bg = Fun_Rgb(C_Pal3),text = "MN", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_MN_WPI_1.config(font = (Font_1,11))
Lbl_MN_WPI_1.place(x=aux_width_monitor*2.5,y=aux_height_monitor*1.2)

Lbl_OP_WPI_1= Label(root, bg = Fun_Rgb(C_Pal3),text = "OP", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_OP_WPI_1.config(font = (Font_1,11))
Lbl_OP_WPI_1.place(x=aux_width_monitor*2.75,y=aux_height_monitor*1.2)

Lbl_QR_WPI_1= Label(root, bg = Fun_Rgb(C_Pal3),text = "QR", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_QR_WPI_1.config(font = (Font_1,11))
Lbl_QR_WPI_1.place(x=aux_width_monitor*3,y=aux_height_monitor*1.2)

Lbl_ST_WPI_1= Label(root, bg = Fun_Rgb(C_Pal3),text = "ST", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_ST_WPI_1.config(font = (Font_1,11))
Lbl_ST_WPI_1.place(x=aux_width_monitor*3.25,y=aux_height_monitor*1.2)

Lbl_UV_WPI_1= Label(root, bg = Fun_Rgb(C_Pal3),text = "UV", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_UV_WPI_1.config(font = (Font_1,11))
Lbl_UV_WPI_1.place(x=aux_width_monitor*3.5,y=aux_height_monitor*1.2)

Lbl_WX_WPI_1= Label(root, bg = Fun_Rgb(C_Pal3),text = "WX", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_WX_WPI_1.config(font = (Font_1,11))
Lbl_WX_WPI_1.place(x=aux_width_monitor*3.75,y=aux_height_monitor*1.2)




#%%------------LABELS FOR USB LETTERS WPI-2------------------------------------
Lbl_AB_WPI_2= Label(root, bg = Fun_Rgb(C_Pal3),text = "AB", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_AB_WPI_2.config(font = (Font_1,11))
Lbl_AB_WPI_2.place(x=aux_width_monitor,y=aux_height_monitor*3.2)

Lbl_CD_WPI_2= Label(root, bg = Fun_Rgb(C_Pal3),text = "CD", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_CD_WPI_2.config(font = (Font_1,11))
Lbl_CD_WPI_2.place(x=aux_width_monitor*1.25,y=aux_height_monitor*3.2)

Lbl_EF_WPI_2= Label(root, bg = Fun_Rgb(C_Pal3),text = "EF", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_EF_WPI_2.config(font = (Font_1,11))
Lbl_EF_WPI_2.place(x=aux_width_monitor*1.5,y=aux_height_monitor*3.2)

Lbl_GH_WPI_2= Label(root, bg = Fun_Rgb(C_Pal3),text = "GH", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_GH_WPI_2.config(font = (Font_1,11))
Lbl_GH_WPI_2.place(x=aux_width_monitor*1.75,y=aux_height_monitor*3.2)

Lbl_IJ_WPI_2= Label(root, bg = Fun_Rgb(C_Pal3),text = "IJ", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_IJ_WPI_2.config(font = (Font_1,11))
Lbl_IJ_WPI_2.place(x=aux_width_monitor*2,y=aux_height_monitor*3.2)

Lbl_KL_WPI_2= Label(root, bg = Fun_Rgb(C_Pal3),text = "KL", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_KL_WPI_2.config(font = (Font_1,11))
Lbl_KL_WPI_2.place(x=aux_width_monitor*2.25,y=aux_height_monitor*3.2)

Lbl_MN_WPI_2= Label(root, bg = Fun_Rgb(C_Pal3),text = "MN", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_MN_WPI_2.config(font = (Font_1,11))
Lbl_MN_WPI_2.place(x=aux_width_monitor*2.5,y=aux_height_monitor*3.2)

Lbl_OP_WPI_2= Label(root, bg = Fun_Rgb(C_Pal3),text = "OP", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_OP_WPI_2.config(font = (Font_1,11))
Lbl_OP_WPI_2.place(x=aux_width_monitor*2.75,y=aux_height_monitor*3.2)

Lbl_QR_WPI_2= Label(root, bg = Fun_Rgb(C_Pal3),text = "QR", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_QR_WPI_2.config(font = (Font_1,11))
Lbl_QR_WPI_2.place(x=aux_width_monitor*3,y=aux_height_monitor*3.2)

Lbl_ST_WPI_2= Label(root, bg = Fun_Rgb(C_Pal3),text = "ST", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_ST_WPI_2.config(font = (Font_1,11))
Lbl_ST_WPI_2.place(x=aux_width_monitor*3.25,y=aux_height_monitor*3.2)

Lbl_UV_WPI_2= Label(root, bg = Fun_Rgb(C_Pal3),text = "UV", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_UV_WPI_2.config(font = (Font_1,11))
Lbl_UV_WPI_2.place(x=aux_width_monitor*3.5,y=aux_height_monitor*3.2)

Lbl_WX_WPI_2= Label(root, bg = Fun_Rgb(C_Pal3),text = "WX", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_WX_WPI_2.config(font = (Font_1,11))
Lbl_WX_WPI_2.place(x=aux_width_monitor*3.75,y=aux_height_monitor*3.2)



#%%------------LABELS FOR USB LETTERS WPI-3------------------------------------
Lbl_AB_WPI_3= Label(root, bg = Fun_Rgb(C_Pal3),text = "AB", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_AB_WPI_3.config(font = (Font_1,11))
Lbl_AB_WPI_3.place(x=aux_width_monitor,y=aux_height_monitor*5.2)

Lbl_CD_WPI_3= Label(root, bg = Fun_Rgb(C_Pal3),text = "CD", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_CD_WPI_3.config(font = (Font_1,11))
Lbl_CD_WPI_3.place(x=aux_width_monitor*1.25,y=aux_height_monitor*5.2)

Lbl_EF_WPI_3= Label(root, bg = Fun_Rgb(C_Pal3),text = "EF", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_EF_WPI_3.config(font = (Font_1,11))
Lbl_EF_WPI_3.place(x=aux_width_monitor*1.5,y=aux_height_monitor*5.2)

Lbl_GH_WPI_3= Label(root, bg = Fun_Rgb(C_Pal3),text = "GH", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_GH_WPI_3.config(font = (Font_1,11))
Lbl_GH_WPI_3.place(x=aux_width_monitor*1.75,y=aux_height_monitor*5.2)

Lbl_IJ_WPI_3= Label(root, bg = Fun_Rgb(C_Pal3),text = "IJ", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_IJ_WPI_3.config(font = (Font_1,11))
Lbl_IJ_WPI_3.place(x=aux_width_monitor*2,y=aux_height_monitor*5.2)

Lbl_KL_WPI_3= Label(root, bg = Fun_Rgb(C_Pal3),text = "KL", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_KL_WPI_3.config(font = (Font_1,11))
Lbl_KL_WPI_3.place(x=aux_width_monitor*2.25,y=aux_height_monitor*5.2)

Lbl_MN_WPI_3= Label(root, bg = Fun_Rgb(C_Pal3),text = "MN", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_MN_WPI_3.config(font = (Font_1,11))
Lbl_MN_WPI_3.place(x=aux_width_monitor*2.5,y=aux_height_monitor*5.2)

Lbl_OP_WPI_3= Label(root, bg = Fun_Rgb(C_Pal3),text = "OP", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_OP_WPI_3.config(font = (Font_1,11))
Lbl_OP_WPI_3.place(x=aux_width_monitor*2.75,y=aux_height_monitor*5.2)

Lbl_QR_WPI_3= Label(root, bg = Fun_Rgb(C_Pal3),text = "QR", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_QR_WPI_3.config(font = (Font_1,11))
Lbl_QR_WPI_3.place(x=aux_width_monitor*3,y=aux_height_monitor*5.2)

Lbl_ST_WPI_3= Label(root, bg = Fun_Rgb(C_Pal3),text = "ST", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_ST_WPI_3.config(font = (Font_1,11))
Lbl_ST_WPI_3.place(x=aux_width_monitor*3.25,y=aux_height_monitor*5.2)

Lbl_UV_WPI_3= Label(root, bg = Fun_Rgb(C_Pal3),text = "UV", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_UV_WPI_3.config(font = (Font_1,11))
Lbl_UV_WPI_3.place(x=aux_width_monitor*3.5,y=aux_height_monitor*5.2)

Lbl_WX_WPI_3= Label(root, bg = Fun_Rgb(C_Pal3),text = "WX", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_WX_WPI_3.config(font = (Font_1,11))
Lbl_WX_WPI_3.place(x=aux_width_monitor*3.75,y=aux_height_monitor*5.2)


#%%------------LABELS FOR USB LETTERS WPI-4------------------------------------
Lbl_AB_WPI_4= Label(root, bg = Fun_Rgb(C_Pal3),text = "AB", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_AB_WPI_4.config(font = (Font_1,11))
Lbl_AB_WPI_4.place(x=aux_width_monitor,y=aux_height_monitor*7.2)

Lbl_CD_WPI_4= Label(root, bg = Fun_Rgb(C_Pal3),text = "CD", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_CD_WPI_4.config(font = (Font_1,11))
Lbl_CD_WPI_4.place(x=aux_width_monitor*1.25,y=aux_height_monitor*7.2)

Lbl_EF_WPI_4= Label(root, bg = Fun_Rgb(C_Pal3),text = "EF", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_EF_WPI_4.config(font = (Font_1,11))
Lbl_EF_WPI_4.place(x=aux_width_monitor*1.5,y=aux_height_monitor*7.2)

Lbl_GH_WPI_4= Label(root, bg = Fun_Rgb(C_Pal3),text = "GH", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_GH_WPI_4.config(font = (Font_1,11))
Lbl_GH_WPI_4.place(x=aux_width_monitor*1.75,y=aux_height_monitor*7.2)

Lbl_IJ_WPI_4= Label(root, bg = Fun_Rgb(C_Pal3),text = "IJ", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_IJ_WPI_4.config(font = (Font_1,11))
Lbl_IJ_WPI_4.place(x=aux_width_monitor*2,y=aux_height_monitor*7.2)

Lbl_KL_WPI_4= Label(root, bg = Fun_Rgb(C_Pal3),text = "KL", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_KL_WPI_4.config(font = (Font_1,11))
Lbl_KL_WPI_4.place(x=aux_width_monitor*2.25,y=aux_height_monitor*7.2)

Lbl_MN_WPI_4= Label(root, bg = Fun_Rgb(C_Pal3),text = "MN", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_MN_WPI_4.config(font = (Font_1,11))
Lbl_MN_WPI_4.place(x=aux_width_monitor*2.5,y=aux_height_monitor*7.2)

Lbl_OP_WPI_4= Label(root, bg = Fun_Rgb(C_Pal3),text = "OP", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_OP_WPI_4.config(font = (Font_1,11))
Lbl_OP_WPI_4.place(x=aux_width_monitor*2.75,y=aux_height_monitor*7.2)

Lbl_QR_WPI_4= Label(root, bg = Fun_Rgb(C_Pal3),text = "QR", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_QR_WPI_4.config(font = (Font_1,11))
Lbl_QR_WPI_4.place(x=aux_width_monitor*3,y=aux_height_monitor*7.2)

Lbl_ST_WPI_4= Label(root, bg = Fun_Rgb(C_Pal3),text = "ST", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_ST_WPI_4.config(font = (Font_1,11))
Lbl_ST_WPI_4.place(x=aux_width_monitor*3.25,y=aux_height_monitor*7.2)

Lbl_UV_WPI_4= Label(root, bg = Fun_Rgb(C_Pal3),text = "UV", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_UV_WPI_4.config(font = (Font_1,11))
Lbl_UV_WPI_4.place(x=aux_width_monitor*3.5,y=aux_height_monitor*7.2)

Lbl_WX_WPI_4= Label(root, bg = Fun_Rgb(C_Pal3),text = "WX", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_WX_WPI_4.config(font = (Font_1,11))
Lbl_WX_WPI_4.place(x=aux_width_monitor*3.75,y=aux_height_monitor*7.2)


#%%------------LABELS FOR USB LETTERS WPI-5------------------------------------
Lbl_AB_WPI_5= Label(root, bg = Fun_Rgb(C_Pal3),text = "AB", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_AB_WPI_5.config(font = (Font_1,11))
Lbl_AB_WPI_5.place(x=aux_width_monitor,y=aux_height_monitor*9.2)

Lbl_CD_WPI_5= Label(root, bg = Fun_Rgb(C_Pal3),text = "CD", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_CD_WPI_5.config(font = (Font_1,11))
Lbl_CD_WPI_5.place(x=aux_width_monitor*1.25,y=aux_height_monitor*9.2)

Lbl_EF_WPI_5= Label(root, bg = Fun_Rgb(C_Pal3),text = "EF", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_EF_WPI_5.config(font = (Font_1,11))
Lbl_EF_WPI_5.place(x=aux_width_monitor*1.5,y=aux_height_monitor*9.2)

Lbl_GH_WPI_5= Label(root, bg = Fun_Rgb(C_Pal3),text = "GH", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_GH_WPI_5.config(font = (Font_1,11))
Lbl_GH_WPI_5.place(x=aux_width_monitor*1.75,y=aux_height_monitor*9.2)

Lbl_IJ_WPI_5= Label(root, bg = Fun_Rgb(C_Pal3),text = "IJ", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_IJ_WPI_5.config(font = (Font_1,11))
Lbl_IJ_WPI_5.place(x=aux_width_monitor*2,y=aux_height_monitor*9.2)

Lbl_KL_WPI_5= Label(root, bg = Fun_Rgb(C_Pal3),text = "KL", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_KL_WPI_5.config(font = (Font_1,11))
Lbl_KL_WPI_5.place(x=aux_width_monitor*2.25,y=aux_height_monitor*9.2)

Lbl_MN_WPI_5= Label(root, bg = Fun_Rgb(C_Pal3),text = "MN", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_MN_WPI_5.config(font = (Font_1,11))
Lbl_MN_WPI_5.place(x=aux_width_monitor*2.5,y=aux_height_monitor*9.2)

Lbl_OP_WPI_5= Label(root, bg = Fun_Rgb(C_Pal3),text = "OP", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_OP_WPI_5.config(font = (Font_1,11))
Lbl_OP_WPI_5.place(x=aux_width_monitor*2.75,y=aux_height_monitor*9.2)

Lbl_QR_WPI_5= Label(root, bg = Fun_Rgb(C_Pal3),text = "QR", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_QR_WPI_5.config(font = (Font_1,11))
Lbl_QR_WPI_5.place(x=aux_width_monitor*3,y=aux_height_monitor*9.2)

Lbl_ST_WPI_5= Label(root, bg = Fun_Rgb(C_Pal3),text = "ST", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_ST_WPI_5.config(font = (Font_1,11))
Lbl_ST_WPI_5.place(x=aux_width_monitor*3.25,y=aux_height_monitor*9.2)

Lbl_UV_WPI_5= Label(root, bg = Fun_Rgb(C_Pal3),text = "UV", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_UV_WPI_5.config(font = (Font_1,11))
Lbl_UV_WPI_5.place(x=aux_width_monitor*3.5,y=aux_height_monitor*9.2)

Lbl_WX_WPI_5= Label(root, bg = Fun_Rgb(C_Pal3),text = "WX", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_WX_WPI_5.config(font = (Font_1,11))
Lbl_WX_WPI_5.place(x=aux_width_monitor*3.75,y=aux_height_monitor*9.2)


#%%------------LABELS FOR USB LETTERS WPI-6------------------------------------
Lbl_AB_WPI_6= Label(root, bg = Fun_Rgb(C_Pal3),text = "AB", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_AB_WPI_6.config(font = (Font_1,11))
Lbl_AB_WPI_6.place(x=aux_width_monitor,y=aux_height_monitor*11.2)

Lbl_CD_WPI_6= Label(root, bg = Fun_Rgb(C_Pal3),text = "CD", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_CD_WPI_6.config(font = (Font_1,11))
Lbl_CD_WPI_6.place(x=aux_width_monitor*1.25,y=aux_height_monitor*11.2)

Lbl_EF_WPI_6= Label(root, bg = Fun_Rgb(C_Pal3),text = "EF", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_EF_WPI_6.config(font = (Font_1,11))
Lbl_EF_WPI_6.place(x=aux_width_monitor*1.5,y=aux_height_monitor*11.2)

Lbl_GH_WPI_6= Label(root, bg = Fun_Rgb(C_Pal3),text = "GH", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_GH_WPI_6.config(font = (Font_1,11))
Lbl_GH_WPI_6.place(x=aux_width_monitor*1.75,y=aux_height_monitor*11.2)

Lbl_IJ_WPI_6= Label(root, bg = Fun_Rgb(C_Pal3),text = "IJ", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_IJ_WPI_6.config(font = (Font_1,11))
Lbl_IJ_WPI_6.place(x=aux_width_monitor*2,y=aux_height_monitor*11.2)

Lbl_KL_WPI_6= Label(root, bg = Fun_Rgb(C_Pal3),text = "KL", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_KL_WPI_6.config(font = (Font_1,11))
Lbl_KL_WPI_6.place(x=aux_width_monitor*2.25,y=aux_height_monitor*11.2)

Lbl_MN_WPI_6= Label(root, bg = Fun_Rgb(C_Pal3),text = "MN", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_MN_WPI_6.config(font = (Font_1,11))
Lbl_MN_WPI_6.place(x=aux_width_monitor*2.5,y=aux_height_monitor*11.2)

Lbl_OP_WPI_6= Label(root, bg = Fun_Rgb(C_Pal3),text = "OP", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_OP_WPI_6.config(font = (Font_1,11))
Lbl_OP_WPI_6.place(x=aux_width_monitor*2.75,y=aux_height_monitor*11.2)

Lbl_QR_WPI_6= Label(root, bg = Fun_Rgb(C_Pal3),text = "QR", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_QR_WPI_6.config(font = (Font_1,11))
Lbl_QR_WPI_6.place(x=aux_width_monitor*3,y=aux_height_monitor*11.2)

Lbl_ST_WPI_6= Label(root, bg = Fun_Rgb(C_Pal3),text = "ST", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_ST_WPI_6.config(font = (Font_1,11))
Lbl_ST_WPI_6.place(x=aux_width_monitor*3.25,y=aux_height_monitor*11.2)

Lbl_UV_WPI_6= Label(root, bg = Fun_Rgb(C_Pal3),text = "UV", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_UV_WPI_6.config(font = (Font_1,11))
Lbl_UV_WPI_6.place(x=aux_width_monitor*3.5,y=aux_height_monitor*11.2)

Lbl_WX_WPI_6= Label(root, bg = Fun_Rgb(C_Pal3),text = "WX", fg = Fun_Rgb(C_Pal5), 
           activebackground=Fun_Rgb(C_Pal8))
Lbl_WX_WPI_6.config(font = (Font_1,11))
Lbl_WX_WPI_6.place(x=aux_width_monitor*3.75,y=aux_height_monitor*11.2)


 
# Set up a Text box and scroll bar.
scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)
 
text = Text(root)
text.place(x=aux_width_monitor*8,y=aux_height_monitor/2)

text.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=text.yview)
 

root.mainloop()