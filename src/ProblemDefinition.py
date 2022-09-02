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
class ProblemDefinition():
    def __init__(self, domain_name, parsed_dictionary, missions, d_now = os.getcwd(),  debug = 'on'):
        
       # Put an adaptable domain file name
        # Put an adaptable problem file name
        if domain_name != 'None':
            self.domain_name = datetime.now().strftime("%Y_%m_%d-%I_%M_%S") + '_' + domain_name + '_' +'_domain.hddl' 
            self.domain_name_simple = domain_name
            self.problem_name = datetime.now().strftime("%Y_%m_%d-%I_%M_%S") + '_' + domain_name + '_' +'_problem.hddl'
        else:
           self.domain_name = datetime.now().strftime("%Y_%m_%d-%I_%M_%S") + '_' +'_domain.hddl' 
           self.domain_name_simple = datetime.now().strftime("%Y_%m_%d-%I_%M_%S")
           self.problem_name = datetime.now().strftime("%Y_%m_%d-%I_%M_%S") + '_' +'_problem.hddl'

    """ New init code goes here.
        Most of the element have already been extracted from the parsing module.
    """


        # # Type list
        # self.hddl_type_list = domain_file_elements["hddl_type_list"]
        # # HighLevel UseCase list - Tasks
        # self.task_list = domain_file_elements["task_list"]
        # # Log file general entries
        # self.log_file_general_entries = domain_file_elements["log_file_general_entries"]   
        # # All the packaged elements
        # self.b_packagedElement = parsed_dictionary["b_packagedElement"]
        # # The rules of the XML file are constraints. They are used to define the task parameters
        # self.b_ownedRules = parsed_dictionary["b_ownedRules"]
        # # Edges List 
        # self.edge_list = parsed_dictionary["edge_list"]
        # # Dependencies in the UseCase
        # self.dependencies_list = parsed_dictionary["dependencies_list"]
        # # Get all the nodes
        # self.b_nodes = parsed_dictionary["b_nodes"]
        # # debug_on
        # self.debug = debug
        # # Directory used now:
        # self.d_now = d_now
        # # General Dictionary with all the output from the Problem File Creation 
        # self.problem_definition_output = {}
        # # Initial Task Network
        # self.htn_tasks = [] 
        # # The task to be accomplished during the mission
        # self.mission_tasks_list = []
        # # Initial conditions in the problem file
        # self.initial_conditions_pf = []
        # # Objects in the problem file
        # self.problem_file_object = []
        # # Mission Dictionary: General Dictionary where you put all the mission specific info
        # self.general_mission_dictionary = []
        # # To order or not the initial task network
        # self.flag_ordering = 'yes'


    # Get out the elements of the Problem File
    def get_order(task):
        return task.get('order')

    def ProblemFileElements(self):    
        
        self.log_file_general_entries.append('------------------------------------------------- \n')
        self.log_file_general_entries.append('Log errors and warnings during the HDDL Problem file element acquisition: \n')
        self.log_file_general_entries.append('------------------------------------------------- \n')
        
        
        
        # Static Mission Data --> Mission Components
        self.mission_components = []            
        # Get the components that you need for the papyrus model
        for uu in self.b_packagedElement:
             
            if uu['xmi:type'] == "uml:Class" and uu.parent.parent['name'] == 'Mission' and uu.parent['name'] == 'StaticMissionData':
                self.mission_components.append({"xmi:id":uu['xmi:id'], "name": uu['name']})
                for ii in uu.children:
                    
                    # Associate the type of the component
                    if ii.name == 'ownedAttribute':
                        self.mission_components[-1]['type'] = ii['type']
                        
                    

        for uu in self.mission_components:

            for ii in self.hddl_type_list:
                if 'type' in uu and uu['type'] == ii['xmi:id']:
                    self.problem_file_object.append('{} - {}'.format(uu['name'].replace(" ", ""), ii['name']))
                elif 'type' not in uu:
                    self.problem_file_object.append('{} - {}'.format(uu['name'].replace(" ", ""), uu['name'].replace(" ", "")))
                    if self.debug == 'on':
                        print('{} is missing his type - please define a type for this component!'.format(uu['name'].replace(" ", "")))
                        print('{} has been appended to the hddl type list!'.format(uu['name'].replace(" ", "")))
                    self.log_file_general_entries.append('\t\t {} is missing his type - please define a type for this component! \n'.format(uu['name']))
                    self.log_file_general_entries.append('\t\t {} has been appended to the hddl type list \n!'.format(uu['name'].replace(" ", "")))
                    
                    self.hddl_type_list.append({"name": uu['name'].replace(" ", ""), "xmi:id":''})                    
        
        # Multiple Problem Files implementation
        number_of_problems = 1
        mission_tasks = []
        initial_conditions_pf = []
        htn_tasks = []
        ordering_task_network = []
        problem_file_object_mutant = []
        for element in self.b_packagedElement:
             
            if element['xmi:type'] == "uml:Activity" and element.parent.parent['name'] == 'Mission' and element.parent['name'] == 'MissionToAccomplish':
                name_problem = '{}-{}-{}'.format(element['name'], number_of_problems, self.problem_name)
                temporary_general_dictionary = {"name": name_problem, "components": self.mission_components, "problem_file_objects_static": self.problem_file_object }
                # Task to be accomplished to generate the task network
                for child in element.children:
                    # Get the Tasks of that specific problem file
                    if not isinstance(child, str) and child.has_attr('xmi:type') and child['xmi:type'] == 'uml:CallBehaviorAction':
                        # Save all your BehaviorActions and their inputs and outputs pins
                        temp_dict = {"name": child['name'], "xmi:id": child['xmi:id'], "behavior": child['behavior'], "incoming_edge": child['incoming'], "outgoing_edge": child['outgoing']} 
                        mission_tasks.append(temp_dict)
                    # Double child if we have a loop node
                    if not isinstance(child, str) and child.has_attr('xmi:type') and child['xmi:type'] == 'uml:LoopNode':
                        x = 0
                        for loop_child in child:
                            if not isinstance(loop_child, str) and loop_child.has_attr('xmi:type') and loop_child['xmi:type'] == 'uml:CallBehaviorAction':
                                # Save all your BehaviorActions and their inputs and outputs pins
                                try:
                                    temp_dict = {"name": loop_child['name'], "xmi:id": loop_child['xmi:id'], "behavior": loop_child['behavior'], "incoming_edge": loop_child['incoming'], "outgoing_edge": loop_child['outgoing']} 
                                    mission_tasks.append(temp_dict)
                                except:
                                    print("Probably you are missing an edge in your function: {}".format(loop_child))
                                    
                    # Get the Initial set of conditions of that specific problem file
                    if not isinstance(child, str) and child.has_attr('xmi:type') and child['xmi:type'] == 'uml:Constraint':  
                        initial_conditions_pf.append(child['name'])
                    if not isinstance(child, str) and child.has_attr('xmi:type') and child['xmi:type'] == 'uml:Comment':
                        x = 0
                        # get files that may have inputs
                        temp_list = []
                        if child.body.contents != []:
                            if "file" in child.body.contents[0]:
                                temp_list = child.body.contents[0].split("\r\n")
                                for line in temp_list:
                                    if "file" and "=" in line:
                                        get_name_file = line.split("=")[-1].strip()
                                        # open file and get the info you want from it
                                        with open(self.d_now +'\\inputs\\' + get_name_file, 'r') as f:
                                            file_data = f.readlines() 
                                        
                                        dummy_list = []
                                        # store the data informations
                                        for f_line in file_data:
                                            
                                            flag_check = 0
                                            if len(f_line.split("-")) == 2:
                                                dummy_list.append(f_line)
                                                # take the second part of the vector and check if it exist in the HDDL types
                                                dummy_variable = f_line.split("-")[-1]
                                                dummy_variable = dummy_variable.replace('\n','').strip()
                                                for uu in self.hddl_type_list:
                                                    if uu['name'] == dummy_variable:
                                                        flag_check = 1
                                                if flag_check != 1:
                                                    if self.debug == 'on':
                                                        print('{} has a wrong type! Please check your types in the map_file!'.format(uu['name'].replace(" ", "")))
                                                    self.log_file_general_entries.append('\t\t {} has a wrong type! Please check your types in the {} \n!'.format(uu['name'].replace(" ", ""), get_name_file))
                                                else:
                                                    problem_file_object_mutant.append('{} - {}'.format(f_line.split("-")[0], f_line.split("-")[-1].replace('\n','').strip()))
                                
                                            if f_line not in dummy_list and f_line.replace('\n','').strip() != "":
                                                initial_conditions_pf.append(f_line.replace('\n','').strip())
                                    
                            # get the htn
                            if "HTN" in child.body.contents[0]:
                                if "ordered" in child.body.contents[0]:
                                    self.flag_ordering = 'no'
                                temp_list = child.body.contents[0].split("\r\n")
                                # we don't consider the first line
                                for index,ii in enumerate(temp_list[1::]):
                                    
                                    if 'task' in ii:
                                    
                                        task_found = 'no'  
                                        object_found = 'no'
                                        
                                        dummy_string = ii.replace('task','').replace('('.format(index),'')[1::]         
                                        dummy_string = dummy_string.replace(')'.format(index),'').strip()
                                        dummy_list = dummy_string.split()
                                      
                                        for task in self.task_list:
                                            if dummy_list[0] == task['name']:
                                                task_found = 'yes'
                                                for hddl_object in dummy_list[1::]:
                                                    object_found = 'no'
                                                    for object_element in self.problem_file_object+ problem_file_object_mutant:
                                                        if hddl_object.lower() in object_element.lower():
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
                                        else:
                                            htn_tasks.append(ii)
                                
                        
                        # Maybe you may have other initial conditions as comment or list --> Implement in the future



                temporary_general_dictionary["initial_conditions"] = [x for x in initial_conditions_pf]
                temporary_general_dictionary["htn"] = [x for x in htn_tasks]
                temporary_general_dictionary["problem_file_objects_mutant"] = [x for x in problem_file_object_mutant]

                
                
                # Hierachie of main tasks
                if self.flag_ordering != 'no':
                    functions_with_incoming_edge = []
                    functions_with_outcoming_edge = []
                    for yy in mission_tasks:
                        for kk in self.edge_list:
                            if 'incoming_edge' in yy and yy['incoming_edge'] == kk['xmi:id']:
                                for uu in mission_tasks:
                                    if uu['xmi:id'] == kk['input']:
                                        functions_with_incoming_edge.append(yy)
                                        yy['previous_action'] = kk['input']
                            
                                
                            if 'outgoing_edge' in yy and yy['outgoing_edge'] == kk['xmi:id']:
                                for uu in mission_tasks:
                                    if uu['xmi:id'] == kk['output']:
                                        functions_with_outcoming_edge.append(yy)
                                        yy['following_action'] = kk['output']
                    
                    ordered_mission_tasks = []
                    for yy in mission_tasks:
                        if yy not in functions_with_incoming_edge and yy in functions_with_outcoming_edge:
                            yy['order'] = 0
                        elif yy in functions_with_incoming_edge and yy not in functions_with_outcoming_edge:
                            yy['order'] = len(mission_tasks) - 1
             
                    flag = 0 
                    counter = 0
                    
                    while flag == 0:
                        for yy in mission_tasks:
                            if 'order' in yy and yy['order'] != len(mission_tasks):
                                # check the next element that should be there
                                for uu in mission_tasks:
                                    if'previous_action'in uu and uu['previous_action'] == yy['xmi:id']:
                                        uu['order'] = yy['order'] + 1 
                            elif 'order' in yy and yy['order'] == len(mission_tasks): 
                                pass
                        
                            if 'order' in yy:
                                counter = counter + 1
                        
                        if counter == len(mission_tasks):
                            flag = 1
                        else:
                            counter = 0
                        
                    # Sort actions based on the ordering    
                    mission_tasks.sort(key = ProblemDefinition.get_order) 
                    temporary_general_dictionary["mission_tasks"] = [x for x in mission_tasks]
                
                
                if htn_tasks != [] and self.flag_ordering == 'yes':
                    ordering_task_network = []
                    for index,ii in enumerate(htn_tasks):
                        dummy_string = ii.replace('task{}('.format(index),'')         
                        dummy_string = dummy_string.replace(')'.format(index),'') 
                        dummy_list_1 = dummy_string.split()
                        task_to_compare_1 = dummy_list_1[0]
                        for index,jj in enumerate(htn_tasks):
                            dummy_string = jj.replace('task{}('.format(index),'') 
                            dummy_string = dummy_string.replace(')'.format(index),'') 
                            dummy_list_2 = dummy_string.split() 
                            task_to_compare_2 = dummy_list_2[0]
                            for kk in mission_tasks:
                                if task_to_compare_1 == kk['name']:
                                    task_number_1 = kk['order']
                                if task_to_compare_2 == kk['name']:
                                    task_number_2 = kk['order']
                        if task_number_1 < task_number_2:
                            dummy_string_1 = ii.split('(')
                            dummy_string_2 = jj.split('(')
                            ordering_task_network.append('(< {} {})'.format(dummy_string_1[0], dummy_string_2[0]))
                        if task_number_2 < task_number_1:
                            dummy_string_1 = ii.split('(')
                            dummy_string_2 = jj.split('(')
                            ordering_task_network.append('(< {} {})'.format(dummy_string_1[0], dummy_string_2[0]))       
            
                    temporary_general_dictionary["htn_order"] = [x for x in ordering_task_network]
                    ordering_task_network = []
                else:
                    temporary_general_dictionary["htn_order"] = []
                    

             
                self.general_mission_dictionary.append(temporary_general_dictionary)  
                temporary_general_dictionary = {}
                mission_tasks = []
                htn_tasks = []
                problem_file_object_mutant = []
                initial_conditions_pf = []
                number_of_problems = number_of_problems + 1
        
        
        self.problem_definition_output["log_file_general_entries"] = self.log_file_general_entries
        self.problem_definition_output["problem_file_object"] = self.problem_file_object
        self.problem_definition_output["mission_dictionary"] = self.general_mission_dictionary
        


        return self.problem_definition_output
        
    def ProblemFileWriting (self):
        
        for element in self.general_mission_dictionary:
        
            file = open(self.d_now + '//outputs//' + element["name"],'w')
            file.write('(define ')
            file.write(' (domain {}) \n'.format(self.domain_name).lower())
            # Objects
            file.write('\t (:objects \n')
            for ii in element["problem_file_objects_static"]:
                file.write('\t\t{}\n'.format(ii.lower()))
            for ii in element["problem_file_objects_mutant"]:
                file.write('\t\t{}\n'.format(ii.lower()))
            file.write('\t )\n\n')
            # Hierarchical Task Network
            file.write('\t :htn( \n')
            file.write('\t\t :parameters () \n')
            
            if self.flag_ordering == 'yes':
                file.write('\t\t :subtasks (and \n')
                for ii in element["htn"]:
                    file.write('\t\t\t({})\n'.format(ii))
                
                file.write('\t\t )\n\n')
                #Ordering
                file.write('\t\t :ordering (and \n')
                for ii in element["htn_order"]:
                    file.write('\t\t\t{}\n'.format(ii.lower()))
                
                file.write('\t\t )\n\n')
                
                #close hierarchical task network
                file.write('\t )\n\n')
            else:
                file.write('\t\t :ordered-subtasks (and \n')
                for ii in element["htn"]:
                    file.write('\t\t\t({})\n'.format(ii))
                
                file.write('\t\t )\n\n')
                
                #close hierarchical task network
                file.write('\t )\n\n')                
            
            # Initial Conditions
            file.write('\t (:init \n')
            for ii in element["initial_conditions"]:
                file.write('\t\t{}\n'.format(ii.lower()))        
            file.write('\t )\n\n')
            # end of the file
            file.write(')')        