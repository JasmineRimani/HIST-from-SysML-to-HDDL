## SysML to HDDL automated translation (Still in Development)

# Motivation
The need to exctract useful information from SysML/MBSE models and convert them in usable entities for other disciplines is raising. This code extracts a Papyrus model of "Functinal Analysis" to automatically generate the HDDL domain file. The code can generate a HDDL problem file as well as a feedback file with the differences between the Papyrus model and the HDDL domain file. 

**Files Languages**
- Papyrus Model --> xmi
- Parsing_module.py --> Python
- *.hddl --> HDDL 

# Still Actively Coding and Polishing :
def Feedback_file(self)


- Feedback from HDDL to LogFile or XML Papyrus 

# Still To Implement:


- In def Domain_FileWriting (self): Check that the task parameters are effectively method parameters. If they are not - search for the right parameters in the method
- In def Feedback_file(self): complete the method feedback matching 
- In def Feedback_Log_FileWriting(self): Improve the log File aspect!
