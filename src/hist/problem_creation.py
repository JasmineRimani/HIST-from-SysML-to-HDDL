# -*- coding: utf-8 -*-
"""
Created on Thu Nov 4 16:19:39 2021

@author: Jasmine Rimani
"""
# https://docs.python.org/3/library/datetime.html
from datetime import datetime
# https://docs.python.org/3/library/re.html
import re
# https://docs.python.org/3/library/uuid.html
import uuid
# https://docs.python.org/3/library/pathlib.html
from pathlib import Path

class ProblemDefinition():
    def __init__(self, domain_name, SysML_data, missions, d_now = None,  debug = 'on', output_dir = None ):
        # problem file name
        self.problem_name = datetime.now().strftime("%Y_%m_%d-%I_%M_%S") + '_' + domain_name + '_' +'_problem.hddl'
        self.domain_name = domain_name 
        # all the data from the .uml file
        self.overall_data = SysML_data 
        # all the data from the missions defined in the .uml file
        self.mission_dictionary = missions
        # debug_on
        self.debug = debug
        # Directory used now:
        self.d_now = Path(d_now) if d_now is not None else Path.cwd()
        self.output_dir = Path(output_dir) if output_dir is not None else self.d_now / 'outputs'
        self.log_file_general_entries = []
    

    def get_order(task):
        return task.get('order')
    
    def ProblemFileElements(self):

        # Log File init - Initialize the problem file log_file
        self.log_file_general_entries.append('------------------------------------------------- \n')
        self.log_file_general_entries.append('Log errors and warnings during the HDDL Problem file element acquisition: \n')
        self.log_file_general_entries.append('------------------------------------------------- \n')
        
        # Create a dictionary where we store all the instances of the problem file

        # Objects

        # Initial Conditions

        # Hierarchical Task Network

    def ProblemFileWriting (self):
        self.output_dir.mkdir(parents=True, exist_ok=True)
        generated_files = []
        for index,mission in enumerate(self.mission_dictionary):
            output_path = self.output_dir / f'{mission["name"]}_problem.hddl'
            file = open(output_path, 'w', encoding='utf-8')
            file.write('(define \n')
            file.write(' (problem {}_{}) \n'.format(mission["name"].lower(), index+1))
            file.write(' (:domain {}) \n'.format(self.domain_name).lower())

            # Objects
            file.write('\t (:objects \n')
            for object in mission["objects"]:
                file.write('\t\t{}\n'.format(object.lower()))
            file.write('\t )\n\n')

            # Hierarchical Task Network
            file.write('\t :htn( \n')
            file.write('\t\t :parameters () \n')
            if mission["init_HTN"] == 'None':
                file.write('\t\t :subtasks () \n')
                file.write('\t\t :ordering () \n')
            else:
                # still to implement
                pass
            
            # Initial Conditions
            # map file reading still to implement - please look at the previous version
            if mission["map_File"] == None:
                pass
            else:
                pass
            # Initial conditions 
            file.write('\t (:init \n')
            for cond in mission["initial_conditions"]:
                file.write('\t\t{}\n'.format(cond.lower()))  
            file.write('\t )\n\n')
            # end of the file
            file.write(')') 
            file.close()
            generated_files.append(output_path)

        return generated_files

