#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 23:46:46 2020

@author: yan
"""


"""
Walden Modular Equipment SAS
WPI_For_Output
2020
"""

#%%-----------LIBRARIES--------------------------------------------------------
import Walden as w
from tkinter import  Scrollbar, Text, Tk, TOP, X, Y, Frame, RIGHT, INSERT, messagebox
from PIL import Image, ImageTk


#%%-----------CREATE WINDOW------------------------------------
# root = Tk()
# root.title('WPI Program')

# def show_text(icon_msg):
#     text.insert(INSERT, str(icon_msg)+'\n')
 
# # Create the toolbar as a frame
# toolbar = Frame(root, borderwidth=2, bg='slategray4', relief='raised')
 
# # Add the toolbar.
# toolbar.pack(side=TOP, fill=X)
 
# # Set up a Text box and scroll bar.
# scrollbar = Scrollbar(root)
# scrollbar.pack(side=RIGHT, fill=Y)
 
# text = Text(root)
# text.pack()
 
# text.config(yscrollcommand=scrollbar.set)
# scrollbar.config(command=text.yview)


#%%-----------YOUR PROGRAM-----------------------------------------------------
def run_program():
    #Devices
    try:
        WPI = w.Get_WPI_12('/dev/ttyACM0')
            
    except:
        WPI = w.Get_WPI_12('/dev/ttyACM1')
    
    #Variables
    NumberIteration = 1000
    #A
    OUT_12 = 'WX'
    #x
    OUT_11 = 'UV'
    #CTX
    OUT_10 = 'ST'
    #EI
    OUT_9 = 'QR'
    
    w.WPI_Out(WPI,OUT_10,'On')
    
    #Program
    for i in range(0, NumberIteration):
        w.WPI_Out(WPI,OUT_11,'On')
        w.WPI_Out(WPI,OUT_12,'On')
        # show_text('ENSAYO ' + str(i + 1))
        # root.update()
        w.Pause_Time(4)
        w.WPI_Out(WPI,OUT_9,'On')
        w.Pause_Time(1)
        w.WPI_Out(WPI,OUT_9,'off')
        w.WPI_Out(WPI,OUT_12,'Off')
        w.WPI_Out(WPI,OUT_11,'Off')
        w.Pause_Time(10)
    
    # show_text('FIN ', i)
    
#%%-----------CLOSE WPI-----------------------------------------------------
    w.Stop_WPI(WPI)
    

run_program()
    
# root.mainloop()


