"""
Walden Modular Equipment SAS
Input
2020
"""


import Walden as w

#Devices
WPI = w.Get_WPI_12('/dev/ttyACM3')



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