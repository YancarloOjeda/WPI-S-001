"""
Walden Modular Equipment SAS
FR
2020
"""

import Walden as w

#Devices
WPI = w.Get_WPI_12('COM7')

#Variables
SesionTime = 20
FR = 5

#Control
CounterTime = 0
TempResponse = 0
CounterTimeRef = 0
CounterFR = 0
ControlRef = 0

#Program
TempTime = w.Get_Time()
while(CounterTime <= SesionTime):
    
    Response = w.WPI_In(WPI,'1')
    NewResponse = w.Discrete_In(TempResponse, Response)
    TempResponse = Response
    
    #Use conditionals to count the number of responses
    if (NewResponse == 1):
        CounterFR = CounterFR + 1
        
    #When the responses counter equals the number of programmed responses, 
    #the reinforcement control is activated and the reinforcement timer is reset
    #NOTE: To use WPI_Out_Time it is necessary to reset reinforcement timer
    if (CounterFR == FR):
        CounterFR = 0
        #Reinforcement control
        ControlRef = 1
        #Reset reinforcement timer
        CounterTimeRef = 0;
        
    if (ControlRef == 1):
        #Use WPI_Out_Time(WPI,out name, Time, Time Counter, Control) to activate an output for a certain time
       ControlRef =  w.WPI_Out_Time(WPI,'WX', 1.5, CounterTimeRef, ControlRef)
    
    
    print(NewResponse, CounterFR, CounterTimeRef)
    #Time
    CounterTime = w.Timer(CounterTime,TempTime,.05)
    CounterTimeRef = w.ETimer(CounterTimeRef,TempTime)
    TempTime = w.Get_Time()
    
#Use Stop_Abort_WPI(WPI) to turn off all outputs
w.Stop_Abort_WPI(WPI)