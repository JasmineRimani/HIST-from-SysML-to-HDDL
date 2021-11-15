# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 16:19:39 2021

@author: Jasmine Rimani
"""
from bs4 import BeautifulSoup
from datetime import datetime

class XML_parsing():
    
    def __init__(self, file):
        # File that we need to parse
        self.file = file
        # Put an adaptable domain file name
        self.domain_name = 'domain'
        
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
        # Domain File Name based on the domain name and date
        self.name_string = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p") + '_' +'_domain.hddl' 
        # Problem_file_Name
        self.name_string_pf = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p") + '_' +'_problem.hddl'
        # # Only the name inputs
        # self.method_input_types_list_names = []
        # # Only the name of predicates
        # self.method_input_predicate_list_names = []
        
    def XML_ActiveParsing(self):

        # Passing the stored data inside
        # the beautifulsoup parser, storing
        # the returned object in a variable - that is the main object to unpack
        Bs_data = BeautifulSoup(self.file, "xml")
         
        # # # Finding all instances of tag - You get a list with all the instances with that tag
        # b_node = Bs_data.find_all('node')
        # If the tags are nested - you get each tag one after the other from the order of the file
        
        # Find all the packaged elements
        # You can divide the packaged elements per Folder - so that you don't have to parse useless informations like the ones for the Mission
        
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
        
        
        # you can check is the packagedElement has the "Functions" package as parent
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
                                        if jj.has_attr('type'):
                                            temp_dict = {"name": jj['name'], "xmi:id":jj['xmi:id'], "type":jj['type'], "method": ii['xmi:id'], "task":uu.get('xmi:id')} 
                                        
                                        else:
                                            temp_dict = {"name": jj['name'], "xmi:id":jj['xmi:id'], "type":" ", "type_name": " ","method": ii['xmi:id'], "task":uu.get('xmi:id')} 
                                        
                                        # Assign to each ActivityParameter a Type
                                        for kk in self.hddl_type_list:
                                            if kk['xmi:id'] == temp_dict['type']:
                                                temp_dict["type_name"] = kk["name"]    
                                                
                                        # Check if the attribute has a type! - if it doesn't just assign the name as type!
                                        if temp_dict['type_name'] == " " and len(temp_dict["name"].split()) <= 1:
                                            temp_dict["type_name"] = jj['name']
                                            self.hddl_type_list.append({"name": jj['name'], "xmi:id":''})
                                            
                                            """ 
                                            TO DO - FEEDBACK TO PAPYRUS
                                                ADD THE TYPE TO THE TYPE PACKAGE IN THE PAPYRUS MODEL
                                            """
                                            
                                            print('No predefined type for {} \n Add it on Papyrus!'.format(temp_dict.get('name')))
                                            
                                        if temp_dict['type_name'] == " " and len(temp_dict["name"].split()) > 1:
                                            temp_dict["type_name"] = 'predicate'
                                            
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

                                        if temp_dict["type_name"] != 'predicate' or len(temp_dict["name"].split()) <= 1:
                                            self.method_input_types_list.append(temp_dict)
                                            method_input_types_list_names.append(temp_dict["name"]+'-'+temp_dict["type_name"])
                                        
                                        # The preconditions are ActivityParameters that have on outgoing edge but no incoming one 
                                        # (if the have an incoming one then they are activated by one on the Opaque Actions)
                                        if 'outgoing' in temp_dict and not('incoming' in temp_dict) and len(temp_dict["name"].split()) > 1:
                                            self.method_input_predicate_list.append(temp_dict)
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
                                            if len(temp_dict["name"].split()) > 1:
                                                 self.method_input_predicate_list.append(temp_dict)
                                                 method_input_predicate_list_names.append(temp_dict["name"])
                                                 self.all_predicates_list.append(temp_dict["name"])
                                            if len(temp_dict["name"].split()) <= 1:
                                                self.method_input_types_list.append(temp_dict)
                                                method_input_types_list_names.append(temp_dict["name"]+'-'+temp_dict["type_name"])
                                            

                                except:
                                    if jj != '\n' and jj.name != 'body' and not(isinstance(jj, str)):
                                        print('Something Wrong! Check lines before 194')                             
                                
                                
                                try:
                                    
                                    
                                    # Initialize the ordered tasks in the Method
                                    self.method_list[-1]['ordered_tasks'] = []
                                    
                                    # Find the atomic actions and Find the tasks in the main task
                                    if jj['xmi:type'] == 'uml:OpaqueAction' or jj['xmi:type'] == 'uml:CallBehaviorAction' :
                                        # An Opaque action should always have an input and an output! 
                                        self.opaqueAction_list.append({"name": jj['name'], "xmi:type": jj['xmi:type'], "xmi:id":jj['xmi:id'], "incoming_link": jj['incoming'],  "outcoming_link": jj['outgoing'], "method": ii['xmi:id'], "task":uu.get('xmi:id')})  
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
                                                if kk != '\n':
                                                    print('Something Wrong! Check lines before 228')
                                    
                                        self.method_Actions.append(jj['xmi:id'])

                                    # 
                                    # if jj['xmi:type'] == 'uml:OpaqueAction' :
                                    #     # An Opaque action should always have an input and an output! 
                                    #     self.opaqueAction_list.append({"name": jj['name'], "xmi:id":jj['xmi:id'], "incoming_link": jj['incoming'],  "outcoming_link": jj['outgoing'], "method": ii['xmi:id'], "task":uu.get('xmi:id')})                                      
      

                                    
                                except:
                                    if jj != '\n' and jj.name != 'body' and not(isinstance(jj, str)):
                                        print('Something Wrong! Check lines before 235')
                                
     
                            self.method_list[-1]['parameters'] = set(method_input_types_list_names)
                            method_input_types_list_names.clear()
                            # For each method associate the inputs
                            self.method_list[-1]['preconditions'] = set(method_input_predicate_list_names)
                            method_input_predicate_list_names.clear()
                            # Add the tasks to the method list of ordered tasks 
                            self.ordered_actions = []
                            for yy in self.method_Actions:
                                for bb in self.opaqueAction_list:
                                    if yy == bb['xmi:type']:
                                        if bb['incoming_link'] in self.method_Actions:
                                            a = self.method_Actions.index(yy)
                                            self.method_Actions.pop(a)
                                            b = self.method_Actions.index(bb['incoming_link'])
                                            self.method_Actions.insert(b+1,yy)

                            self.method_list[-1]['ordered_tasks'] = set(self.method_Actions)
                            self.method_Actions.clear()
                                
                    except:
                        if ii != '\n' and ii.name != 'body' and not(isinstance(ii, str)):
                            print('Something Wrong! Check lines before 248')
            
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
            
            # Associate inputs and outputs to the action 
            ii["preconditions"] = set(temporary_input_list)
            ii["effects"] = set(temporary_output_list)
            ii["parameters"] = set(temporary_parameter_list)
            # Clear the lists
            temporary_input_list.clear() 
            temporary_output_list.clear()
            temporary_parameter_list.clear()
        
        # x = 1
        # Check the tasks - if they all have the initial name and the same parameters, inputs and effects then they are one function
        final_opaque_action = []
        # Look at all the Actions
        for ii in self.opaqueAction_list:
            
            # Split the name of the action
            name = ii['name'].split('_')[0]
            final_opaque_action.append(name)
            
        
        final_opaque_action_set = set(final_opaque_action)  
        
        final_opaque_action_list = []
        
        for ii in self.opaqueAction_list:
            for jj in final_opaque_action_set:
                if ii['name'] == jj and ii['xmi:type'] != 'uml:OpaqueAction':
                    final_opaque_action_list.append(ii)
                
            
            

        

        # # Among the methods of the task take the one with the least input paramters - those are the parameter of the task unless the task is used in another task
        # # then take the parameter of that task as minumum parameters.
        
        # task_inputs = []
        # # Search in all tasks
        
        # # For each task search the method
        
        # Missing - when a Task is an action of another task - xmi:type="uml:CallBehaviorAction (should be ok - still to test - look at method1 of TakePicture)
        # Missing - when a Method don't have incoming or outcoming edges (should be ok - still to test - look at method2 of NavigateToGoal)
        # """START TESTING FROM HERE!!!!!!!!!"""
        # First Look if the task is in another task with its parameters.
        for ii in self.opaqueAction_list:
            if ii['xmi:type'] == 'uml:CallBehaviorAction':
                for jj in self.task_list:
                    if jj.get('name') == ii.get('name'): 
                        jj["parameters"] = ii.get('parameters')


        for ii in self.task_list:
            for jj in self.method_list:
                
                if ii.get('xmi:id') == jj.get('task'):
                    # for each method check the length of the parameters list - if it longer than the one of the task, leave it like that - if not replace the list
                    if ii["parameters"] != []:
                        if len(ii["parameters"]) >= len(jj.get('parameters')):
                            ii["parameters"] = jj.get('parameters')
                    else:
                        ii["parameters"] = jj.get('parameters')
        
        
        # x = 1 # the random x=1 that you find around are my debug point - just ignore them
        
        
        # # Take the overall predicate list and:
        #     # search for duplicates and associate the type to each predicate
        #     # write the predicate on the predicate list
        #     # always check for duplicates
        
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
            
            
            if not(final_predicate in self.predicate_list):
                self.predicate_list.append(('{}').format(final_predicate))
                
            temporary_predicate.clear()
                        
        x = 1                  
        # xmi:id https://stackoverflow.com/questions/58839091/how-to-generate-uuid-in-python-withing-given-range
        
        
        # print('Packages:', package_list)
        # print('HDDL Types:', hddl_type_list)
        # print('Use Cases - Task Level:',Task_list)
        # print('Use Cases - Method Level:',Method_list)
        

        
    def Domain_FileWriting (self):
        ###################################################################
        # Open/Create the File
        file = open(self.name_string,'w')
        # Start writing on the file
        file.write('(define (domain {}) \n'.format(self.domain_name))
        """
        Maybe consider the different type or requirement - define on papyrus a way to define the requirements 
        of the domain file --> maybe as comment to the packages.
        """
        file.write('(:requirements :typing :hierachie) \n')
        #Object Type
        file.write('(:types \n')
        for ii in self.hddl_type_list:
            file.write('{} - object'.format(ii.get('name')))
        # End of object type
        file.write(') \n')  
        
        # x = 0
        
        # Predicates
        file.write('(:predicates \n')
        #Writes Predicates
        for ii in self.predicate_list:
            file.write('({})'.format(ii))
        # End of predicates
        file.write(') \n')   
            
        # #Tasks!
        file.write('\n')  #space!
        for ii in self.task_list:
            file.write('(:task {} \n)'.format(ii.get('name')))            
            file.write('\t :parameters (?{}) \n'.format(' ?'.join(ii.get('parameters'))))
            file.write('\t :precondition ()\n')
            file.write('\t :effect ()\n')
            file.write(') \n') 
            
        #Methods!
        # Introduce the order in the tasks
        # have just the first word of the parameters
        string_vector = []
        order_vector = []
        file.write('\n')  #space!
        for ii in self.method_list:
            file.write('(:method {} \n)'.format(ii.get('name')))
            file.write('\t :parameters (?{}) \n'.format(' ?'.join(ii.get('parameters'))))
            if ii.get('preconditions') != '':
                file.write('\t :precondition (and {})\n'.format(' \n'.join(ii.get('preconditions'))))
            else:
                file.write('\t :precondition ()\n')
            counter = 0
                
            for jj in ii['ordered_tasks']: 
                for kk in self.opaqueAction_list:
                    if kk['xmi:id'] == jj:
                        # Task Parameters
                        dummy_string = ' '.join(kk['parameters'])
                        dummy_vector = dummy_string.split()
                        # vector[start:end:step]
                        dummy_vector = dummy_vector[0::2]
                        string_vector.append('task{} ({} ?{}) \n'.format(counter,kk['name'], ' ?'.join(dummy_vector) ))
                        counter = counter + 1
                    if counter != 0:
                        # For each task check incoming and outcoming links
                        order_vector.append('(< task{} task{})'.format(counter-1, counter))

            if counter != 0 and counter != 1:
                file.write('\t :subtasks (and \n')
                file.write('\t {}\n'.format(string_vector))
                file.write('\t ) \n')
                file.write('\t :ordering (and \n')
                file.write('\t {}\n'.format(order_vector))
                file.write('\t ) \n')
            elif counter == 1:
                file.write('\t :subtasks (and \n')
                file.write('\t {}\n'.format(string_vector))
                file.write('\t ) \n')
            else:
               file.write('\t :subtasks () \n') 
                
            file.write(') \n') 

        #Actions
        file.write('\n')  #space!
        for ii in self.opaqueAction_list:
            if ii['xmi:type'] != 'uml:CallBehaviorAction':
        
                for ii in self.opaqueAction_list:
                    file.write('(:action {} \n)'.format(ii.get('name')))            
                    file.write('\t :parameters (?{}) \n'.format(' ?'.join(ii.get('parameters'))))
                    if ii.get('preconditions') != '':
                        file.write('\t :precondition (and {})\n'.format(' \n'.join(ii.get('preconditions'))))
                    else:
                        file.write('\t :precondition ()\n')
                    if ii.get('preconditions') != '':
                        file.write('\t :effect (and {})\n'.format(' \n'.join(ii.get('effects'))))
                    else:
                        file.write('\t :effect ()\n')
                        
                    file.write(') \n') 
        
        # end of the file
        file.write(')')
    
    def Problem_FileWriting (self):
        file = open(self.name_string_pf,'w')
        file.write('(define ')
        file.write('\t (domain {}) \n'.format(self.domain_name))
        file.write('\t (:objects')
        # Take the first part of the C++ code
        
        # Add the equipments of the system
        
        # Create the initial task network
        
        # Put the ordering of the tasks
        
        # Set the problem initial conditions
        
        file.write(') \n') 
        
    
def main():

    with open('xml_sample.uml', 'r') as f:
        data = f.read()
    
    file_final = XML_parsing(data)
    # Actively Parse the XML
    file_final.XML_ActiveParsing()
    # Create the file that you need/want
    # Create domain file
    file_final.Domain_FileWriting()



if __name__ == "__main__":
    main()