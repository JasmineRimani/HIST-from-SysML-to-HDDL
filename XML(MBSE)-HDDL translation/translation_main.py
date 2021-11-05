# -*- coding: utf-8 -*-

"""
Created on Tue Nov  2 09:03:32 2021

@author: Jasmine Rimani

Useful links:
    https://www.geeksforgeeks.org/reading-and-writing-xml-files-in-python/
    https://towardsdatascience.com/python-dictionaries-651acb069f94
    https://beautiful-soup-4.readthedocs.io/en/latest/#navigating-the-tree

"""

from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
 
 

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


"""
# List of Tags in the XML file

Maybe_useful_later_Tags = ['upperBound'] 

NotUsed_Tags = ['ownedComment', 'body', 'generalization']

Used_Tags = ['packagedElement', 'ownedEnd', 'ownedUseCase', 'ownedBehavior', 'edge', 'node', 'inputValue', 'outputValue', 'extend']

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

"""
#xmi:type
Type = ['uml:Package', 'uml:Actor', 'uml:Generalization','uml:Association','uml:Property','uml:UseCase', 'uml:Activity' ]

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

"""

Others = ['visibility', 'name', 'general', 'memberEnd', 'node', 'target', 'source']

# List SysML

# Packages list 
package_list = []
# Type list
hddl_type_list = []
# Predicates list
hddl_predicate_list = []
# Requirements domain files
requirements_list = [] # <-- To implement!!
# HighLevel UseCase list - Tasks
Task_list = []
# UseCase parameter list
UseCase_list_parameter = []
# Methods UseCase list - Tasks
Method_list = []


# Reading the data inside the xml
# file to a variable under the name
# data

with open('xml_sample.uml', 'r') as f:
    data = f.read()
 
# Passing the stored data inside
# the beautifulsoup parser, storing
# the returned object
Bs_data = BeautifulSoup(data, "xml")
 
# # Finding all instances of tag - You get a list with all the instances with that tag
b_node = Bs_data.find_all('node')
# If the tags are nested - you get each tag one after the other from the order of the file
b_packagedElement = Bs_data.find_all('packagedElement') 
# Isolate the "xmi:type="uml:Package" " --> e.g. b_packagedElement[0]['xmi:type']
for index,ii in enumerate(b_packagedElement):
    
    if ii['xmi:type'] == 'uml:Package':
        package_list.append(ii['name'])    
    
    
    if ii['xmi:type'] == 'uml:Class':
        hddl_type_list.append(ii['name'])
    # Isolate Actors:
    
    # Isolate Usecases that are packegedElements --> You get your tasks name, however you still need your parameters
    # Parameters --> Take the minumum parameters from the method
    if ii['xmi:type'] == 'uml:UseCase':
        Task_list.append({"name": ii['name'], "xmi:id":ii['xmi:id'], "general_xml_index": index})   
        
        # Access any instance of the dictionary use case with UseCase_list[n] and any key of the dictionary with get() UseCase_list[1].get('name')
        
"""
For each useCase, we  can access to the sub-tags with: 
    a = b_packagedElement[10].children  # --> where the 10 comes from "general_xml_index": index in the soup
    for i in a: print(i) # --> you will see all the subtags


"""

for index,ii in enumerate(b_packagedElement[10].children):
    # Find the methods
    try: 
        # Check the sub-UseCases that can be methods: double check on the type(considered as attribute) and the tag name
        if ii['xmi:type'] == 'uml:UseCase' and ii.name == 'ownedUseCase':
            Method_list.append({"name": ii['name'], "xmi:id":ii['xmi:id'], "general_xml_index": index, "task":b_packagedElement[10].get('name')})  
    except:
        pass

"""
Define the parameters in the method and start building the predicate list
"""






print('Packages:', package_list)
print('HDDL Types:', hddl_type_list)
print('Use Cases - Task Level:',Task_list)
print('Use Cases - Method Level:',Method_list)





# Using find() to extract attributes
# of the first instance of the tag
# b_packagedElement = Bs_data.find_all('packagedElement', {'xmi:type="uml:UseCase"'})