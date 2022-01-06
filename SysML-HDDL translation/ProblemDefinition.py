# -*- coding: utf-8 -*-
"""
Created on Thu Nov 4 16:19:39 2021

@author: Jasmine Rimani
"""
# https://docs.python.org/3/library/os.html
import os


# MAIN PARSING CLASS!
class ProblemDefinition():
    def __init__(self, domain_name, parsed_dictionary, domain_file_elements, map_data, htn_tasks, d_now = os.getcwd(),  debug = 'on'):
        
        # File with the map data
        self.map_data = map_data
        # domain name
        self.domain_name = domain_file_elements["domain_name"]
        # problem name 
        self.problem_name = domain_file_elements["problem_name"]
        # Type list
        self.hddl_type_list = domain_file_elements["hddl_type_list"]
        # HighLevel UseCase list - Tasks
        self.task_list = domain_file_elements["task_list"]
        # Log file general entries
        self.log_file_general_entries = domain_file_elements["log_file_general_entries"]   
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
        # debug_on
        self.debug = debug
        # Directory used now:
        self.d_now = d_now
        # General Dictionary with all the output from the Problem File Creation 
        self.problem_definition_output = {}
        # Initial Task Network
        self.htn_tasks = htn_tasks 
        # The task to be accomplished during the mission
        self.mission_tasks = []
        # Initial conditions in the problem file
        self.initial_conditions_pf = []
        # Objects in the problem file
        self.problem_file_object = []


    # Get out the elements of the Problem File
    def get_order(task):
        return task.get('order')

    def ProblemFileElements(self):    
        
        self.log_file_general_entries.append('------------------------------------------------- \n')
        self.log_file_general_entries.append('Log errors and warnings during the HDDL Problem file element acquisition: \n')
        self.log_file_general_entries.append('------------------------------------------------- \n')
        
        # The tasks that have to be defined by the designer in the initial task network
        # In that way, they can easily change and try different configuration of tasks
        # The task order is automatically generated looking at the general mission Activity Diagram!! 
        # Just create a Activity Diagram "General layout"


        # b_ownedRules
        # Problem file instances analysis
        for uu in self.b_nodes:
            
            # If the packagedElement is a UseCase
            # Just consider the inputs in the Mission Folder 
            # We are just considering the Problem File entries here! 
            if uu['xmi:type'] == 'uml:CallBehaviorAction' and  (uu.parent.parent.parent['name'] == 'Mission' or uu.parent.parent.parent.parent['name'] == 'Mission'):
                # Get hierarchy of the tasks - the tasks
                
                # Save all your BehaviorActions and their inputs and outputs pins 
                temp_dict = {"name": uu['name'], "xmi:id":uu['xmi:id'], "behavior":uu['behavior'], "incoming_edge": uu['incoming'], "outgoing_edge": uu['outgoing']} 
                self.mission_tasks.append(temp_dict)
                    
        # Hierachie of main tasks
        functions_with_incoming_edge = []
        functions_with_outcoming_edge = []
        for yy in self.mission_tasks:
            for kk in self.edge_list:
                if 'incoming_edge' in yy and yy['incoming_edge'] == kk['xmi:id']:
                    for uu in self.mission_tasks:
                        if uu['xmi:id'] == kk['input']:
                            functions_with_incoming_edge.append(yy)
                            yy['previous_action'] = kk['input']
                
                    
                if 'outgoing_edge' in yy and yy['outgoing_edge'] == kk['xmi:id']:
                    for uu in self.mission_tasks:
                        if uu['xmi:id'] == kk['output']:
                            functions_with_outcoming_edge.append(yy)
                            yy['following_action'] = kk['output']
        
        self.ordered_mission_tasks = []
        for yy in self.mission_tasks:
            if yy not in functions_with_incoming_edge and yy in functions_with_outcoming_edge:
                yy['order'] = 0
            elif yy in functions_with_incoming_edge and yy not in functions_with_outcoming_edge:
                yy['order'] = len(self.mission_tasks) - 1
 
        flag = 0 
        counter = 0
        
        while flag == 0:
            for yy in self.mission_tasks:
                if 'order' in yy and yy['order'] != len(self.mission_tasks):
                    # check the next element that should be there
                    for uu in self.mission_tasks:
                        if'previous_action'in uu and uu['previous_action'] == yy['xmi:id']:
                            uu['order'] = yy['order'] + 1 
                elif 'order' in yy and yy['order'] == len(self.mission_tasks): 
                    pass
            
                if 'order' in yy:
                    counter = counter + 1
            
            if counter == len(self.mission_tasks):
                flag = 1
            else:
                counter = 0
            
        # Sort actions based on the ordering    
        self.mission_tasks.sort(key = ProblemDefinition.get_order)

        # Common inputs in the problem file
        # Get initial conditions as constraints 
        for ii in self.b_ownedRules:
            
            if ii.parent.parent['name'] == 'MissionToAccomplish':
                self.initial_conditions_pf.append(ii['name'])

        self.mission_components = []            
        # Get the components that you need for the papyrus model
        for uu in self.b_packagedElement:
             
            if uu['xmi:type'] == "uml:Component" and uu.parent['name'] == 'Mission':
                self.mission_components.append({"xmi:id":uu['xmi:id'], "name": uu['name']})
                for ii in uu.children:
                    
                    # Associate the type of the component
                    if ii.name == 'ownedAttribute':
                        self.mission_components[-1]['type'] = ii['type']
                        
                        
                    if ii.name == 'packagedElement' and ii['xmi:type'] == "uml:Component":
                        # the replace should remove spaces from strings! 
                        self.mission_components.append({"xmi:id":ii['xmi:id'], "name": ii['name'].replace(" ", "")})
                        for jj in ii.children:
                            if jj.name == 'ownedAttribute' and jj['xmi:type'] == "uml:Property":
                                self.mission_components[-1]['type'] = jj['type']
                        for jj in ii.children:
                            if jj.name == 'ownedAttribute' and jj['xmi:type'] == "uml:Port":
                                self.mission_components.append({"xmi:id":jj['xmi:id'], "name": jj['name'], "type": jj['type']})

        for uu in self.mission_components:

            for ii in self.hddl_type_list:
                if 'type' in uu and uu['type'] == ii['xmi:id']:
                    self.problem_file_object.append('{}-{}'.format(uu['name'].replace(" ", ""), ii['name']))
                elif 'type' not in uu:
                    self.problem_file_object.append('{}-{}'.format(uu['name'].replace(" ", ""), uu['name'].replace(" ", "")))
                    if self.debug == 'on':
                        print('{} is missing his type - please define a type for this component!'.format(uu['name'].replace(" ", "")))
                        print('{} has been appended to the hddl type list!'.format(uu['name'].replace(" ", "")))
                    self.log_file_general_entries.append('\t\t {} is missing his type - please define a type for this component! \n'.format(uu['name']))
                    self.log_file_general_entries.append('\t\t {} has been appended to the hddl type list \n!'.format(uu['name'].replace(" ", "")))
                    
                    self.hddl_type_list.append({"name": uu['name'].replace(" ", ""), "xmi:id":''})
                    
        
        # Let's start with the map data to create the problem file
        # self.map_data
        
        dummy_list = []

        for ii in self.map_data:
            flag_check = 0
            if len(ii.split("-")) == 2:
                dummy_list.append(ii)
                # take the second part of the vector and check if it exist in the HDDL types
                dummy_variable = ii.split("-")[-1]
                dummy_variable = dummy_variable.replace('\n','').strip()
                for uu in self.hddl_type_list:
                    if uu['name'] == dummy_variable:
                        flag_check = 1
                if flag_check != 1:
                    if self.debug == 'on':
                        print('{} has a wrong type! Please check your types in the map_file!'.format(uu['name'].replace(" ", "")))
                    self.log_file_general_entries.append('\t\t {} has a wrong type! Please check your types in the map_file \n!'.format(uu['name'].replace(" ", "")))
                else:
                    self.problem_file_object.append('{}-{}'.format(ii.split("-")[0], ii.split("-")[-1].replace('\n','').strip()))

            if ii not in dummy_list:
                self.initial_conditions_pf.append(ii.replace('\n','').strip())
        
        # Analyse the Initial Task network:
            # get the tasks
            # check that the tasks exists in your domain
            # check that the parameters exist in your parameter list
            # check that the order of the tasks
        
        for index,ii in enumerate(self.htn_tasks):
            
            task_found = 'no'  
            object_found = 'no'
            dummy_string = ii.replace('task{}('.format(index),'')         
            dummy_string = dummy_string.replace(')'.format(index),'') 
            dummy_list = dummy_string.split()
          
            for kk in self.task_list:
                if dummy_list[0] == kk['name']:
                    task_found = 'yes'
                    for hh in dummy_list[1::]:
                        object_found = 'no'
                        for uu in self.problem_file_object:
                            if hh in uu:
                                object_found = 'yes'
                        if object_found == 'no':
                            if self.debug == 'on':
                                print('{} not found in the problem file objects'.format(dummy_list[-1]))
                            self.log_file_general_entries.append('\t\t {} not found in the problem file objects \n!'.format(dummy_list[-1]))
                            break
                        
                
            if task_found != 'yes' and object_found != 'yes':
                if self.debug == 'on':
                    print('Please check your initial task network! Something is wrong! \n Or your task or your task parameters are not in the domain definition')
                self.log_file_general_entries.append('\t\t Please check your initial task network! Something is wrong! \n Or your task or your task parameters are not in the domain definition \n')
                break
        
        self.ordering_task_network = []
        for index,ii in enumerate(self.htn_tasks):
            dummy_string = ii.replace('task{}('.format(index),'')         
            dummy_string = dummy_string.replace(')'.format(index),'') 
            dummy_list_1 = dummy_string.split()
            task_to_compare_1 = dummy_list_1[0]
            for index,jj in enumerate(self.htn_tasks):
                dummy_string = jj.replace('task{}('.format(index),'') 
                dummy_string = dummy_string.replace(')'.format(index),'') 
                dummy_list_2 = dummy_string.split() 
                task_to_compare_2 = dummy_list_2[0]
                for kk in self.mission_tasks:
                    if task_to_compare_1 == kk['name']:
                        task_number_1 = kk['order']
                    if task_to_compare_2 == kk['name']:
                        task_number_2 = kk['order']
            if task_number_1 < task_number_2:
                dummy_string_1 = ii.split('(')
                dummy_string_2 = jj.split('(')
                self.ordering_task_network.append('(< {} {})'.format(dummy_string_1[0], dummy_string_2[0]))
            if task_number_2 < task_number_1:
                dummy_string_1 = ii.split('(')
                dummy_string_2 = jj.split('(')
                self.ordering_task_network.append('(< {} {})'.format(dummy_string_1[0], dummy_string_2[0]))                    
                          
        
        self.problem_definition_output["log_file_general_entries"] = self.log_file_general_entries
        self.problem_definition_output["problem_file_object"] = self.problem_file_object
        self.problem_definition_output["htn_tasks"] = self.htn_tasks
        self.problem_definition_output["ordering_task_network"] = self.ordering_task_network
        self.problem_definition_output["initial_conditions_pf"] = self.initial_conditions_pf
        
        return self.problem_definition_output
        
    def ProblemFileWriting (self):
        
        file = open(self.d_now + '//outputs//' + self.problem_name,'w')
        file.write('(define ')
        file.write(' (domain {}) \n'.format(self.domain_name))
        # Objects
        file.write('\t (:objects \n')
        for ii in self.problem_file_object:
            file.write('\t\t{}\n'.format(ii))
        file.write('\t )\n\n')
        # Hierarchical Task Network
        file.write('\t :htn( \n')
        file.write('\t\t :parameters () \n')
        file.write('\t\t :subtasks (and \n')
        for ii in self.htn_tasks:
            file.write('\t\t\t({})\n'.format(ii))
        
        file.write('\t\t )\n\n')
        #Ordering
        file.write('\t\t :ordering (and \n')
        for ii in self.ordering_task_network:
            file.write('\t\t\t{}\n'.format(ii))
        
        file.write('\t\t )\n\n')
        
        #close hierarchical task network
        file.write('\t )\n\n')
        
        # Initial Conditions
        file.write('\t (:init \n')
        for ii in self.initial_conditions_pf:
            file.write('\t\t{}\n'.format(ii))        
        file.write('\t )\n\n')
        # end of the file
        file.write(')')        