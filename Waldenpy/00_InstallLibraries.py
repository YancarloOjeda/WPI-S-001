"""
Walden Modular Equipment SAS
install libraries
2020
"""
import Walden as w

PList = ['serial',
         'pyfirmata', 
         'opencv-python',
         'python-tk',
         'random',
         'matplotlib',
         'time' ]

for i in PList:
    w.install(i)
    w.Pause_Time(1)
    print(i,'...ok')