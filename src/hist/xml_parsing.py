"""Papyrus UML/XMI parsing helpers for HIST."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .errors import DependencyError, MissingModelPackageError, ModelValidationError


@dataclass(frozen=True)
class ParsedModel:
    sysml_data: Any
    domain_dictionary: dict[str, Any]
    missions: list[dict[str, Any]]


class XML_parsing:
    """Legacy-compatible XML parser for Papyrus-exported UML models."""

    def __init__(self, file, package_HDDL, package_domain, package_problem, d_now=None, debug='on'):
        self.file = file
        self.debug = debug
        self.d_now = d_now
        self.package_HDDL = package_HDDL
        self.package_domain = package_domain
        self.package_problem = package_problem

    def _load_parser(self):
        try:
            from bs4 import BeautifulSoup
        except ImportError as exc:
            raise DependencyError(
                "beautifulsoup4 is required to parse Papyrus UML/XMI files. "
                "Install it with 'python3 -m pip install -r requirements.txt'."
            ) from exc

        return BeautifulSoup

    def _get_required_package(self, sysml_data, package_name):
        package = sysml_data.find(attrs={"name": package_name})
        if package is None:
            raise MissingModelPackageError(package_name)
        return package

    def _extract_domain_dictionary(self, domain_elements):
        domain_types = domain_elements.find_all('packagedElement', attrs={"xmi:type": "uml:Class"})
        if not any(item.get("name") == "predicate" for item in domain_types):
            raise ModelValidationError(
                "The domain package does not define the expected 'predicate' class."
            )

        nodes = (
            domain_elements.find_all('node', attrs={"xmi:type": "uml:ActivityParameterNode"})
            + domain_elements.find_all('node', attrs={"xmi:type": "uml:CentralBufferNode"})
        )
        domain_predicates = [x for x in nodes if len(x["name"].split()) != 1]
        task_elements = domain_elements.find_all('packagedElement', attrs={"xmi:type": "uml:UseCase"})
        task_parameters = domain_elements.find_all('ownedRule', attrs={"xmi:type": "uml:Constraint"})
        methods_elements = domain_elements.find_all('ownedUseCase', attrs={"xmi:type": "uml:UseCase"})
        actions_elements = domain_elements.find_all('node', attrs={"xmi:type": "uml:OpaqueAction"})
        action_parameters = domain_elements.find_all('edge')

        return {
            'types': domain_types,
            'predicates': domain_predicates,
            'tasks': task_elements,
            'tasks_param': task_parameters,
            'methods': methods_elements,
            'actions': actions_elements,
            'action_param': action_parameters,
        }

    def _extract_missions(self, problem_elements):
        problem_files_definition = problem_elements.find(
            'packagedElement',
            attrs={"xmi:type": "uml:Package", "name": "ProblemFilesDefinition"},
        )
        if problem_files_definition is None:
            return []

        missions = problem_files_definition.find_all(
            'packagedElement',
            attrs={"xmi:type": "uml:Package"},
            recursive=False,
        )

        missions_vector = []
        for mission in missions:
            temp_dict = {'name': mission["name"]}

            temp_initi_cond = mission.find_all(attrs={"xmi:type": "uml:Constraint"})
            temp_dict['initial_conditions'] = [cond["name"] for cond in temp_initi_cond]

            temp_task_network = None
            temp_map_file = None
            temp_comments = mission.find_all(attrs={"xmi:type": "uml:Comment"})
            for comment in temp_comments:
                body = comment.find("body")
                body_text = body.text if body is not None else ""
                if "Initial HTN" in body_text:
                    temp_task_network = body_text
                if "Map_file" in body_text:
                    temp_map_file = body_text

            temp_dict["init_HTN"] = temp_task_network
            temp_dict["map_File"] = temp_map_file

            temp_components = mission.find_all(attrs={"xmi:type": "uml:Class"})
            temp_components_list = []
            for component in temp_components:
                owned_attribute = component.find("ownedAttribute")
                if owned_attribute is None or not owned_attribute.has_attr("name"):
                    raise ModelValidationError(
                        "Mission object extraction expects each mission class to define an "
                        f"'ownedAttribute' with a name. Missing attribute in mission "
                        f"'{mission.get('name', '<unknown>')}', component '{component.get('name', '<unknown>')}'."
                    )
                temp_components_list.append(
                    "{}-{}".format(component["name"], owned_attribute["name"])
                )
            temp_dict["objects"] = temp_components_list
            missions_vector.append(temp_dict)

        return missions_vector

    def parse(self, require_domain: bool = True, require_problem: bool = True) -> ParsedModel:
        BeautifulSoup = self._load_parser()
        sysml_data = BeautifulSoup(self.file, "xml")

        # Keep validating the top-level HDDL package when any downstream package is required.
        if require_domain or require_problem:
            self._get_required_package(sysml_data, self.package_HDDL)

        domain_dictionary = {
            'types': [],
            'predicates': [],
            'tasks': [],
            'tasks_param': [],
            'methods': [],
            'actions': [],
            'action_param': [],
        }
        if require_domain:
            domain_elements = self._get_required_package(sysml_data, self.package_domain)
            domain_dictionary = self._extract_domain_dictionary(domain_elements)

        missions = []
        if require_problem:
            problem_elements = self._get_required_package(sysml_data, self.package_problem)
            missions = self._extract_missions(problem_elements)

        return ParsedModel(
            sysml_data=sysml_data,
            domain_dictionary=domain_dictionary,
            missions=missions,
        )

    def Parsing(self):
        parsed = self.parse()
        return parsed.sysml_data, parsed.domain_dictionary, parsed.missions
