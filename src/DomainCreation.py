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

from soupsieve import escape

# MAIN PARSING CLASS!
class Domain():
    def __init__(self, domain_name, SysML_data, domain_dictionary, domain_requirements, task_parameters = 'common', flag_ordering_file = 'yes', method_precondition_from_action = 'yes', d_now = os.getcwd(),  debug = 'on'):
        # domain file name
        self.domain_name = datetime.now().strftime("%Y_%m_%d-%I_%M_%S") + '_' + domain_name + '_' +'_domain.hddl'
        # all the data from the .uml file
        self.overall_data = SysML_data
        # all the data from the domain definition of the .uml file
        self.domain_dictionary = domain_dictionary
        # domain requirements
        self.domain_requirements = domain_requirements
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
        # Create a dictionary where you are going to store all instance related to the domain definition
        domain_definition_output = {}
        # requirements --> self.domain_requirements
        # types in the HDDL file
        hddl_types_preprocess = self.domain_dictionary['types']
        # write the hddl type as a list of dictionary
        hddl_types = []
        for type in hddl_types_preprocess:
            hddl_types.append(type.attrs)
        # save HDDL tasks
        tasks_domain_prepocess = self.domain_dictionary['tasks']
        
        tasks_domain = []
        for task in tasks_domain_prepocess:
            tasks_domain.append(task.attrs)
            task_owned_behavior = task.find_all('ownedBehavior')
            for behavior in task_owned_behavior:
                tasks_domain[-1]["behavior"] = behavior.attrs
        task_parameters_preprocess = self.domain_dictionary['tasks_param']
        task_parameters = []
        for parameter in task_parameters_preprocess:
            task_parameters.append(parameter.attrs)

        # predicate_type = [x for x in hddl_types if x['name'] == "predicate"][0]
        # Create the HDDL methods
        methods = self.domain_dictionary['methods']
        methods_list = []
        for method in methods:
            temporary_dictionary = {}
            temporary_dictionary["method"] = method.attrs
            # --------------------------------------------------------------------
            # find the parameters
            nodes1 = method.find_all('node', attrs={"xmi:type": "uml:ActivityParameterNode"})
            nodes2 = method.find_all('node', attrs={"xmi:type": "uml:CentralBufferNode"})
            nodes = nodes1 + nodes2
            parameters_preprocess = [x for x in nodes if len(x["name"].split()) == 1]
            # predicates
            predicates_preprocess = [x for x in nodes if len(x["name"].split()) != 1]

            # if the parameter do not have a type
            for param in parameters_preprocess:
                if not param.has_attr("type"):
                    # look if there is an already defined parameter with the same or similar name 
                    # similar name are name without the possible following numbers
                    flag_param = 0
                    for type in hddl_types:
                        new_param = ''.join([i for i in param['name'] if not i.isdigit()])
                        if type['name'] == new_param:
                            param['type'] = type['xmi:id']
                            param["type_name"] = type['name']
                            flag_param = 1

                    # creating a parameter with that name and print a warning to the user
                    if flag_param == 0:
                        # create an adhoc name based on the parameter name
                        id_uuid = str(uuid.uuid1())
                        param['type'] = id_uuid
                        param["type_name"] = param['name']
                        hddl_types.append({"name": param['name'], "xmi:id": id_uuid})
                        if self.debug == 'on': 
                            print('No predefined type for {}. Add it on Papyrus!'.format(param['name']))
                        self.log_file_general_entries('\t\t No predefined type for {}. We added as its own type \n'.format(param['name']))

                if param.has_attr("type"):
                    for type in hddl_types:
                        if type["xmi:id"] == param["type"]:
                            param["type_name"] = type['name']



            # format parameters as a list of dictionary
            parameters = []
            for param in parameters_preprocess:
                parameters.append(param.attrs)
                        
            # add parameters to the method temporary dictionary
            temporary_dictionary['parameters'] = parameters

            # find the associated task
            task = method.parent.attrs
            temporary_dictionary['task'] = task

            # find the actions
            opaque_actions_preprocess = method.find_all('node', attrs={"xmi:type": "uml:OpaqueAction"})
            behavioral_actions_preprocess = method.find_all('node', attrs={"xmi:type": "uml:CallBehaviorAction"})
            # format the actions as a list of dictionary 
            actions = []
            for action in opaque_actions_preprocess:
                # find input values (action pins)
                input_values = action.find_all('inputValue')
                # find all output values
                output_values = action.find_all('outputValue')
                actions.append(action.attrs)
                actions[-1]["inputs"] = input_values
                actions[-1]["outputs"] = output_values
            for action in behavioral_actions_preprocess:
                # find input values (action pins)
                input_values = action.find_all('argument', attrs={"xmi:type": "uml:InputPin"})
                # find all output values
                output_values = action.find_all('argument', attrs={"xmi:type": "uml:OutputPin"})
                actions.append(action.attrs)
                actions[-1]["inputs"] = input_values
                actions[-1]["outputs"] = output_values

            temporary_dictionary['actions'] = actions
            # find the preconditions
            output_predicates =[]
            input_predicates = []
            for predicate in predicates_preprocess:
                # output of an action of the method
                if predicate.has_attr('incoming'):
                    output_predicates.append(predicate.attrs)
                if predicate.has_attr('outgoing'):
                    input_predicates.append(predicate.attrs)

            temporary_dictionary['input_predicates'] = input_predicates
            temporary_dictionary['output_predicates'] = output_predicates
            # Store the method edge - they give you the action order and the give you the link action/parameters or action/predicates
            edges_preprocess = method.find_all('edge')
            edges = []
            for edge in edges_preprocess:
                edges.append(edge.attrs)

            temporary_dictionary['edges'] = edges
            # find the order of the action
            # assumption: actions are linked with control flows
            actions_order = []
            actions_partial_order = []
            for edge in edges:
                for action in actions:
                    if edge["target"] == action["xmi:id"]:
                        for prev_action in actions:
                            if edge["source"] == prev_action["xmi:id"]:
                                actions_partial_order.append([prev_action["xmi:id"], action["xmi:id"]])
            
            # first order the list so that all the same elements are neighbours
            for index,list in enumerate(actions_partial_order):
                for next_list in actions_partial_order[index::]:
                    if list[-1] == next_list[0]:
                        index_next_list = actions_partial_order.index(next_list)
                        new_index_list = actions_partial_order.index(list)
                        actions_partial_order.pop(index_next_list)
                        actions_partial_order.insert(new_index_list+1,next_list)
    
            # merge list maintaning order
            for list in actions_partial_order:
                for element in list:
                    if element not in actions_order:
                        actions_order.append(element)
            
            temporary_dictionary['actions_order'] = actions_order

            methods_list.append(temporary_dictionary)
        
        # Check the predicate list - clean it and make it ready for the domain file
        predicates = self.domain_dictionary['predicates']
        temporary_predicate = []
        final_predicate_list = []
        for predicate_object in predicates:
            predicate = predicate_object["name"]
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
            # analyse all other words in the predicate: you should have them in input_types
            for index_predicate, predicate_atom in enumerate(cleaned_predicate[1::]):
                predicate_atom = predicate_atom.replace('?',' ').strip()
                for method in methods_list:
                    for method_type in method["parameters"]:
                        if predicate_atom == method_type['name']:
                            predicate_input = '?arg{}-{}'.format(index_predicate,method_type['type_name'])
                            if predicate_input not in temporary_predicate:
                                temporary_predicate.append(predicate_input)

            if len(temporary_predicate) <= 1:
                self.log_file_general_entries.append('t\t The {} is not used in any method, therefore it is not in the final domain file \n'.format(predicate))
                if self.debug == 'on':
                    print('The {} is not used in any method, therefore it is not in the final domain file'.format(predicate))   
            else:
                final_predicate = ' '.join(temporary_predicate)
                if not(final_predicate in final_predicate_list) and not('=' in final_predicate):
                    final_predicate_list.append(final_predicate)
                
                temporary_predicate.clear() 

        # Identify the HDDL actions, parameters, pre and post conditions
        final_action_list = []
        for method in methods_list:
            for action in method['actions']:
                # if you have a "xmi:type": "uml:OpaqueAction" --> you need to define parameters and pre and post conditions
                if action["xmi:type"] == "uml:OpaqueAction":
                    action_parameters = []
                    action_preconditions = []
                    action_postconditions = []
                    for edge in method["edges"]:
                        for inputs in action["inputs"]: 
                            # look at parameters and preconditions
                            if edge["target"] == inputs["xmi:id"]:
                                # look for the source
                                for param in method["parameters"]:
                                    if edge["source"] == param["xmi:id"]:
                                        action_parameters.append(param)
                            # look for the preconditions
                                for input_predicate in method["input_predicates"]:
                                    if edge["source"] == input_predicate["xmi:id"]:
                                        action_preconditions.append(input_predicate)
                        
                        # look at post conditions
                        for outputs in action["outputs"]: 
                            if "source" in edge and edge["source"] == outputs["xmi:id"]:
                            # look for the target
                                for output_predicate in method["output_predicates"]:
                                    if edge["target"] == output_predicate["xmi:id"]:
                                        action_postconditions.append(output_predicate)

                    action["parameters"] = action_parameters
                    action["preconditions"] = action_preconditions
                    action["effects"] = action_postconditions
                    final_action_list.append(action)
        
        # Identify the HDDL tasks
        final_tasks_list = []
        bev_action_list = []
        # Look at the task used in the methods and check their parameters
        for method in methods_list:
            for action in method['actions']:
                # if you have a "xmi:type": "uml:CallBehaviorAction" --> you can look to the linked parameters
                if action["xmi:type"] == "uml:CallBehaviorAction":
                    action_parameters = []
                    action_predicates = []
                    for edge in method["edges"]:
                        for inputs in action["inputs"]: 
                            # look at parameters and preconditions
                            if edge["target"] == inputs["xmi:id"]:
                                # look for the source
                                for param in method["parameters"]:
                                    if edge["source"] == param["xmi:id"]:
                                        action_parameters.append(param)
                            # look for the preconditions
                                for input_predicate in method["input_predicates"]:
                                    if "source" in edge and edge["source"] == input_predicate["xmi:id"]:
                                        # Print a warning if the task has preconditions! 
                                        self.log_file_general_entries.append('t\t The {} is a task with precondition. Check if this is intended or not!'.format(action["name"]))
                                        if self.debug == 'on':
                                            print('The {} is a task with precondition. Check if this is intended or not!'.format(action["name"]))   
                                        action_predicates.append(input_predicate)

                    action["parameters"] = action_parameters
                    action["predicate"] = action_predicates
                    bev_action_list.append(action)

        # Loot at the tasks that have no parameters defined yet
        for task in tasks_domain:
            
            # check if you have parameters from the methods because of behavioral actions
            for action in bev_action_list:
                if action["behavior"] == task["behavior"]["xmi:id"]:
                    if "parameters" in action and "parameters" not in task:
                        task["parameters"] = action["parameters"]
            # check if you have parameters from the main use case
            if "parameters" not in task:
                for param in task_parameters:
                    task["parameters"] = []
                    for constrained_element in param["constrainedElement"].split():
                        if constrained_element == task["xmi:id"]:
                            task["parameters"].append(constrained_element)

            # check if you have parameters from the methods (minimum or common)
            if "parameters" not in task:
                task["parameters"] = []
                task_parameters_matrix = []
                # minum parameters
                if self.task_parameters == 'min':
                    for method in methods_list:
                        if task["xmi:id"] == methods_list[0]["task"]["xmi:id"]:
                            # for each method check the length of the parameters list -
                            #  if it longer than the one of the task, leave it like that - if not replace the list
                            if task["parameters"] != []:
                                if len(task["parameters"]) >= len(method.get('parameters')):
                                    task["parameters"] = method['parameters']
                            else:
                                task["parameters"] = method['parameters']

                # Common parameters
                else:
                    for method in methods_list:
                        if task["xmi:id"] == methods_list[0]["task"]["xmi:id"]:
                            task_parameters_matrix.append(method['parameters'])
                    for index, task_param in enumerate(task_parameters_matrix):
                        if index == 0:
                            common_param = task_param
                        elif index == 1:
                            common_param = task_param.intersection(task_parameters_matrix[index-1])
                        else:
                            common_param = task_param.intersection(common_param)                        

                    task["parameters"] = common_param
        
        # write return function and test the last lines! 
        domain_definition_output["domain_name"] = self.domain_name
        domain_definition_output["hddl_type_list"] = hddl_types
        domain_definition_output["predicate_list"] = final_predicate_list
        domain_definition_output["task_list"] = tasks_domain
        domain_definition_output["method_list"] = methods_list
        domain_definition_output["final_action_list"] = final_action_list

        return domain_definition_output, self.log_file_general_entries


    # Write the Domain File
    def DomainFileWriting (self, domain_definition_output):
        ###################################################################
        # Flag to know how to write the domain file
        # Open/Create the File
        file = open(self.d_now + '//outputs//' + self.domain_name,'w')
        # Start writing on the file
        file.write('(define (domain {}) \n'.format(self.domain_name_simple.lower()))
        # Write requirement
        file.write('\t (:requirements :{}) \n'.format(' :'.join(self.requirement_list_domain_file).lower()))
        #Object Type
        file.write('\t (:types  ')
        for hddl_type in domain_definition_output["hddl_type_list"]:
            # predicates are not type
            if hddl_type["name"].strip() != 'predicate':
                pass
            # This line consider typing
            elif "parent" in hddl_type:
                file.write('\n\t\t{} - {} '.format(hddl_type["name"].lower(), hddl_type["parent"]))
            else:
                file.write('\n\t\t{} - object '.format(hddl_type["name"].lower()))
                    
        # End of object type
        file.write(') \n\n')  
        
        # Predicates
        file.write('\t (:predicates \n')
        #Writes Predicates
        for predicate in domain_definition_output["predicate_list"]:
            file.write('\t\t ({}) \n'.format(predicate).lower())
        # End of predicates
        file.write('\t) \n\n')   
            
        #Tasks!
        for task in domain_definition_output["task_list"]:
            file.write('\t (:task {} \n'.format(task["name"])) 
            parameters = []
            for param in task["parameters"]:
                parameters.append(param["name"].lower())   
            file.write('\t\t :parameters (?{}) \n'.format(' ?'.join(parameters)))
            file.write('\t\t :precondition ()\n')
            file.write('\t\t :effect ()\n')
            file.write('\t ) \n\n') 
            
        #Methods!
        # Introduce the order in the tasks
        # have just the first word of the parameters
        string_vector = []
        order_vector = []
        file.write('\n')  #space!
        for method in domain_definition_output["method_list"]:
            # method name
            file.write('\t (:method {} \n'.format(method["method"]["name"].lower()))
            # method parameters
            parameters = []
            for param in method["parameters"]:
                parameters.append(param["name"].lower())  
            file.write('\t\t :parameters (?{}) \n'.format(' ?'.join(parameters)))
            # method task
            for task in domain_definition_output["task_list"]:
                if task['xmi:id'] == method['task']['xmi:id']:
                    task_name = task['name']
                    task_parameters = []
                    for param in task["parameters"]:
                        task_parameters.append(param["name"].lower())                         
            file.write('\t\t :task ({} ?{}) \n'.format(task_name, ' ?'.join(task_parameters).lower()))
            # method preconditions
            if method["input_predicates"] != []:
                predicates = []
                for predicate in method["input_predicates"]:
                    predicates.append(predicate["name"].lower())
                file.write('\t\t :precondition (and \n\t\t\t{} \n\t\t) \n'.format(' \n\t\t\t'.join(predicates)))
            else:
                file.write('\t\t :precondition ()\n')
            counter = 0
            
            # method actions
            temporary_string = []
            ordering = []
            for action in method["actions_order"]:
                # You can check if the action have been identified
                flag_found = 0
                # it can be an opaque action
                for opaque_action in domain_definition_output["final_action_list"]:
                    if action["xmi:id"] == opaque_action["xmi:id"]:
                        flag_found = flag_found + 1
                        parameters = []
                        for param in opaque_action["parameters"]:
                            parameters.append(param["name"].lower())  
                        if parameters != [] :
                            temporary_string.append('task{}({} ?{})'.format(counter,opaque_action['name'], ' ?'.join(parameters) ))
                        else:
                            temporary_string.append('task{}({})'.format(counter,opaque_action['name']))
                        counter = counter + 1
                # it can be a behavioral action
                for bev_action in domain_definition_output["task_list"]:
                    if action["xmi:id"] == bev_action["behavior"]["xmi:id"]:
                        flag_found = flag_found + 1
                        parameters = []
                        for param in bev_action["parameters"]:
                            parameters.append(param["name"].lower())  
                        if parameters != [] :
                            temporary_string.append('task{}({} ?{})'.format(counter,bev_action['name'], ' ?'.join(parameters) ))
                        else:
                            temporary_string.append('task{}({})'.format(counter,bev_action['name']))
                        counter = counter + 1
                if flag_found == 1:
                    if counter > 1 and '(< task{} task{})'.format(counter-2, counter-1) not in ordering:
                            # For each task check incoming and outcoming links
                            ordering.append('(< task{} task{})'.format(counter-2, counter-1))
                else:
                    raise IndexError 
                    # You need to create an ad-hoc error for clarity!!!!!!!!
                            
            if self.flag_ordering_file == 'yes':                            
                if counter != 0 and counter != 1:
                    file.write('\t\t :subtasks (and \n')
                    file.write('\t\t\t{}\n'.format('\n\t\t\t'.join(temporary_string)))
                    file.write('\t\t ) \n')
                    file.write('\t\t :ordering (and \n')
                    file.write('\t\t\t{}\n'.format(' \n\t\t\t'.join(ordering).lower()))
                    file.write('\t\t ) \n')
                    string_vector.clear()
                    order_vector.clear()
                elif counter == 1:
                    file.write('\t\t :subtasks (and \n')
                    file.write('\t\t\t {}\n'.format(' \n\t\t\t'.join(temporary_string)))
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
                    file.write('\t\t\t{}\n'.format('\n\t\t\t'.join(temporary_string)))
                    file.write('\t\t ) \n')
                    string_vector.clear()
                    order_vector.clear()
                elif counter == 1:
                    file.write('\t\t :ordered-subtasks (and \n')
                    file.write('\t\t\t {}\n'.format(' \n\t\t\t'.join(temporary_string)))
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
        for action in domain_definition_output["final_action_list"]:
            # Name
            file.write('\t(:action {} \n'.format(action["name"].lower()))  
            parameters = []
            for param in action["parameters"]:
                parameters.append(param["name"].lower())    
            if parameters != []:
                file.write('\t\t :parameters (?{}) \n'.format(' ?'.join(parameters)))
            else:
                file.write('\t\t :parameters () \n')

            if action["preconditions"] != []:
                predicates = []
                for predicate in action["preconditions"]:
                    predicates.append(predicate["name"].lower())
                file.write('\t\t :precondition (and \n\t\t\t{})\n'.format(' \n\t\t\t'.join(predicates)))
            else:
                file.write('\t\t :precondition ()\n')
            if action["effects"] != []:
                effects = []
                for effect in action["preconditions"]:
                    effects.append(effect["name"].lower())
                file.write('\t\t :effect (and \n\t\t\t{})\n'.format(' \n\t\t\t'.join(effects)))
            else:
                file.write('\t\t :effect ()\n')
                        
            file.write('\t) \n\n') 
        
        # end of the file
        file.write(')')


