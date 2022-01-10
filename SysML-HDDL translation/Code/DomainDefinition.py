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
class DomainDefinition():
    def __init__(self, domain_name, parsed_dictionary, task_parameters = 'common', flag_ordering_file = 'yes', method_precondition_from_action = 'yes', d_now = os.getcwd(),  debug = 'on'):

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
        # All the packaged elements
        self.b_packagedElement = parsed_dictionary["b_packagedElement"]
        # The rules of the XML file are constraints. They are used to define the task parameters
        self.b_ownedRules = parsed_dictionary["b_ownedRules"]
        # Requirement list for the specific domain file
        self.requirement_list_domain_file = parsed_dictionary["requirement_list_domain_file"]
        # Type list
        self.hddl_type_list = parsed_dictionary["hddl_type_list"]
        # HighLevel UseCase list - Tasks
        self.task_list = parsed_dictionary["task_list"]
        # Edges List 
        self.edge_list = parsed_dictionary["edge_list"]
        # Dependencies in the UseCase
        self.dependencies_list = parsed_dictionary["dependencies_list"]
        # Log file general entries
        self.log_file_general_entries = parsed_dictionary["log_file_general_entries"]        
        # Methods UseCase list - Tasks
        self.method_list = []
        # OpaqueAction List
        self.opaqueAction_list = []
        # Parameters List
        self.all_predicates_list = []
        # Method Input Predicate List
        self.method_input_predicate_list = []
        # Method Output Predicate List
        self.method_output_predicate_list = []
        # Methos input types List
        self.method_input_types_list = []
        #Action Inputs
        self.opaqueAction_input_list = []
        #Action Outputs 
        self.opaqueAction_output_list = []
        # Final list of action without doubles
        self.final_opaque_action_list = []
        # feedback vector:
        self.hddl_type_feedback = []
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
        self.method_precondition_from_action = method_precondition_from_action
        # General Dictionary with all the output from the Domain File Creation 
        self.domain_definition_output = {}

    # Get out the elements of the Problem File
    def get_order(task):
        return task.get('order')
        
    # Get out the elements of the Domain File
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
        method_input_predicate_list_names = []
        method_input_types_list_names = []
        self.method_Actions = []
        # The packagedElements are: Packages, Actors, UseCases, Classes
        
        # you can check is the packagedElement has the "Functions" package as parent
        for uu in self.b_packagedElement:
            
            # If the packagedElement is a UseCase
            # Just consider the inputs in the DomainDefinition Folder (or any folder that is defined by the Requirements)
            """STILL TO IMPLEMET - REASONING ON THE TAGS BASED ON THE PACKAGE DIAGRAM"""
            
            # We are just considering the Domain File entries here! 
            if uu['xmi:type'] == 'uml:UseCase' and uu.parent.parent['name'] == 'DomainDefinition':
                
                # Look at its children and find...
                for index,ii in enumerate(uu.children):
                
                    # Find the methods
                    # try: 
                        # Check the sub-UseCases that can be methods: double check on the type 'uml:UseCase' (considered as attribute) and the tag name 'ownedUseCase'
                        if not isinstance(ii, str) and ii.has_attr('xmi:type') and ii['xmi:type'] == 'uml:UseCase' and ii.name == 'ownedUseCase':
                            
                            self.method_list.append({"name": ii['name'], "xmi:id":ii['xmi:id'], "task":uu.get('xmi:id')})  
                            
                            # Look at the children of the method to recognize parameters and opaque actions
                            for jj in ii.descendants:
                                
                                    # Start already dividing predicates(sentences) from the parameters
                                    if not isinstance(jj, str) and jj.has_attr('xmi:type') and jj['xmi:type'] == 'uml:ActivityParameterNode':
                                        
                                        # Create a temporary dictionary with the paramters characteristics
                                        if jj.has_attr('type'):
                                            temp_dict = {"name": jj['name'], "xmi:id":jj['xmi:id'], "type":jj['type'], "method": ii['xmi:id'], "task":uu.get('xmi:id')} 
                                        
                                        else:
                                            # if we don't have a type - we can give a type name based on the amount of words 
                                            temp_dict = {"name": jj['name'], "xmi:id":jj['xmi:id'], "type":" ", "type_name": " ","method": ii['xmi:id'], "task":uu.get('xmi:id')} 
                                        
                                        # Assign to each ActivityParameter a Type
                                        for kk in self.hddl_type_list:
                                            if kk['xmi:id'] == temp_dict['type']:
                                                temp_dict["type_name"] = kk["name"]    
                                                
                                        # Check if the attribute has a type! - if it doesn't just assign the name as type!
                                        if 'type_name' in temp_dict and temp_dict['type_name'] == " " and len(temp_dict["name"].split()) <= 1:
                                            temp_dict["type_name"] = jj['name']
                                            id_uuid = str(uuid.uuid1())
                                            self.hddl_type_list.append({"name": jj['name'], "xmi:id": id_uuid})
                                            self.hddl_type_feedback.append({"name": jj['name'], "xmi:id": id_uuid})
                                            if self.debug == 'on':                                            
                                                print('No predefined type for {}. Add it on Papyrus!'.format(temp_dict.get('name')))
                                            self.log_file_general_entries('\t\t No predefined type for {}. We added as its own type \n'.format(temp_dict.get('name')))
                                        
                                        # Flag the predicates
                                        if 'type_name' in temp_dict and temp_dict['type_name'] == " " and len(temp_dict["name"].split()) > 1:
                                            temp_dict["type_name"] = 'predicate'
                                            
                                        # Check if the attribute has an incoming edge - output
                                        if jj.has_attr('incoming'):
                                            temp_dict["incoming"] = jj["incoming"]   
                                        
                                        # Check if the attribute has an outcoming edge - input
                                        if jj.has_attr('outgoing'):
                                            temp_dict["outgoing"] = jj["outgoing"] 
                                        
                                        # Check if the attribute is a parameters - if yes save it in the method inputs list
                                        if temp_dict["type_name"] != 'predicate' or len(temp_dict["name"].split()) <= 1:
                                            self.method_input_types_list.append(temp_dict)
                                            method_input_types_list_names.append((temp_dict["name"]+'-'+temp_dict["type_name"]).replace(" ", ""))
                                        
                                        # The preconditions are ActivityParameters that have on outgoing edge but no incoming one 
                                        # (if the have an incoming one then they are activated by one on the Opaque Actions)
                                        if 'outgoing' in temp_dict and not('incoming' in temp_dict) and len(temp_dict["name"].split()) > 1:
                                            self.method_input_predicate_list.append(temp_dict)
                                            if self.method_precondition_from_action == 'yes':
                                                method_input_predicate_list_names.append(temp_dict["name"])
                                            # Save all the predicates name to a list 
                                            self.all_predicates_list.append(temp_dict["name"])
                                        
                                        # If the attribute is an output, so it has an incoming edge- save it! :) 
                                        if 'incoming' in temp_dict and len(temp_dict["name"].split()) > 1:
                                            self.method_output_predicate_list.append(temp_dict)
                                            # Save all the predicates name to a list 
                                            self.all_predicates_list.append(temp_dict["name"])
                                        
                                        # If a method has nothing inside however to be realized it needs some parameters! 
                                        # E.g. when you call navigate to a waypoint action but you are already at that waypoint! Look at the example method2
                                        if not('incoming' in temp_dict) and not('outgoing' in temp_dict):
                                            self.method_input_predicate_list.append(temp_dict)
                                            if len(temp_dict["name"].split()) > 1:                                                
                                                 method_input_predicate_list_names.append(temp_dict["name"])
                                                 self.all_predicates_list.append(temp_dict["name"])
                                            if len(temp_dict["name"].split()) <= 1:
                                                self.method_input_types_list.append(temp_dict)
                                                method_input_types_list_names.append((temp_dict["name"]+'-'+temp_dict["type_name"]).replace(" ", ""))
                                            
                                    # Find the atomic actions and Find the tasks in the main task
                                    if not isinstance(jj, str) and jj.has_attr('xmi:type') and (jj['xmi:type'] == 'uml:OpaqueAction' or jj['xmi:type'] == 'uml:CallBehaviorAction') :
                                        # Initialize the ordered tasks in the Method
                                        self.method_list[-1]['ordered_tasks'] = []
                                        # An Opaque action should always have an input and an output! 
                                        self.opaqueAction_list.append({"name": jj['name'], "xmi:type": jj['xmi:type'], "xmi:id":jj['xmi:id'], "incoming_link": jj['incoming'],  "outcoming_link": jj['outgoing'], "method": ii['xmi:id'], "task":uu.get('xmi:id')})  
                                        for kk in jj.children:
                                            # Each Opaque Action has input and outputs defined by xmi:type="uml:InputPin" or xmi:type="uml:OutputPin"
                                            # try:
                                                # If it is an input save it into an input data structure associated to the Action name and ID
                                                if not isinstance(kk, str) and kk.has_attr('xmi:type') and kk['xmi:type'] == 'uml:InputPin':
                                                    self.opaqueAction_input_list.append({"xmi:id":kk['xmi:id'], "action": jj['xmi:id'], "incoming_edge": kk['incoming'], "method": ii['xmi:id'], "task":uu.get('xmi:id')})  
                                                
                                                # If it is an output save it into an output  data structure associated to the Action name and ID
                                                if not isinstance(kk, str) and kk.has_attr('xmi:type') and kk['xmi:type'] == 'uml:OutputPin':
                                                    self.opaqueAction_output_list.append({ "xmi:id":kk['xmi:id'], "action": jj['xmi:id'], "outgoing_edge": kk['outgoing'], "method": ii['xmi:id'], "task":uu.get('xmi:id')}) 
                                                    
                                                    # Check if the outcoming edge has a name or not - Names are used to define the orders of the output
                                                    if (kk.has_attr('name')):
                                                        self.opaqueAction_output_list[-1]["name"] = kk['name']
                                                        # the number of the output is the end value of the string
                                                        self.opaqueAction_output_list[-1]["number"] = ''.join((filter(str.isdigit, self.opaqueAction_output_list[-1].get('name')))) 
                                                
                                    
                                        # self.method_Actions.append(jj['xmi:id'])
                                        self.method_Actions.append({"name": jj['name'], "xmi:type": jj['xmi:type'], "xmi:id":jj['xmi:id'], "incoming_link": jj['incoming'],  "outcoming_link": jj['outgoing']})

     
                            self.method_list[-1]['parameters'] = set(method_input_types_list_names)
                            method_input_types_list_names.clear()
                            # For each method associate the inputs
                            self.method_list[-1]['preconditions'] = [x for x in method_input_predicate_list_names]
                            method_input_predicate_list_names.clear()
                            # Add the tasks to the method list of ordered tasks 
                            # ordered_actions = []
                            # In the next section we study the action order from the method and we save it!
                            # In this case the actions are defined only by their xmi:id - this id will be related to a real action in the next section
                            
                            if self.method_Actions != []:
                            
                                functions_with_incoming_edge = [] 
                                functions_with_outcoming_edge= []
                                for bb in self.method_Actions:
                                    for kk in self.edge_list:
                                        if 'incoming_link' in bb and bb['incoming_link'] == kk['xmi:id']:
                                            for action in self.method_Actions:
                                                if action['xmi:id'] == kk['input']:
                                                    functions_with_incoming_edge.append(bb)
                                                    bb['previous_action'] = kk['input']
                                        if 'outcoming_link' in bb and bb['outcoming_link'] == kk['xmi:id']:
                                            for action in self.method_Actions:
                                                if action['xmi:id'] == kk['output']:
                                                  functions_with_outcoming_edge.append(bb)
                                                  bb['following_action'] = kk['output']  
                                for yy in self.method_Actions:
                                    if yy not in functions_with_incoming_edge and yy in functions_with_outcoming_edge:
                                        yy['order'] = 0
                                    elif yy in functions_with_incoming_edge and yy not in functions_with_outcoming_edge:
                                        yy['order'] = len(self.method_Actions) - 1
                                    elif yy not in functions_with_incoming_edge and yy not in functions_with_outcoming_edge:
                                        yy['order'] = 0
                                
                                flag = 0
                                counter = 0
                                counter_while = 0
                                
                                while flag == 0:
                                    counter_while = counter_while +1
                                    for yy in self.method_Actions:
                                        if 'order' in yy and yy['order'] != len(self.method_Actions):
                                            # check the next element that should be there
                                            for action in self.method_Actions:
                                                if'previous_action'in action and action['previous_action'] == yy['xmi:id']:
                                                    action['order'] = yy['order'] + 1 
                                        elif 'order' in yy and yy['order'] == len(self.method_Actions):
                                            pass
                                        
                                        if 'order' in yy:
                                            counter = counter + 1

                                    
                                    if counter == len(self.method_Actions):
                                        flag = 1
                                    else:
                                        counter = 0
                                    
                                    if counter_while > 50:
                                        flag = 1
                                
                                # Sort actions based on the ordering 
                                self.method_Actions.sort(key = DomainDefinition.get_order)             
                                                            
                            self.method_list[-1]['ordered_tasks'] = [x['xmi:id'] for x in self.method_Actions]
                            self.method_Actions.clear()
                                

        # For each method go back to the opaque action and associate the inputs/outputs and the parameters as well as the types
        temporary_input_list = []
        temporary_output_list = []
        temporary_parameter_list = []
        
        # Look at all the Actions
        for ii in self.opaqueAction_list:
            
            # Look at the inputs' and paramaters predicate to the actions
            for jj in self.opaqueAction_input_list:
                # check the action id
                if jj.get('action') == ii.get('xmi:id'):
                    # Get the incoming edge ID
                    get_Edge_id = jj.get('incoming_edge')
                    for kk in self.edge_list:
                        # check the edges id
                        if kk.get('xmi:id') == get_Edge_id:
                            # get the source of the edge
                            input_edge = kk.get('input')
                            
                            for gg in self.method_input_predicate_list :
                                # in the method predicate list get the name of the predicate
                                if ii['method'] == gg['method'] and gg['xmi:id'] == input_edge:
                                    # Inputs
                                    temporary_input_list.append(gg['name'])
                                    
                            for gg in self.method_input_types_list :
                                # in the method predicate list get the name of the predicate
                                if ii['method'] == gg['method'] and gg['xmi:id'] == input_edge:
                                    # Inputs
                                    temporary_parameter_list.append(gg.get('name')+'-'+gg.get('type_name'))
                    
                    
            # Look at the outputs' predicate to the actions
            for jj in self.opaqueAction_output_list:
                # check the action id
                if jj.get('action') == ii.get('xmi:id'):
                    # Get the incoming edge ID
                    get_Edge_id = jj.get('outgoing_edge')
                    for kk in self.edge_list:
                        # check the edges id
                        if kk.get('xmi:id') == get_Edge_id:
                            # get the source of the edge
                            output_edge = kk.get('output')
                            
                            for gg in self.method_output_predicate_list :
                                # in the method predicate list get the name of the predicate
                                if ii['method'] == gg['method'] and gg['xmi:id'] == output_edge:
                                    # Inputs
                                    temporary_output_list.append(gg.get('name'))           
            
            # if the action has no effect or no parameters print a warning!
            if temporary_output_list == [] and ii['xmi:type'] != 'uml:CallBehaviorAction':
                if self.debug == 'on':
                    print('The action {} has no effects - is there something wrong in the model?'.format(ii['name']))
                self.log_file_general_entries.append('\t\t The action {} has no effects - is there something wrong in the model? \n'.format(ii['name']))
            # if the action has no effect or no parameters print a warning!
            if temporary_parameter_list == []:
                if self.debug == 'on':
                    print('The action {} has no parameters - is there something wrong in the model?'.format(ii['name']))
                self.log_file_general_entries.append('\t\t The action {} has no parameters - is there something wrong in the model? \n'.format(ii['name']))
            # Associate inputs and outputs to the action 
            ii["preconditions"] = [x for x in temporary_input_list]
            ii["effects"] = [x for x in temporary_output_list]
            ii["parameters"] = set([x for x in temporary_parameter_list])
            # Clear the lists
            temporary_input_list.clear() 
            temporary_output_list.clear()
            temporary_parameter_list.clear()
        
        # Check the tasks - if they all have the initial name and the same parameters, inputs and effects then they are one function
        final_opaque_action = []
        # Look at all the Actions
        for action in self.opaqueAction_list:
            
            # Split the name of the action
            name = action['name']
            final_opaque_action.append(name.lower())
            
        # we want the action to have just one occurance
        final_opaque_action_set = set(final_opaque_action)  
        
        for final_action in final_opaque_action_set:
            for action in self.opaqueAction_list:
                if action['name'].lower() == final_action and action['xmi:type'] == 'uml:OpaqueAction':
                    self.final_opaque_action_list.append(action)
                    break
        
        # Task Parameters for task used as :subtask in a method
        for action in self.opaqueAction_list:
            if action ['xmi:type'] == 'uml:CallBehaviorAction':
                for task in self.task_list:
                    if task.get('name') == action.get('name'): 
                        task["parameters"] = set(action.get('parameters'))
       
        # Check if the user defined some constraints in UseCase diagram to get the task parameters
        get_param = []
        flag_found = 0
        for ii in self.b_ownedRules:            
            if ii.parent['name'] == 'DomainDefinition' or ii.parent['name'] == 'UseCase':
                # check that the parameters have a known type!
                dummy_string = ii['name']
                dummy_vector = re.split(' |-', dummy_string)
                
                for uu in self.hddl_type_list:
                    if uu['name'] == dummy_vector[-1]:
                        flag_found = 1
                
                if flag_found != 1:
                    self.hddl_type_list.append(dummy_vector[-1].replace(" ", ""))
                    self.hddl_type_feedback.append(dummy_vector[-1].replace(" ", ""))
                    if self.debug == 'on':
                        print('Plese check your constraints in the UseCase - your type extension for {} was not found in the type folder'.format(ii['name'].replace(" ", "")))
                        print('We added that type - however, please check if that was what you were planning to do!')
                        self.log_file_general_entries.append('\t\t Plese check your constraints in the UseCase - your type extension for {} was not found in the type folder \n'.format(ii['name'].replace(" ", "")))
                
                for jj in self.dependencies_list:
                    flag_found = 0
                    get_param_dict = { "xmi:type":ii['xmi:type'], "xmi:id":ii['xmi:id'], "name":ii['name']}
                    if jj['output'] == ii['xmi:id']:
                        get_param_dict['task'] = jj['input']
                        get_param.append(get_param_dict)
                        # get_param_dict ={}
                        
                
            
        
        task_parameters = []
        # If the task parameters are already defined in the main use case diagram as constraints
        for ii in self.task_list:
            if get_param != []:
                for jj in get_param:
                    if ('task') in jj:
                        if jj['task'] == ii['xmi:id']:
                            task_parameters.append(jj['name'].replace(" ", ""))
            
            if ii["parameters"] == []:
                ii["parameters"] = set([x for x in task_parameters])
                task_parameters.clear()
                
        # If the tasks have no parameter defined --> Get the minimum or the common parameters out of the methods parameters associated to that task
        task_parameters_matrix = []

        for ii in self.task_list:
            if ii["parameters"] == set():
                # Minimum parameters
                if self.task_parameters == 'min':
                    for jj in self.method_list:
                        
                        if ii.get('xmi:id') == jj.get('task'):
                            # for each method check the length of the parameters list - if it longer than the one of the task, leave it like that - if not replace the list
                            if ii["parameters"] != []:
                                if len(ii["parameters"]) >= len(jj.get('parameters')):
                                    # dummy_parameter = [x for x in jj.get('parameters')]
                                    ii["parameters"] = jj.get('parameters')
                            else:
                                ii["parameters"] = jj.get('parameters')
                            
                # Common parameters
                if self.task_parameters == 'common':
                    for jj in self.method_list:
                        
                        if ii.get('xmi:id') == jj.get('task'):
                            # for each method check the length of the parameters list - look if there are common paramaters
                                task_parameters_matrix.append(jj.get('parameters'))     
                    
                    for index, task_param in enumerate(task_parameters_matrix):
                        if index == 0:
                            common_param = task_param
                        elif index == 1:
                            common_param = task_param.intersection(task_parameters_matrix[index-1])
                        else:
                            common_param = task_param.intersection(common_param)
                
                    ii["parameters"] = common_param
                    
        
        # Take the overall predicate list and:
            # search for duplicates and associate the type to each predicate
            # write the predicate on the predicate list
            # always check for duplicates
        
        temporary_predicate = []
        self.predicate_list = []

        
        for ii in self.all_predicates_list:
            # First remove brankets 
            cleaned_predicate = ii.replace('(',' ')
            cleaned_predicate = cleaned_predicate.replace(')',' ')
            # Remove negations  
            cleaned_predicate = cleaned_predicate.replace('not',' ')   
            # Take the predicate and open it:
            cleaned_predicate = cleaned_predicate.split()
            #get the first word of the predicate
            temporary_predicate.append(cleaned_predicate[0])
            # analyse all other words
            for index,jj in enumerate(cleaned_predicate[1::]):
                jj = jj.replace('?',' ').strip()
                flag = 0
                
                for kk in self.method_input_types_list:
                    # if you found a match - break free. Try to find a better way to define this 
                    if jj == kk.get('name') and flag == 0:
                        temporary_predicate.append('?arg{} - {}'.format(index,kk.get('type_name')))
                        flag = 1
            
            #create the predicate final version
            final_predicate= ' '.join(temporary_predicate)
            if len(final_predicate) <= 1:
                
                print('\t\t The predicate {} has no parameters - it has been inserted as it was written - please check it!'.format(jj))
                self.log_file_general_entries.append('\t\t The predicate {} has no parameters - it has been inserted as it was written - please check it!'.format(jj))
                # Final predicate in its original form - there is an error in the format - inform the user
                final_predicate = kk
            
            # We don't consider equality constraints in the predicates
            if not(final_predicate in self.predicate_list) and not('=' in final_predicate):
                self.predicate_list.append(('{}').format(final_predicate))

                
            temporary_predicate.clear()
            
        self.domain_definition_output["domain_name"] = self.domain_name
        self.domain_definition_output["problem_name"] = self.problem_name
        self.domain_definition_output["log_file_general_entries"] = self.log_file_general_entries
        self.domain_definition_output["hddl_type_list"] = self.hddl_type_list
        self.domain_definition_output["predicate_list"] = self.predicate_list
        self.domain_definition_output["task_list"] = self.task_list
        self.domain_definition_output["method_list"] = self.method_list
        self.domain_definition_output["opaqueAction_list"] = self.opaqueAction_list
        self.domain_definition_output["final_opaque_action_list"] = self.final_opaque_action_list
            
        return self.domain_definition_output
            
            
            

    # Write the Domain File
    def DomainFileWriting (self):
        ###################################################################

        # Open/Create the File
        file = open(self.d_now + '//outputs//' + self.domain_name,'w')
        # Start writing on the file
        file.write('(define (domain {}) \n'.format(self.domain_name_simple.lower()))
        # Write requirement
        file.write('\t (:requirements :{}) \n'.format(' :'.join(self.requirement_list_domain_file).lower()))
        #Object Type
        file.write('\t (:types  ')
        for ii in self.hddl_type_list:
            if ii.get('name').strip() != 'predicate':
                file.write('{} '.format(ii.get('name').lower()))
        # End of object type
        file.write(') \n\n')  
        
        # Predicates
        file.write('\t (:predicates \n')
        #Writes Predicates
        for ii in self.predicate_list:
            file.write('\t\t ({}) \n'.format(ii).lower())
        # End of predicates
        file.write('\t) \n\n')   
            
        #Tasks!
        for ii in self.task_list:
            file.write('\t (:task {} \n'.format(ii.get('name')))            
            file.write('\t\t :parameters (?{}) \n'.format(' ?'.join(ii.get('parameters')).lower()))
            file.write('\t\t :precondition ()\n')
            file.write('\t\t :effect ()\n')
            file.write('\t ) \n\n') 
            
        #Methods!
        # Introduce the order in the tasks
        # have just the first word of the parameters
        string_vector = []
        order_vector = []
        file.write('\n')  #space!
        for ii in self.method_list:
            # method name
            file.write('\t (:method {} \n'.format(ii.get('name')))
            # method parameters
            file.write('\t\t :parameters (?{}) \n'.format(' ?'.join(ii.get('parameters')).lower()))
            # method task
            """
            STILL TO IMPLEMENT - Check that the task parameters are effectively method parameters.
                                 If they are not - search for the right parameters in the method
            """
            for jj in self.task_list:
                if jj['xmi:id'] == ii['task']:
                    task_name = jj['name']
                    task_parameters = []
                    for uu in jj['parameters']:
                        regex_pattern ='\w+.'
                        parameters = re.findall(regex_pattern, uu)
                        task_parameters.append(parameters[0].replace('-', ''))
                                        
            file.write('\t\t :task ({} ?{}) \n'.format(task_name, ' ?'.join(task_parameters).lower()))
            # method preconditions
            if ii.get('preconditions') != '':
                file.write('\t\t :precondition (and \n\t\t\t{} \n\t\t) \n'.format(' \n\t\t\t'.join(ii.get('preconditions')).lower()))
            else:
                file.write('\t\t :precondition ()\n')
            counter = 0
            
            # method actions
            if self.flag_ordering_file == 'yes':
                for jj in ii['ordered_tasks']: 
                    for kk in self.opaqueAction_list:
                        if kk['xmi:id'] == jj:
                            # Task Parameters
                            dummy_string = ' '.join(kk['parameters'])
                            dummy_vector = re.split(' |-', dummy_string)
                            # vector[start:end:step]
                            dummy_vector = dummy_vector[0::2]
                            string_vector.append('task{}({} ?{})'.format(counter,kk['name'], ' ?'.join(dummy_vector).lower() ))
                            counter = counter + 1
                        if counter > 1 and '(< task{} task{})'.format(counter-2, counter-1) not in order_vector:
                            # For each task check incoming and outcoming links
                            order_vector.append('(< task{} task{})'.format(counter-2, counter-1))

            if self.flag_ordering_file == 'no':
                for jj in ii['ordered_tasks']: 
                    for kk in self.opaqueAction_list:
                        if kk['xmi:id'] == jj:
                            # Task Parameters
                            dummy_string = ' '.join(kk['parameters'])
                            dummy_vector = re.split(' |-', dummy_string)
                            # vector[start:end:step]
                            dummy_vector = dummy_vector[0::2]
                            if kk["parameters"] != set():
                                string_vector.append('task{}({} ?{})'.format(counter,kk['name'], ' ?'.join(dummy_vector).lower() ))
                            else:
                                string_vector.append('task{}({})'.format(counter,kk['name']))
                            counter = counter + 1

                            
            if self.flag_ordering_file == 'yes':                            
                if counter != 0 and counter != 1:
                    file.write('\t\t :subtasks (and \n')
                    file.write('\t\t\t{}\n'.format('\n\t\t\t'.join(string_vector)))
                    file.write('\t\t ) \n')
                    file.write('\t\t :ordering (and \n')
                    file.write('\t\t\t{}\n'.format(' \n\t\t\t'.join(order_vector).lower()))
                    file.write('\t\t ) \n')
                    string_vector.clear()
                    order_vector.clear()
                elif counter == 1:
                    file.write('\t\t :subtasks (and \n')
                    file.write('\t\t\t {}\n'.format(' \n\t\t\t'.join(string_vector)))
                    file.write('\t\t ) \n')
                    string_vector.clear()
                    order_vector.clear()
                else:
                    file.write('\t\t :subtasks () \n')
                    string_vector.clear()
                    order_vector.clear()

            if self.flag_ordering_file == 'no':
                if counter != 0 and counter != 1:
                    file.write('\t\t :ordered-subtasks (and \n')
                    file.write('\t\t\t{}\n'.format('\n\t\t\t'.join(string_vector)))
                    file.write('\t\t ) \n')
                    string_vector.clear()
                    order_vector.clear()
                elif counter == 1:
                    file.write('\t\t :ordered-subtasks (and \n')
                    file.write('\t\t\t {}\n'.format(' \n\t\t\t'.join(string_vector)))
                    file.write('\t\t ) \n')
                    string_vector.clear()
                    order_vector.clear()
                else:
                    file.write('\t\t :ordered-subtasks () \n')
                    string_vector.clear()
                    order_vector.clear()                
                
                
                
            file.write('\t ) \n\n') 

        #Actions
        file.write('\n')  #space!
        for ii in self.final_opaque_action_list:

            file.write('\t(:action {} \n'.format(ii.get('name')))     
            if ii['parameters'] != set():
                file.write('\t\t :parameters (?{}) \n'.format(' ?'.join(ii.get('parameters')).lower()))
            else:
                file.write('\t\t :parameters () \n')
            if ii.get('preconditions') != []:
                file.write('\t\t :precondition (and \n\t\t\t{})\n'.format(' \n\t\t\t'.join(ii.get('preconditions')).lower()))
            else:
                file.write('\t\t :precondition ()\n')
            if ii.get('effects') != []:
                file.write('\t\t :effect (and \n\t\t\t{})\n'.format(' \n\t\t\t'.join(ii.get('effects')).lower()))
            else:
                file.write('\t\t :effect ()\n')
                        
            file.write('\t) \n\n') 
        
        # end of the file
        file.write(')')