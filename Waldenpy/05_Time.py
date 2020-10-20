"""
Walden Modular Equipment SAS
Time
2020
"""


import Walden as w

#Variables
SesionTime = 10

#Control
CounterTime = 0

#Program
#Use Get_Time() to start time recording
TempTime = w.Get_Time()

while(CounterTime <= SesionTime):
    
    #Use Timer to calculate the log time - Timer(Counter,Temporal time, rate seconds)
    CounterTime = w.Timer(CounterTime,TempTime,.05)
    
    #Use Get_Time() get current time
    TempTime = w.Get_Time()
    
    print(CounterTime)