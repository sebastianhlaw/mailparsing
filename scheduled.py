__author__ = 'Sebastian.Law'

import os
import datetime

path = "C:/Users/Sebastian.Law/Downloads/"
name = "output.txt"

file = open(path+name, 'a')
file.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
file.close()