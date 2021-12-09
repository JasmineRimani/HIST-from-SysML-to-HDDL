## SysML to HDDL automated translation (Still in Development)

# Motivation
The need to exctract useful information from SysML/MBSE models and convert them in usable entities for other disciplines is raising. This code extracts a Papyrus model of "Functinal Analysis" to automatically generate the HDDL domain file. The code can generate a HDDL problem file as well as a feedback file with the differences between the Papyrus model and the HDDL domain file. 

**Files and their Languages**
- Papyrus Model --> uml 
     - uml file with all the information stored in the Papyrus SysML model.
     - It can usually be found in ../user/*user name*/papyrus_workspace/*name of the workspace*.
     - In the analysis the sample papyrus model is ../inputs/xml_sample_5.uml
- configuration_file.xml --> xml
      - This file in in the initial folder. It is used now to store the needed input parameter for the code. 
      - It will be probably substited with parameters from command line (?)
- parsing_module.py --> Python
      - The real code that takes the *.uml* file and generates the HDDL file
- *.hddl* --> HDDL 
      - The generated HDDL files or feedback sample domain.hddl file
      - The generated HDDL files can be found in ..outputs/*.hddl*
      - The feedback sample domain.hddl file can be found in ../inputs/*.hddl*
- *.txt* --> Map generated from the SLAM module (code by Maximilien Dreier of CoRoDro)
      - the sample file is plan_final_1m_1_int.txt and it can be find in ../inputs/*.txt*

# Modules in parsing_module.py
- ***Class*** : class XML_parsing()
    - ** Required Class Instance Variable**:  
        - file --> Papyrus file name
        -  map_data --> if we want to generate the HDDL problem file for a robotic exploration we need some information on the environment.  
        -  htn_tasks --> if we want to generate the HDDL problem file for a robotic exploration we need some information on the environment. 
- ***Functions in class XML_parsing()***:
     - **def XML_ActiveParsing(self):**  the function saves all the instances from the Papyrus Model using https://beautiful-soup-4.readthedocs.io/en/latest/#
     - **def DomainFileElements(self):** the function saves in nested dictionaries all the inputs needed to create the *_domain.hddl* file
     - **def ProblemFileElements(self):** the function saves in nested dictionaries all the inputs needed to create the *_problem.hddl* file
     - **def Domain_FileWriting(self):** the function that actively writes the *_domain.hddl* file
     - **def Feedback_file(self):** the function that parse the *_domain.hddl* file and store the information in nested dictionaries. This dictionaries will then be used to add the Feedback information in the Papyrus modl.
     - **def Feedback_Log_FileWriting(self):** the function list all the errors/warning from the *def DomainFileElements(self)* and *def ProblemFileElements(self)* in a log file. If a feedback file is requested, it listes all the differences between the UML model classes and the HDDL model classes (***still coding***).
     - **def Feedback_xml_file(self)**: the function create uml classes for all the discrepancies found in *def Feedback_file(self)* so that those can be directly added to the uml Papyrus model.

# Paper to cite if you use this repository 
***still to write***

# Still Actively Coding and Polishing:
- ***Functions***:
     - def Feedback_file(self):
        - Check the methods parsing from the HDDL file:
            - Check that the name, parameters, tasks, preconditions, subtasks and ordering are the same.
            - If one of them is different add the method to the feedback log with a comment on the different entries 
        - Check the task and action parsing from the HDDL file:
            - Check that the name, parameters, preconditions, and effects are the same.
            - If one of them is different add the method to the feedback log with a comment on the different entries  
     - In def Feedback_Log_FileWriting(self):
        - Find a way to clearly state the missing information in ordered sections
        - Add for each section related to each HDDL "classes" which Papyrus SysML definition counter part should be used in the modeling. 
     - In def Domain_FileWriting (self):
        - Code a check to match the task's parameters' names with the method's parameters' name when defining a HDDL method 

# To Code:
- ***Functions***:
     - def Feedback_xml_file(self):
        - Directly add the information from Feedback_file(self) to the Papyrus model in a folder called Feedback.
           - The feedback entries will be already in the final Papyrus model 

# How to use Papyrus to model domains:

