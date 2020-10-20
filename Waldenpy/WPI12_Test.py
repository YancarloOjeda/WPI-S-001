"""
Walden Modular Equipment SAS
WPI12_Test
2020
"""
#import walden as w
#NOTE: before each function we must use the w
import Walden as w

#Check on which COM port WPI is connected
#w.Check_Connected_WPI()

#Establish communication with WPI and WPI name
#NOTE: you must include the COM port where the WPI is connected
WPI = w.Get_WPI_12('COM7')

#Output list
Out_List = ['AB', 'CD', 'EF', 'GH', 'IJ', 'KL', 'MN', 'OP', 'QR', 'ST', 'UV', 'WX'] 

#Output list iteration
print('-------On---------')
for i in Out_List: 
    #Print on Console
    print(i, 'On')
    #Output control - WPI_Out(WPI name, Output name, On/Off)
    w.WPI_Out(WPI,i,'On')
    #Delay time - Pause_Time(Seconds)
    w.Pause_Time(.5)
    
#Output list iteration
print('-------Off---------')
for i in Out_List: 
    #Print on Console
    print(i, 'Off')
    #Output control - WPI_Out(WPI name, Output name, On/Off)
    w.WPI_Out(WPI,i,'Off')
    #Delay time - Pause_Time(Seconds)
    w.Pause_Time(.5)
    
#In list
In_List = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'] 
#Input list iteration
print('-------Read---------')
for i in In_List: 
    #Output control - WPI_Out(WPI name, Output name, On/Off)
    Response = w.WPI_AIn(WPI,i)
    #Print on Console
    print(i, str(Response))
    #Delay time - Pause_Time(Seconds)
    w.Pause_Time(.5)

#Stop WPI communication WPI
w.Stop_WPI(WPI)