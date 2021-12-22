# -*- coding: utf-8 -*-
"""
Created on Thu Nov 4 16:19:39 2021

@author: Jasmine Rimani
"""
# https://beautiful-soup-4.readthedocs.io/en/latest/#
from bs4 import BeautifulSoup
# https://docs.python.org/3/library/datetime.html
from datetime import datetime
# https://docs.python.org/3/library/re.html
import re
# https://docs.python.org/3/library/uuid.html
import uuid
# https://docs.python.org/3/library/os.html
import os
# https://docs.python.org/3/library/traceback.html
import traceback


"""
---------------------------------------------------------------------------------------------------------------------------------------
PAPYRUS XML TAGS ANALYSIS
---------------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------------

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

---------------------------------------------------------------------------------------------------------------------------------------
PAPYRUS XML ATTRIBUTES ANALYSIS
---------------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------------
TYPES:
---------------------------------------------------------------------------------------------------------------------------------------


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
---------------------------------------------------------------------------------------------------------------------------------------
OTHER USEFUL ATTRIBUTES:
---------------------------------------------------------------------------------------------------------------------------------------

xmi:id = unique identifier for each element of the xml

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

"""


# MAIN PARSING CLASS!
class XML_parsing():
    
    def __init__(self, file, map_data, hddl_requirements, domain_name, htn_tasks, feedback_name, d_now = os.getcwd(),  debug = 'on', task_parameters = 'common'):
        # File that we need to parse
        self.file = file
        # File with the map data
        self.map_data = map_data
        # File hddl domain file requirements
        self.hddl_requirements_list = hddl_requirements
        # Put an adaptable domain file name
        # Put an adaptable problem file name
        if domain_name != 'None':
            self.domain_name = datetime.now().strftime("%Y_%m_%d-%I_%M_%S") + '_' + domain_name + '_' +'_domain.hddl' 
            self.problem_name = datetime.now().strftime("%Y_%m_%d-%I_%M_%S") + '_' + domain_name + '_' +'_problem.hddl'
        else:
           self.domain_name = datetime.now().strftime("%Y_%m_%d-%I_%M_%S") + '_' +'_domain.hddl' 
           self.problem_name = datetime.now().strftime("%Y_%m_%d-%I_%M_%S") + '_' +'_problem.hddl'
        # Initial Task Network
        self.htn_tasks = htn_tasks 
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
        # Feedback edge list
        self.edge_list_feedback = []
        # List with all the parameters
        self.all_parameters_list = []
        #Action Inputs
        self.opaqueAction_input_list = []
        #Action Outputs 
        self.opaqueAction_output_list = []
        # Final list of action without doubles
        self.final_opaque_action_list = []
        # Feedback file name
        try:
            # see if you have a feedback file
            self.feedback_file_name = feedback_name
        except NameError:
            # if not named if as the self.domain_name
            self.feedback_file_name = self.domain_name
        # Dependencies in the UseCase
        self.dependencies_list = []
        # feedback vector:
        self.hddl_type_feedback = []
        # debug_on
        self.debug = debug
        # Directory used now:
        self.d_now = d_now
        # Log file general entries
        self.log_file_general_entries = []
        # Task parameters consideration
        self.task_parameters = task_parameters

        
    def XML_ActiveParsing(self):

        # Log File init
        self.log_file_general_entries.append('Log errors and warnings during parsing: \n')
        self.log_file_general_entries.append('------------------------------------------------- \n')
        # Passing the stored data inside the beautifulsoup parser, 
        # storing the returned object in a variable - that is the main object to unpack

        self.Bs_data = BeautifulSoup(self.file, "xml")
        
        
        # How to use BeautifulSoup:
            # Finding all instances of tag - You get a list with all the instances with that tag:
                # b_node = Bs_data.find_all('node')
                # If the tags are nested - you get each tag one after the other from the order of the file
        
            # Find all the packaged elements
                # You can divide the packaged elements per Folder - so that you don't have to parse useless information like the ones for the Mission
        
        self.b_packagedElement = self.Bs_data.find_all('packagedElement') 
        

        for index,ii in enumerate(self.b_packagedElement):
            
            # Isolate the "xmi:type="uml:Package" " --> e.g. b_packagedElement[0]['xmi:type']
            if ii['xmi:type'] == 'uml:Package':
                self.package_list.append({"name": ii['name'], "xmi:id":ii['xmi:id']})    
            
            # Isolate the classes - ':types' in HDDL
            if ii['xmi:type'] == 'uml:Class':
                self.hddl_type_list.append({"name": ii['name'], "xmi:id":ii['xmi:id']})
                
            # Isolate Actors:
            if ii['xmi:type'] == 'uml:Actor':
                self.actor_list.append({"name": ii['name'], "xmi:id":ii['xmi:id']})
            
            # Isolate Usecases that are packegedElements --> You get your tasks name, however you still need your parameters
            if ii['xmi:type'] == 'uml:UseCase':
                self.task_list.append({"name": ii['name'], "xmi:id":ii['xmi:id'], "parameters": []})   

        # Find all the constraints tag = ownedRule and xmi:type="uml:Constraint"
        self.b_ownedRules = self.Bs_data.find_all('ownedRule') 
        
        # Find all the edges
        self.b_edges = self.Bs_data.find_all('edge')    
        # Map all the edges
        for index,ii in enumerate(self.b_edges):
            try:
                self.edge_list.append({"xmi:id":ii['xmi:id'], "input":ii['source'], "output":ii['target']}) 
            except:
                # if you can't find one of the ends of the edge: save the edge in the edge list and in the feedback log
                if self.debug == 'on' :
                    print('Check your model! Edge id:{} is ill defined! It is probably missing an input or an output'.format(ii['xmi:id']))
                # Add this to the future Log File
                self.log_file_general_entries.append('\t\t Check your model! Edge id:{} is ill defined! It is probably missing an input or an output \n'.format(ii['xmi:id']))
                if ii.has_attr('source'):
                    self.edge_list.append({"xmi:id":ii['xmi:id'], "input":ii['source'], "output":''}) 
                    self.edge_list_feedback.append({"xmi:id":ii['xmi:id'], "input":ii['source'], "output":''}) 
                if ii.has_attr('target'):
                    self.edge_list.append({"xmi:id":ii['xmi:id'], "input":' ', "output":['target']}) 
                    self.edge_list_feedback.append({"xmi:id":ii['xmi:id'], "input":' ', "output":['target']}) 
            
        #Find the dependencies
        for index,ii in enumerate(self.b_packagedElement):
            if ii['xmi:type'] == 'uml:Dependency':
                self.dependencies_list.append({"xmi:id":ii['xmi:id'], "input":ii['supplier'], "output":ii['client']})        
        
        # Find all the comments
        self.b_comments = self.Bs_data.find_all('ownedComment') 
        # Find all the nodes
        self.b_nodes = self.Bs_data.find_all('node')
        
        # Domain file instances analysis  
        for ii in self.b_comments:
            # The requirements for the HDDL domain file are included as comment in the UseCase
            if ii.parent['name'] == 'UseCase':
                comment_body = ii.body.string
                for jj in self.hddl_requirements_list:
                    # avoid case-sensitivity 
                    if jj.lower() in comment_body.lower():
                        self.requirement_list_domain_file.append(jj)
                        


    def DomainFileElements(self):     
        # Log File init
        self.log_file_general_entries.append('------------------------------------------------- \n')
        self.log_file_general_entries.append('Log errors and warnings during the HDDL Domain file element acquisition: \n')
        self.log_file_general_entries.append('------------------------------------------------- \n')
        # Check your parsing (comment after use):
        # print('Packages list: \n {}'.format(self.package_list))
        # print('Classes list: \n {}'.format(self.hddl_type_list))
        # print('Actors list: \n {}'.format(self.actor_list))
        # print('UseCase: \n {}'.format(self.task_list))
        # print('Links between the entities: \n {}'.format(self.edge_list))

        # To access any instance of the dictionary use case with UseCase_list[n] and any key of the dictionary with get() UseCase_list[1].get('name')
                
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
                        # Check the sub-UseCases that can be methods: double check on the type(considered as attribute) and the tag name
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
                                            self.log_file_general_entries('\t\t No predefined type for {}. Add it on Papyrus! \n'.format(temp_dict.get('name')))
                                        
                                        if 'type_name' in temp_dict and temp_dict['type_name'] == " " and len(temp_dict["name"].split()) > 1:
                                            temp_dict["type_name"] = 'predicate'
                                            if self.debug == 'on': 
                                                print('No predefined type for {}. Add it on Papyrus!'.format(temp_dict.get('name'))) 
                                            self.log_file_general_entries.append('\t\t No predefined type for {}. Add it on Papyrus! \n'.format(temp_dict.get('name')))
                                        
                                        # Check if the attribute has an incoming edge - output
                                        if jj.has_attr('incoming'):
                                            temp_dict["incoming"] = jj["incoming"]   
                                        
                                        # Check if the attribute has an outcoming edge - input
                                        if jj.has_attr('outgoing'):
                                            temp_dict["outgoing"] = jj["outgoing"] 
                                        
                                        # Chek if the attribute is a parameters - if yes save it in the method inputs list
                                        if temp_dict["type_name"] != 'predicate' or len(temp_dict["name"].split()) <= 1:
                                            self.method_input_types_list.append(temp_dict)
                                            method_input_types_list_names.append((temp_dict["name"]+'-'+temp_dict["type_name"]).replace(" ", ""))
                                        
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
                                                
                                            
                                            # except:
                                            #     if kk != '\n':
                                            #         traceback.print_exc() 
                                    
                                        # self.method_Actions.append(jj['xmi:id'])
                                        self.method_Actions.append({"name": jj['name'], "xmi:type": jj['xmi:type'], "xmi:id":jj['xmi:id'], "incoming_link": jj['incoming'],  "outcoming_link": jj['outgoing']})

                                    
                                # except:
                                #     if jj != '\n' and jj.name != 'body' and not(isinstance(jj, str)):
                                #         traceback.print_exc() 
                                #         self.log_file_general_entries('\t\t Error in UseCase {}, something off in the activity diagram action definition \n'.format(ii['xmi:type']))
                                
     
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
                                self.method_Actions.sort(key = XML_parsing.get_order)             
                                                            
                            self.method_list[-1]['ordered_tasks'] = [x['xmi:id'] for x in self.method_Actions]
                            self.method_Actions.clear()
                                
                    # except:
                    #     if ii != '\n' and ii.name != 'body' and not(isinstance(ii, str)):
                    #         self.log_file_general_entries.append('\t\t Error in UseCase {}, something off in the UseCase definition \n'.format(ii['name']))
            
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
                self.log_file_general_entries('\t\t The action {} has no parameters - is there something wrong in the model? \n'.format(ii['name']))
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

        for ii in self.opaqueAction_list:
            if ii['xmi:type'] == 'uml:CallBehaviorAction':
                for jj in self.task_list:
                    if jj.get('name') == ii.get('name'): 
                        jj["parameters"] = ii.get('parameters')
       
        # Check if the user defined some constraints in UseCase diagram to get the task parameters
        get_param = []
        flag_found = 0
        for ii in self.b_ownedRules:
            if ii.parent['name'] == 'DomainDefinition':
                # check that the parameters have a known type!
                dummy_string = ii['name']
                dummy_vector = re.split(' |-', dummy_string)
                
                for uu in self.hddl_type_list:
                    if uu['name'] == dummy_vector[-1]:
                        flag_found = 1
                
                if flag_found != 1:
                    self.hddl_type_list.append(dummy_vector[-1])
                    self.hddl_type_feedback.append(dummy_vector[-1])
                    if self.debug == 'on':
                        print('Plese check your constraints in the UseCase - your type extension for {} was not found in the type folder'.format(ii['name']))
                        print('We added that type - however, please check if that was what you were planning to do!')
                        self.log_file_general_entries.append('\t\t Plese check your constraints in the UseCase - your type extension for {} was not found in the type folder \n'.format(ii['name']))
                
                
                
                
                for jj in self.dependencies_list:
                    flag_found = 0
                    get_param_dict = { "xmi:type":ii['xmi:type'], "xmi:id":ii['xmi:id'], "name":ii['name']}
                    if jj['output'] == ii['xmi:id']:
                        get_param_dict['task'] = jj['input']
                        get_param.append(get_param_dict)
                        get_param_dict ={}
                        
                
            
        
        task_parameters = []
        # If the task parameters are already defined in the main use case diagram as constraints
        for ii in self.task_list:
            if get_param != []:
                for jj in get_param:
                    if ('task') in jj:
                        if jj['task'] == ii['xmi:id']:
                            task_parameters.append(jj['name'].replace(" ", ""))
            
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
                                    dummy_parameter = [x for x in jj.get('parameters')]
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
            
            
            if not(final_predicate in self.predicate_list):
                self.predicate_list.append(('{}').format(final_predicate))
                
            temporary_predicate.clear()
                        
  
        
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
                    self.problem_file_object.append('{} - {}'.format(uu['name'], ii['name']))
                elif 'type' not in uu:
                    self.problem_file_object.append('{} - {}'.format(uu['name'], uu['name']))
                    if self.debug == 'on':
                        print('{} is missing his type - please define a type for this component!'.format(uu['name']))
                        print('{} has been appended to the hddl type list!'.format(uu['name']))
                    self.log_file_general_entries.append('\t\t {} is missing his type - please define a type for this component! \n'.format(uu['name']))
                    self.log_file_general_entries.append('\t\t {} has been appended to the hddl type list \n!'.format(uu['name']))
                    
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
                    if self.debug == 'on':
                        print('{} has a wrong type! Please check your types in the map_file!'.format(uu['name']))
                    self.log_file_general_entries.append('\t\t {} has a wrong type! Please check your types in the map_file \n!'.format(uu['name']))
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
                        
                
        # print('Packages:', package_list)
        # print('HDDL Types:', hddl_type_list)
        # print('Use Cases - Task Level:',Task_list)
        # print('Use Cases - Method Level:',Method_list)
        

        
    def Domain_FileWriting (self):
        ###################################################################
        self.log_file_general_entries.append('------------------------------------------------- \n')
        self.log_file_general_entries.append('Log errors and warnings during the HDDL Domain file generation: \n')
        self.log_file_general_entries.append('------------------------------------------------- \n')

        # Open/Create the File
        file = open(self.d_now + '//outputs//' + self.domain_name,'w')
        # Start writing on the file
        file.write('(define (domain {}) \n'.format(self.domain_name))
        # Write requirement
        file.write('\t (:requirements :{}) \n'.format(' :'.join(self.requirement_list_domain_file)))
        #Object Type
        file.write('\t (:types \n')
        for ii in self.hddl_type_list:
            if ii != 'predicate':
                file.write('\t\t {} - object \n'.format(ii.get('name')))
        # End of object type
        file.write('\t) \n\n')  
        
        # Predicates
        file.write('\t (:predicates \n')
        #Writes Predicates
        for ii in self.predicate_list:
            file.write('\t\t ({}) \n'.format(ii))
        # End of predicates
        file.write('\t) \n\n')   
            
        #Tasks!
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
            # method name
            file.write('\t (:method {} \n'.format(ii.get('name')))
            # method parameters
            file.write('\t\t :parameters (?{}) \n'.format(' ?'.join(ii.get('parameters'))))
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
                                        
            file.write('\t\t :task ({} ?{}) \n'.format(task_name, ' ?'.join(task_parameters)))
            # method preconditions
            if ii.get('preconditions') != '':
                file.write('\t\t :precondition (and \n\t\t\t{} \n\t\t) \n'.format(' \n\t\t\t'.join(ii.get('preconditions'))))
            else:
                file.write('\t\t :precondition ()\n')
            counter = 0
            
            # method actions
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
        self.log_file_general_entries.append('------------------------------------------------- \n')
        self.log_file_general_entries.append('Log errors and warnings during the HDDL Problem file generation: \n')
        self.log_file_general_entries.append('------------------------------------------------- \n')
        
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
        
        
    def Feedback_file(self): 
        self.log_file_general_entries.append('------------------------------------------------- \n')
        self.log_file_general_entries.append('Log errors and warnings during the Feedback generation: \n')
        self.log_file_general_entries.append('------------------------------------------------- \n')
        # This class is already written as if it was to be used alone - however, the other things no!
        # Sooooo, I still need to finish the coding. 
        # At the end everything should be able to be used in tandem or alone :)
        # Unfortunately all this file reading takes time
        
        # Types --> self.hddl_type_list --> list of types --> Already created while parsing the xml file
        # However if I need to use this class alone without the xml file
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
                
                if ':task' in line:
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
                if ii.replace('(','').replace(')','') not in self.predicate_list:
                    self.predicate_list_feedback.append(ii.replace('(','').replace(')',''))
                    
        
        # Store the parameters of the model
        temp_param_list = []
        task_name = ''
        flag_task = 0
        counter = 0
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
                    if task_name != '':
                        temp_dictionary = {'name': task_name ,'xmi:id': str(uuid.uuid1())}
                        task_name = ''
                    # If you don't have parameters
                    else:
                        flag_task = 2
                        if self.debug == 'on':
                            print('The task has no name!')
                        self.log_file_general_entries.append('\t\t {} is defined as task, however it has no name \n'.format(uu))
                    if parameters != []:
                        temp_dictionary['parameters'] = temp_param_list[-1]
                        temp_param_list = []
                        parameters = []
                    # If you don't have parameters
                    else:
                        flag_task = 2
                        if self.debug == 'on':
                            print('The task has no parameters!')
                        self.log_file_general_entries.append('\t\t {} is defined as task, however it has no parameters \n'.format(uu))
        
        
                    # Let's search in the tasks - can we add one to the task feedback list?
                    if flag_task != 2: 
                        for jj in self.task_list:
                            if temp_dictionary['name'] == jj['name']:
                                flag_task = 1 
                                
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
                            if self.debug == 'on':
                                print("ok: {}".format(temp_dictionary))
                            flag_task = 0
                            x = 0

        # for all the method in method_actions (i) extract name and parameters,(ii) extract preconditions and ordered subtasks, (iii) create a xmi:id
        temp_param_list = []
        method_name = ''
        task_name = ''
        flag_method = 0
        counter = 0
        
        parameters = []
        preconditions = []
        ordered_substasks = []

        for uu in data_methods:

            flag_preconditions = 0
            flag_subtasks = 0
            flag_task_method = 0
            for ii in uu:
                if ':method' in ii:
                    method_name = ii.split()[1].strip()
                if ':parameters' in ii:

                    regex_pattern ='\?\w+.*\w+'
                    parameters = re.findall(regex_pattern, ii, re.S)

                    for jj in parameters:
                        
                        temp_param_list.append(jj.strip().split('?')[1::])
                        # No unwanted white spaces needed!
                        for index,oo in enumerate(temp_param_list[-1]):
                            oo = oo.strip()
                            temp_param_list[-1][index] = oo
                            
                if ':task' in ii and flag_task_method == 0:
                    regex_pattern ='\w+.'
                    task_name = re.findall(regex_pattern,ii)[1].strip()
                
                if ':precondition' in ii:
                    flag_preconditions = 1
                    flag_task_method = 1
                
                if flag_preconditions == 1 and ':precondition' not in ii and ':subtasks' not in ii and ii != ')':
                    # Just remove all the paranteses and make a new string
                    precondition_str = ii.strip()
                    precondition_str = '{}'.format(precondition_str)
                    preconditions.append(precondition_str)  
                
                if ':subtasks' in ii:
                    flag_preconditions = 0
                    flag_subtasks = 1

                if ':ordering' in ii:
                    flag_subtasks = 0
                
                if flag_subtasks == 1  and ':subtasks' not in ii and ii != ')':
                    # Just remove all the paranteses and make a new string
                    regex_pattern ='\(\w+.*'
                    subtask = re.findall(regex_pattern, ii)
                    if subtask!= '':
                        subtask_name = subtask[0].split()[0].replace('(','')
                        ordered_substasks.append(subtask_name)
            
            # Check if the method has a name
            if method_name != '' :
                temp_dictionary = {'name': method_name, 'xmi:id': str(uuid.uuid1())}
                method_name = ''
            else:
                flag_method = 2
                if self.debug == 'on':
                    print('The method has no name')
                self.log_file_general_entries.append('\t\t {} is defined as method, however it has no name \n'.format(uu))
            # Check if the method is associate to a task
            if task_name != '' :
                temp_dictionary['task'] = task_name
                task_name = ''
            else:
                flag_method = 2
                if self.debug == 'on':
                    print('The method is not refered to any task')
                self.log_file_general_entries.append('\t\t {} is defined as method, however it has no name \n'.format(uu))
            # Check if the method has parameters
            if parameters != []:
                temp_dictionary['parameters'] = temp_param_list[-1]
                temp_param_list = []
            else:
                flag_method = 2
                if self.debug == 'on':
                    print('The method has no parameters')
                self.log_file_general_entries.append('\t\t {} is defined as method, however it has no parameters \n'.format(uu))
            # Check if the method has preconditions
            if preconditions != []:
                temp_dictionary['preconditions'] = [x for x in preconditions]
                preconditions = []
            else:
                flag_method = 2
                if self.debug == 'on':
                    print('The method has no preconditions')
                self.log_file_general_entries.append('\t\t {} is defined as method, however it has no preconditions \n'.format(uu))
            # Check if the method has ordered substaks
            if ordered_substasks != []:
                temp_dictionary['actions'] = [x for x in ordered_substasks]
                ordered_substasks = []
            else:
                # It is possible that a method has no ordered subtasks
                # flag_method = 2
                temp_dictionary['actions'] = []
                if self.debug == 'on':
                    print('The method has no ordered substasks: is this correct?')
            
            # Let's search in the methods - can we add one to the task feedback list?
            if flag_method != 2: 
                for jj in self.method_list:
                    # Check the name
                    if temp_dictionary['name'] == jj['name']:
                        flag_method = 1
                        # Check the task name
                        for kk in self.task_list:
                            if kk['name'].strip() == temp_dictionary['task'].strip():
                                flag_method = 1
                            # Check the parameters
                            for xx in temp_dictionary['parameters']:
                                for kk in jj['parameters']:
                                    if xx == kk:
                                        flag_method = 1
                                        counter = counter + 1
                                    
                                if counter == len(jj['parameters']):
                                    flag_method = 1
                                    counter = 0
                                else:
                                    flag_method = 0
                            # Check the preconditions
                            for xx in temp_dictionary['preconditions']:
                                for kk in jj['preconditions']:
                                    if xx == kk:
                                        flag_method = 1
                                        counter = counter + 1
                                    
                                if counter == len(jj['preconditions']):
                                    flag_method = 1
                                    counter = 0
                                else:
                                   flag_method = 0
                            # Check the actions names
                            name_task = []
                            # Check the names in order of the actions in the method
                            for kk in jj['ordered_tasks']:
                                for uu in self.opaqueAction_list:
                                    if kk == uu['xmi:id']:
                                        name_task.append(uu['name'])                        
                            
                            for xx in temp_dictionary['actions']:
                                # Check if the order and the names are the same
                                for oo in name_task:
                                    if xx == oo:
                                        flag_method = 1
                                        counter = counter + 1
                                if counter == len(jj['ordered_tasks']):
                                    flag_method = 1
                                    counter = 0
                                else:
                                   flag_method = 0
                              
                        
                if flag_method == 0:
                    self.method_list_feedback.append(temp_dictionary)
                    flag_method = 0
                else:
                    if self.debug == 'on':
                        print("ok: {}".format(temp_dictionary))
                    flag_method = 0
                 

        # for all the actions in data_actions (i) extract name and parameters,(ii) extract preconditions and effects, (iii) create a xmi:id
        temp_param_list = []
        action_name = ''
        flag_action = 0
        counter = 0
        parameters = []
        preconditions = []
        effects = []

        for uu in data_actions:
            flag_effects = 0
            flag_preconditions = 0
            for ii in uu:
                if ':action' in ii:
                    action_name = ii.split()[1].strip()
                if ':parameters' in ii:

                    regex_pattern ='\?\w+.*\w+'
                    parameters = re.findall(regex_pattern, ii, re.S)

                    for jj in parameters:
                        
                        temp_param_list.append(jj.strip().split('?')[1::])
                        # No unwanted white spaces needed!
                        for index,oo in enumerate(temp_param_list[-1]):
                            oo = oo.strip()
                            temp_param_list[-1][index] = oo
                if ':precondition' in ii:
                    flag_preconditions = 1
                
                if flag_preconditions == 1 and ':precondition' not in ii and ':effect' not in ii and ii != ')':
                    # Just remove all the paranteses and make a new string
                    precondition_str = ii.strip()
                    precondition_str = '({})'.format(precondition_str)
                    preconditions.append(precondition_str)  
                
                if ':effect' in ii:
                    flag_preconditions = 0
                    flag_effects = 1
                
                if flag_effects == 1  and ':effect' not in ii and ii != ')':
                    # Just remove all the paranteses and make a new string
                    effect_str = ii.replace(')','').replace('(','')
                    effect_str = '({})'.format(effect_str)
                    effects.append(effect_str)                     
                        

            if action_name != '' :
                # Add on thing at the time so you know which feedback to print.
                temp_dictionary = {'name': action_name , 'xmi:type': 'uml:OpaqueAction', 'xmi:id': str(uuid.uuid1())}
                if parameters != []:
                    temp_dictionary['parameters'] =  temp_param_list[-1]
                    temp_param_list = []
                    parameters = []
                else: 
                    flag_action = 2
                    if self.debug == 'on':
                        print('The action {} has no parameters: is it an error?'.format(action_name))
                    self.log_file_general_entries.append('\t\t The action {} has no parameters: is it an error? \n'.format(action_name))
                if preconditions != []:
                    temp_dictionary['preconditions'] =  [x for x in preconditions]
                    preconditions = []
                else: 
                    flag_action = 2
                    if self.debug == 'on':
                        print('The action {} has no preconditions: is it an error?'.format(action_name))
                    self.log_file_general_entries.append('\t\t The action {} has no preconditions: is it an error? \n'.format(action_name))
                if effects != []:
                    temp_dictionary['effects']  = [x for x in effects]
                    effects = []
                else: 
                    flag_action = 2
                    if self.debug == 'on':
                        print('The action {} has no effects: is it an error?'.format(action_name))                 
                    self.log_file_general_entries.append('\t\t The action {} has no effects: is it an error? \n'.format(action_name))
                action_name = ''
            else:
                flag_action = 2
                if self.debug == 'on':
                    print('The action has no name, is it an error?')
                self.log_file_general_entries.append('\t\t {} is defined as an action, however it has no name \n'.format(uu))
                # maybe print a log file anyway

        
            # Let's search in the tasks - can we add one to the task feedback list?
            if flag_action != 2: 
                for jj in self.opaqueAction_list:
                    # Check the name
                    if temp_dictionary['name'] == jj['name']:
                        # flag_task = 1 
                        counter = 0
                        # Check the parameters
                        for xx in temp_dictionary['parameters']:
                            for kk in jj['parameters']:
                                if xx == kk:
                                    flag_action = 1
                                    counter = counter + 1
                                
                            if counter == len(jj['parameters']):
                                flag_action = 1
                                counter = 0
                            else:
                                flag_action = 0
                        # Check the preconditions
                        for xx in temp_dictionary['preconditions']:
                            for kk in jj['preconditions']:
                                if xx == kk:
                                    flag_action = 1
                                    counter = counter + 1
                                
                            if counter == len(jj['preconditions']):
                                flag_action = 1
                                counter = 0
                            else:
                               flag_action = 0

                        # Check the effects
                        for xx in temp_dictionary['effects']:
                            for kk in jj['effects']:
                                if xx == kk:
                                    flag_action = 1
                                    counter = counter + 1
                                
                            if counter == len(jj['effects']):
                                flag_action = 1
                                counter = 0
                            else:
                                flag_task = 0
                                
                        
            if flag_action == 0:
                self.opaqueAction_list_feedback.append(temp_dictionary)
                flag_action = 0
            else:
                if self.debug == 'on':
                    print("ok: {}".format(temp_dictionary))
                flag_action = 0
                x = 0                
                
    def Feedback_Log_FileWriting (self):
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
        file.write('\t Missing or Modified Requirements: \n')
        for ii in self.hddl_requirement_feedback:
            file.write('\t\t {} \n'.format(ii))        
        # Missing Types:
        file.write('\t Missing or Modified Types: \n')
        for ii in self.hddl_type_feedback:
            file.write('\t\t {} \n'.format(ii))
        # Missing Predicates:
        file.write('\t Missing or Modified Predicates: \n')
        for ii in self.predicate_list_feedback:
            file.write('\t\t {} \n'.format(ii))
        # Missing Tasks:
        file.write('\t Missing or Modified Tasks: \n')
        for ii in self.task_list_feedback:
            file.write('\t\t {} \n'.format(ii))
        # Missing Methods:
        file.write('\t Missing or Modified Methods: \n')
        for ii in self.method_list_feedback:
            file.write('\t\t {} \n'.format(ii))
        # Missing Methods:
        file.write('\t Missing or Modified Actions: \n')
        for ii in self.opaqueAction_list_feedback:
            file.write('\t\t {} \n'.format(ii))
        
                     
            
    
def main():
    
    
    # First Parse de input file to get the information you need
    # The configuration file should be in the same folder of the parsing module - at least for now
    with open('configuration_file.xml', 'r') as f:
        configuration_file = f.read()    
    
    # Get current directory address
    d_now = os.getcwd()
    # Go to the input directory
    d_input = d_now + '\\inputs'
    
    
    # Read the configuration file.xml with BeautifulSoup (https://beautiful-soup-4.readthedocs.io/en/latest/#)
    configuration_file_soup = BeautifulSoup(configuration_file, 'xml')
    file_parameters = configuration_file_soup.find_all('file')
    
    # Get the name of the Papyrus File
    file_papyrus = file_parameters[0]['file_name']
    
    # Get the name of the Domain File - if not create an automatic name
    if file_parameters[0].has_attr('domain_name'):
        domain_name = file_parameters[0]['domain_name']
    else:
        domain_name = 'None'
    
    # Get the name of the Feedback file - if you want to create one
    if file_parameters[0].has_attr('feedback_file_name'):
        feedback_name = file_parameters[0]['feedback_file_name']
    else:
        feedback_name = 'None'
    
    # Get the name of map file (from Maximilien Code - Look at the CORODRO Repository of the drone)
    # Maximilien code is available even here: https://github.com/MaxIGL/SLAM_Igluna
    if file_parameters[0].has_attr('map_file_name'):
        map_file_name = file_parameters[0]['map_file_name']
        with open(d_input +'\\' + map_file_name, 'r') as f:
            map_data = f.readlines() 
    else:
        map_file_name = 'None'
    
    # See which analysis we should do with the data from Papyrus
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
        
    if file_parameters[0].has_attr('task_parameters'):
        task_parameters = file_parameters[0]['task_parameters']
    else:
        # if nothing is said consider the common task parameters
        task_parameters = 'common'
    
    # Get the HDDL Requirements
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
    # Get the initial Task Network for the problem file!
    htn_tasks = []
    for xx in htn_tasks_soup:
        dummy_string = xx.contents[0]
        htn_tasks.append(dummy_string)    

    with open(d_input +'\\' +file_papyrus, 'r') as f:
        data = f.read()
        
    
    # Now let's start with the real analysis
    # First create the class with all the parameter you need
    file_final = XML_parsing(data, map_data, hddl_requirements, domain_name, htn_tasks, feedback_name, d_now, task_parameters)
    # Parse the XLM from Papyrus
    file_final.XML_ActiveParsing()
    # Create domain file
    if generate_domain_file == 'yes':
        # Take out the element you need for the domain file:
        file_final.DomainFileElements()
        file_final.Domain_FileWriting()
    # Get the elements to design the problem file:
    if generate_problem_file == 'yes':
        file_final.ProblemFileElements()
        file_final.Problem_FileWriting()
    # Create Feedback file - For now it's a simple log:
        # We listed the requirements, types, predicates, tasks, methods and actions different from the XML file
        # A routine will be soon implemented to directly translate the log file into usable Papyrus elements! 
    if generate_feedback_file == 'yes':
        if generate_domain_file == 'no':
            file_final.DomainFileElements()
        # Get the Feedback information from the modified domain file
        file_final.Feedback_file()
        # Create the log with the different info
        file_final.Feedback_Log_FileWriting()



if __name__ == "__main__":
    main()