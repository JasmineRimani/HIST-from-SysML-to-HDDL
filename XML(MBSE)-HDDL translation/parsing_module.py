# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 16:19:39 2021

@author: Jasmine Rimani
"""
from bs4 import BeautifulSoup

class XML_parsing():
    
    def __init__(self, file):
        # XML file to parse
        self.file = file
        # Types in the Domain File
        self.list_types = []
        # Predicates in the Domain File
        self.predicate_list_hddl = []
        # Tasks in the Domain File
        self.task_list_hddl = []
        # Methods in the Domain File
        self.method_list_hddl = []
        # Actions in teh Domain File
        self.action_list_hddl = []
        
    def DomainFileList(self):

        Bs_data = BeautifulSoup(self.file, "xml")
        
        # Tasks
        # Find the instance with the tag 'node'
        b_node = Bs_data.find_all('node')

        
        
        # Methods
        
        # Actions
        
        #
        
    def GeneralParsing(self):
        
        # Functions
        
        # Parameters
        
        # Actors
        
        # C
        
        pass
    
    
    
    