# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 19:05:50 2021

@author: felix
"""

import subprocess
# import os

# # create batch script
# myBat = open(r'.\Test.bat','w+') # create file with writing access
# myBat.write('''echo hello
# pause''') # write commands to file
# myBat.close()

subprocess.call(["start", "Test.bat"], shell=True)