"""
Walden Modular Equipment SAS
WPI_Output
2020
"""

#import walden as w
#NOTE: before each function we must use the w - w.funtion
import Walden as w

#Check on which COM port WPI is connected
#w.Check_Connected_WPI()

#Establish communication with WPI and WPI name
#NOTE: you must include the COM port where the WPI is connected
WPI = w.Get_WPI_12('COM7')


#Output control - WPI_Out(WPI name, Output name, On/Off)
w.WPI_Out(WPI,'WX','On')

#Delay time - Pause_Time(Seconds)
w.Pause_Time(1)

#Output control - WPI_Out(WPI name, Output name, On/Off)
w.WPI_Out(WPI,'WX','Off')

#Stop WPI communication WPI
w.Stop_WPI(WPI)