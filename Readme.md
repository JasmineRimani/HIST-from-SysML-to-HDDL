# HIST (HDDL fIles SysML Translation): A SysML to HDDL automated translation 
## Motivation
MBSE models are usuful knowledge engineering references that can easily incorporate the knowledge of the designer and make it usable for other disciplines. 
In our case, we worked with AI planning and specifically HDDL. 
The tool has been implemented as a part of the IGLUNA-CoRoDro analogue mission, however, it is still under development to add capabilities and test its robusteness in different modelling context. 
You are free re-use the code and change it. However, if you are using it for your project, please cite:
```
  @article{rimani2021applicationMBSE,
    title={Application of MBSE to model Hierarchical AI Planning problems in HDDL},
    author={Rimani, Jasmine and Lesire, Charles and Lizy-Destrez, Stéphanie and Viola, Nicole},
    publisher={ International Conference on Automated Planning and Scheduling (ICAPS) 2021, KEPS Workshop},
    year={2021}
  }
```
## Licence 
This work is distributed under the MIT License.

## Status
The code is still under development. We try to polish it, test it and add modules as we go. 

## What are we implementing
This code extracts from a model in Papyrus (https://www.eclipse.org/papyrus/) the information to automatically generate an HDDL domain file. 

In addition, the code can partially generate an HDDL problem files. Because AI planning problem files are domain dependent, they are difficult to generalize. We are still trying to find a way to do so.

The code provides a feedback file:
  - with the possible problem that may be arised from the translation.
  - with the differences between the Papyrus model and an externally provided HDDL domain file. However, this last instance can be improved. 
