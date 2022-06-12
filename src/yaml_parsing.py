# -*- coding: utf-8 -*-
"""
Created on Thu Apr 4 16:19:39 2022

@author: Jasmine Rimani
"""
# https://yaml.org/
import yaml

# Custom modules
from errors import NotDefinedRequirements

class YAML_parsing():
    def __init__(self, file, debug = 'on'):
        # File that we need to parse
        self.file = file
        # debug_on
        self.debug = debug
        self.input_dictionary = yaml.safe_load(self.file)
        if self.debug == 'on':
            for key, value in self.input_dictionary.items():
                print (key + " : " + str(value))

    def YAML_fileNames(self):
        # Get the name of the Papyrus File
        file_papyrus = self.input_dictionary["file_name"]
        # Get the name of the Domain File - if the domain would have the same name of the file_name
        if "domain_name" in self.input_dictionary:
            domain_name = self.input_dictionary["domain_name"]
        else:
            domain_name = '{}_{}'.format('domain', self.input_dictionary["file_name"])  
        # Get the name of the Feedback file if any
        if "feedback_file_name" in self.input_dictionary:
            feedback_name = self.input_dictionary['feedback_file_name']
        else:
            feedback_name = '{}_{}'.format('feedback', self.input_dictionary["file_name"]) 
        # Get additional files to add to the problem file, if any
        if "additional_files" in self.input_dictionary:
            pass
        
        return file_papyrus, domain_name, feedback_name

    def YAML_mainFlags(self):
        # Flags
        if 'generate_problem_file' in self.input_dictionary:
            generate_problem_file = self.input_dictionary['generate_problem_file']
        else:
            generate_problem_file = 'no'  

        if 'generate_domain_file' in self.input_dictionary:
            generate_domain_file = self.input_dictionary['generate_domain_file']
        else:
            generate_domain_file = 'no'     

        if 'generate_feedback' in self.input_dictionary:
            generate_feedback_file = self.input_dictionary['generate_feedback']
        else:
            generate_feedback_file = 'no'  
               
        if 'domain_requirements' in self.input_dictionary:
            domain_requirements = self.input_dictionary['domain_requirements']
        else:
            raise NotDefinedRequirements

        return generate_problem_file, generate_domain_file, generate_feedback_file, domain_requirements

    def YAML_otherFlags(self):
        if 'method_precondition_from_action' in self.input_dictionary:
            method_precondition_from_action = self.input_dictionary['method_precondition_from_action']
        else:
            method_precondition_from_action = 'yes'   

        if 'flag_ordering' in self.input_dictionary:
            flag_ordering_file = self.input_dictionary['flag_ordering']
        else:
            flag_ordering_file = 'yes'    

        if 'task_parameters' in self.input_dictionary:
            task_parameters = self.input_dictionary['task_parameters']
        else:
            # if nothing is said consider the common task parameters
            task_parameters = 'common'

        return method_precondition_from_action, flag_ordering_file, task_parameters
    
    def YAML_PackagesNames(self):
        if 'package_HDDL' in self.input_dictionary:
            package_HDDL= self.input_dictionary['package_HDDL']
        else:
            package_HDDL = 'ElementsHDDL'   

        if 'package_domain' in self.input_dictionary:
            package_domain = self.input_dictionary['package_domain']
        else:
            package_domain = 'DomainDefinition'    

        if 'package_problem' in self.input_dictionary:
            package_problem = self.input_dictionary['package_problem']
        else:
            package_problem = 'ProblemDefinition'

        if 'package_feedback' in self.input_dictionary:
            package_feedback = self.input_dictionary['package_feedback']
        else:
            package_feedback = 'Feedback'

        return package_HDDL, package_domain, package_problem, package_feedback
