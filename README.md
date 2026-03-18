# HIST: Translating Papyrus SysML/MBSE Models into HDDL for AI Planning and ConOps Analysis

HIST, short for `HDDL fIles SysML Translation`, is a research codebase for transforming Papyrus SysML / MBSE models into HDDL planning artifacts. The repository was created to support the study of mission operations and Concept of Operations (ConOps) for autonomous robotic space exploration systems while preserving traceability between systems engineering models and AI planning models.

In practice, HIST helps bridge two communities that often work with different abstractions:

- systems engineers who describe functions, architecture, items, and operational logic in MBSE and SysML;
- AI planning researchers and autonomy engineers who need HDDL domain and problem models for hierarchical planning.

This repository focuses on the translation layer between those two worlds.

## Why This Repository Exists

For autonomous space systems, it is not enough to define hardware and functions in an MBSE model. Designers also need to understand how the system may operate in realistic scenarios, how tasks decompose into lower-level activities, and how resources and mission constraints shape feasible plans.

Writing planning models by hand is possible, but it is time-consuming, difficult to maintain, and easy to desynchronize from the reference MBSE model. HIST was built to reduce that gap by reusing Papyrus-based MBSE knowledge and exporting it into HDDL-oriented planning structures.

The repository was originally used on rover-oriented operational studies and analogue mission scenarios, including models inspired by the IGLUNA context.

## Research Context

This code sits inside a broader research line on MBSE, AI planning, and operational analysis for autonomous robotic exploration systems.

### 1. MBSE to HDDL Translation

The most direct research reference for this repository is the 2021 KEPS paper:

- `Application of MBSE to model Hierarchical AI Planning problems in HDDL`
- Authors: Jasmine Rimani, Charles Lesire, Stephanie Lizy-Destrez, Nicole Viola
- Context: ICAPS 2021 KEPS Workshop
- Link: https://hal.science/hal-03434905/document

That paper explains the core idea behind HIST: mapping MBSE functional analysis concepts to HDDL constructs such as tasks, methods, actions, predicates, and objects.

### 2. Broader ConOps Validation Framework

The broader operational motivation is developed in the 2023 Aerospace paper:

- `Simulating Operational Concepts for Autonomous Robotic Space Exploration Systems: A Framework for Early Design Validation`
- Authors: Jasmine Rimani, Nicole Viola, Stephanie Lizy-Destrez
- DOI: `10.3390/aerospace10050408`
- Link: https://www.mdpi.com/2226-4310/10/5/408

This paper explains why early operational validation matters for autonomous robotic missions and how MBSE can act as a knowledge base for downstream operational reasoning. The repository you are reading is closer to the translator side of that research program than to the later simulation framework itself.

### 3. PhD Thesis

For the larger methodological picture, see the PhD thesis:

- `Application of AI planning and MBSE to the Study and Optimization of ConOps for Autonomous Robotic Space Exploration Systems`
- Author: Jasmine Rimani
- Official handle: https://hdl.handle.net/11583/2979887
- ResearchGate mirror: https://www.researchgate.net/publication/395009030_Application_of_AI_planning_and_MBSE_to_the_Study_and_Optimization_of_ConOps_for_Autonomous_Robotic_Space_Exploration_Systems

## What HIST Does

Given a Papyrus-exported UML/XMI model and a YAML configuration, HIST currently supports:

- parsing selected MBSE model elements from Papyrus-exported `.uml` files;
- extracting types, predicates, tasks, methods, actions, and mission information from the model;
- generating an HDDL domain file;
- partially generating an HDDL problem file;
- writing a feedback log to help inspect discrepancies or modeling issues.

At a high level, the repository translates:

- high-level functions into HDDL tasks;
- decompositions and behavioral logic into HDDL methods;
- executable leaf functions into HDDL actions;
- model items, parameters, and state information into HDDL objects and predicates.

## Typical Workflow

This is the workflow the repository was designed for:

1. Model the system and its operational logic in Papyrus using agreed MBSE conventions.
2. Export the model as a `.uml` file.
3. Point the YAML configuration to the desired input model.
4. Run HIST to parse the model and generate HDDL artifacts.
5. Inspect the generated domain, problem, and feedback outputs before using them in a planner or a larger operational study.

The current default configuration uses the sample IGLUNA model stored in `examples/inputs/`.

## Expected Modeling Conventions

The translator assumes a Papyrus model organized around the package names configured in `config/configuration.yaml`, including:

- `ElementsHDDL`
- `DomainDefinition`
- `ProblemDefinition`
- `Feedback`

The current implementation also assumes a specific modeling style for:

- functional decomposition;
- activity-based method logic;
- predicate-like parameter node naming;
- mission-specific problem description.

Because of this, HIST should be read as a research prototype with a clear workflow rather than as a fully generic Papyrus-to-HDDL compiler.

## Project Structure

- `src/hist/`: main Python package
- `src/main.py`: legacy-compatible entry point
- `config/`: YAML configuration files
- `examples/inputs/`: example Papyrus UML inputs
- `examples/outputs/`: reference generated outputs
- `outputs/`: runtime output directory
- `tests/`: baseline tests for parsing and configuration handling

## Getting Started

Install the Python dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Run the legacy entry point:

```bash
python3 src/main.py
```

Or run the package entry point from the repository root:

```bash
PYTHONPATH=src python3 -m hist
```

You can also override the paths explicitly:

```bash
PYTHONPATH=src python3 -m hist \
  --config config/configuration.yaml \
  --input-dir examples/inputs \
  --output-dir outputs
```

## Current Status

- The domain-generation path is the most mature part of the prototype.
- Problem generation is partial and still includes research-specific assumptions.
- The feedback path exists, but the detailed feedback module is not yet a polished end-user feature.
- The repository is currently being cleaned up and refactored into a more standard Python project structure.

## Who May Find This Useful

This repository may be useful if you work on:

- Model-Based Systems Engineering (MBSE)
- SysML and Papyrus modeling
- HDDL and hierarchical AI planning
- knowledge engineering for planning and scheduling
- autonomous robotic space exploration
- Concept of Operations (ConOps) analysis
- mission design and early operational validation

## Citation

If you use HIST in research, please cite the papers above and reference this repository as the software artifact used for Papyrus SysML / MBSE to HDDL translation.

## Keywords

Model-Based Systems Engineering, MBSE, SysML, Papyrus, HDDL, hierarchical planning, HTN planning, AI planning, knowledge engineering, ConOps, OpsCon, autonomous systems, space robotics, rover operations, mission design, preliminary design validation.

## Tags

#MBSE #SysML #Papyrus #HDDL #AIPlanning #HTNPlanning #KnowledgeEngineering #ConOps #OpsCon #SpaceRobotics #AutonomousSystems #MissionDesign

## License

This work is distributed under the MIT License. See `LICENSE.md`.
