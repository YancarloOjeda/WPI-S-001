"""
Walden Modular Equipment SAS
VI
2020
"""

import Walden as w

#Devices
WPI = w.Get_WPI_12('COM7')

#Variables
SesionTime = 30
VIList = [5,10,15]
VI = w.RandList(VIList) 

#Control
CounterTime = 0
TempResponse = 0
CounterTimeRef = 0
CounterTimeFI = 0
ControlRef = 0
CounterResponse = 0
CounterRef = 0

#Data
Data = ''
NumberData = 1
Events = ''


#Program
TempTime = w.Get_Time()
while(CounterTime <= SesionTime):
    
    Response = w.WPI_In(WPI,'1')
    NewResponse = w.Discrete_In(TempResponse, Response)
    TempResponse = Response
    
    if (NewResponse == 1):
        CounterResponse = CounterResponse + 1

    if (CounterTimeFI >= FI) & (NewResponse == 1):
        VI = w.RandList(VIList) 
        ControlRef = 1
        CounterTimeRef = 0
        CounterTimeFI = 0
        CounterRef = CounterRef + 1
        
    if (ControlRef == 1):
        ControlRef = w.WPI_Out_Time(WPI,'WX', 1.5, CounterTimeRef, ControlRef)
        
    Events = str(CounterResponse) + ',' + str(CounterRef) 
    Data = w.WaldenData(Data,NumberData,CounterTime,Events,1)
    NumberData = NumberData + 1

    CounterTime = w.Timer(CounterTime,TempTime,.05)
    CounterTimeRef = w.ETimer(CounterTimeRef,TempTime)
    CounterTimeFI = w.ETimer(CounterTimeRef,TempTime)
    TempTime = w.Get_Time()
    
w.Stop_Abort_WPI(WPI)

w.SimplePlot(Data,1,2)

