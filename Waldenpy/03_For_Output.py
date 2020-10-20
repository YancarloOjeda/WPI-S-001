"""
Walden Modular Equipment SAS
WPI_For_Output
2020
"""


import Walden as w

#Devices
WPI = w.Get_WPI_12('COM7')

#Variables
NumberIteration = 10

#Program
for i in range(0, NumberIteration):
    w.WPI_Out(WPI,'WX','On')
    w.Pause_Time(.5)
    w.WPI_Out(WPI,'WX','Off')
    w.Pause_Time(.5)
w.Stop_WPI(WPI)