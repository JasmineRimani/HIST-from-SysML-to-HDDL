# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 09:31:22 2021

@author: jasmi

Useful links:
    https://www.geeksforgeeks.org/reading-and-writing-xml-files-in-python/
    
"""

# importing element tree
# under the alias of ET
import xml.etree.ElementTree as ET
 
# Passing the path of the
# xml document to enable the
# parsing process
tree = ET.parse('xml_sample.uml')
 
# getting the parent tag of
# the xml document
root = tree.getroot()
 
# printing the root (parent) tag
# of the xml document, along with
# its memory location
print(root)

# printing the attributes of the
# first tag from the parent
print(root[0].attrib)