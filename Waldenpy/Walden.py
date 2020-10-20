"""
Walden Modular Equipment SAS
Walden-01.1
2020
"""

import serial
import serial.tools.list_ports
import pyfirmata
import time
import cv2
import tkinter
import random 
from tkinter import  filedialog
import matplotlib.pyplot as plt
import os

global Font_CV, Key
Font_CV = cv2.FONT_HERSHEY_SIMPLEX
Key = 0

Dir_Data = 'C:/'

Out_List = ['AB', 'CD', 'EF', 'GH', 'IJ', 'KL', 'MN', 'OP', 'QR', 'ST', 'UV', 'WX'] 
#TreshLow = .80
#TreshUp = .96
#LTreshLow = .01
#LTreshUp = .15
UpTime = 1

##WPI
#def Check_Connected_WPI():
#    Serial_Port = list(serial.tools.list_ports.comports())
#    print('-------Serial Port---------\n')
#    for i in range(0,len(Serial_Port)):
#            print(Serial_Port[i].description)
#    print('\n---------------------------')
#    
#def Get_WPI(COM): 
#    print('\n')
#    Serial = serial.Serial(COM, baudrate=9600, timeout=1.0)
#    for i in range(0,9): 
#        print('.',end = " ")
#        Pause_Time(.1)
#    print('WPI Ready')
#    return Serial
#    
#def Stop_WPI(WPI):
#    WPI.close()
#    print('WPI Stop')
#    
#def WPI_Out(WPI,Out):
#    WPI.flush()
#    WPI.write(Out.encode())
#    
#def WPI_In2(WPI,In):
#    WPI.flush()
#    Out = 'X'
#    WPI.write(Out.encode())
#    Temp = WPI.readline()
#    return Temp.decode("utf-8")[int(In)-1]

#WPI
def Check_Connected_WPI():
    Serial_Port = list(serial.tools.list_ports.comports())
    print('-------Serial Port---------\n')
    for i in range(0,len(Serial_Port)):
            print(Serial_Port[i].description)
    print('\n---------------------------')
    
def Get_WPI_12(COM): 
    Serial = pyfirmata.ArduinoMega(COM)
    for i in range(0,9): 
        print('.',end = " ")
        Pause_Time(.05)
    it = pyfirmata.util.Iterator(Serial)
    it.start()
    print('WPI Ready\n')
    return Serial
    
def Stop_WPI(WPI):
    WPI.exit()
    print('\nWPI Stop')
    
def Stop_Abort_WPI(WPI):
    for i in range(0,13):
        WPI.digital[i+2].write(0)
    WPI.exit()
    print('\nWPI Stop')

def WPI_Out(WPI,Out,State):
    try:
        if (State == 'On') | (State == 'on') | (State == 'ON') :
            State = 1
        elif (State == 'Off') | (State == 'off') | (State == 'OFF'):
            State = 0
        WPI.digital[Out_List.index(Out)+2].write(State)
    except:
        pass
    
def WPI_Out_Time(WPI,Out, Time, TimeCounter, Control):
    try:
        if (Control == 1):
            if (TimeCounter == 0):
                WPI.digital[Out_List.index(Out)+2].write(1)
            elif (TimeCounter >= Time) & (TimeCounter < (Time + UpTime)):
                WPI.digital[Out_List.index(Out)+2].write(0)
                Control = 0
        return Control
    except:
        pass

def WPI_AIn(WPI,In):
    In = int(In)-1
    WPI.analog[In].enable_reporting()
    Pause_Time(.015)
    try:
        State = round(round(WPI.analog[In].read(),3)*100,1)
    except:
        State = 0 
    return State

TreshLow = 80
TreshUp = 99.9
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

LTreshLow = 8
LTreshUp = 10
def WPI_LIn(WPI,In):
    In = int(In)-1
    WPI.analog[In].enable_reporting()
    Pause_Time(.015)
    try:
        Temp = round(round(WPI.analog[In].read(),3)*100,1)
        if (Temp >= LTreshLow) & (Temp < LTreshUp):
            State = 1
        elif Temp == 100:
            State = 0    
        else:
            State = 0
    except:
        State = 0        
    return State

def Discrete_In(TempResponse, Response):
    try:
        if (Response == 1) & (TempResponse == 0):
            NewResponse = 1
        else:
            NewResponse = 0
    except:
        NewResponse = 0
    return NewResponse

#Time
def Get_Time():
    return time.time()

def Timer(Time,TempTime,Seconds):
    if Time == 0:
        time.sleep(Seconds)
        Time = Seconds
    else:
        time.sleep(Seconds)
        Time = Time + (time.time() - TempTime)
    Time = round(Time,4)
    return Time  

def Event_Timer(Time,TempTime):
    if Time == 0:
        Time = 0.0001
    else:
        Time = Time + (time.time() - TempTime)
    Time = round(Time,4)
    return Time   

def ETimer(Time,TempTime):
    if Time == 0:
        Time = 0.0001
    else:
        Time = Time + (time.time() - TempTime)
    Time = round(Time,4)
    return Time  

def Pause_Time(Seconds):
    time.sleep(Seconds)
    
#Data
def WaldenData(Data,Number,Time,Events,show):
    Data = (Data + '[' +  str(Number) + ',' + str(round(Time,2)) + ',' + Events + ']')
    if show == 1:
        print(str(Number), str(round(Time,2)), Events)
    return Data

def WaldenData_Export(Data):
    TK = tkinter.Tk()
    File =  filedialog.asksaveasfilename(initialdir = Dir_Data,
                                         title = "Save Data",
                                         filetypes = (("all files","*.*"), ("txt files","*.txt"))) 
    File_Data = open(File + '.txt','w')
    File_Data.write('Walden Modular Equipment SAS\n')
#    File_Data.write(str(datetime.now()))
    File_Data.write('\nNumber,Time,Events\n')
    for i in range(0,len(Data)): 
        if Data[i] == '[':
            a = 0
        elif Data[i] == ']':
            File_Data.write('\n')
        else:
            File_Data.write(Data[i])
    File_Data.close() 
    TK.destroy()
    TK.mainloop() 
    
def SimplePlot(Data,Data1,Data2):
    TempData = Data.split(']')
    NewData = [[0] for i in range(len(TempData)-1)]
    PData1 = [[0] for i in range(len(TempData)-1)]
    PData2 = [[0] for i in range(len(TempData)-1)]
    Row = -1
    for i in range(0,len(TempData)-1): 
        Row += 1
        NewData[Row] = TempData[i].split('[')[1]
    for i in range(0,len(TempData)-1):
        PData1[i] = NewData[i].split(',')[Data1]
        PData2[i] = NewData[i].split(',')[Data2]
    plt.plot(PData1,PData2,'k-')
    plt.ylabel('A')
    plt.xlabel('B')
    plt.show()
    
    
#General
def Stop_Abort_Key():
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print('Stop Abort')
        
def Show_WPI_12(WPI):
    Image = cv2.imread('BG1.png',0)
    cv2.putText(Image,('AB: ' + str(WPI_In(WPI,'1'))),(5,20),Font_CV, .5,(0,0,0),1)
    cv2.imshow('WPI 12',Image)
    cv2.waitKey(0)
    
def install(package):
    installPythonPackage = 'pip install ' + package
    os.system('start cmd /c ' + installPythonPackage)
    
def RandList(List):
    return random.choice(List) 