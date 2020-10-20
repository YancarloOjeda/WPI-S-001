"""
Walden Modular Equipment SAS
WPI_While_Output
2020
"""


import Walden as w

#Devices
WPI = w.Get_WPI_12('COM7')

#Variables
NumberOutput = 10

#Control
CounterOutput = 1

#Program
while(CounterOutput <= NumberOutput):
    w.WPI_Out(WPI,'WX','On')
    w.Pause_Time(.5)
    w.WPI_Out(WPI,'WX','Off')
    w.Pause_Time(.5)
    
    print(CounterOutput)
    #Count the number of times that output has been turned on / off
    CounterOutput = CounterOutput + 1


w.Stop_WPI(WPI)