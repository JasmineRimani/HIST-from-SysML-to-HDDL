## HIST (HDDL fIles SysML Translation): A SysML to HDDL automated translation (Still in Development)

# Motivation
The need to extract useful information from SysML/MBSE models and convert them into usable entities for other disciplines is rising. This code extracts from a Papyrus model the information to automatically generate the HDDL domain file. In addition, the code can generate an HDDL problem file and a feedback file with the differences between the Papyrus model and the HDDL domain file. 

**Files and Folder and their Languages**
- Igluna_Benchmark: Papyrus model created for the planner of the CoRoDro mission.
- SysML-HDDL Translation Satellite: Papyrus model used for the validation of HIST in respect to the official HDDL benchmarks.
- SysML-HDDL Translation Transport: Papyrus model used for the validation of HIST in respect to the official HDDL benchmarks.
- Template: Papyrus model template to use HIST at its potential
- Code: Folder with all the code developed up until now for the SysML-HDDL translation
     - inputs: Folder that groups all inputs needed for the translation --> uml model + "map of the environment" + "possible domain feedback file that we want to check"
     - outputs: Folder that groups all outputs domain file + problem file + feedback file 
- old_files: Folder with the back-up of the old code
- step_by_step_tutorial.pptx: presentation with step by step tutorial to define the domain instances in Papyrus using SysML
- Updates MBSE-SysML translation to HDDL.pptx: presentation where I keep track of the advancement of HIST

**In Detail Documentation**
[TO DO] --> An initial documentation would be soon uploaded to the repository 


**Files and their Languages**
- Papyrus Model --> uml 
     - uml file with all the information stored in the Papyrus SysML model.
     - It can usually be found in ../user/*user name*/papyrus_workspace/*name of the workspace*.
     - In the analysis the sample papyrus model is ../inputs/xml_sample_5.uml
- configuration_file.xml --> xml
      - This file in in the initial folder. It is used now to store the needed input parameter for the code. 
      - It will be probably substited with parameters from command line (?)
- *''.py* --> Python
      - The real code modules that take the *.uml* file and generates the HDDL file
- *''.hddl* --> HDDL 
      - The generated HDDL files or feedback sample domain.hddl file
      - The generated HDDL files can be found in ..outputs/*.hddl*
      - The feedback sample domain.hddl file can be found in ../inputs/*.hddl*
- *''.txt* --> Map generated from the SLAM module (code by Maximilien Dreier of CoRoDro: https://github.com/MaxIGL/SLAM_Igluna)
      - the sample file is plan_final_1m_1_int.txt and it can be find in ../inputs/*.txt*

# Required inputs for the Classes in the CODE 
- ***Class inputs*** :  
        - configuration file --> defines the parameters of the translation
        - main file --> Papyrus file name
        -  map_data --> if we want to generate the HDDL problem file for a robotic exploration we need some information on the environment.  
        -  htn_tasks --> if we want to generate the HDDL problem file for a robotic exploration we need some information on the environment. 
- ***Classes in Code***:
     - **def XML_Parsing(self):**  the class saves all the instances from the Papyrus Model using https://beautiful-soup-4.readthedocs.io/en/latest/#
     - **def DomainDefinition(self):** the class saves in nested dictionaries all the inputs needed to create the *_domain.hddl* file and it creates the *_domain.hddl* file
     - **def ProblemDefinition(self):** the class saves in nested dictionaries all the inputs needed to create the *_problem.hddl* file and it creates the *_problem.hddl* file
     - **def FeedbackDefinition(self):** the class parses a *_domain.hddl* file and compares it with the DomainDefinition(self). It generates a log file with the discrepancy and the errors/warning found during coding. 

# Paper to cite if you use this repository 
***still to write***

# Still Actively Coding and Polishing:
- The initial validation has been performed. Therefore a second cycle of development starts to polish and better define the code, answer the open points and define in detail all the required instances from Papyrus. 
- Now to focus is on:
     - Define all the instances of the papyrus model with a brief explaination of their role [DOING]
     - Polish the parsing, domain and problem modules. [DOING]
     - Write a clear reference manual on how to use the tool and how to model the instances in Papyrus. [DOING]   
     - Polish the feedback file generator [TO DO]  


# HDDL Benchmarks to try:
**official repository** : https://github.com/panda-planner-dev/ipc2020-domains

# New comments to implement:
