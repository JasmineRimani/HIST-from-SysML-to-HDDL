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
import yaml
# https://yaml.org/

# Custom Functions
# xml_parsing function
from Parsing_module import XML_parsing
# Domain Problem Definition
from DomainCreation import Domain
# Problem Definition
from ProblemCreation import ProblemDefinition
# Feedback Definition
from FeedbackDefinition import FeedbackDefinition
from Partial_FeedbackDefinition import Simple_FeedbackDefinition
from yaml_parsing import YAML_parsing


LOGGER = logging.getLogger(__name__)


def main():
    
    # First Parse de input file to get the information you need
    # The configuration file should be in the same folder of the parsing module - at least for now
    with open('configuration.yaml', 'r') as f:
        configuration_file = f.read()    
    # Get the input from teh yaml parsing
    yaml_class = YAML_parsing(configuration_file)
    # Files
    file_papyrus, domain_name, feedback_name = yaml_class.YAML_fileNames()
    # Flags
    generate_problem_file, generate_domain_file, generate_feedback_file, domain_requirements = yaml_class.YAML_mainFlags()
    method_precondition_from_action, flag_ordering_file, task_parameters = yaml_class.YAML_otherFlags()
    # Get package name
    package_HDDL, package_domain, package_problem, package_feedback = yaml_class.YAML_PackagesNames()
    # Get current directory address
    d_now = os.getcwd()
    # Go to the input directory
    d_input = d_now + '\\inputs'
    
    # Open the papyrus file
    with open(d_input +'\\' + file_papyrus, 'r') as f:
        data = f.read()
    
    # Parse the input file
    print("Parsing input file: ", file_papyrus)
    # Set up the parsing environment
    initial_dictionary = XML_parsing(data, package_HDDL, package_domain, package_problem, package_feedback)
    # Parse the file and create a dictionary of entries
    SysML_data, domain_dictionary, missions = initial_dictionary.Parsing()
    # Create domain file
    if generate_domain_file == 'yes':
        print("Generating Domain File")
        # Take out the element you need for the domain file:

        DomainFile = Domain(domain_name, SysML_data, domain_dictionary, domain_requirements, task_parameters, flag_ordering_file, method_precondition_from_action)
        # Identify the Domain File Elements
        domain_file_elements, log_file_general_entries = DomainFile.DomainFileElements()
        # Write the Domain FIle
        DomainFile.DomainFileWriting(domain_file_elements)    
        print("Domain File Generated under the name of ", domain_name)
        print("Generating Simple Feedback File")
        FeedbackFile = Simple_FeedbackDefinition(log_file_general_entries)
        FeedbackFile.Simple_FeedbackLogFileWriting()
        print("Feedback File Generated")    
        
    if generate_problem_file == 'yes':
        print("On-going implementation!")
        print("The problem file provides objects and initial conditions")
        print("However, we are trying new ways to create the HDDL code form MBSE and graphs")
        ProblemFile = ProblemDefinition(domain_name, SysML_data, missions)
        ProblemFile.ProblemFileWriting()
        
    if generate_feedback_file == 'yes':
        print("Not yet implemented! Please look at the previous version!")


    

if __name__ == "__main__":
    main()

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