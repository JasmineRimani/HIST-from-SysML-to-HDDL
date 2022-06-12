# -*- coding: utf-8 -*-
"""
Created on Thu Nov 4 16:19:39 2021

@author: Jasmine Rimani
"""
# https://beautiful-soup-4.readthedocs.io/en/latest/#
from bs4 import BeautifulSoup
# https://docs.python.org/3/library/os.html
import os

class XML_parsing():
    
    def __init__(self, file, package_HDDL, package_domain, package_problem,  d_now = os.getcwd(),  debug = 'on'):
        # File that we need to parse
        self.file = file
        # debug_on
        self.debug = debug
        # Directory used now:
        self.d_now = d_now
        # General Dictionary with all the entries 
        self.xml_parsing_output = {}
        # Package with the HDDL instance
        self.package_HDDL = package_HDDL
        # Package with the domain instances
        self.package_domain = package_domain
        # Package with the problem instances
        self.package_problem = package_problem
    
    def Parsing(self):
        # "-------- Initial Variables Set-up --------"
        # # Log file general entries
        # log_file_general_entries = []
        # # Dependencies in the UseCase
        # dependencies_list = []
        # # Constraints in a Package: 
        #     # the constraints are or Task parameters or Problem file initial conditions
        # b_ownedRules_from_package = []

        # # Log File init
        # log_file_general_entries.append('Log errors and warnings during parsing: \n')
        # log_file_general_entries.append('------------------------------------------------- \n')
       
        # "-------- Actual Code --------"
        # Passing the stored data inside the beautifulsoup parser, 
        # storing the returned object in a variable - that is the main object to unpack
        SysML_data = BeautifulSoup(self.file, "xml")
        # get the packages with the HDDL elements
        HDDL_elements = SysML_data.find(attrs={"name": self.package_HDDL})
        domain_elements = SysML_data.find(attrs={"name": self.package_domain})
        problem_elements = SysML_data.find(attrs={"name": self.package_problem})
        # -------------------------------------------------------
        # Let's focus on the domain file
        # Let's extract the types
        domain_types = domain_elements.find_all('packagedElement', attrs={"xmi:type": "uml:Class"})
        # get the predicate that are in the tree
        predicate_type = [x for x in domain_types if x['name'] == "predicate"][0]
        # Let's get the list of predicates
        nodes = domain_elements.find_all('node', attrs={"xmi:type": "uml:ActivityParameterNode", "xmi:type": "uml:CentralBufferNode"})
        domain_predicates = [x for x in nodes if x['type'] == predicate_type["xmi:id"]]
        # We want to extract the task elements - let's look for the useCases without a method
        # tasks are defined as packaged elements and xmi:type="uml:UseCase"
        task_elements = domain_elements.find_all('packagedElement', attrs={"xmi:type": "uml:UseCase"})
        task_parameters = domain_elements.find_all('ownedRule', attrs={"xmi:type": "uml:Constraint"})
        # We want to extract the method elements
        methods_elements = domain_elements.find_all('ownedUseCase', attrs={"xmi:type": "uml:UseCase"})
        # we want to exctract the actions and their parameters
        actions_elements = domain_elements.find_all('node', attrs={"xmi:type": "uml:OpaqueAction"})
        action_parameters = domain_elements.find_all('edge')
        # We want to extract the action elements
        domain_dictionary = {'types': domain_types, 'predicates': domain_predicates, 'tasks': task_elements, 'tasks_param': task_parameters, 'methods': methods_elements, 'actions':  actions_elements, 'action_param' : action_parameters}
        # -------------------------------------------------------
        # Lets' focus on the problem file...
        # Get the mission folders 
        missions = problem_elements.find_all('packagedElement', attrs={"xmi:type": "uml:Package"})

        return SysML_data, domain_dictionary, missions