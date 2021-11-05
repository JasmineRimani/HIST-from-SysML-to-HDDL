# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 16:22:53 2021

@author: Jasmine Rimani
"""

import time
from datetime import datetime
import re

class DomainFileDefinition():
    
    def __init__(self, file, list_types, predicate_list_hddl, task_list_hddl, method_list_hddl, action_list_hddl):
        # XML file to parse
        self.file = file
        # Domain File Name based on the domain name and date
        self.name_string = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p") + '_'+ self.file +'_domain.hddl' 
        # Types in the Domain File
        self.list_types = list_types
        # Predicates in the Domain File
        self.predicate_list_hddl = predicate_list_hddl
        # Tasks in the Domain File
        self.task_list_hddl = task_list_hddl
        # Methods in the Domain File
        self.method_list_hddl = method_list_hddl
        # Actions in teh Domain File
        self.action_list_hddl = action_list_hddl
        
    
    def FileWriting (self):
        ###################################################################
        # Open/Create the File
        file = open(self.name_string,'w')
        # Start writing on the file
        file.write('(define (domain {}) \n'.format(self.domain_name))
        """
        Maybe consider the different type or requirement - define on papyrus a way to define the requirements 
        of the domain file --> maybe as comment to the packages.
        """
        file.write('(:requirements :typing :hierachie) \n')
        #Object Type
        file.write('(:types \n')
        for ii in self.list_types:
            file.write('{}'.format(ii))
        # End of object type
        file.write(') \n')  
        
        # Predicates
        file.write('(:predicates \n')
        #Writes Predicates
        for ii in self.predicate_list_hddl:
            file.write('{}'.format(ii))
        # End of predicates
        file.write(') \n')   
            
        #Tasks!
        file.write('\n')  #space!
        for ii in self.task_list_hddl:
            file.write('{}'.format(ii))
            file.write('\n  \n') 
            
        #Methods!
        file.write('\n')  #space!
        for ii in self.method_list_hddl:
            file.write('{}'.format(ii))
            file.write('\n  \n') 

        #Actions
        file.write('\n')  #space!
        for ii in self.action_list_hddl:
            file.write('{}'.format(ii))
            file.write('\n  \n')  
        
        # end of the file
        file.write(')')