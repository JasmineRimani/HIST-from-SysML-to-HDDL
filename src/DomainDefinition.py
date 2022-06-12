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
    # Get the difference bewteen two lists
    def Diff(li1, li2):
        li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
        return li_dif
        
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
        for element in self.b_packagedElement:
            
            # If the packagedElement is a UseCase
            # Just consider the inputs in the DomainDefinition Folder (or any folder that is defined by the Requirements)
            """STILL TO IMPLEMET - REASONING ON THE TAGS BASED ON THE PACKAGE DIAGRAM"""
            
            # We are just considering the Domain File entries here! 
            if element['xmi:type'] == 'uml:UseCase' and element.parent.parent['name'] == 'DomainDefinition':
                
                # Look at its children and find...
                for index,e_child in enumerate(element.children):
                 
                        # Check the sub-UseCases that can be methods: double check on the type 'uml:UseCase' (considered as attribute) and the tag name 'ownedUseCase'
                        if not isinstance(e_child, str) and e_child.has_attr('xmi:type') and e_child['xmi:type'] == 'uml:UseCase' and e_child.name == 'ownedUseCase':
                            
                            self.method_list.append({"name": e_child['name'], "xmi:id":e_child['xmi:id'], "task":element.get('xmi:id')})  
                            
                            # Look at the children of the method to recognize parameters and opaque actions
                            for descendant in e_child.descendants:
                                
                                    # Start already dividing predicates(sentences) from the parameters
                                    if not isinstance(descendant, str) and descendant.has_attr('xmi:type') and descendant['xmi:type'] == 'uml:ActivityParameterNode':
                                        
                                        # Create a temporary dictionary with the parameters characteristics
                                        if descendant.has_attr('type'):
                                            temp_dict = {"name": descendant['name'], "xmi:id":descendant['xmi:id'], "type":descendant['type'], "method": e_child['xmi:id'], "task":element.get('xmi:id')} 
                                        
                                        else:
                                            # if we don't have a type - we can give a type name based on the amount of words 
                                            temp_dict = {"name": descendant['name'], "xmi:id":descendant['xmi:id'], "type":" ", "type_name": " ","method": e_child['xmi:id'], "task":element.get('xmi:id')} 
                                        
                                        # Assign to each ActivityParameter a Type
                                        for hddl_type in self.hddl_type_list:
                                            if hddl_type['xmi:id'] == temp_dict['type']:
                                                temp_dict["type_name"] = hddl_type["name"]    
                                                
                                        # Check if the attribute has a type! - if it doesn't just assign the name as type!
                                        if 'type_name' in temp_dict and temp_dict['type_name'] == " " and len(temp_dict["name"].split()) <= 1:
                                            temp_dict["type_name"] = descendant['name']
                                            id_uuid = str(uuid.uuid1())
                                            self.hddl_type_list.append({"name": descendant['name'], "xmi:id": id_uuid})
                                            self.hddl_type_feedback.append({"name": descendant['name'], "xmi:id": id_uuid})
                                            if self.debug == 'on':                                            
                                                print('No predefined type for {}. Add it on Papyrus!'.format(temp_dict.get('name')))
                                            self.log_file_general_entries('\t\t No predefined type for {}. We added as its own type \n'.format(temp_dict.get('name')))
                                        
                                        # Flag the predicates
                                        if 'type_name' in temp_dict and temp_dict['type_name'] == " " and len(temp_dict["name"].split()) > 1:
                                            temp_dict["type_name"] = 'predicate'
                                            
                                        # Check if the attribute has an incoming edge - output
                                        if descendant.has_attr('incoming'):
                                            temp_dict["incoming"] = descendant["incoming"]   
                                        
                                        # Check if the attribute has an outcoming edge - input
                                        if descendant.has_attr('outgoing'):
                                            temp_dict["outgoing"] = descendant["outgoing"] 
                                        
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
                                    if not isinstance(descendant, str) and descendant.has_attr('xmi:type') and (descendant['xmi:type'] == 'uml:OpaqueAction' or descendant['xmi:type'] == 'uml:CallBehaviorAction') :
                                        # Initialize the ordered tasks in the Method
                                        self.method_list[-1]['ordered_tasks'] = []
                                        # An Opaque action should always have an input and an output! 
                                        self.opaqueAction_list.append({"name": descendant['name'], "xmi:type": descendant['xmi:type'], "xmi:id":descendant['xmi:id'], "incoming_link": descendant['incoming'],  "outcoming_link": descendant['outgoing'], "method": e_child['xmi:id'], "task":element.get('xmi:id')}) 
                                        # if the action is a compound action - a task we should add its behavior to avoid to the important information in opaqueAction
                                        if descendant['xmi:type'] == 'uml:CallBehaviorAction':
                                            self.opaqueAction_list[-1]['behavior'] = descendant['behavior']
                                        
                                        for d_child in descendant.children:
                                            # Each Opaque Action has input and outputs defined by xmi:type="uml:InputPin" or xmi:type="uml:OutputPin"
                                            # try:
                                                # If it is an input save it into an input data structure associated to the Action name and ID
                                                if not isinstance(d_child, str) and d_child.has_attr('xmi:type') and d_child['xmi:type'] == 'uml:InputPin':
                                                    self.opaqueAction_input_list.append({"xmi:id":d_child['xmi:id'], "action": descendant['xmi:id'], "incoming_edge": d_child['incoming'], "method": e_child['xmi:id'], "task":element.get('xmi:id')})  
                                                
                                                # If it is an output save it into an output  data structure associated to the Action name and ID
                                                if not isinstance(d_child, str) and d_child.has_attr('xmi:type') and d_child['xmi:type'] == 'uml:OutputPin':
                                                    self.opaqueAction_output_list.append({ "xmi:id":d_child['xmi:id'], "action": descendant['xmi:id'], "outgoing_edge": d_child['outgoing'], "method": e_child['xmi:id'], "task":element.get('xmi:id')}) 
                                                    
                                                    # Check if the outcoming edge has a name or not - Names are used to define the orders of the output
                                                    # In HDDL the order of the oputput doesn't matter!!!!
                                                    # if (kk.has_attr('name')):
                                                    #     self.opaqueAction_output_list[-1]["name"] = kk['name']
                                                    #     # the number of the output is the end value of the string
                                                    #     self.opaqueAction_output_list[-1]["number"] = ''.join((filter(str.isdigit, self.opaqueAction_output_list[-1].get('name')))) 
                                                
                                    
                                        # self.method_Actions.append(jj['xmi:id'])
                                        self.method_Actions.append({"name": descendant['name'], "xmi:type": descendant['xmi:type'], "xmi:id":descendant['xmi:id'], "incoming_link": descendant['incoming'],  "outcoming_link": descendant['outgoing']})

     
                            # self.method_list[-1]['parameters'] = set(method_input_types_list_names)
                            self.method_list[-1]['parameters'] = [x for x in method_input_types_list_names]
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
                                # For each action in the method_Actions
                                for action_init in self.method_Actions:
                                    # For each edge in the edge_list check if the action has in incoming link
                                    for edge in self.edge_list:
                                        #check if the action has in incoming link
                                        if 'incoming_link' in action_init and action_init['incoming_link'] == edge['xmi:id']:
                                            # If the action has an incoming link - check which is the previous action
                                            for action in self.method_Actions:
                                                if action['xmi:id'] == edge['input']:
                                                    # if the incoming link is an action, add the initial action to the list functions_with_incoming_edge
                                                    functions_with_incoming_edge.append(action_init)
                                                    action_init['previous_action'] = edge['input']
                                        #check if the action has in outcoming link
                                        if 'outcoming_link' in action_init and action_init['outcoming_link'] == edge['xmi:id']:
                                            # If the action has an outcoming link - check which is the next action
                                            for action in self.method_Actions:
                                                if action['xmi:id'] == edge['output']:
                                                    # if the outcoming link is an action, add the initial action to the list functions_with_outcoming_edge
                                                  functions_with_outcoming_edge.append(action_init)
                                                  action_init['following_action'] = edge['output']  
                                for m_action in self.method_Actions:
                                    # Initial action
                                    if m_action not in functions_with_incoming_edge and m_action in functions_with_outcoming_edge:
                                        m_action['order'] = 0
                                    # End action
                                    elif m_action in functions_with_incoming_edge and m_action not in functions_with_outcoming_edge:
                                        m_action['order'] = len(self.method_Actions) - 1
                                    # Just one action in the method
                                    elif m_action not in functions_with_incoming_edge and m_action not in functions_with_outcoming_edge:
                                        m_action['order'] = 0
                                
                                flag = 0
                                counter = 0
                                counter_while = 0
                                M_big = 50 # M_big is used just to exist the while in the wrost conditions
                                
                                while flag == 0:
                                    counter_while = counter_while +1
                                    # Check you action
                                    for action_init in self.method_Actions:
                                        # if this is this an element that have been already ordered
                                        if 'order' in action_init and action_init['order'] != len(self.method_Actions):
                                            # check the next element that should be there to get the order
                                            for action in self.method_Actions:
                                                if'previous_action'in action and action['previous_action'] == action_init['xmi:id']:
                                                    action['order'] = action_init['order'] + 1 
                                        # For now, we don't care about the last action - we know that is the last
                                        elif 'order' in action_init and action_init['order'] == len(self.method_Actions):
                                            pass
                                        
                                        # if the action has been ordered count it 
                                        if 'order' in action_init:
                                            counter = counter + 1

                                    # if all teh actions have been ordered we are good to go!
                                    if counter == len(self.method_Actions):
                                        flag = 1
                                    else:
                                        counter = 0
                                    
                                    # Additional out of while condition to avoid infinite loop
                                    if counter_while > M_big:
                                        flag = 1
                                
                                # Sort actions based on the ordering number you gave them 
                                self.method_Actions.sort(key = DomainDefinition.get_order)             
                                                            
                            self.method_list[-1]['ordered_tasks'] = [x['xmi:id'] for x in self.method_Actions]
                            self.method_Actions.clear()

        # Analyse the predicates - so you can check if the action preconditions and effect of the actions are considered or not
        temporary_predicate = []
        self.predicate_list = []

        for predicate in self.all_predicates_list:
            # First remove brankets 
            cleaned_predicate = predicate.replace('(',' ')
            cleaned_predicate = cleaned_predicate.replace(')',' ')
            # Remove negations  
            cleaned_predicate = cleaned_predicate.replace('not',' ')   
            # Remove random copy or similar -- if you copy and pasted an element on papyrus this can happen!
            cleaned_predicate = cleaned_predicate.replace('_copy',' ')   
            # Take the predicate and open it:
            cleaned_predicate = cleaned_predicate.split()
            #get the first word of the predicate - this can be a equal sign! 
            temporary_predicate.append(cleaned_predicate[0])
            # analyse all other words - therefore you should have them in input_types
            for index_predicate, predicate_atom in enumerate(cleaned_predicate[1::]):
                predicate_atom = predicate_atom.replace('?',' ').strip()
                flag = 0
                
                for index,input_types in enumerate(self.method_input_types_list):
                    # if you found a match - break free. Try to find a better way to define this 
                    if flag == 0 and predicate_atom == input_types.get('name'):
                        temporary_predicate.append('?arg{}-{}'.format(index_predicate,input_types.get('type_name')))
                        flag = 1
                    if index == (len(self.method_input_types_list)-1) and flag != 1:
                        # This entry is missing from the method inputs --> probably an error while writing the domain in Papyrus
                        temporary_predicate.append('?arg{}-{}'.format(index_predicate,predicate_atom))
                        self.log_file_general_entries.append('\t\t The {} is not define in any method input!!!! Probably you need to check the Activity Parameters in Papyrus \n'.format(predicate_atom))
                        if self.debug == 'on':
                            print('The {} is not define in any method input!!!! Probably you need to check the Activity Parameters in Papyrus'.format(predicate_atom))
                        # add this to the methods inputs [method parameters]
                        # First check at which method it is related: 
                        for method_input in self.method_input_predicate_list:
                            if method_input.get("name") == predicate:
                                # then associate the new parameter to the method inputs
                                method_selected = method_input.get("method")
                                for method in self.method_list:
                                    if method.get("xmi:id") ==  method_selected:
                                        # You add the predicate_atom to the method parameters
                                        method.get("parameters").append(predicate_atom)
                                        self.log_file_general_entries.append('\t\t The {} has been added to the parameters of method {}. Please check if that is correct \n'.format(predicate_atom, method["name"]))
                                        if self.debug == 'on':
                                            print('The {} has been added to the parameters of method {}. Please check if that is correct'.format(predicate_atom, method["name"]))
                                        # self.method_list[-1]['parameters'] = set(method_input_types_list_names)
                                        # self.method_list[-1]['parameters'] = [x for x in method_input_types_list_names]
                        # We need to check if this input already exist in the hddl_type list and if it does not exist we add it to the list and have the pop up for the user
                        found_flag = 0 
                        for hddl_type in self.hddl_type_list:
                            if hddl_type["name"] == predicate_atom:
                                temporary_predicate.append('?arg{}-{}'.format(index_predicate,predicate_atom))
                                found_flag = 1
                        if found_flag == 0:
                            id_uuid = str(uuid.uuid1())
                            self.hddl_type_list.append({"name":predicate_atom, "xmi:id": id_uuid})
                            self.hddl_type_feedback.append({"name":predicate_atom, "xmi:id": id_uuid})
                            self.log_file_general_entries.append('t\t The {} is not in the HDDL type list - it has been added to it. Please check if that was your expected result \n'.format(predicate_atom))
                            if self.debug == 'on':
                                print('The {} is not in the HDDL type list - it has been added to it. Please check if that was your expected result'.format(predicate_atom))
                        
            
            #create the predicate final version
            final_predicate = ' '.join(temporary_predicate)

            # We don't consider equality constraints in the predicates
            if not(final_predicate in self.predicate_list) and not('=' in final_predicate):
                self.predicate_list.append(('{}').format(final_predicate))

                
            temporary_predicate.clear()                                

        # For each method go back to the opaque action and associate the inputs/outputs and the parameters as well as the types
        temporary_input_list = []
        temporary_output_list = []
        temporary_parameter_list = []
        
        # Slip the action and the tasks
        # simple_actions_list = []
        # compound_actions_list = []
        
        # Split Actions and Tasks of the method avoiding doubles name - this first analysis is only based on names
        # for entity in self.opaqueAction_list:

        #     flag_double = 0
        #     if entity['xmi:type'] != 'uml:CallBehaviorAction':
        #         if simple_actions_list == []:
        #             simple_actions_list.append(entity)
        #         # the doubles here are linked to same name associated to the same task
        #         for action in simple_actions_list:
        #             if action["name"] == entity['name'] and action["task"] == entity['task']:
        #                 flag_double = 1
        #         # If no doubles are there
        #         if flag_double == 0:
        #             simple_actions_list.append(entity)
        #     else:
        #         if compound_actions_list == []:
        #             compound_actions_list.append(entity)
        #         for task in compound_actions_list:
        #             # Check for doubles --> the check is based on the behavior link that action to a precise task
        #             if entity['behavior'] == task['behavior']:
        #                 flag_double = 1
        #             # If no doubles are there
        #         if flag_double == 0:
        #             compound_actions_list.append(entity)
                
        
        # Now let's define the inputs to the simple actions
        for action in self.opaqueAction_list:
            for action_input in self.opaqueAction_input_list:
                # check the action id
                if action_input.get('action') == action.get('xmi:id'):
                    # Get the incoming edge ID
                    get_Edge_id = action_input.get('incoming_edge')
                    for edge in self.edge_list:
                        if edge['xmi:id'] == get_Edge_id:
                            # get the source of the edge
                            input_edge = edge.get('input')

                            # Look at the method inputs to find the edge's source name
                            for source in self.method_input_types_list :
                                # in the method predicate list get the name of the predicate
                                if action['method'] == source['method'] and source['xmi:id'] == input_edge:
                                    # before this - check if the input is in the predicate list?
                                    temporary_parameter_list.append(source.get('name')+'-'+source.get('type_name'))  
                                    
                            # Look at the method inputs to find the edge's source name
                            for source in self.method_input_predicate_list :
                                # in the method predicate list get the name of the predicate
                                if action['method'] == source['method'] and source['xmi:id'] == input_edge:
                                    # before this - check if the input is in the predicate list?
                                    temporary_input_list.append(source['name'])
            
            # Now let's define the outputs to the simple actions                  
            for action_output in self.opaqueAction_output_list:
                # check the action id
                if action_output.get('action') == action.get('xmi:id'):
                    # Get the incoming edge ID
                    get_Edge_id = action_output.get('outgoing_edge')
                    for edge in self.edge_list:
                        if edge['xmi:id'] == get_Edge_id:
                            output_edge = edge.get('output')
                            for method_output in self.method_output_predicate_list :
                                # in the method predicate list get the name of the predicate
                                if action['method'] == method_output['method'] and method_output['xmi:id'] == output_edge:
                                    # Inputs
                                    temporary_output_list.append(method_output.get('name'))                            

            # The predicates have been all analysed therefore, what you need to analyse is that all the parameters 
            # of the preconditions and effect are considered in the action parameters         
            for input_action in (temporary_input_list + temporary_output_list):
                # take the input predicate - open it
                cleaned_predicate = input_action.replace('(',' ')
                cleaned_predicate = cleaned_predicate.replace(')',' ')
                cleaned_predicate = cleaned_predicate.replace('not',' ') 
                cleaned_predicate = cleaned_predicate.replace('_copy',' ')  
                cleaned_predicate = cleaned_predicate.split()
                for index_predicate, predicate_atom in enumerate(cleaned_predicate[1::]):
                    predicate_atom = predicate_atom.replace('?',' ').strip()
                    flag = 0        
                    # find a match with the action parameters - if not you will have to add the parameter
                    for index,input_type in enumerate(temporary_parameter_list):
                        if flag == 0 and predicate_atom == input_type.split('-')[0]:
                            flag = 1
                        if index == (len(temporary_parameter_list)-1) and flag != 1:
                            for method in self.method_list:
                                if method["xmi:id"] == action["method"]:
                                    first_method = method["name"]
                            if self.debug == 'on':
                                print("The input {} of your predicate {} is not considered in the action. It has been added".format(input_action,input_type))
                                print("Check Action {} and associated method {}".format(action.get("name"), first_method))
                            self.log_file_general_entries.append('\t\t The input {} of your predicate {} is not considered in the action. It has been added \n'.format(input_action,input_type))
                            self.log_file_general_entries.append('\t\t Check Action {} and associated method {} \n'.format(action.get("name"), first_method))
                            # Add this parameter to the action parameters
                            # Check if the parameter is already associate to a HDDL type or not 
                            # If it is not in action parameters it was not listed in the method Activity Parameter so 
                            # it doesn't have an associate native hddl_type_list
                            found_flag = 0 
                            for hddl_type in self.hddl_type_list:
                                if hddl_type["name"] == predicate_atom:
                                    temporary_predicate.append('?arg{}-{}'.format(index_predicate,predicate_atom))
                                    temporary_parameter_list.append('{}-{}'.format(predicate_atom, hddl_type)) 
                                    found_flag = 1
                            if found_flag == 0:
                                id_uuid = str(uuid.uuid1())
                                self.hddl_type_list.append({"name":predicate_atom, "xmi:id": id_uuid})
                                self.hddl_type_feedback.append({"name":predicate_atom, "xmi:id": id_uuid})
                                self.log_file_general_entries.append('\t\t The {} is not in the HDDL type list - it has been added to it. Please check if that was your expected result \n'.format(predicate_atom))
                                if self.debug == 'on':
                                    print('The {} is not in the HDDL type list - it has been added to it. Please check if that was your expected result'.format(predicate_atom))
                                temporary_parameter_list.append(predicate_atom+'-'+predicate_atom)                      


        
            # if the action has no effect or no parameters print a warning!
            if temporary_output_list == [] and action['xmi:type'] != 'uml:CallBehaviorAction':
                if self.debug == 'on':
                    print('The action {} has no effects - is there something wrong in the model?'.format(action['name']))
                self.log_file_general_entries.append('\t\t The action {} has no effects - is there something wrong in the model? \n'.format(action['name']))
            # if the action has no effect or no parameters print a warning!
            if temporary_parameter_list == []:
                if self.debug == 'on':
                    print('The action {} has no parameters - is there something wrong in the model?'.format(action['name']))
                self.log_file_general_entries.append('\t\t The action {} has no parameters - is there something wrong in the model? \n'.format(action['name']))
            # Associate inputs and outputs to the action 
            action["preconditions"] = [x for x in temporary_input_list]
            action["effects"] = [x for x in temporary_output_list]
            action["parameters"] = [x for x in temporary_parameter_list]
            # Clear the lists
            temporary_input_list.clear() 
            temporary_output_list.clear()
            temporary_parameter_list.clear()
                                             
        duplicate_actions = []
        # Check if you have duplicate actions - the duplicate actions may have different names!        
        for index_prev,action in enumerate(self.opaqueAction_list):
            if index > index_prev:
                for index,next_action in enumerate(self.opaqueAction_list):
                    # If both actions have the same parameters we can get suspicious
                    if set(action["parameters"]) == set(next_action["parameters"]) and index != index_prev:
                        # we should check the preconditions:
                            if set(action["preconditions"]) == set(next_action["preconditions"]):
                                # if the preconditions are the same - we should check the effects:
                                    if set(action["effects"]) == set(next_action["effects"]):
                                        # if everything is similar just pop the action out! --> but then you can lose this info in the method - write a warning!
                                        # self.opaqueAction_list.pop(index)
                                        for method in self.method_list:
                                            if method["xmi:id"] == action["method"]:
                                                first_method = method["name"]
                                            if method["xmi:id"] == next_action["method"]:
                                                second_method = method["name"]
                                        if self.debug == 'on':
                                            print('action {} and {} have same parameters, preconditions and effect - are they two different actions? The are both considered in your domain'.format(action["name"], next_action["name"]))
                                            print('action {} is associate to method {}, while action {} is associated to method {}'.format(action["name"], next_action["name"], first_method, second_method))
                                        self.log_file_general_entries.append(' \t\t action {} and {} have same parameters, preconditions and effect - are they two different actions? The are both considered in your domain \n'.format(action["name"], next_action["name"]))
                                        self.log_file_general_entries.append(' \t\t action {} is associate to method {}, while action {} is associated to method {} \n'.format(action["name"], next_action["name"], first_method, second_method))
                                        # Flag the action as double!! 
                                        next_action["double_action"] = action['xmi:id']
        # Check if you have duplicate actions with the same name - if the action has the same name it is going to be removed from the actions
        # in your final domain file
        for index_prev,action in enumerate(self.opaqueAction_list):
            for index,next_action in enumerate(self.opaqueAction_list):
                # To not remove even the first occurance of a duplicated action
                if index > index_prev:
                    if action["name"] in next_action["name"] and index != index_prev and action['xmi:type'] != 'uml:CallBehaviorAction':
                            # Check if the action is duplicate
                            duplicate_actions.append(next_action)
                            # Check the order of the parameters - we want the same order!! If they are the same action, 
                            # We want to guarantee that in any case the solver can find the right parameters.                        
                            next_action["parameters"] = []
                            for param in action["parameters"]:
                                next_action["parameters"].append(param) # So now we have the same parameters order
    
    
                            for method in self.method_list:
                                if method["xmi:id"] == action["method"]:
                                    first_method = method["name"]
                                if method["xmi:id"] == next_action["method"]:
                                    second_method = method["name"]
                            if self.debug == 'on':
                                print('action {} and {} have similar names - are they two different actions? Action {} has been removed from the domain'.format(action["name"], next_action["name"], next_action["name"]))
                                print('action {} is associate to method{}, while action {} is associated to method {}'.format(action["name"], next_action["name"], first_method, second_method))
                            self.log_file_general_entries.append('\t\t action {} and {} have similar names - are they two different actions? Action {} has been removed from the domain \n'.format(action["name"], next_action["name"], next_action["name"]))
                            self.log_file_general_entries.append('\t\t action {} is associate to method{}, while action {} is associated to method {} \n'.format(action["name"], next_action["name"], first_method, second_method))

        no_duplicate_actions = []
        if duplicate_actions != []:
            # Add action to the final set of actions in your domain
            no_duplicate_actions = DomainDefinition.Diff(self.opaqueAction_list,duplicate_actions)
        
        for action in no_duplicate_actions:
            if action ['xmi:type'] != 'uml:CallBehaviorAction':
                self.final_opaque_action_list.append(action)
            
        
        # Task Parameters for task used as :subtask in a method
        for action in self.opaqueAction_list:
            if action ['xmi:type'] == 'uml:CallBehaviorAction':
                for task in self.task_list:
                    if task.get('name') == action.get('name'): 
                        if task["parameters"] == []:
                            task["parameters"] = action.get('parameters')          
       
        # Check if the user defined some constraints in UseCase diagram to get the task parameters
        get_param = []
        flag_found = 0
        for constraint in self.b_ownedRules:            
            if constraint.parent['name'] == 'DomainDefinition' or constraint.parent['name'] == 'UseCase':
                # check that the parameters have a known type!
                dummy_string = constraint['name']
                dummy_vector = re.split(' |-', dummy_string)

                # # if element.descent
                # for child in element.children:
                #     # If the tag has been defined as Parameter Spec
                #     try:
                #         if not isinstance(child, str) and child.attrs['name'] == 'ParamSpec':
                #             element_type = child.body.contents[0]
                #             b_ownedRules_from_package.append('{} - {}'.format(element['name'], element_type))
                #         # If the tag has been defined as constraintSpec
                #         if not isinstance(child, str) and child.attrs['name'] == 'constraintSpec':
                #             b_ownedRules_from_package.append(element['name']) 
                #         else:
                #             pass
                #     except:
                #         pass
                
                # You check if the input in the constraints exist as a type in your HDDL types
                for hddl_type in self.hddl_type_list:
                    if hddl_type['name'] == dummy_vector[-1]:
                        flag_found = 1
            
                # You check if the input in the constraints exist as a type in your HDDL types - if it doesn't you add it to your HDDL list
                if flag_found != 1:
                    self.hddl_type_list.append(dummy_vector[-1].replace(" ", ""))
                    self.hddl_type_feedback.append(dummy_vector[-1].replace(" ", ""))
                    if self.debug == 'on':
                        print('Plese check your constraints in the UseCase - your type extension for {} was not found in the type folder'.format(constraint['name'].replace(" ", "")))
                        print('We added that type - however, please check if that was what you were planning to do!')
                        self.log_file_general_entries.append('\t\t Plese check your constraints in the UseCase - your type extension for {} was not found in the type folder \n'.format(constraint['name'].replace(" ", "")))
                
                # Here you are looking for the connection between your constraints and your task
                for edge in self.dependencies_list:
                    flag_found = 0
                    get_param_dict = { "xmi:type":constraint['xmi:type'], "xmi:id":constraint['xmi:id'], "name":constraint['name']}
                    if edge['output'] == constraint['xmi:id']:
                        get_param_dict['task'] = edge['input']
                        get_param.append(get_param_dict)
                        
        task_parameters = []
        # If the task parameters are already defined in the main use case diagram as constraints
        for task in self.task_list:
            if task["parameters"] == []:
                if get_param != []:
                    for param in get_param:
                        if ('task') in param:
                            if param['task'] == task['xmi:id']:
                                task_parameters.append(param['name'].replace(" ", ""))
            
                # if task["parameters"] == []:
                    task["parameters"] = [x for x in task_parameters]
                    task_parameters.clear()
                
        # If the tasks have no parameter defined --> Get the minimum or the common parameters out of the methods parameters associated to that task
        task_parameters_matrix = []

        for task in self.task_list:
            if task["parameters"] == []:
                # Minimum parameters
                if self.task_parameters == 'min':
                    for method in self.method_list:
                        
                        if task.get('xmi:id') == method.get('task'):
                            # for each method check the length of the parameters list - if it longer than the one of the task, leave it like that - if not replace the list
                            if task["parameters"] != []:
                                if len(task["parameters"]) >= len(method.get('parameters')):
                                    # dummy_parameter = [x for x in jj.get('parameters')]
                                    task["parameters"] = method.get('parameters')
                            else:
                                task["parameters"] = method.get('parameters')
                            
                # Common parameters
                #if self.task_parameters == 'common':
                else:
                    for method in self.method_list:
                        
                        if task.get('xmi:id') == method.get('task'):
                            # for each method check the length of the parameters list - look if there are common paramaters
                                task_parameters_matrix.append(method.get('parameters'))     
                    
                    for index, task_param in enumerate(task_parameters_matrix):
                        if index == 0:
                            common_param = task_param
                        elif index == 1:
                            common_param = task_param.intersection(task_parameters_matrix[index-1])
                        else:
                            common_param = task_param.intersection(common_param)
                
                    task["parameters"] = common_param
        
        # Now you should do a re-check on your methods:
            # Check that all the task parameters are considered in the method definition
            # Check that the tasks of the method exist and 
            # check if the tasks are duplicate of other tasks
    
            
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
        # Flag to know how to write the domain file
        flag_type = 0

        # Open/Create the File
        file = open(self.d_now + '//outputs//' + self.domain_name,'w')
        # Start writing on the file
        file.write('(define (domain {}) \n'.format(self.domain_name_simple.lower()))
        # Write requirement
        file.write('\t (:requirements :{}) \n'.format(' :'.join(self.requirement_list_domain_file).lower()))
        #Object Type
        file.write('\t (:types  ')
        for hddl_type in self.hddl_type_list:
            if "parent" in hddl_type.keys():
                flag_type = 1
        for hddl_type in self.hddl_type_list:
            if flag_type == 0:
                if hddl_type.get('name').strip() != 'predicate':
                    file.write('{} '.format(hddl_type.get('name').lower()))
            else:
                if hddl_type.get('name').strip() != 'predicate':
                    if "parent" in hddl_type.keys():
                        file.write('\n\t\t{} - {} '.format(hddl_type.get('name').lower(), hddl_type["parent"]))
                    else:
                        file.write('\n\t\t{} - object '.format(hddl_type.get('name').lower()))
                    
        # End of object type
        file.write(') \n\n')  
        
        # Predicates
        file.write('\t (:predicates \n')
        #Writes Predicates
        for predicate in self.predicate_list:
            file.write('\t\t ({}) \n'.format(predicate).lower())
        # End of predicates
        file.write('\t) \n\n')   
            
        #Tasks!
        for task in self.task_list:
            file.write('\t (:task {} \n'.format(task.get('name')))            
            file.write('\t\t :parameters (?{}) \n'.format(' ?'.join(task.get('parameters')).lower()))
            file.write('\t\t :precondition ()\n')
            file.write('\t\t :effect ()\n')
            file.write('\t ) \n\n') 
            
        #Methods!
        # Introduce the order in the tasks
        # have just the first word of the parameters
        string_vector = []
        order_vector = []
        file.write('\n')  #space!
        for method in self.method_list:
            # method name
            file.write('\t (:method {} \n'.format(method.get('name')))
            # method parameters
            file.write('\t\t :parameters (?{}) \n'.format(' ?'.join(method.get('parameters')).lower()))
            # method task
            for task in self.task_list:
                if task['xmi:id'] == method['task']:
                    task_name = task['name']
                    task_parameters = []
                    for uu in task['parameters']:
                        regex_pattern ='\w+.'
                        parameters = re.findall(regex_pattern, uu)
                        task_parameters.append(parameters[0].replace('-', ''))
                                        
            file.write('\t\t :task ({} ?{}) \n'.format(task_name, ' ?'.join(task_parameters).lower()))
            # method preconditions
            if method.get('preconditions') != '':
                file.write('\t\t :precondition (and \n\t\t\t{} \n\t\t) \n'.format(' \n\t\t\t'.join(method.get('preconditions')).lower()))
            else:
                file.write('\t\t :precondition ()\n')
            counter = 0
            
            # method actions
            if self.flag_ordering_file == 'yes':
                for task in method['ordered_tasks']: 
                    for action in self.opaqueAction_list:
                        if action['xmi:id'] == task:
                            if action['parameters'] != []:
                                # Task Parameters
                                dummy_string = ' '.join(action['parameters'])
                                dummy_vector = re.split(' |-', dummy_string)
                                # vector[start:end:step]
                                dummy_vector = dummy_vector[0::2]
                                string_vector.append('task{}({} ?{})'.format(counter,action['name'], ' ?'.join(dummy_vector).lower() ))
                                counter = counter + 1
                            else:
                                string_vector.append('task{}({})'.format(counter,action['name']))
                                counter = counter + 1                                
                        if counter > 1 and '(< task{} task{})'.format(counter-2, counter-1) not in order_vector:
                            # For each task check incoming and outcoming links
                            order_vector.append('(< task{} task{})'.format(counter-2, counter-1))

            if self.flag_ordering_file == 'no':
                for task in method['ordered_tasks']: 
                    for kk in self.opaqueAction_list:
                        if kk['xmi:id'] == task:
                            # Task Parameters
                            dummy_string = ' '.join(kk['parameters'])
                            dummy_vector = re.split(' |-', dummy_string)
                            # vector[start:end:step]
                            dummy_vector = dummy_vector[0::2]
                            if kk["parameters"] != []:
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
        for action in self.final_opaque_action_list:

            file.write('\t(:action {} \n'.format(action.get('name')))     
            if action['parameters'] != []:
                file.write('\t\t :parameters (?{}) \n'.format(' ?'.join(action.get('parameters')).lower()))
            else:
                file.write('\t\t :parameters () \n')
            if action.get('preconditions') != []:
                file.write('\t\t :precondition (and \n\t\t\t{})\n'.format(' \n\t\t\t'.join(action.get('preconditions')).lower()))
            else:
                file.write('\t\t :precondition ()\n')
            if action.get('effects') != []:
                file.write('\t\t :effect (and \n\t\t\t{})\n'.format(' \n\t\t\t'.join(action.get('effects')).lower()))
            else:
                file.write('\t\t :effect ()\n')
                        
            file.write('\t) \n\n') 
        
        # end of the file
        file.write(')')