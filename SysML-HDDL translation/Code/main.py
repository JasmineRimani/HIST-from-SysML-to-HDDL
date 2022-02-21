# -*- coding: utf-8 -*-
"""
Created on Thu Nov 4 16:19:39 2021

@author: Jasmine Rimani
"""
# https://beautiful-soup-4.readthedocs.io/en/latest/#
from bs4 import BeautifulSoup
# https://docs.python.org/3/library/datetime.html
import os
# https://docs.python.org/3/library/traceback.html
import logging
# https://docs.python.org/3/howto/logging.html
# xml_parsing function
from xml_parsing import XML_parsing
# Domain Problem Definition
from DomainDefinition import DomainDefinition
# Problem Definition
from ProblemDefinition import ProblemDefinition
# Feedback Definition
from FeedbackDefinition import FeedbackDefinition
from Partial_FeedbackDefinition import Simple_FeedbackDefinition



LOGGER = logging.getLogger(__name__)

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
    # if file_parameters[0].has_attr('map_file_name'):
    #     map_file_name = file_parameters[0]['map_file_name']
    #     with open(d_input +'\\' + map_file_name, 'r') as f:
    #         map_data = f.readlines() 
    # else:
    #     map_file_name = 'None'
    
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

    if file_parameters[0].has_attr('method_precondition_from_action'):
        method_precondition_from_action = file_parameters[0]['method_precondition_from_action']
    else:
        method_precondition_from_action = 'yes'        


    if file_parameters[0].has_attr('flag_ordering'):
        flag_ordering_file = file_parameters[0]['flag_ordering']
    else:
        flag_ordering_file = 'yes'        
        
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
                         'Expression Evaluation', 'Fluents', 'Open World', 'True Negation', 'ADL', 'UCPOP', 'hierarchy', 'method-preconditions',  'negative-preconditions']
    else:
        hddl_requirements = list_requirements
    
    # htn_tasks_soup = configuration_file_soup.find_all('li_htn')
    # # Get the initial Task Network for the problem file!
    # htn_tasks = []
    # for xx in htn_tasks_soup:
    #     dummy_string = xx.contents[0]
    #     htn_tasks.append(dummy_string)    

    with open(d_input +'\\' +file_papyrus, 'r') as f:
        data = f.read()
        
    
    # Parse the input file
    print("Parsing input file", file_papyrus)
    # Set up the parsing environment
    initial_dictionary = XML_parsing(data, hddl_requirements)
    # Parse the file and create a dictionary of entries
    parsed_dictionary = initial_dictionary.XML_ActiveParsing()
    # Create domain file
    if generate_domain_file == 'yes':
        print("Generating Domain File")
        # Take out the element you need for the domain file:
        DomainFile = DomainDefinition(domain_name, parsed_dictionary, task_parameters, flag_ordering_file, method_precondition_from_action)
        # Identify the Domain File Elements
        domain_file_elements = DomainFile.DomainFileElements()
        # Write the Domain FIle
        DomainFile.DomainFileWriting()    
        print("Domain File Generated under the name of ", domain_name)
        print("Generating Simple Feedback File")
        FeedbackFile = Simple_FeedbackDefinition(domain_name, parsed_dictionary, domain_file_elements)
        FeedbackFile.Simple_FeedbackLogFileWriting()
        print("Feedback File Generated")    
        
    if generate_problem_file == 'yes':
        print("Generating Problem File/s")
        ProblemFile = ProblemDefinition(domain_name, parsed_dictionary, domain_file_elements)
        problem_file_elements = ProblemFile.ProblemFileElements()
        ProblemFile.ProblemFileWriting()
        print("Problem File Generated under the name of ", domain_file_elements["problem_name"])
        
    if generate_feedback_file == 'yes':
        print("Generating Feedback File")
        FeedbackFile = FeedbackDefinition(domain_name, parsed_dictionary, domain_file_elements, problem_file_elements, feedback_name)
        feedback_file_elements = FeedbackFile.FeedbackFile()
        FeedbackFile.FeedbackLogFileWriting()
        print("Feedback File Generated under the name of ", feedback_file_elements["feedback_file_name"])

    
    x = 1

if __name__ == "__main__":
    main()