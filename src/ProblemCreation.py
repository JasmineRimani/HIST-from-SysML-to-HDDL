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

class ProblemDefinition():
    def __init__(self, domain_name, SysML_data, missions, d_now = os.getcwd(),  debug = 'on' ):
        # problem file name
        self.domain_name = datetime.now().strftime("%Y_%m_%d-%I_%M_%S") + '_' + domain_name + '_' +'_problem.hddl'
        # all the data from the .uml file
        self.overall_data = SysML_data 
        # all the data from the missions defined in the .uml file
        self.mission_dictionary = missions
        # debug_on
        self.debug = debug
    

    def get_order(task):
        return task.get('order')
    
    def ProblemFileElements(self):

        # Log File init - Initialize the problem file log_file
        self.log_file_general_entries.append('------------------------------------------------- \n')
        self.log_file_general_entries.append('Log errors and warnings during the HDDL Problem file element acquisition: \n')
        self.log_file_general_entries.append('------------------------------------------------- \n')
        