# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 08:32:34 2021

@author: Jasmine

Read the MBSE-HDDL excel file from Vitech CORE 
First Version



"""

import pandas as pd
import numpy as np
import time
from datetime import datetime
import re

class MBSE_HDDL_TRANSLATION_VITECH():
    def __init__(self, domain_name, Number, Class, Name, Inputs, Outputs, Decomposed_by, Decomposes, Category, Description):
        self.domain_name = domain_name
        # Object Class ("denomination")
        self.Class = Class
        # Object Type
        self.Category = Category
        # Object Name
        self.Name = Name
        # Object Description - Used by the methods to match objects in methods and actions
        self.Description = Description 
        # Object Inputs
        self.Inputs = Inputs
        # Object Outputs
        self.Outputs = Outputs
        # Decomposed by 
        self.Decomposed_by = Decomposed_by
        # Decomposes
        self.Decomposes = Decomposes

    
    def domain_file_VITECH(self):
        
        # Domain File Name based on the domain name and date
        name_string = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p") + '_'+ self.domain_name +'_domain.hddl' 

        ##########################################
        # Object Type from MBSE
        # Create a List of objects that will be added to the file
        list_object = []
        #memory list to remember the types that have already been analysed
        memory_types = [] 
        #Remove the nan value from the Category
        new_Category = [item for item in self.Category if not(pd.isnull(item)) == True]
        for ii in new_Category:
            # Considering only the objects - I don't care about the predicates
            if ii.strip() != 'predicates':
                # If you still have to write it
                if not (ii.strip() in memory_types): 
                    list_object.append('\t {} - object \n'.format(ii.strip()))
                    print('\t {} - object \n'.format(ii.strip()))
                # Add to memory
                memory_types.append(ii.strip())
                
        ########################################
        # Predicates
        # List with memory of the predicates
        memory_predicates = []
        # Temporary string where you save the final version of the predicate
        temp_string_added = []
        # List of predicate to add to the HDDL domain file 
        predicate_list_hddl = []
        # Save string and category for task, methods and actions
        name_and_cat = []
        #Counter of the string arguments
        counter_arg = 0
        # Counter index - to know the index in the list
        counter_for_loop = 0
        
        for ii in self.Category:
            try: 
                if ii.strip() == 'predicates':
                    index_predicate = counter_for_loop
                    # print(index_predicate)
                    temp_string = self.Name[index_predicate].strip()
                    if temp_string.split()[0] == '(not':
                        # remover do not
                        temp_string = temp_string.replace("(not", "")
                        
                    # print(temp_string)
                    # add the first part in string to be added
                    temp_string_added.append(temp_string.split()[0][1::])
                    # print(temp_string_added)
                    # split the string
                    for jj in temp_string.split():
                        if jj[0] == '?':
                            # print(jj)
    
                            if jj[-1] == ')' and jj[-2] == ')':
                                jj = jj[0:-2]
                                
                            if jj[-1] == ')':
                                jj = jj[0:-1]
                            # search for the argument in the Entity Column (here called name)
                            if (jj[1::] in self.Name):
                                index_name = self.Name.index(jj[1::])
                                # print(index_name)
                                # Get the category of the object 
                                temp_category = self.Category[index_name]
                                
                                
                            else:
                                #add a string in the predicates part
                                print("no category pre-assigned, adding a new object for {}".format(jj[1::]))    
                                list_object.append('\t {} - object \n'.format(jj[1::]))
                                # Get the category of the object - new added category
                                temp_category = jj[1::]
                            
                            temp_string_added.append('?arg{} - {}'.format(counter_arg,temp_category))
                            # print(temp_string_added)
                            # Add an argument
                            counter_arg = counter_arg + 1
                            
                    temp_string_added_var = " ".join(temp_string_added)
                    
                    if not (temp_string_added_var in memory_predicates ):
                        predicate_list_hddl.append('\t ({}) \n'.format(temp_string_added_var))
                        memory_predicates.append(temp_string_added_var)
                        
                    temp_string_added.clear()
                    counter_arg = 0  
            except:
                    print(ii)

            # index in in the list
            counter_for_loop = counter_for_loop + 1
        
                        
        ########################################
        # Tasks, Methods and Actions
        # Counter index - to know the index in the list
        counter_for_loop = 0
        # List will all the tasks
        task_list_hddl = []
        #list of parameter of the tasks 
        task_parameters = []
        # List will all the methods
        method_list_hddl = []
        #list of parameter of the methods
        method_parameters = []
        # method inputs list
        method_inputs_list = []
        # method decomposition list
        method_decomposed_list = []
        # method decomposition list
        method_ordering_list = []
        # method parameter task
        method_task_param = []
        method_action_param = []
        # List will all the methods
        action_list_hddl = []
        #list of parameter of the methods
        action_parameters = []
        # method inputs list
        action_inputs_list = []
        # method inputs list
        action_output_list = []
        
        # Let's search our tasks 
        for ii in self.Class:
            
            # TASK
            if ii == 'Function':   
                index_function = counter_for_loop
                temp_string = self.Name[index_function]
                if temp_string[0] == 't':
                    task = temp_string[2::].strip()
                    task_inputs = self.Inputs[counter_for_loop]
                    # Search which items are in the inputs
                    cleaned_inputs = task_inputs.replace("\r\n", "")
                    cleaned_inputs = re.sub(r"\d+", "", cleaned_inputs)
                    for jj in cleaned_inputs.split():
                        if (jj.strip() in self.Name):
                            index_name = self.Name.index(jj.strip())
                            # print(index_name)
                            # Get the category of the object 
                            temp_category = self.Category[index_name]
                            task_parameters.append('?{} - {} '.format(jj.strip(),temp_category))
                            
                    task_list_hddl.append('(:task {} \n \t :parameters({}) \n \t :preconditions() \n \t :effect() \n )'.format(task,"".join(task_parameters)))
                    task_parameters.clear()
                
                # METHODS
                if temp_string[0] == 'm':
                    method = temp_string
                    method_inputs = self.Inputs[counter_for_loop]
                    # Search which items are in the inputs
                    cleaned_inputs = method_inputs.replace("\r", "")
                    cleaned_inputs = re.sub(r"\d+", "", cleaned_inputs)
                    cleaned_inputs = cleaned_inputs.replace(".", "")
                    for kk in cleaned_inputs.split('\n'):
                        if (kk.strip() in self.Name) :
                            if (kk.strip()[0] != '('):
                                index_name = self.Name.index(kk.strip())
                                # print(index_name)
                                # Get the category of the object 
                                temp_category = self.Category[index_name]
                                method_parameters.append('?{} - {} '.format(kk.strip(),temp_category))
                            else:
                                # Get the method inputs
                                #Precodintions 
                                method_inputs_list.append('\t\t {}\n'.format(kk.strip()))
                    
                    # Task associated to the method
                    decomposed_task = self.Decomposes[counter_for_loop]
                    decomposed_task = re.sub(r"\d+", "", decomposed_task)
                    decomposed_task = decomposed_task.replace(".", "").strip()
                    decomposed_task = decomposed_task[2::]
                    # The parameters of the task should be then written by the designer
                    # Decomposition of the method
                    decomposing_actions = self.Decomposed_by[counter_for_loop]
                    description = self.Description[counter_for_loop] 
                    try:
                        description = description.replace("\r", "")
                        for yy in description.split('\n'):
                            if 'task_parameters' in yy: 
                                temp_index = yy.index(':')
                                yy_string = yy[(temp_index+1)::]
                                for yyy in yy_string.split(','):
                                    temp_index = yyy.index('=')
                                    method_task_param.append('?{} '.format(yyy[(temp_index+1)::].strip()))
                                
                    except:
                        pass
                            
                    
                    try:
                        decomposing_actions = decomposing_actions.replace("\r", "")
                        decomposing_actions = re.sub(r"\d+", "", decomposing_actions)
                        decomposing_actions = decomposing_actions.replace(".", "")
                        counter_ordering_methods = 0
                        for nn in decomposing_actions.split('\n'):
                            nn = nn.strip()
                            try:  
                              description = description.replace("\r", "")
                              for yy in description.split('\n'):
                                  if 'task{}'.format(counter_ordering_methods) in yy:
                                      temp_index = yy.index(':')
                                      yy_string = yy[(temp_index+1)::]
                                      for yyy in yy_string.split(','):
                                          temp_index = yyy.index('=')
                                          method_action_param.append('?{} '.format(yyy[(temp_index+1)::].strip()))
                              
                            except:
                                pass
                            
                            
                           
                            method_decomposed_list.append('\n \t\t (task{} ({} {}))  '.format(counter_ordering_methods,nn, "".join(method_action_param)))
                            
                            if counter_ordering_methods > 0:
                                method_ordering_list.append(('\n \t\t (< task{}  task{}) '.format(counter_ordering_methods-1,counter_ordering_methods)))
                            counter_ordering_methods = counter_ordering_methods + 1
                            method_action_param.clear()
                        
                    
                        method_list_hddl.append( \
                                                '(:method {} \n\t :parameters({}) \n\t :task({} {}) \n\t :precondition(and \n {}) \n\t \n\t :subtasks(and {}) \n\t :ordering(and {} \n)'.format(method,"".join(method_parameters), decomposed_task, "".join(method_task_param) , "".join(method_inputs_list), "".join(method_decomposed_list), "".join(method_ordering_list)))

                        
                    except:
                        print('no decomposition')
                        method_list_hddl.append( \
                                                '(:method {} \n\t :parameters({}) \n\t :task({} {}) \n\t :precondition(and \n {}) \n\t :subtasks( ) \n\t :ordering( ) \n)'.format(method,"".join(method_parameters), decomposed_task, "".join(method_task_param), "".join(method_inputs_list)))
                    method_parameters.clear()
                    method_inputs_list.clear() 
                    method_decomposed_list.clear()
                    method_ordering_list.clear()
                    method_task_param.clear()
                    method_action_param.clear()
                        
                            
                    
                 
                    
                    
                    # Task parameter allocation
                    # method_description = self.Description[counter_for_loop]
                    # method_description = method_description.replace("\r", "")
                    # for gg in method_description.split('\n'):
                    #     if 'action' in gg :
                    #         x = 0
                    #     x = 0
                    
                    
                    
                    
                    # for uu in self.Decomposed_by:
                    #     # give an error! Fix it
                    #     if np.isnan(uu):
                    #         pass
                    #     else:
                    #         if uu.find(method):
                    #             id_task = self.Decomposed_by.index(uu)
                    #             method_task = self.Name[id_task]
                    #             method_task = method_task[2::]
                                

                            

                
                    
                    # Ordering 
                    
                    
                            
                            
                            
                            
                            
                    
                    
                
                            

                
                #ACTIONS
                if temp_string[0] == 'a':
                    action = temp_string
                    action_inputs = self.Inputs[counter_for_loop]
                    # Search which items are in the inputs
                    cleaned_inputs = action_inputs.replace("\r", "")
                    cleaned_inputs = re.sub(r"\d+", "", cleaned_inputs)
                    cleaned_inputs = cleaned_inputs.replace(".", "")
                    for kk in cleaned_inputs.split('\n'):
                        # clean the string of any non wanted space at the beginning or end of it with strip method
                        if (kk.strip() in self.Name) :
                            if (kk.strip()[0] != '('):
                                index_name = self.Name.index(kk.strip())
                                # print(index_name)
                                # Get the category of the object 
                                temp_category = self.Category[index_name]
                                action_parameters.append('?{} - {}'.format(kk.strip(),temp_category))
                            else:
                                # Get the method inputs
                                #Precodintions 
                                action_inputs_list.append('\t\t {}\n'.format(kk.strip()))
                    # Clean Outputs in the same way
                    action_outputs = self.Outputs[counter_for_loop]
                    cleaned_outputs = action_outputs.replace("\r", "")
                    cleaned_outputs = re.sub(r"\d+", "", cleaned_outputs)
                    cleaned_outputs = cleaned_outputs.replace(".", "")
                    # cleaned_outputs = cleaned_outputs.strip()
                    for ii in cleaned_outputs.split('\n'):
                        action_output_list.append('\t\t {}\n'.format(ii.strip()))
                    # The ouputs can already be already used as they are
                    
                    
                            
                    action_list_hddl.append('(:action {} \n \t :parameters({}) \n \t :preconditions(and \n {} \n\t) \n \t :effect (\n  {}\t) \n)'.format(action,"".join(action_parameters),\
                                                    "".join(action_inputs_list), "".join(action_output_list)))
                    action_parameters.clear()
                    action_inputs_list.clear()
                    action_output_list.clear()
                
                    

                
        
            # index in in the list
            counter_for_loop = counter_for_loop + 1            
        
        ########################################
        # Method      
        
        ########################################
        # Action 
                        
                        
                        
                        
                        
        ###################################################################
        # Open/Create the File
        file = open(name_string,'w')
        # Start writing on the file
        file.write('(define (domain {}) \n'.format(self.domain_name))
        file.write('(:requirements :typing :hierachie) \n')
        #Object Type
        file.write('(:types \n')
        for ii in list_object:
            file.write('{}'.format(ii))
        # End of object type
        file.write(') \n')  
        
        # Predicates
        file.write('(:predicates \n')
        #Writes Predicates
        for ii in predicate_list_hddl:
            file.write('{}'.format(ii))
        # End of predicates
        file.write(') \n')   
            
        #Tasks!
        file.write('\n')  #space!
        for ii in task_list_hddl:
            file.write('{}'.format(ii))
            file.write('\n  \n') 
            
        #Methods!
        file.write('\n')  #space!
        for ii in method_list_hddl:
            file.write('{}'.format(ii))
            file.write('\n  \n') 

        #Actions
        file.write('\n')  #space!
        for ii in action_list_hddl:
            file.write('{}'.format(ii))
            file.write('\n  \n')  
        


        # end of the file
        file.write(')')
        
        
    
    def problem_file_VITECH():
        pass


def main():
    file_name = "MBSE_HDDL_translation_excel_v3_01_09_2021.xlsx"
    # read the excel file and save it in a database 
    mbse_db = pd.read_excel(file_name)
    print('--------------')
    print(mbse_db.shape)
    
    print('Save to List the different rows')
    Number = mbse_db['Number'].tolist()
    Class = mbse_db['Class Class'].tolist()
    Name = mbse_db['Entity'].tolist()
    Inputs = mbse_db['Inputs'].tolist()
    Outputs = mbse_db['Outputs'].tolist()
    Decomposed_by = mbse_db['decomposed by Targets'].tolist()
    Decomposes= mbse_db['decomposes Targets'].tolist()
    Category = mbse_db['categorized by Targets'].tolist()
    Description = mbse_db['description'].tolist()
    
    # print(Number)
    # print(Class)
    # print(Name)
    # print(Inputs)
    # print(Outputs)
    # print(Tasks)
    # print(Category)
    # print(Description)
    print('--------------')
    
    domain_name = 'rover'
    file = MBSE_HDDL_TRANSLATION_VITECH(domain_name, Number, Class, Name, Inputs, Outputs, Decomposed_by, Decomposes, Category, Description)
    file.domain_file_VITECH()
    
    
    
    # # Dataframe to list! Directly! 
    # mbse_df_list = mbse_db.values.tolist()
    # print(mbse_df_list[0:2])
    
    
    
    
    
    
    

if __name__ == "__main__":
    main()