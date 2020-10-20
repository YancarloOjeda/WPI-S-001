"""
Walden Modular Equipment SAS
Discrete Response
2020
"""


import Walden as w

#Devices
WPI = w.Get_WPI_12('COM7')

#Variables
SesionTime = 10

#Control
CounterTime = 0
TempResponse = 0

#Program
TempTime = w.Get_Time()
while(CounterTime <= SesionTime):
    
    #Use Discrete_In(TempResponse, Response) to discretize the response
    #-------------------------------------------
    Response = w.WPI_In(WPI,'1')
    NewResponse = w.Discrete_In(TempResponse, Response)
    TempResponse = Response
    #-------------------------------------------
    
    print(Response, NewResponse, round(CounterTime,2))
    
    #Time
    CounterTime = w.Timer(CounterTime,TempTime,.05)
    TempTime = w.Get_Time()
    
w.Stop_WPI(WPI)