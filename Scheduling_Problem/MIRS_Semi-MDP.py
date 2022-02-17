#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 09:26:31 2022

@author: Jasmine Rimani
"""

# Observation Requests - OR (a site defined in [ID, latitude and longitude, priority] the mapping of a zone of phobos) - let's start with the landing site because we have both the landing site latitude and longitude and we have the calculation of the slots. I would expect an excel with this informations.
# Observation Opportunities- OO  (MMX-MIRS-CNES-TNO-01777-MIRS Observation Plan Examplev1.3.1.dox)
    # landing site observations (longitude, latitude, start_time, end_time, PhaseAngle, LocalTime, SunIncidence, Cross-track-mid-slot,  Cross-track-mid-slot)
    # phobos observations (start_time, end_time, duration, delay with previous MIRS observation, Subsatellite_Longitude_Start, Subsatellite_Longitude_End, Cross-track, along-track)
# Downlink Opportunities- DO (5h30/6h00 every day counting Mars occultation)
# Planning Horizon - PH - 1 month
# Slew time = 10 mintes (MMX-MIRS-CNES-TNO-01777-MIRS Observation Plan Example.excel)
# Objective: minimizing delay in data return

# For each observation we need to define the data volume


""" Assumption:
    Set defined as:
        OR_i = [ID, latitude and longitude, priority]
        OO_i = [longitude, latitude, start_time, end_time, PhaseAngle, LocalTime, SunIncidence, Cross-track-mid-slot,  Cross-track-mid-slot]
        DO_i = [start_time, end_time, max allowed data volume]
    Observation Constraints:
        PH = [start_time, end_time]
    Optimization Objective:
        max OR_i(priority)
"""

import pandas as pd

class GetSets():
    def __init__(self, observation_ops_file, observation_req_file):
        observation_req = pd.read_excel(observation_req_file, sheet_name='Synthesis' )
        observation_ops = []
        observation_ops.append(pd.read_excel(observation_req_file, sheet_name='QSO-M plan'))
        observation_ops.append(pd.read_excel(observation_req_file, sheet_name='QSO-LA plan'))
        observation_ops.append(pd.read_excel(observation_req_file, sheet_name='QSO-LBapril plan'))
        observation_ops.append(pd.read_excel(observation_req_file, sheet_name='QSO-LBmay plan'))
        observation_ops.append(pd.read_excel(observation_req_file, sheet_name='QSO-LCjune plan'))
        observation_ops.append(pd.read_excel(observation_req_file, sheet_name='QSO-LCjuly plan'))
        
        
        
    
# the ideq is to deconflict overlapping or duplicate observations between satellites, across time
class MutuallyExclusiveCollects():
    def __init__(self):
        pass



def main():
    # get your input file
    observation_ops_file = '/MMX-MIRS-CNES-TNO-0177Annex1MIRSObservationPlans.xlsx' 
    observation_req_file ='/MMX-MIRS-CNES-TNO-0177 Annex 2 Analysis of JAXA Landing Site Candidates.xlsx'


if __name__ == "__main__":
    main()