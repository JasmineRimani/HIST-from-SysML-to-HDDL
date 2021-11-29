# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 16:19:39 2021

@author: Jasmine Rimani
"""
from bs4 import BeautifulSoup
from datetime import datetime
import re
import uuid


"""
packagedElement = Everything that is packaged by the model

ownedComment = comments in the UML/SysML model

body = body of comments or notes in UML/SysML

generalization = in UML Use Case - the generalization extends the capabilities of an element with the capabilities of the parent element

ownedEnd = in the association type we have owned end --> they define the end that are connected by the association as new elements (xmi:type="uml:Property")
           the end element are defined by a type (type="_Tkl1IC2FEeylqPZKkKN_nQ") that links them to the original ends. So you need to read the type in the association
           ownedEnd to find which primitive elements are associated.

ownedUseCase = in the UseCase type - if the task is decomposed, we will have this tag! To see if the ownedUseCase is a method you can: (i) check for the word 'method' in the string,
               (ii) see if the ownedUseCase has an ownedBehavior, (iii) see if the UseCase has an "extend" tag

ownedBehavior = Activity Diagram associated to the ownedUseCase --> It describes the method graphically!


edge = connections in the Activity Diagram


node = elements in the activity diagrams (e.g starting node, end node, actions)

inputValue/outputValue = Inputs/outputs to an opaque actions --> you can use it to see the edges and

upperBound = Used in the input pin if we have a numerical input --> maybe useful for temporal HDDL planning

extend = when a UseCase can be explained by other sub-UseCases it extends the UseCase --> Used to define the method of a task

ownedRule = Used to define Constrains - used to create automatically the initial conditions in the problem file.

# List of Tags in the XML file

Maybe_useful_later_Tags = ['upperBound'] 

NotUsed_Tags = ['ownedComment', 'body', 'generalization']

Used_Tags = ['packagedElement', 'ownedEnd', 'ownedUseCase', 'ownedBehavior', 'edge', 'node', 'inputValue', 'outputValue', 'extend']

"""


"""

xmi:id = unique identifier for each element of the xml

xmi:type="uml:Package"  -->  uml folder/package - in our translation for the domain file we have:
    - Requirements: e.g.
        <packagedElement xmi:type="uml:Package" xmi:id="_rfy78C2DEeylqPZKkKN_nQ" name="Requirements"/>
    - Functions : e.g.
        <packagedElement xmi:type="uml:Package" xmi:id="_uVrj8C2DEeylqPZKkKN_nQ" name="Functions">
    - Types: e.g.
        <packagedElement xmi:type="uml:Package" xmi:id="_wVEBwC2DEeylqPZKkKN_nQ" name="Types">
        
xmi:type="uml:Actor" -->  Actor in the UseCase Diagrams:
    <packagedElement xmi:type="uml:Actor" xmi:id="_rSxXIC2EEeylqPZKkKN_nQ" name="Drone">

xmi:type="uml:Generalization" --> Used with the generalization tab:
    <generalization xmi:type="uml:Generalization" xmi:id="_IHgGwC2FEeylqPZKkKN_nQ" general="_qErzYC2EEeylqPZKkKN_nQ"/>

xmi:type="uml:Association" --> Link between two elements:
    <packagedElement xmi:type="uml:Association" xmi:id="_ovqEsC2FEeylqPZKkKN_nQ" memberEnd="_ovsg8C2FEeylqPZKkKN_nQ _ovtvEC2FEeylqPZKkKN_nQ">
    the starting and ending point are identified in memberEnd separared by a space
    
xmi:type="uml:Property" --> used in the association ownedEnd tag to define the ends:
    <ownedEnd xmi:type="uml:Property" xmi:id="_1ejZMi2FEeylqPZKkKN_nQ" name="goback" type="_Y5doEC2FEeylqPZKkKN_nQ" association="_1eiyIC2FEeylqPZKkKN_nQ"/>

xmi:type="uml:UseCase" --> This is the functions we need for the translation! You have the task that is the high-level UseCase:
    <packagedElement xmi:type="uml:UseCase" xmi:id="_a2yF0C2EEeylqPZKkKN_nQ" name="NavigateToGoal" visibility="public">

xmi:type="uml:Activity" --> Activity Diagram owned by the ownedBehavior in the ownedUseCase:
    <ownedBehavior xmi:type="uml:Activity" xmi:id="_zBZsMC2DEeylqPZKkKN_nQ" name="NavigateToGoal_method1" 
    node="_qEhrQC2YEeylqPZKkKN_nQ _b4pl8C2ZEeylqPZKkKN_nQ _Z4GYkC2bEeylqPZKkKN_nQ _uzdYMC2bEeylqPZKkKN_nQ _2wQPoC2bEeylqPZKkKN_nQ _-6gUQC2bEeylqPZKkKN_nQ _D6FzsC2cEeylqPZKkKN_nQ _FqL4UC2cEeylqPZKkKN_nQ _K3QaIC2cEeylqPZKkKN_nQ _KKOfkC2dEeylqPZKkKN_nQ _Nnha8C2fEeylqPZKkKN_nQ _WfN0YC2fEeylqPZKkKN_nQ _ZDercC2gEeylqPZKkKN_nQ _3c_nkC2gEeylqPZKkKN_nQ">
    In the Activity node, we the list of the elements included in the activity diagram: actions, connections, inputs, outputs

xmi:type="uml:ObjectFlow" --> the associations in the activity diagram: they have a target and a source - so we can know if a predicate is an input or an output of an action:
    <edge xmi:type="uml:ObjectFlow" xmi:id="_v6CwUC2cEeylqPZKkKN_nQ" target="_TdB9IC2cEeylqPZKkKN_nQ" source="_2wQPoC2bEeylqPZKkKN_nQ">

xmi:type="uml:ControlFlow" --> same of the ObjectFlow for this translation - however the  xmi:type="uml:ObjectFlow" has more characteristics and it show a flow of data.
                               However, for this translation they are equal.        

xmi:type="uml:ActivityParameterNode" --> The input/outputs of the Activity Diagram:
    <node xmi:type="uml:ActivityParameterNode" xmi:id="_b4pl8C2ZEeylqPZKkKN_nQ" name="(at ?system ?from_wp)" outgoing="_9U9dUC2cEeylqPZKkKN_nQ" type="_94GG8C2ZEeylqPZKkKN_nQ">
    the type sub-tag defines if it is a predicate of HDDL or something different.

xmi:type="uml:OpaqueAction" --> the actions in the HDDL:
    <node xmi:type="uml:OpaqueAction" xmi:id="_uzdYMC2bEeylqPZKkKN_nQ" name="Visit" incoming="_r8VAwC2gEeylqPZKkKN_nQ" outgoing="_odRf8C2gEeylqPZKkKN_nQ">
              <inputValue xmi:type="uml:InputPin" xmi:id="_TdB9IC2cEeylqPZKkKN_nQ" name="" incoming="_v6CwUC2cEeylqPZKkKN_nQ">
              The incoming/outcoming are related to the other actions
             
xmi:type="uml:InputPin"/ xmi:type="uml:OutputPin" --> input/output to an opaque action:
    <inputValue xmi:type="uml:InputPin" xmi:id="_TdB9IC2cEeylqPZKkKN_nQ" name="" incoming="_v6CwUC2cEeylqPZKkKN_nQ">
                <upperBound xmi:type="uml:LiteralInteger" xmi:id="_TdCkMC2cEeylqPZKkKN_nQ" value="1"/>
    </inputValue>

xmi:type="uml:ActivityFinalNode"/ --> Initial/Final node of the Activity
                             
xmi:type="uml:Extend" ---> Define the extension of a UseCase - one usecase extends the other. Perfect to define methods of a task:
    <extend xmi:type="uml:Extend" xmi:id="_RP4HEC2yEeyropzrv_OlDA" extendedCase="_a2yF0C2EEeylqPZKkKN_nQ" extensionLocation="_RP4uIC2yEeyropzrv_OlDA"/>

xmi:type="uml:Class" --> the types in the HDDL have been classified as classes
        <ownedRule xmi:type="uml:Constraint" xmi:id="_JH5wAEZAEeyhYpX6KgufSQ" name="(at rover waypoint(n))" constrainedElement="__GKP0EXzEeyhYpX6KgufSQ">
          <specification xmi:type="uml:OpaqueExpression" xmi:id="_JH6XEEZAEeyhYpX6KgufSQ" name="constraintSpec">
            <language>OCL</language>
            <body>true</body>
          </specification>
        </ownedRule>



xmi:type="uml:Constraint" --> constrains to the functions in the Mission package (the one that will define the problem file)

# List of Tags in the XML file

Maybe_useful_later_Tags = ['upperBound'] 

NotUsed_Tags = ['ownedComment', 'body', 'generalization']

Used_Tags = ['packagedElement', 'ownedEnd', 'ownedUseCase', 'ownedBehavior', 'edge', 'node', 'inputValue', 'outputValue', 'extend']

"""


"""
visibility = if the class if public/private or accessible only by subclasses

name = name of the element as given from the UML/SySML model

general = used in the generalization tag to show what is being generalized

memberEnd = used in association to define the extremes of the association "start_node end_node" separated by a space

node = all the elements used in an activity diagram

target = end element in an edge in the activity diagram

source = starting element in an edge in the activity diagram

outgoing/incoming = gives you the ID of the edge leaving/entering the ActivityParameterNode 

extendedCase = useCase that has been extended 

extensionLocation = indicates the extension point

Others = ['visibility', 'name', 'general', 'memberEnd', 'node', 'target', 'source']

"""

class XML_parsing():
    
    def __init__(self, file, map_data, hddl_requirements, domain_name, htn_tasks, feedback_name):
        # File that we need to parse
        self.file = file
        # File with the map data
        self.map_data = map_data
        # File hddl domain file requirements
        self.hddl_requirements_list = hddl_requirements
        # Put an adaptable domain file name
        if domain_name != 'None':
            self.domain_name = domain_name
        else:
           self.domain_name = ' ' 
        # Put an adaptable problem file name
        self.problem_name = ' '
        # Initial Task Network
        self.htn_tasks = htn_tasks
        # Feedback file name
        self.feedback_file_name = feedback_name
        # Requirement list for the specific domain file
        self.requirement_list_domain_file = []
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
        # Final list of action without doubles
        self.final_opaque_action_list = []
        # Domain File Name based on the domain name and date
        self.name_string = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p") + '_' +'_domain.hddl' 
        # Problem_file_Name
        self.name_string_pf = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p") + '_' +'_problem.hddl'
        # # Only the name inputs
        # self.method_input_types_list_names = []
        # # Only the name of predicates
        # self.method_input_predicate_list_names = []
        # Dependencies in the UseCase
        self.dependencies_list = []
        # feedback vector:
        self.hddl_type_feedback = []
        
    def XML_ActiveParsing(self):

        # Passing the stored data inside
        # the beautifulsoup parser, storing
        # the returned object in a variable - that is the main object to unpack
        self.Bs_data = BeautifulSoup(self.file, "xml")
        

         
        # # # Finding all instances of tag - You get a list with all the instances with that tag
        # b_node = Bs_data.find_all('node')
        # If the tags are nested - you get each tag one after the other from the order of the file
        
        # Find all the packaged elements
        # You can divide the packaged elements per Folder - so that you don't have to parse useless informations like the ones for the Mission
        
        self.b_packagedElement = self.Bs_data.find_all('packagedElement') 
        
        # Name of the Domain file
        self.domain_name = self.b_packagedElement[0].parent['name']
        self.problem_name = self.domain_name
        
        # Isolate the "xmi:type="uml:Package" " --> e.g. b_packagedElement[0]['xmi:type']
        for index,ii in enumerate(self.b_packagedElement):
            
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

        

        # Find all the constraints tag = ownedRule and xmi:type="uml:Constraint"
        self.b_ownedRules = self.Bs_data.find_all('ownedRule') 
        
        # Find all the edges
        self.b_edges = self.Bs_data.find_all('edge')    
        # Map all the edges
        for index,ii in enumerate(self.b_edges):
            self.edge_list.append({"xmi:id":ii['xmi:id'], "input":ii['source'], "output":ii['target']}) 
            
        #Find the dependencies
        # Find all the edges
        for index,ii in enumerate(self.b_packagedElement):
            if ii['xmi:type'] == 'uml:Dependency':
                self.dependencies_list.append({"xmi:id":ii['xmi:id'], "input":ii['supplier'], "output":ii['client']})        
        
        # Find all the comments
        self.b_comments = self.Bs_data.find_all('ownedComment') 
        # Find all the nodes
        self.b_nodes = self.Bs_data.find_all('node')
        
        # Domain file instances analysis  
        
        for ii in self.b_comments:
            # The requirements for the domain file are included as comment in the UseCase
            if ii.parent['name'] == 'UseCase':
                comment_body = ii.body.string
                for jj in self.hddl_requirements_list:
                    # avoid case-sensitivity 
                    if jj.lower() in comment_body.lower():
                        self.requirement_list_domain_file.append(jj)
                        


    def DomainFileElements(self):        
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
        for uu in self.b_packagedElement:
            
            # If the packagedElement is a UseCase
            # Just consider the inputs in the Function Folder (or any folder that is defined by the Requirements)
            # We are just considering the Domain File entries here! 
            if uu['xmi:type'] == 'uml:UseCase' and  uu.parent.parent['name'] == 'Functions':
                
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
                                            id_uuid = str(uuid.uuid1())
                                            self.hddl_type_list.append({"name": jj['name'], "xmi:id": id_uuid})
                                            self.hddl_type_feedback.append({"name": jj['name'], "xmi:id": id_uuid})
                                            
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
                                    
                                        # self.method_Actions.append(jj['xmi:id'])
                                        self.method_Actions.append({"name": jj['name'], "xmi:type": jj['xmi:type'], "xmi:id":jj['xmi:id'], "incoming_link": jj['incoming'],  "outcoming_link": jj['outgoing']})

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
                            # ordered_actions = []
                            
                            if self.method_Actions != []:
                            
                                functions_with_incoming_edge = [] 
                                functions_with_outcoming_edge= []
                                for bb in self.method_Actions:
                                    for kk in self.edge_list:
                                        if 'incoming_link' in bb and bb['incoming_link'] == kk['xmi:id']:
                                            for uu in self.method_Actions:
                                                if uu['xmi:id'] == kk['input']:
                                                    functions_with_incoming_edge.append(bb)
                                                    bb['previous_action'] = kk['input']
                                        if 'outcoming_link' in bb and bb['outcoming_link'] == kk['xmi:id']:
                                            for uu in self.method_Actions:
                                                if uu['xmi:id'] == kk['output']:
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
                                            for uu in self.method_Actions:
                                                if'previous_action'in uu and uu['previous_action'] == yy['xmi:id']:
                                                    uu['order'] = yy['order'] + 1 
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
                                self.method_Actions.sort(key = XML_parsing.get_order)             
                                
                                
                            # for yy in self.method_Actions:
                                
            
                            #     for bb in self.opaqueAction_list:
                            #         if yy == bb['xmi:id']:
                            #             for kk in self.edge_list:
                            #                 if bb['incoming_link'] == kk['xmi:id']:
                            #                     if kk['input'] in self.method_Actions:
                            #                         action_to_pop = self.method_Actions.index(yy)
                            #                         self.method_Actions.pop(action_to_pop)
                            #                         action_before = self.method_Actions.index(kk['input'])
                            #                         self.method_Actions.insert(action_before+1,yy)
                            self.method_list[-1]['ordered_tasks'] = [x['xmi:id'] for x in self.method_Actions]
                            self.method_Actions.clear()
                                
                    except:
                        if ii != '\n' and ii.name != 'body' and not(isinstance(ii, str)):
                            print('Something Wrong! Check lines before 547 - check the while loop!!')
            
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
            ii["preconditions"] = [x for x in temporary_input_list]
            ii["effects"] = [x for x in temporary_output_list]
            ii["parameters"] = [x for x in temporary_parameter_list]
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
            
        # we want the action to have just one occurance
        final_opaque_action_set = set(final_opaque_action)  
        
        
        
        for ii in self.opaqueAction_list:
            for jj in final_opaque_action_set:
                if ii['name'] == jj and ii['xmi:type'] == 'uml:OpaqueAction':
                    self.final_opaque_action_list.append(ii)

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
       
        # Check if the user defined some constraints in the 
        get_param = []
        flag_found = 0
        for ii in self.b_ownedRules:
            if ii.parent['name'] == 'Functions':
                # check that the parameters have a known type!
                dummy_string = ii['name']
                dummy_vector = re.split(' |-', dummy_string)
                
                for uu in self.hddl_type_list:
                    if uu['name'] == dummy_vector[-1]:
                        flag_found = 1
                
                if flag_found != 1:
                    self.hddl_type_list.append(dummy_vector[-1])
                    self.hddl_type_feedback.append(dummy_vector[-1])
                    print('Plese check your constraints in the UseCase - your type extension for {} was not found in the type folder'.format(ii['name']))
                    print('We added that type - however, please check if that was what you were planning to do!')
                
                get_param_dict = { "xmi:type":ii['xmi:type'], "xmi:id":ii['xmi:id'], "name":ii['name']}
                for jj in self.dependencies_list:
                    if jj['output'] == ii['xmi:id']:
                        get_param_dict['task'] = jj['input']
                get_param.append(get_param_dict)
            
        
        task_parameters = []
        for ii in self.task_list:
            if get_param != []:
                for jj in get_param:
                    if ('task') in jj:
                        if jj['task'] == ii['xmi:id']:
                            task_parameters.append(jj['name'])
            
            ii["parameters"] = [x for x in task_parameters]
            task_parameters.clear()
                

        for ii in self.task_list:
            for jj in self.method_list:
                
                if ii.get('xmi:id') == jj.get('task'):
                    # for each method check the length of the parameters list - if it longer than the one of the task, leave it like that - if not replace the list
                    if ii["parameters"] != []:
                        if len(ii["parameters"]) >= len(jj.get('parameters')):
                            dummy_parameter = [x for x in jj.get('parameters')]
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
                        
        # x = 1    
        
    def get_order(task):
        return task.get('order')

    def ProblemFileElements(self):        
        
        # The tasks that have to be defined by the designer in the initial task network
        self.mission_tasks = []
        # Initial conditions in the problem file
        self.initial_conditions_pf = []
        # Objects in the problem file
        self.problem_file_object = []

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
                
                # Analyse input and output to simplify the task inputs
                # We are not considering those parameters anymore 
                # for kk in uu.children:
                #     # We can analyse the input (xmi:type="uml:InputPin") 
                #     try:
                        
                #         if kk['xmi:type'] == 'uml:InputPin':
                #             self.mission_tasks_input_parameter.append({"xmi:id":kk['xmi:id'], "mission_task": uu['xmi:id'], "incoming_edge": kk['incoming']})  
                                                                           
                #     except:
                #         if kk != '\n' and not(isinstance(kk, str)) and kk.name != 'argument' and kk.name != 'UpperBound'  :
                #             print('Something Wrong! Check lines before 669')
                            
                            
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
        self.mission_tasks.sort(key = XML_parsing.get_order)


        # Get initial conditions as constraints 
        """CHECK THIS!"""
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
                        self.mission_components.append({"xmi:id":ii['xmi:id'], "name": ii['name']})
                        for jj in ii.children:
                            if jj.name == 'ownedAttribute' and jj['xmi:type'] == "uml:Property":
                                self.mission_components[-1]['type'] = jj['type']
                        for jj in ii.children:
                            if jj.name == 'ownedAttribute' and jj['xmi:type'] == "uml:Port":
                                self.mission_components.append({"xmi:id":jj['xmi:id'], "name": jj['name'], "type": jj['type']})

        for uu in self.mission_components:

            for ii in self.hddl_type_list:
                if 'type' in uu and uu['type'] == ii['xmi:id']:
                    self.problem_file_object.append('{} - {}'.format(uu['name'], ii['name']))
                elif 'type' not in uu:
                    self.problem_file_object.append('{} - {}'.format(uu['name'], uu['name']))
                    print('{} is missing his type - please define a type for this component!'.format(uu['name']))
                    print('{} has been appended to the hddl type list!'.format(uu['name']))
                    self.hddl_type_list.append({"name": uu['name'], "xmi:id":''})
                    
        
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
                    print('{} has a wrong type! Please check your types in the map_file!')
                else:
                    self.problem_file_object.append('{} - {}'.format(ii.split("-")[0], ii.split("-")[-1].replace('\n','').strip()))

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
                            print('{} not found in the problem file objects'.format(dummy_list[-1]))
                            break
                        
                
            if task_found != 'yes' and object_found != 'yes':
                print('Please check your initial task network! Something is wrong!')
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
                        
                

        # x = 1   
         
         # I suggest that the initial task network - therefore, what the system should do if given by the designer as input!
         # Additional inputs can be encoded in the input file as well! 
         # If not - I can consider that the tasks for the systems are!

        
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
        file.write('\t (:requirements :{}) \n'.format(' :'.join(self.requirement_list_domain_file)))
        #Object Type
        file.write('\t (:types \n')
        for ii in self.hddl_type_list:
            file.write('\t\t {} - object \n'.format(ii.get('name')))
        # End of object type
        file.write('\t) \n\n')  
        
        # x = 0
        
        # Predicates
        file.write('\t (:predicates \n')
        #Writes Predicates
        for ii in self.predicate_list:
            file.write('\t\t ({}) \n'.format(ii))
        # End of predicates
        file.write('\t) \n\n')   
            
        # #Tasks!

        for ii in self.task_list:
            file.write('\t (:task {} \n'.format(ii.get('name')))            
            file.write('\t\t :parameters (?{}) \n'.format(' ?'.join(ii.get('parameters'))))
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
            file.write('\t (:method {} \n'.format(ii.get('name')))
            file.write('\t\t :parameters (?{}) \n'.format(' ?'.join(ii.get('parameters'))))
            if ii.get('preconditions') != '':
                file.write('\t\t :precondition (and \n\t\t\t{} \n\t\t) \n'.format(' \n\t\t\t'.join(ii.get('preconditions'))))
            else:
                file.write('\t\t :precondition ()\n')
            counter = 0
                
            for jj in ii['ordered_tasks']: 
                for kk in self.opaqueAction_list:
                    if kk['xmi:id'] == jj:
                        # Task Parameters
                        dummy_string = ' '.join(kk['parameters'])
                        dummy_vector = re.split(' |-', dummy_string)
                        # vector[start:end:step]
                        dummy_vector = dummy_vector[0::2]
                        string_vector.append('task{}({} ?{})'.format(counter,kk['name'], ' ?'.join(dummy_vector) ))
                        counter = counter + 1
                    if counter > 1 and '(< task{} task{})'.format(counter-2, counter-1) not in order_vector:
                        # For each task check incoming and outcoming links
                        order_vector.append('(< task{} task{})'.format(counter-2, counter-1))

            if counter != 0 and counter != 1:
                file.write('\t\t :subtasks (and \n')
                file.write('\t\t\t{}\n'.format('\n\t\t\t'.join(string_vector)))
                file.write('\t\t ) \n')
                file.write('\t\t :ordering (and \n')
                file.write('\t\t\t{}\n'.format(' \n\t\t\t'.join(order_vector)))
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
                
            file.write('\t ) \n\n') 

        #Actions
        file.write('\n')  #space!
        for ii in self.final_opaque_action_list:

            file.write('\t(:action {} \n'.format(ii.get('name')))            
            file.write('\t\t :parameters (?{}) \n'.format(' ?'.join(ii.get('parameters'))))
            if ii.get('preconditions') != '':
                file.write('\t\t :precondition (and \n\t\t\t{})\n'.format(' \n\t\t\t'.join(ii.get('preconditions'))))
            else:
                file.write('\t\t :precondition ()\n')
            if ii.get('effects') != '':
                file.write('\t\t :effect (and \n\t\t\t{})\n'.format(' \n\t\t\t'.join(ii.get('effects'))))
            else:
                file.write('\t\t :effect ()\n')
                        
            file.write('\t) \n\n') 
        
        # end of the file
        file.write(')')
    
    def Problem_FileWriting (self):
        file = open(self.name_string_pf,'w')
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
            file.write('\t\t({})\n'.format(ii))
        
        file.write('\t\t )\n\n')
        #Ordering
        file.write('\t\t :ordering (and \n')
        for ii in self.ordering_task_network:
            file.write('\t\t{}\n'.format(ii))
        
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
        
        # Take the first part of the C++ code
        
        # Add the equipments of the system
        
        # Create the initial task network
        
        # Put the ordering of the tasks
        
        # Set the problem initial conditions
        
    def Feedback_file(self): 
        
        # self.hddl_type_list --> list of types
        # self.predicate_list --> list of predicates
        # self.task_list --> list of tasks
        # self.method_list --> list of methods
        # self.opaqueAction_list --> list of tasks
        # self.feedback_file_name --> file from which we start
        # self.hddl_type_feedback --> start building memory of the things changed while reading the first xml
        
        # Read the lines of the feedback file
        with open(self.feedback_file_name, 'r') as f:
            feedback_file_lines = f.readlines()
            f.seek(0)
            feedback_file = f.read()


        # Section requirements
        flag_requirements = 0
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
        # Types --> self.hddl_type_feedback
        # Predicates
        self.predicate_list_feedback = []
        # Tasks
        self.task_list_feedback =[]
        # Methods
        self.method_list_feedback =[]
        # Actions
        self.opaqueAction_list_feedback =[]
        
        
        
        with open(self.feedback_file_name, 'r') as f:
            for ii in f:
                line = ii.replace("\n", '').replace("\t",'').strip()
                
                if ':requirements' in line:
                    data_requirements.append(line)
                
                if ':types' in line:
                    flag_types = 1 
                if flag_types == 1 and line != '':
                    data_types.append(line)
                    if line == ')':
                       flag_types = 0 
                       
                if ':predicates' in line:
                    flag_predicates = 1 
                if flag_predicates == 1 and line != '':
                    data_predicates.append(line)
                    if line == ')':
                       flag_predicates = 0 
                
                if ':task' in line:
                    flag_task = 1 
                if flag_task == 1 and line != '':
                    temporary_task_list.append(line)
                    if line == ')':
                       flag_task = 0  
                       data_tasks.append([x for x in temporary_task_list])
                       temporary_task_list.clear()
                
                if ':method' in line:
                    flag_method = 1 
                if flag_method == 1 and line != '':
                    temporary_method_list.append(line)
                    if line == ')':
                       flag_method = 0  
                       data_methods.append([x for x in temporary_method_list])
                       temporary_method_list.clear()        
                       
                if ':action' in line:
                    flag_action = 1 
                if flag_action == 1 and line != '':
                    temporary_action_list.append(line)
                    if line == ')':
                       flag_action = 0  
                       data_actions.append([x for x in temporary_action_list])
                       temporary_action_list.clear()    
                    
        
        # x = 0
        flag_type = 0 
        
        
        
        for ii in data_types:
            if ii != '(:types' and ii != ')':
                for jj in self.hddl_type_list:
                    if ii.split('-')[0].strip() != jj['name'] and flag_type == 0:
                        flag_type = 0
                    if ii.split('-')[0].strip() == jj['name']:
                        flag_type = 1
                if flag_type != 1:
                    self.hddl_type_feedback.append({'name': ii.split('-')[0].strip(),'xmi:id': str(uuid.uuid1())})
                
                        
        for ii in data_predicates:
            
            if ii != '(:predicates' and ii != ')':
                if ii.replace('(','').replace(')','') not in self.predicate_list:
                    self.predicate_list_feedback.append(ii.replace('(','').replace(')',''))
                    
        
        # Store the parameters of the model
        temp_param_list = []
        task_name = ''
        flag_task = 0
        parameters = []
        
        # for all the task in data_task (i) extract name and parameters, (ii) create a xmi:id
        for uu in data_tasks:
            for ii in uu:
                if ':task' in ii:
                    task_name = ii.split()[1].strip()
                if ':parameters' in ii:

                    regex_pattern ='\?\w+.*\w+'
                    parameters = re.findall(regex_pattern, ii, re.S)

                    for jj in parameters:
                        
                        temp_param_list.append(jj.strip().split('?')[1::])
                        # No unwanted white spaces needed!
                        for index,oo in enumerate(temp_param_list[-1]):
                            oo = oo.strip()
                            temp_param_list[-1][index] = oo
                        
                    # If you have name and parameters
                    if task_name != '' and parameters != []:
                        temp_dictionary = {'name': task_name ,'xmi:id': str(uuid.uuid1()), 'parameters': temp_param_list[-1]}
                        temp_param_list = []
                        parameters = []
                        task_name = ''
                    # If you don't have parameters
                    else:
                        flag_task = 2
                        print('There is an error in the task definition in the HDDL document. Did you gave the task parameters?')
        
                    # Let's search in the tasks - can we add one to the task feedback list?
                    if flag_task != 2: 
                        for jj in self.task_list:
                            if temp_dictionary['name'] == jj['name']:
                                # flag_task = 1 
                                counter = 0
                                for xx in temp_dictionary['parameters']:
                                    for kk in jj['parameters']:
                                        if xx == kk:
                                             flag_task = 1
                                             counter = counter + 1

                                if counter == len(jj['parameters']):
                                    flag_task = 1
                                    counter = 0
                                else:
                                    flag_task = 0
                        
                        if flag_task == 0:
                            self.task_list_feedback.append(temp_dictionary)
                            flag_task = 0
                        else:
                            print("ok: {}".format(temp_dictionary))
                            flag_task = 0
                            x = 0
            
                
                
                
                
    
                    
        
        # Patterns that may work with the tasks
        # pattern = '\(:\w.+\s\s\s\s :\w'
        # pattern that may work with the types
        # pattern = '\(:\w.+\s\s\s\s \w'
        # This may work as well
        # pattern = '(\(:\w.+) (.*)'
        # ['(:requirements :typing :hierachie) ', '(:types ', '(:predicates ', 
        # '(:task NavigateToGoal ', '(:task EvaluateAvailableResources ', 
        # '(:task TakePicture ', '(:task GoBack ', '(:task StartMission ', 
        # '(:task Dummy_Task  ', '(:method Dummy_Task _method1 ', 
        # '(:method NavigateToGoal_method1 ', '(:method NavigateToGoal_method2 ', 
        # '(:method NavigateToGoal_method3 ', '(:method EvaluateAvailableResource_method1 ', 
        # '(:method TakePicture_method1 ', '(:method GoBack_method1 ', 
        # '(:method StartMission_method1 ', '(:action Dummy_action_1 ', 
        # '(:action Dummy_action_2', '(:action Visit ', '(:action Navigate ', 
        # '(:action Unvisit ', '(:action GetDataFromSensors ', '(:action SendSystemState ', 
        # '(:action ReadArTag ', '(:action CommunicateArTagData ', '(:action TakeImage ', 
        # '(:action CommunicateImageData ', '(:action MakeAvailable ']
        
        # Finds everything thats starts wurg :\w
        # pattern = '(\(:\w.+)'
        
        # In theory you can use regex - however, now I am not in the mood for it
        # matches = re.findall('(:types[])', feedback_file_lines.read())
        
        # pattern_types = '^(:types ...)$'
        # https://stackoverflow.com/questions/35888841/how-to-read-a-file-and-extract-data-between-multiline-patterns
        
        # I love python:
            # https://www.programiz.com/python-programming/methods/string/startswith
            # https://www.programiz.com/python-programming/methods/string/endswith
        
        # Find the beginning of the section -  Pattern - 
        # pattern = '(\(:\w.+)\s\s\s '
        # re.findall(pattern, feedback_file)

        
        
        
        # for ii in feedback_file_lines:
        #     # Regex Pattern 
        #     # pattern = '(\(:\w.+)\s\s\s '
            
        #     # Find the pattern: re.findall(pattern, feedback_file)
        #     # dummy_string = re.findall(pattern, ii)
        #     # if the dummy string is not activated - then it's a normal line - treat it like that inside the case
        #     # You have to do some reconfiguration things
            
        #     # clean the string
        #     dummy_string = ii.replace("\n", '').replace("\t",'').strip()
            
            
        #     if dummy_string != '':
            
        #         if dummy_string == ':requirements':
        #             # Activate the flag - 
        #             pass
                
        #         if dummy_string == ':types':
        #             # activate types
        #             # deactivate the flag of requirements
        #             pass
                
        #         if dummy_string == ':predicates':
        #             # activate predicates
        #             # deactive the flag of types
        #             pass
                
        #         if dummy_string == ':task':
        #             # activate task
        #             # deactivate predicates 
        #             pass
    
        #         if dummy_string == ':methods':
        #             # activate methods
        #             pass
                
        #         if dummy_string == ':action':
        #             # activate actions
        #             pass
                
        
        
        
        
        
        
        
        # self.predicate_list_feedback = []
        # self.task_list_feedback = []
        # flag_types = 0
        # type_existing = 'no'
        # flag_predicates = 0
        # flag_tasks = 0
        # task_existing = 'no'
        
        
        # #Check the list of types 
        # for ii in feedback_file_lines:
            
        #     dummy_string = ii.replace('\n', '')
        #     dummy_string = dummy_string.replace('\t', '')
            
        #     # When we arrive at the types part 
        #     if flag_types == 1:
        #         for jj in self.hddl_type_list:
        #             if jj['name'] == dummy_string.split('-')[0].strip():
        #                 type_existing = 'yes'
        #         if type_existing != 'yes':
        #             self.hddl_type_feedback.append({'name':dummy_string.split('-')[0].strip(), 'xmi:id':uuid.uuid1()})
        #             type_existing = 'no'
            
        #     if ':types' in dummy_string:
        #         flag_types = 1

        #     # Found the end of the type section
        #     if ')' in dummy_string and flag_types == 1:
        #         flag_types = 0
                
        #     # Find the predicates
        #     if flag_predicates == 1:
        #         dummy_string = dummy_string.replace('(', '')
        #         dummy_string = dummy_string.replace(')', '')
        #         dummy_string = dummy_string.strip()
        #         if not dummy_string in self.predicate_list and dummy_string != '':
        #             self.predicate_list_feedback.append(dummy_string)
            
        #     if ':predicates' in dummy_string:
        #         flag_predicates = 1

        #     # Found the end of the predicate section
        #     if ':task' in dummy_string and flag_predicates == 1:
        #         flag_predicates = 0 
        #         flag_tasks = 1
            
        #     # Find tasks!!!
            
        #     """Still Writing This part - I am thinking: how can I extract portions of file so that I can easily
        #     store the information I need for the feedback line?"""
            
        #     if ':task' in dummy_string:
        #         dummy_string = dummy_string.replace('(', '')
        #         dummy_string = dummy_string.replace(')', '')
        #         dummy_list = dummy_string.split()
        #         task_name = dummy_list[-1].strip()
                
                
                
        #         for jj in self.task_list:
        #             if jj['name'] == task_name and task_name!= '' :
        #                 task_existing = 'yes'
        #         if task_existing == 'yes':
        #             self.task_list_feedback.append({'name':task_name, 'xmi:id':uuid.uuid1()}) 
            
            
            
        #     # Find methods!!!
            
            
        #     # Find actions!!!
            
        
            
        
        
        
    
def main():
    
    
    # First Parse de input file to get the information you need
    with open('configuration_file.xml', 'r') as f:
        configuration_file = f.read()    
    
    configuration_file_soup = BeautifulSoup(configuration_file, 'xml')
    file_parameters = configuration_file_soup.find_all('file')
    
    file_papyrus = file_parameters[0]['file_name']
    
    if file_parameters[0].has_attr('domain_name'):
        domain_name = file_parameters[0]['domain_name']
    else:
        domain_name = 'None'
        
    if file_parameters[0].has_attr('feedback_file_name'):
        feedback_name = file_parameters[0]['feedback_file_name']
    else:
        feedback_name = 'None'
        
    if file_parameters[0].has_attr('map_file_name'):
        map_file_name = file_parameters[0]['map_file_name']
        with open(map_file_name, 'r') as f:
            map_data = f.readlines() 
    else:
        map_file_name = 'None'

    if file_parameters[0].has_attr('generate_problem_file'):
        generate_problem_file = file_parameters[0]['generate_problem_file']
    else:
        generate_problem_file = 'no' 
        
    if file_parameters[0].has_attr('generate_domain_file'):
        generate_domain_file = file_parameters[0]['generate_domain_file']
    else:
        generate_domain_file = 'no'
        
    if file_parameters[0].has_attr('generate_feedback'):
        generate_feedback_file = file_parameters[0]['generate_feedback']
    else:
        generate_feedback_file = 'no'
        
    hddl_requirements_soup = configuration_file_soup.find_all('li')
    list_requirements = []
    for xx in hddl_requirements_soup:
        dummy_string = xx.contents[0]
        list_requirements.append(dummy_string)
    
    
    if list_requirements == [] :
        # Types of domain requirements considered in the HDDL module
        # call them from the configuration file - you can even create an executable of python where you ask for them
        hddl_requirements = ['typing', 'hierachie', 'fluents', 'STRIPS', 'Disjunctive Preconditions', 'Equality'
                         'Existential Preconditions','Universal Preconditions', 'Quantified Preconditions', 'Conditional Effects',
                         'Action Expansions','Foreach Expansions', 'DAG Expansions', 'Domain Axioms', 'Subgoals Through Axioms', 'Safety Constraints'
                         'Expression Evaluation', 'Fluents', 'Open World', 'True Negation', 'ADL', 'UCPOP']
    else:
        hddl_requirements = list_requirements
    
    htn_tasks_soup = configuration_file_soup.find_all('li_htn')
    htn_tasks = []
    for xx in htn_tasks_soup:
        dummy_string = xx.contents[0]
        htn_tasks.append(dummy_string)    

    with open(file_papyrus, 'r') as f:
        data = f.read()
        

    file_final = XML_parsing(data, map_data, hddl_requirements, domain_name, htn_tasks, feedback_name)
    # Actively Parse the XML
    file_final.XML_ActiveParsing()
    # Create the file that you need/want
    # Take out the element you need for the domain file:
    file_final.DomainFileElements()
    # Create domain file
    if generate_domain_file == 'yes':
        file_final.Domain_FileWriting()
    # Get the elements to design the problem file:
    if generate_problem_file == 'yes':
        file_final.ProblemFileElements()
        file_final.Problem_FileWriting()
    # Create Feedback file
    if generate_feedback_file == 'yes':
        file_final.Feedback_file() 



if __name__ == "__main__":
    main()