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
class FeedbackDefinition():
    def __init__(self, domain_name, parsed_dictionary, domain_file_elements, problem_file_elements, feedback_name, d_now = os.getcwd(),  debug = 'on'):
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
        # Log file general entries
        self.log_file_general_entries = problem_file_elements["log_file_general_entries"]   
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
        try:
            # see if you have a feedback file
            self.feedback_file_name = feedback_name
        except NameError:
            # if not named if as the self.domain_name
            self.feedback_file_name = domain_file_elements["domain_name"]
        # General Dictionary with all the output from the Feedback File
        self.feedback_output = {}

    def FeedbackFile(self): 
        self.log_file_general_entries.append('------------------------------------------------- \n')
        self.log_file_general_entries.append('Log errors and warnings during the Feedback generation: \n')
        self.log_file_general_entries.append('------------------------------------------------- \n')
        
        try:
            self.hddl_type_list
        except NameError:
            self.hddl_type_list = []        

        # Predicates--> self.predicate_list --> list of predicates --> Already created while parsing the xml file
        # However if I need to use this class alone without the xml file
        try:
            self.predicate_list
        except NameError:
            self.predicate_list = []   
            
        # Task --> self.task_list --> list of task --> Already created while parsing the xml file
        # However if I need to use this class alone without the xml file
        try:
            self.task_list
        except NameError:
            self.task_list = []   
            
        # Method --> self.method_list --> list of methods --> Already created while parsing the xml file
        # However if I need to use this class alone without the xml file   
        try:
            self.method_list
        except NameError:
            self.method_list = []   

        # Action --> self.opaqueAction_list --> list of action --> Already created while parsing the xml file
        # However if I need to use this class alone without the xml file 
        try:
            self.opaqueAction_list
        except NameError:
            self.opaqueAction_list = []   
        
        # self.feedback_file_name --> file from which we start <-- you should directly add it here more than have it as a class instance

        # Section Types
        flag_types = 0
        # Section Predicates
        flag_predicates = 0
        # Section tasks
        flag_task = 0
        # Section method
        flag_method = 0
        # Section  Actions
        flag_action = 0
        
        # Save the requirements
        data_requirements = []
        # Save the types
        data_types = []
        # Save the predicates
        data_predicates = []
        # Save the tasks
        data_tasks = []
        temporary_task_list = []
        # Save the methods
        data_methods = []
        temporary_method_list = []
        # Save the actions
        data_actions = []
        temporary_action_list = []
        
        # create a feedback lists to get the new requirements, types, predicates, tasks, methods and actions
        # Requirements
        self.hddl_requirement_feedback = []
        # Types --> self.hddl_type_feedback --> Already created while parsing the xml file
        # However if I need to use this class alone without the xml file
        try:
            self.hddl_type_feedback
        except NameError:
            self.hddl_type_feedback = []
        # Predicates
        self.predicate_list_feedback = []
        # Tasks
        self.task_list_feedback =[]
        # Methods
        self.method_list_feedback =[]
        # Actions
        self.opaqueAction_list_feedback =[]
        
        
        # Read the feedback file and start splitting requirements, types, predicates, tasks, methods and actions!
        with open(self.d_now + '//inputs//' + self.feedback_file_name, 'r') as f:
            feedback_file_lines = f.readlines()
            for index,ii in enumerate(feedback_file_lines):
                line = ii.replace("\n", '').replace("\t",'').strip()
                if index+1< len(feedback_file_lines):
                    next_line = feedback_file_lines[index+1].replace("\n", '').replace("\t",'').strip()
                else :
                    next_line = ''
                
                if ':requirements' in line:
                    data_requirements.append(line)
                
                if ':types' in line:
                    flag_types = 1 
                if flag_types == 1:
                    # this if is not added to the previous so that we can activate the out condition "if ':predicates' in next_line"
                    # same for the other "definitions", or "HDDL classes"
                    if line != '':
                        data_types.append(line)
                    if ':predicates' in next_line:
                       flag_types = 0 
                       
                if ':predicates' in line:
                    flag_predicates = 1 
                if flag_predicates == 1:
                    if line != '':
                        data_predicates.append(line)
                    if ':method' in next_line or ':action' in next_line or ':task' in next_line:
                       flag_predicates = 0 
                
                if ':task' in line and flag_method == 0:
                    flag_task = 1 
                if flag_task == 1:
                    if line != '':
                        temporary_task_list.append(line)
                    if ':method' in next_line or ':action' in next_line or ':task' in next_line:
                       flag_task = 0  
                       data_tasks.append([x for x in temporary_task_list])
                       temporary_task_list.clear()
                
                if ':method' in line:
                    flag_method = 1 
                if flag_method == 1:
                    if line != '':
                        temporary_method_list.append(line)
                    if ':method' in next_line or ':action' in next_line:
                       flag_method = 0  
                       data_methods.append([x for x in temporary_method_list])
                       temporary_method_list.clear()        
                       
                if ':action' in line:
                    flag_action = 1 
                if flag_action == 1:
                    if line != '':
                        temporary_action_list.append(line)
                    if ':method' in next_line or ':action' in next_line or ':task' in next_line:
                       flag_action = 0  
                       data_actions.append([x for x in temporary_action_list])
                       temporary_action_list.clear()    
                    
        # To keep into account the last action in the file as well
        data_actions.append([x for x in temporary_action_list])
        # For all the "HDDL classes", we will analyse only the different instances in respect to the one from the xml file
        # In the log file - we will put ony the feedback instances.
        # The function to write the xml file derived from this analysis need still to be written! I hope to have time soon!
        
        
        flag_type = 0 
        # Get the types different from the ones in the Papyrus xml file
        for ii in data_types:
            if ii != '(:types' and ii != ')':
                for jj in self.hddl_type_list:
                    if ii.split('-')[0].strip() != jj['name'] and flag_type == 0:
                        flag_type = 0
                    if ii.split('-')[0].strip() == jj['name']:
                        flag_type = 1
                if flag_type != 1:
                    self.hddl_type_feedback.append({'name': ii.split('-')[0].strip(),'xmi:id': str(uuid.uuid1())})
                
        # Get the predicates!                
        for ii in data_predicates:
            
            if ii != '(:predicates' and ii != ')':
                if ii.replace('(','').replace(')','').replace(" ", "") not in [jj.replace('(','').replace(')','').replace(" ", "") for jj in self.predicate_list]:
                    self.predicate_list_feedback.append(ii.replace('(','').replace(')',''))
                    
        
        # Store the parameters of the model
        temp_param_list = []
        task_name = ''
        counter = 0
        parameters = []
        flag_parameter = 0
        check = 0
        
        # for all the task in data_task (i) extract name and parameters, (ii) create a xmi:id
        for task in data_tasks:
            for ii in task:
                if ':task' in ii:
                    task_name = ii.split()[1].strip()
                    check = 1
                if ':parameters' in ii:
                    parameters = ii.replace('(','').replace(')','').replace(":parameters", "").replace(" ", "").split("?")[1::]
                    check = 2
                
                if check == 2:
                    check = 0
                    for jj in self.task_list:
                        if jj['name'] == task_name:
                            for parameter in parameters:
                                if parameter in [uu.replace(" ", "") for uu in jj['parameters']]:
                                    flag_parameter = flag_parameter + 1
                            break
                            
                    
                            
                    if flag_parameter != len(jj['parameters']):
                        self.task_list_feedback.append(task)
                    else: 
                        if self.debug == 'on':
                            print("ok: {}".format(task_name))

                    flag_parameter = 0
                
        # for all the method in method_actions (i) extract name and parameters,(ii) extract preconditions and ordered subtasks, (iii) create a xmi:id
        temp_param_list = []
        method_name = ''
        task_name = ''
        flag_method = 0
        counter = 0
        
        parameters = []
        preconditions = []
        
        check = 0
        flag_parameter = 0
        flag_preconditions = 0
        flag_subtasks = 0
        store_preconditions = []
        store_tasks = []
        flag_precondition = 0
        flag_task = 0
        
        for method in data_methods:
            for ii in method:
                if ':method' in ii:
                    method_name = ii.split()[1].strip()
                    flag_subtasks = 0
                    check = 1
                if ':parameters' in ii:
                    parameters = ii.replace('(','').replace(')','').replace(":parameters", "").replace(" ", "").split("?")[1::]
                    check = 2
                if ':precondition' in ii:
                    flag_preconditions = 1
                if ':subtasks' in ii:
                    flag_preconditions = 0
                    flag_subtasks = 1
                    
                if ':ordering' in ii:
                    flag_subtasks = 0
                    
                if flag_preconditions == 1 and ':precondition' not in ii and ':subtasks' not in ii and ii != ')':
                    store_preconditions.append(ii)
                    check = 3
                
                if flag_subtasks == 1 and ':subtasks' not in ii and ii != ')':
                    store_tasks.append(ii)
                    check = 4
                
            if check >= 3:
                check = 0
                preconditions = store_preconditions
                substasks = store_tasks
                    
                    
                for jj in self.method_list:
                    if jj['name'] == method_name:
                        for parameter in parameters:
                            if parameter in [uu.replace(" ", "") for uu in jj['parameters']]:
                                flag_parameter = flag_parameter + 1
                        for precondition in preconditions:
                            if precondition.replace(" ", "") in [uu.replace(" ", "") for uu in jj['preconditions']]:
                                flag_precondition = flag_precondition + 1
                        
                        for task in self.opaqueAction_list:
                            for method_task in jj['ordered_tasks']:
                                if method_task == task['xmi:id']:
                                    for subtask in substasks:
                                        if task['name'] in subtask:
                                            flag_task = flag_task + 1
                        break
                
                            
                if flag_parameter != len(jj['parameters']) or flag_precondition != len(jj['preconditions']) or flag_task != len(jj['ordered_tasks']) :
                    self.method_list_feedback.append(method)
                else: 
                    if self.debug == 'on':
                        print("ok: {}".format(method_name))
                flag_parameter = 0
                flag_precondition = 0
                flag_task = 0
                store_tasks = []
                store_preconditions = []
                 

        # for all the actions in data_actions (i) extract name and parameters,(ii) extract preconditions and effects, (iii) create a xmi:id
        temp_param_list = []
        action_name = ''
        flag_action = 0
        counter = 0
        parameters = []
        preconditions = []
        effects = []
        flag_effects = 0
        flag_precondition = 0
        flag_effect = 0
        
        # for all the task in data_task (i) extract name and parameters, (ii) create a xmi:id
        for action in data_actions:
            for ii in action:
                if ':action' in ii:
                    action_name = ii.split()[1].strip()
                    check = 1
                    flag_effects = 0
                if ':parameters' in ii:
                    parameters = ii.replace('(','').replace(')','').replace(":parameters", "").replace(" ", "").split("?")[1::]
                    check = 2
                if ':precondition' in ii:
                    flag_preconditions = 1
                    
                if flag_preconditions == 1 and ':precondition' not in ii and ':effect' not in ii and ii != ')':
                    # Just remove all the paranteses and make a new string
                    precondition_str = ii.replace(')','').replace('(','')
                    precondition_str = '{}'.format(precondition_str)
                    preconditions.append(precondition_str)
                    check = 3
                
                if ':effect' in ii:
                    flag_preconditions = 0
                    flag_effects = 1
                
                if flag_effects == 1  and ':effect' not in ii and ii != ')':
                    # Just remove all the paranteses and make a new string
                    effect_str = ii.replace(')','').replace('(','')
                    effect_str = '{}'.format(effect_str)
                    effects.append(effect_str) 
                    check = 4
                
                
            if check == 4:
                check = 0   
                flag_effects = 0                 
                    
                for jj in self.opaqueAction_list:
                    if jj['name'] == action_name:
                        for parameter in parameters:
                            if parameter in [uu.replace(" ", "") for uu in jj['parameters']]:
                                flag_parameter = flag_parameter + 1
                        for precondition in preconditions:
                            if precondition.replace(" ", "") in [uu.replace(" ", "").replace(')','').replace('(','') for uu in jj['preconditions']]:
                                flag_precondition = flag_precondition + 1
                        for effect in effects:
                            if effect.replace(" ", "").replace(')','').replace('(','') in [uu.replace(" ", "").replace(')','').replace('(','') for uu in jj['effects']]:
                                flag_effect = flag_effect + 1                        

                        break
                
                            
                if flag_parameter != len(jj['parameters']) or flag_precondition != len(jj['preconditions']) or flag_effect != len(jj['effects']) :
                    self.opaqueAction_list_feedback.append(action)
                else: 
                    if self.debug == 'on':
                        print("ok: {}".format(action_name))
                flag_parameter = 0
                flag_effect = 0
                flag_precondition = 0
                flag_task = 0
                effects = []
                preconditions = []            
        
        self.feedback_output["log_file_general_entries"] = self.log_file_general_entries
        self.feedback_output["hddl_requirement_feedback"] = self.hddl_requirement_feedback
        self.feedback_output["hddl_type_feedback"] = self.hddl_type_feedback
        self.feedback_output["predicate_list_feedback"] = self.predicate_list_feedback
        self.feedback_output["task_list_feedback"] = self.task_list_feedback
        self.feedback_output["method_list_feedback"] = self.method_list_feedback
        self.feedback_output["opaqueAction_list_feedback"] = self.opaqueAction_list_feedback
        self.feedback_output["feedback_file_name"] = self.feedback_file_name
            
        return self.feedback_output
            
            
                
    def FeedbackLogFileWriting(self):
        file = open(self.d_now + '//outputs//' + datetime.now().strftime("%Y_%m_%d-%I_%M_%S")+ 'Feedback.txt','w')
        file.write('Feedback Log File \n')        
        file.write('This file record all the discrepancy of the Papyrus model and/or the feedback from HDDL Domain File \n')
        file.write('------------------------------------------------- ')
        file.write('The following information shows discrepancies between the expected input and the real one \n')
        for ii in self.log_file_general_entries:
            file.write(ii)
        file.write('------------------------------------------------- ')
        file.write('The following information is missing in the Papyrus module \n')
        # Missing Requirements:
        file.write('\t Possible Missing or Modified Requirements: \n')
        for ii in self.hddl_requirement_feedback:
            file.write('\t\t {} \n'.format(ii))        
        # Missing Types:
        file.write('\t Possible Missing or Modified Types: \n')
        for ii in self.hddl_type_feedback:
            file.write('\t\t {} \n'.format(ii))
        # Missing Predicates:
        file.write('\t Possible Missing or Modified Predicates: \n')
        for ii in self.predicate_list_feedback:
            file.write('\t\t {} \n'.format(ii))
        # Missing Tasks:
        file.write('\t Possible Missing or Modified Tasks: \n')
        for ii in self.task_list_feedback:
            file.write('\t\t {} \n'.format(ii[0]))
        # Missing Methods:
        file.write('\t Possible Missing or Modified Methods: \n')
        for ii in self.method_list_feedback:
            file.write('\t\t {} \n'.format(ii[0]))
        # Missing Methods:
        file.write('\t Possible Missing or Modified Actions: \n')
        for ii in self.opaqueAction_list_feedback:
            file.write('\t\t {} \n'.format(ii[0]))