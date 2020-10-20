"""
Walden Modular Equipment SAS
FR Plot
2020
"""

import Walden as w

#Devices
WPI = w.Get_WPI_12('COM7')

#Variables
SesionTime = 10
FR = 3

#Control
CounterTime = 0
TempResponse = 0
CounterTimeRef = 0
CounterFR = 0
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
        CounterFR = CounterFR + 1
        CounterResponse = CounterResponse + 1
        
    if (CounterFR == FR):
        CounterFR = 0
        ControlRef = 1
        CounterTimeRef = 0;
        CounterRef = CounterRef + 1
        
    if (ControlRef == 1):
        ControlRef = w.WPI_Out_Time(WPI,'WX', 1.5, CounterTimeRef, ControlRef)

    Events = str(CounterResponse) + ',' + str(CounterRef) 
    Data = w.WaldenData(Data,NumberData,CounterTime,Events,1)
    NumberData = NumberData + 1

    CounterTime = w.Timer(CounterTime,TempTime,.05)
    CounterTimeRef = w.ETimer(CounterTimeRef,TempTime)
    TempTime = w.Get_Time()
    
w.Stop_Abort_WPI(WPI)

#Use SimplePlot(Data,Colum1,Colum2) to view the data, enter the data and columns you want to see
w.SimplePlot(Data,1,2)


