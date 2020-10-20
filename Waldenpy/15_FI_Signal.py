"""
Walden Modular Equipment SAS
WPI12_Output
2020
"""

import Walden as w

#Devices
WPI = w.Get_WPI_12('COM7')

#Variables
SesionTime = 30
FI = 5

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
DataSignal = 0


#Program
TempTime = w.Get_Time()
while(CounterTime <= SesionTime):
    
    Response = w.WPI_In(WPI,'1')
    NewResponse = w.Discrete_In(TempResponse, Response)
    TempResponse = Response
    
    if (NewResponse == 1):
        CounterResponse = CounterResponse + 1

    if (CounterTimeFI >= FI) & (NewResponse == 1):
        ControlRef = 1
        CounterTimeRef = 0
        CounterTimeFI = 0
        CounterRef = CounterRef + 1
        
    if (ControlRef == 1):
        ControlRef = w.WPI_Out_Time(WPI,'CD', 1.5, CounterTimeRef, ControlRef)
    
    #use conditionals to control the signal
    if (CounterTimeFI < FI) & (ControlRef == 0): 
        w.WPI_Out(WPI,'WX', 'On')
        DataSignal = 1
    elif (CounterTimeFI > FI):
        w.WPI_Out(WPI,'WX', 'Off')
        CounterTimeFI = 0
        DataSignal = 0
        
    Events = str(CounterResponse) + ',' + str(CounterRef)  + ',' + str(DataSignal) 
    Data = w.WaldenData(Data,NumberData,CounterTime,Events,1)
    NumberData = NumberData + 1

    CounterTime = w.Timer(CounterTime,TempTime,.05)
    CounterTimeRef = w.ETimer(CounterTimeRef,TempTime)
    #Use a timer to control the signal
    CounterTimeFI = w.ETimer(CounterTimeRef,TempTime)
    TempTime = w.Get_Time()
    
w.Stop_Abort_WPI(WPI)

w.SimplePlot(Data,1,2)

