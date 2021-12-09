## SysML to HDDL automated translation (Still in Development)

# Motivation
The need to exctract useful information from SysML/MBSE models and convert them in usable entities for other disciplines is raising. This code extracts a Papyrus model of "Functinal Analysis" to automatically generate the HDDL domain file. The code can generate a HDDL problem file as well as a feedback file with the differences between the Papyrus model and the HDDL domain file. 

**Files Languages**
- Papyrus Model --> xmi
- Parsing_module.py --> Python
- *.hddl --> HDDL 

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

# TO CODE:
- ***Functions***:
     - def Feedback_xml_file(self):
        - Directly add the information from Feedback_file(self) to the Papyrus model in a folder called Feedback.
           - The feedback entries will be already in the final Papyrus model 

