# -*- coding: utf-8 -*-
"""
Created on Thu Nov 4 16:19:39 2021

@author: Jasmine Rimani
"""

# https://docs.python.org/3/library/datetime.html
from datetime import datetime
# https://docs.python.org/3/library/re.html
import re
# https://docs.python.org/3/library/uuid.html
import uuid
# https://docs.python.org/3/library/os.html
import os

# MAIN PARSING CLASS!
class Simple_FeedbackDefinition():
    def __init__(self, log_file_general_entries, d_now = os.getcwd(),  debug = 'on'):
        # directory
        self.d_now = d_now
        # Log file general entries
        self.log_file_general_entries = log_file_general_entries

   
    def Simple_FeedbackLogFileWriting(self):
        file = open(self.d_now + '//outputs//' + datetime.now().strftime("%Y_%m_%d-%I_%M_%S")+ '_Feedback.txt','w')
        file.write('Feedback Log File \n')        
        file.write('This file record all the discrepancy of the Papyrus model and/or the feedback from HDDL Domain File \n')
        file.write('------------------------------------------------- ')
        file.write('The following information shows discrepancies between the expected input and the real one \n')
        for ii in self.log_file_general_entries:
            file.write(ii)
        file.write('------------------------------------------------- ')
