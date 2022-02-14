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
    
    def __init__(self, file, hddl_requirements,  d_now = os.getcwd(),  debug = 'on'):
        # File that we need to parse
        self.file = file
        # File hddl domain file requirements
        self.hddl_requirements_list = hddl_requirements
        # debug_on
        self.debug = debug
        # Directory used now:
        self.d_now = d_now
        # General Dictionary with all the entries 
        self.xml_parsing_output = {}

        
    # Parse the XML File with BeautifulSoap    
    def XML_ActiveParsing(self):
        # Requirement list for the specific domain file
        requirement_list_domain_file = []
        # Packages list 
        package_list = []
        # Type list
        hddl_type_list = []
        # Actors list
        actor_list = []       
        # HighLevel UseCase list - Tasks
        task_list = []
        # Edges List
        edge_list = []
        # Feedback edge list
        edge_list_feedback = []
        # Log file general entries
        log_file_general_entries = []
        # Dependencies in the UseCase
        dependencies_list = []
        # Constraints in a Package
        b_ownedRules_from_package = []

        # Log File init
        log_file_general_entries.append('Log errors and warnings during parsing: \n')
        log_file_general_entries.append('------------------------------------------------- \n')
        # Passing the stored data inside the beautifulsoup parser, 
        # storing the returned object in a variable - that is the main object to unpack

        Bs_data = BeautifulSoup(self.file, "xml")
        
        # How to use BeautifulSoup:
            # Finding all instances of tag - You get a list with all the instances with that tag:
                # b_node = Bs_data.find_all('node')
                # If the tags are nested - you get each tag one after the other from the order of the file
        
            # Find all the packaged elements
                # You can divide the packaged elements per Folder - so that you don't have to parse useless information like the ones for the Mission
        
        b_packagedElement = Bs_data.find_all('packagedElement') 
        b_nestedClassifier = Bs_data.find_all('nestedClassifier') 
        self.xml_parsing_output["b_packagedElement"] = b_packagedElement
        

        for index,element in enumerate(b_packagedElement):
            
            # Isolate the "xmi:type="uml:Package" " --> e.g. b_packagedElement[0]['xmi:type']
            if element['xmi:type'] == 'uml:Package':
                package_list.append({"name": element['name'], "xmi:id":element['xmi:id']})    
            
            # Isolate the classes - ':types' in HDDL
            if element['xmi:type'] == 'uml:Class' and element.parent["name"] == 'Types':
                hddl_type_list.append({"name": element['name'].replace(" ", ""), "xmi:id":element['xmi:id']})

            # Isolate Actors:
            if element['xmi:type'] == 'uml:Actor':
                actor_list.append({"name": element['name'], "xmi:id":element['xmi:id']})
            
            # Isolate Usecases that are packegedElements --> You get your tasks name, however you still need your parameters
            if element['xmi:type'] == 'uml:UseCase':
                task_list.append({"name": element['name'], "xmi:id":element['xmi:id'], "parameters": []})   
                
            # Isolate Packaged Constraints:
            if element['xmi:type'] == 'uml:Constraint':
                b_ownedRules_from_package.append(element)                

        for index,classifier in enumerate(b_nestedClassifier):
            if classifier['xmi:type'] == 'uml:Class' and classifier.parent.parent["name"] == 'Types':
                hddl_type_list.append({"name": classifier['name'].replace(" ", ""), "xmi:id":classifier['xmi:id'], "parent": classifier.parent["name"]})
                

        self.xml_parsing_output["b_package_list"] = package_list
        self.xml_parsing_output["hddl_type_list"] = hddl_type_list
        self.xml_parsing_output["actor_list"] = actor_list
        self.xml_parsing_output["task_list"] = task_list
        
        
        # Find all the constraints tag = ownedRule and xmi:type="uml:Constraint"
        b_ownedRules = Bs_data.find_all('ownedRule') 
        self.xml_parsing_output["b_ownedRules"] = b_ownedRules + b_ownedRules_from_package
        
        # Find all the edges
        b_edges = Bs_data.find_all('edge')    
        self.xml_parsing_output["b_edges"] = b_edges
        # Map all the edges
        for index,edge in enumerate(b_edges):
            try:
                edge_list.append({"xmi:id":edge['xmi:id'], "input":edge['source'], "output":edge['target']}) 
            except:
                # if you can't find one of the ends of the edge: save the edge in the edge list and in the feedback log
                if self.debug == 'on' :
                    print('Check your model! Edge id:{} is ill defined! It is probably missing an input or an output'.format(edge['xmi:id']))
                # Add this to the future Log File
                log_file_general_entries.append('\t\t Check your model! Edge id:{} is ill defined! It is probably missing an input or an output \n'.format(edge['xmi:id']))
                if edge.has_attr('source'):
                    edge_list.append({"xmi:id":edge['xmi:id'], "input":edge['source'], "output":''}) 
                    edge_list_feedback.append({"xmi:id":edge['xmi:id'], "input":edge['source'], "output":''}) 
                if edge.has_attr('target'):
                    edge_list.append({"xmi:id":edge['xmi:id'], "input":' ', "output":['target']}) 
                    edge_list_feedback.append({"xmi:id":edge['xmi:id'], "input":' ', "output":['target']}) 
            
        self.xml_parsing_output["edge_list"] = edge_list
        #Find the dependencies
        for index,connector in enumerate(b_packagedElement):
            if connector['xmi:type'] == 'uml:Dependency' or connector['xmi:type'] == 'uml:Realization':
                dependencies_list.append({"xmi:id":connector['xmi:id'], "input":connector['supplier'], "output":connector['client']})        
        
        self.xml_parsing_output["dependencies_list"] = dependencies_list
        # Find all the comments
        b_comments = Bs_data.find_all('ownedComment') 
        self.xml_parsing_output["b_comments"] = b_comments
        # Find all the nodes
        b_nodes = Bs_data.find_all('node')
        self.xml_parsing_output["b_nodes"] = b_nodes
        
        # Domain file instances analysis  
        for comment in b_comments:
            # The requirements for the HDDL domain file are included as comment in the UseCase
            if comment.parent['name'] == 'UseCase' and "Requirements" in comment.body.contents[0]:
                comment_body = comment.body.string
                for requirement in self.hddl_requirements_list:
                    # avoid case-sensitivity 
                    if requirement.lower() in comment_body.lower() and requirement.lower() not in requirement_list_domain_file:
                        requirement_list_domain_file.append(requirement.lower())
      
        self.xml_parsing_output["requirement_list_domain_file"] = requirement_list_domain_file
        self.xml_parsing_output["log_file_general_entries"] = log_file_general_entries
        
        return self.xml_parsing_output