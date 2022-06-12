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
class Domain():
    def __init__(self, domain_name, SysML_data, domain_dictionary, task_parameters = 'common', flag_ordering_file = 'yes', method_precondition_from_action = 'yes', d_now = os.getcwd(),  debug = 'on'):
        # domain file name
        self.domain_name = datetime.now().strftime("%Y_%m_%d-%I_%M_%S") + '_' + domain_name + '_' +'_domain.hddl'
        # all the data from the .uml file
        self.overall_data = SysML_data
        # all the data from the domain definition of the .uml file
        self.domain_dictionary = domain_dictionary
        # Log file general entries
        self.log_file_general_entries = []
        # debug_on
        self.debug = debug
        # Directory used now:
        self.d_now = d_now
        # Task parameters consideration
        self.task_parameters = task_parameters
        # Parameters Ordering 
        self.flag_ordering_file = flag_ordering_file
        # A flag to indicate if the method considers its substasks preconditions or not
        # For default it doesn't
        self.method_precondition_from_action = method_precondition_from_action    # Get out the elements of the Problem File

    # Get list order based on a key
    def get_order(task):
        return task.get('order')

    # Get the difference bewteen two lists
    def Diff(li1, li2):
        li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
        return li_dif

    def DomainFileElements(self):     
        # Log File init
        self.log_file_general_entries.append('------------------------------------------------- \n')
        self.log_file_general_entries.append('Log errors and warnings during the HDDL Domain file element acquisition: \n')
        self.log_file_general_entries.append('------------------------------------------------- \n')
         
        """
        For each useCase, we  can access to the sub-tags with: 
            a = b_packagedElement[n].children  # --> with n elements in b_packagedElement
            for i in a: print(i) # --> you will see all the subtags
        """
        # types in the HDDL file
        hddl_types = self.domain_dictionary['types']
        predicate_type = [x for x in hddl_types if x['name'] == "predicate"][0]
        # Create the HDDL methods
        methods = self.domain_dictionary['methods']
        methods_dictionary = {}
        for method in methods:
            temporary_dictionary = {}
            # --------------------------------------------------------------------
            # find the parameters
            nodes = method.find_all('node', attrs={"xmi:type": "uml:ActivityParameterNode"})
            parameters = [x for x in nodes if len(x["name"].split()) == 1]
            
            # if the parameter do not have a type
            #------------------- 
            # NOT WORKING - rewrite
            #-----------------------
            for param in parameters:
                if not "type" in param:
                    # look if there is an already defined parameter with the same or similar name 
                    # similar name are name without the possible following numbers
                    flag_param = 0
                    for type in hddl_types:
                        new_param = ''.join([i for i in param['name'] if not i.isdigit()])
                        if type['name'] == new_param:
                            param['type'] = type['xmi:id']
                            flag_param = 1

                    # creating a parameter with that name and print a warning to the user
                    if flag_param == 0:
                        # create an adhoc name based on the parameter name
                        param['type'] = param['name']
                        id_uuid = str(uuid.uuid1())
                        hddl_types.append({"name": param['name'], "xmi:id": id_uuid})
                        if self.debug == 'on': 
                            print('No predefined type for {}. Add it on Papyrus!'.format(param['name']))
                        self.log_file_general_entries('\t\t No predefined type for {}. We added as its own type \n'.format(param['name']))
            
            # add parameters to the method temporary dictionary
            temporary_dictionary['parameters'] = parameters
            x = 0

            


            # find the associated task

            # find the actions

            # find the preconditions

            # find the order of the action

