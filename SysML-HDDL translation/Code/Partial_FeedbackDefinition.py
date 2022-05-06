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
    def __init__(self, domain_name, parsed_dictionary, domain_file_elements, d_now = os.getcwd(),  debug = 'on'):
        # domain name 
        self.domain_name = domain_file_elements["domain_name"]
        # Type list
        self.hddl_type_list = domain_file_elements["hddl_type_list"]
        # HighLevel UseCase list - Tasks
        self.task_list = domain_file_elements["task_list"]
        # Methods UseCase list - Tasks
        self.method_list = domain_file_elements["method_list"]
        # OpaqueAction List
        self.opaqueAction_list = domain_file_elements["opaqueAction_list"]
        # Parameters List
        self.predicate_list = domain_file_elements["predicate_list"]
        # Final list of action without doubles
        self.final_opaque_action_list = domain_file_elements["final_opaque_action_list"]
        # All the packaged elements
        self.b_packagedElement = parsed_dictionary["b_packagedElement"]
        # The rules of the XML file are constraints. They are used to define the task parameters
        self.b_ownedRules = parsed_dictionary["b_ownedRules"]
        # Edges List 
        self.edge_list = parsed_dictionary["edge_list"]
        # Dependencies in the UseCase
        self.dependencies_list = parsed_dictionary["dependencies_list"]
        # Get all the nodes
        self.b_nodes = parsed_dictionary["b_nodes"]   
        # feedback vector:
        self.hddl_type_feedback = []
        # debug_on
        self.debug = debug
        # Directory used now:
        self.d_now = d_now
        # if not named if as the self.domain_name
        self.feedback_file_name = domain_file_elements["domain_name"]
        # General Dictionary with all the output from the Feedback File
        self.feedback_output = {}
        # Log file general entries
        self.log_file_general_entries = domain_file_elements["log_file_general_entries"] 

   
    def Simple_FeedbackLogFileWriting(self):
        file = open(self.d_now + '//outputs//' + datetime.now().strftime("%Y_%m_%d-%I_%M_%S")+ 'Feedback.txt','w')
        file.write('Feedback Log File \n')        
        file.write('This file record all the discrepancy of the Papyrus model and/or the feedback from HDDL Domain File \n')
        file.write('------------------------------------------------- ')
        file.write('The following information shows discrepancies between the expected input and the real one \n')
        for ii in self.log_file_general_entries:
            file.write(ii)
        file.write('------------------------------------------------- ')
