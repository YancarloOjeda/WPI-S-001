"""
Walden Modular Equipment SAS
FR Data
2020
"""

import Walden as w

#Devices
WPI = w.Get_WPI_12('COM7')

#Variables
SesionTime = 20
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
#Create a variable to save the data
Data = ''
#Create a data counter
NumberData = 1
#Create a variable for the events
Events = ''

#Program
TempTime = w.Get_Time()
while(CounterTime <= SesionTime):
    
    Response = w.WPI_In(WPI,'1')
    NewResponse = w.Discrete_In(TempResponse, Response)
    TempResponse = Response
    
    if (NewResponse == 1):
        CounterFR = CounterFR + 1
        #Response Counter
        CounterResponse = CounterResponse + 1
        
    if (CounterFR == FR):
        CounterFR = 0
        ControlRef = 1
        CounterTimeRef = 0;
        #Outcome Counter
        CounterRef = CounterRef + 1
        
    if (ControlRef == 1):
        ControlRef = w.WPI_Out_Time(WPI,'WX', 1.5, CounterTimeRef, ControlRef)
        
    #Convert variables to string with the str(my variable)
    #Then separate it by commas
    Events = str(CounterResponse) + ',' + str(CounterRef) 
    #Use WaldenData(Data,Number,Time,Events,show) to make a walden compatible database
    #NOTE: show = 1 prints on console
    Data = w.WaldenData(Data,NumberData,CounterTime,Events,1)
    #Data Counter
    NumberData = NumberData + 1
    
    #Time
    CounterTime = w.Timer(CounterTime,TempTime,.05)
    CounterTimeRef = w.ETimer(CounterTimeRef,TempTime)
    TempTime = w.Get_Time()
    
#Use Stop_Abort_WPI(WPI) to turn off all outputs
w.Stop_Abort_WPI(WPI)

#Use WaldenData_Export(Data) to save data in a text file
w.WaldenData_Export(Data)