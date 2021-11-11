# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 16:19:39 2021

@author: Jasmine Rimani
"""
from bs4 import BeautifulSoup

class XML_parsing():
    
    def __init__(self, file):
        # File that we need to parse
        self.file = file
        
        # Packages list 
        self.package_list = []
        # Type list
        self.hddl_type_list = []
        # Predicates list
        self.hddl_predicate_list = []
        # Actors list
        self.actor_list = []       
        # Requirements domain files
        self.requirements_list = [] # <-- To implement!!
        # HighLevel UseCase list - Tasks
        self.task_list = []
        # UseCase parameter list
        self.useCase_list_parameter = []
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
        # Edges List 
        self.edge_list = []
        # List with all the parameters
        self.all_parameters_list = []
        #Action Inputs
        self.opaqueAction_input_list = []
        #Action Outputs 
        self.opaqueAction_output_list = []
        # # Only the name inputs
        # self.method_input_types_list_names = []
        # # Only the name of predicates
        # self.method_input_predicate_list_names = []
        
    def DomainFileList(self):

        # Passing the stored data inside
        # the beautifulsoup parser, storing
        # the returned object in a variable - that is the main object to unpack
        Bs_data = BeautifulSoup(self.file, "xml")
         
        # # # Finding all instances of tag - You get a list with all the instances with that tag
        # b_node = Bs_data.find_all('node')
        # If the tags are nested - you get each tag one after the other from the order of the file
        
        # Find all the packaged elements
        b_packagedElement = Bs_data.find_all('packagedElement') 
        # Isolate the "xmi:type="uml:Package" " --> e.g. b_packagedElement[0]['xmi:type']
        for index,ii in enumerate(b_packagedElement):
            
            if ii['xmi:type'] == 'uml:Package':
                self.package_list.append({"name": ii['name'], "xmi:id":ii['xmi:id']})    
            
            if ii['xmi:type'] == 'uml:Class':
                self.hddl_type_list.append({"name": ii['name'], "xmi:id":ii['xmi:id']})
                
            # Isolate Actors:
            if ii['xmi:type'] == 'uml:Actor':
                self.actor_list.append({"name": ii['name'], "xmi:id":ii['xmi:id']})
            
            # Isolate Usecases that are packegedElements --> You get your tasks name, however you still need your parameters
            # Parameters --> Take the minumum parameters from the method --> look lower in the 
            if ii['xmi:type'] == 'uml:UseCase':
                self.task_list.append({"name": ii['name'], "xmi:id":ii['xmi:id'], "parameters": []})   
        
        
        # Find all the edges
        b_edges = Bs_data.find_all('edge')      
        
        # Map all the edges
        for index,ii in enumerate(b_edges):
            self.edge_list.append({"xmi:id":ii['xmi:id'], "input":ii['source'], "output":ii['target']}) 
        
        # Check your parsing (comment after use):
        # print('Packages list: \n {}'.format(self.package_list))
        # print('Classes list: \n {}'.format(self.hddl_type_list))
        # print('Actors list: \n {}'.format(self.actor_list))
        # print('UseCase: \n {}'.format(self.task_list))
        # print('Links between the entities: \n {}'.format(self.edge_list))

        # # Access any instance of the dictionary use case with UseCase_list[n] and any key of the dictionary with get() UseCase_list[1].get('name')
                
        """
        For each useCase, we  can access to the sub-tags with: 
            a = b_packagedElement[n].children  # --> with n elements in b_packagedElement
            for i in a: print(i) # --> you will see all the subtags
        """
        method_input_predicate_list_names = []
        method_input_types_list_names = []
        self.method_Actions = []
        # The packagedElements are: Packages, Actors, UseCases, Classes
        for uu in b_packagedElement:
            
            # If the packagedElement is a UseCase
            if uu['xmi:type'] == 'uml:UseCase':
                
                # Look at its children and find...
                for index,ii in enumerate(uu.children):
                
                    # Find the methods
                    try: 
                        # Check the sub-UseCases that can be methods: double check on the type(considered as attribute) and the tag name
                        if ii['xmi:type'] == 'uml:UseCase' and ii.name == 'ownedUseCase':
                            
                            self.method_list.append({"name": ii['name'], "xmi:id":ii['xmi:id'], "task":uu.get('xmi:id')})  
                            
                            # Look at the children of the method to recognize parameters and opaque actions
                            for jj in ii.descendants:
                                # print(jj.name)
                                
                                try:
                
                                    # Start already dividing predicates(sentences) from the parameters
                                    if jj['xmi:type'] == 'uml:ActivityParameterNode':
                                        
                                        # Create a temporary dictionary with the paramters characteristics
                                        temp_dict = {"name": jj['name'], "xmi:id":jj['xmi:id'], "type":jj['type'], "method": ii['xmi:id'], "task":uu.get('xmi:id')} 
                                        
                                        # Assign to each ActivityParameter a Type
                                        for kk in self.hddl_type_list:
                                            if kk['xmi:id'] == temp_dict['type']:
                                                temp_dict["type_name"] = kk["name"]    
                                                
                                        # Check if the attribute has a type! - if it doesn't just assign the name as type!
                                        if not(temp_dict['type_name']) and len(temp_dict["type_name"].split()) <= 1:
                                            temp_dict["type_name"] = jj['name']
                                            self.hddl_type_list.append({"name": jj['name'], "xmi:id":''})
                                            
                                            """ 
                                            TO DO - FEEDBACK TO PAPYRUS
                                                ADD THE TYPE TO THE TYPE PACKAGE IN THE PAPYRUS MODEL
                                            """
                                            
                                            print('No predefined type for {} \n Add it on Papyrus!'.format(temp_dict.get('name')))
                                            
                                        if not(temp_dict['type_name']) and len(temp_dict["type_name"].split()) > 1:
                                            temp_dict["type_name"] == 'predicate'
                                            
                                            """ 
                                            TO DO - FEEDBACK TO PAPYRUS
                                                ADD THE TYPE TO THE TYPE PACKAGE IN THE PAPYRUS MODEL
                                            """
                                            
                                            print('No predefined type for {} \n Add it on Papyrus!'.format(temp_dict.get('name')))                                        
                                        
                                        # Check if the attribute has an incoming edge - output
                                        if jj.has_attr('incoming'):
                                            temp_dict["incoming"] = jj["incoming"]   
                                        
                                        # Check if the attribute has an outcoming edge - input
                                        if jj.has_attr('outgoing'):
                                            temp_dict["outgoing"] = jj["outgoing"] 
                                        
                                        # Chek if the attribute is a parameters - if yes save it in the method inputs list
                                        x = 1
                                        if temp_dict["type_name"] != 'predicate' or len(temp_dict["name"].split()) <= 1:
                                            self.method_input_types_list.append(temp_dict)
                                            method_input_types_list_names.append(temp_dict["name"]+'-'+temp_dict["type_name"])
                                        
                                        # The preconditions are ActivityParameters that have on outgoing edge but no incoming one 
                                        # (if the have an incoming one then they are activated by one on the Opaque Actions)
                                        if 'outgoing' in temp_dict and  not('incoming' in temp_dict) and len(temp_dict["name"].split()) > 1:
                                            self.method_input_predicate_list.append(temp_dict)
                                            method_input_predicate_list_names.append(temp_dict["name"])
                                            # Save all the predicates name to a list 
                                            self.all_predicates_list.append(temp_dict["name"])
                                        
                                        # If the attribute is an output, so it has an incoming edge- save it! :) 
                                        if 'incoming' in temp_dict and len(temp_dict["name"].split()) > 1:
                                            self.method_output_predicate_list.append(temp_dict)
                                            # Save all the predicates name to a list 
                                            self.all_predicates_list.append(temp_dict["name"])

                                except:
                                    pass
                                
                                try:
                                    
                                    
                                    # Initialize the ordered tasks in the Method
                                    self.method_list[-1]['ordered_tasks'] = []
                                    
                                    # Find the tasks 
                                    if jj['xmi:type'] == 'uml:OpaqueAction' :
                                        # An Opaque action should always have an input and an output! 
                                        self.opaqueAction_list.append({"name": jj['name'], "xmi:id":jj['xmi:id'], "incoming_link": jj['incoming'],  "outcoming_link": jj['outgoing'], "method": ii['xmi:id'], "task":uu.get('xmi:id')})  
                                        for kk in jj.children:
                                            # Each Opaque Action has input and outputs defined by xmi:type="uml:InputPin" or xmi:type="uml:OutputPin"
                                            try:
                                                # If it is an input save it into an input data structure associated to the Action name and ID
                                                if kk['xmi:type'] == 'uml:InputPin':
                                                    self.opaqueAction_input_list.append({"xmi:id":kk['xmi:id'], "action": jj['xmi:id'], "incoming_edge": kk['incoming'], "method": ii['xmi:id'], "task":uu.get('xmi:id')})  
                                                
                                                # If it is an output save it into an output  data structure associated to the Action name and ID
                                                if kk['xmi:type'] == 'uml:OutputPin':
                                                    self.opaqueAction_output_list.append({ "xmi:id":kk['xmi:id'], "action": jj['xmi:id'], "outgoing_edge": kk['outgoing'], "method": ii['xmi:id'], "task":uu.get('xmi:id')}) 
                                                    
                                                    # Check if the outcoming edge has a name or not - Names are used to define the orders of the output
                                                    if (kk.has_attr('name')):
                                                        self.opaqueAction_output_list[-1]["name"] = kk['name']
                                                        # the number of the output is the end value of the string
                                                        self.opaqueAction_output_list[-1]["number"] = ''.join((filter(str.isdigit, self.opaqueAction_output_list[-1].get('name')))) 
                                                
                                               
                                            
                                            except:
                                                pass
                                    
                                        self.method_Actions.append(jj['xmi:id'])


                                    
                                except:
                                    pass
                                
     
                            self.method_list[-1]['parameters'] = set(method_input_types_list_names)
                            method_input_types_list_names.clear()
                            # For each method associate the inputs
                            self.method_list[-1]['preconditions'] = set(method_input_predicate_list_names)
                            method_input_predicate_list_names.clear()
                            # Add the tasks to the method list of ordered tasks 
                            self.method_list[-1]['ordered_tasks'] = set(self.method_Actions)
                            self.method_Actions.clear()
                                
                    except:
                        pass
            
        
        
        x = 1 
        # # For each method go back to the opaque action and associate the inputs/outputs and the parameters as well as the types
        # temporary_input_list = []
        # temporary_output_list = []
        # temporary_parameter_list = []
        
        # # Look at all the Actions
        # for ii in OpaqueAction_list:
            
        #     # Look at the inputs' and paramaters predicate to the actions
        #     for jj in OpaqueAction_input_list:
        #         # check the action id
        #         if jj.get('action') == ii.get('xmi:id'):
        #             # Get the incoming edge ID
        #             get_Edge_id = jj.get('incoming_edge')
        #             for kk in edge_list:
        #                 # check the edges id
        #                 if kk.get('xmi:id') == get_Edge_id:
        #                     # get the source of the edge
        #                     input_edge = kk.get('input')
                            
        #                     for gg in method_input_predicate_list :
        #                         # in the method predicate list get the name of the predicate
        #                         if ii.get('method') == method_input_predicate_list.get('method'):
        #                             # Inputs
        #                             temporary_input_list.append(gg.get('name'))
                                    
        #                     for gg in method_input_types_list :
        #                         # in the method predicate list get the name of the predicate
        #                         if ii.get('method') == method_input_types_list.get('method'):
        #                             # Inputs
        #                             temporary_parameter_list.append(gg.get('name')+'-'+gg.get('type_name'))
                    
                    
        #     # Look at the outputs' predicate to the actions
        #     for jj in OpaqueAction_output_list:
        #         # check the action id
        #         if jj.get('action') == ii.get('xmi:id'):
        #             # Get the incoming edge ID
        #             get_Edge_id = jj.get('incoming_edge')
        #             for kk in edge_list:
        #                 # check the edges id
        #                 if kk.get('xmi:id') == get_Edge_id:
        #                     # get the source of the edge
        #                     input_edge = kk.get('output')
        #                     for gg in method_input_predicate_list :
        #                         # in the method predicate list get the name of the predicate
        #                         if ii.get('method') == method_output_predicate_list.get('method'):
        #                             # Inputs
        #                             temporary_output_list.append(gg.get('name'))           
            
        #     # Associate inputs and outputs to the action 
        #     ii["preconditions"] = temporary_input_list
        #     ii["effects"] = temporary_output_list
        #     ii["parameters"] = temporary_parameter_list
        #     # Clear the lists
        #     temporary_input_list.clear() 
        #     temporary_output_list.clear()
        #     temporary_parameter_list.clear()
        
        
        # # Check the tasks - if they all have the initial name and the same parameters, inputs and effects then they are one function
        # Final_Opaque_Action_List = OpaqueAction_list
        # # Look at all the Actions
        # for ii in OpaqueAction_list:
        #     for jj in OpaqueAction_list:
        #         if ii['name'] in jj['name'] and ii['name']!=jj['name']:
        #             # OpaqueAction_list.remove(jj)
        #             # or you can do it with a dummy list 
        #             Final_Opaque_Action_List.remove(jj)
        
        # # Among the methods of the task take the one with the least input paramters - those are the parameter of the task unless the task is used in another task
        # # then take the parameter of that task as minumum parameters.
        
        # task_inputs = []
        # # Search in all tasks
        
        # # For each task search the method
        # for jj in Method_list:
            
        #     if b_packagedElement[10].get('xmi:id') == jj.get('task'):
        #         # for each method check the length of the parameters list - if it longer than the one of the task, leave it like that - if not replace the list
        #         if len(b_packagedElement[10]["parameters"]) >= len(jj.get('parameters')):
        #             b_packagedElement[10]["parameters"] = jj.get('parameters')
        
        
        
        # # Take the overall predicate list and:
        #     # search for duplicates and associate the type to each predicate
        #     # write the predicate on the predicate list
        #     # always check for duplicates
        
        # temporary_predicate = []
        # predicate_list = []
        
        # for ii in all_predicates_list:
        #     # first take the predicate and open it:
        #     cleaned_predicate = ii.split()
        #     #remove the branket 
        #     cleaned_predicate.remove('(')
        #     #remove negations
        #     cleaned_predicate.remove('not')
        #     #get the first word of the predicate
        #     temporary_predicate.append(cleaned_predicate[0])
        #     # analyse all other words
        #     for jj in cleaned_predicate[1::]:
        #         counter_arg = 0 
        #         for kk in method_input_types_list:
        #             if jj == kk.get('name'):
        #                 temporary_predicate.append('?arg{} - {}'.format(counter_arg,kk.get('type_name')))
        #                 counter_arg  = counter_arg + 1
            
        #     #create the predicate final version
        #     final_predicate= ' '.join(temporary_predicate)
            
        #     if not(final_predicate in predicate_list):
        #         predicate_list.append(({}).format(final_predicate))
        #         temporary_predicate.clear()
                        
                    
        # xmi:id https://stackoverflow.com/questions/58839091/how-to-generate-uuid-in-python-withing-given-range
        
        
        # print('Packages:', package_list)
        # print('HDDL Types:', hddl_type_list)
        # print('Use Cases - Task Level:',Task_list)
        # print('Use Cases - Method Level:',Method_list)
        

        
    def GeneralParsing(self):
        
        # Functions
        
        # Parameters
        
        # Actors
        
        # C
        
        pass
    
    
    
def main():

    with open('xml_sample.uml', 'r') as f:
        data = f.read()
    
    file_final = XML_parsing(data)
    file_final.DomainFileList()



if __name__ == "__main__":
    main()