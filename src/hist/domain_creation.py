# -*- coding: utf-8 -*-
"""Domain-file generation utilities for HIST."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import uuid

from .errors import ModelValidationError


class Domain:
    """Generate HDDL domain content from parsed Papyrus domain data."""

    def __init__(
        self,
        domain_name,
        SysML_data,
        domain_dictionary,
        domain_requirements,
        task_parameters='common',
        flag_ordering_file='yes',
        method_precondition_from_action='yes',
        d_now=None,
        debug='on',
        output_dir=None,
    ):
        """Store the parsed domain data and rendering options."""

        self.domain_name = datetime.now().strftime("%Y_%m_%d-%I_%M_%S") + '_' + domain_name + '_' + '_domain.hddl'
        self.overall_data = SysML_data
        self.domain_dictionary = domain_dictionary
        self.domain_requirements = domain_requirements
        self.log_file_general_entries = []
        self.debug = debug
        self.d_now = Path(d_now) if d_now is not None else Path.cwd()
        self.output_dir = Path(output_dir) if output_dir is not None else self.d_now / 'outputs'
        self.task_parameters = task_parameters
        self.flag_ordering_file = flag_ordering_file
        self.method_precondition_from_action = method_precondition_from_action

    def get_order(task):
        """Return the optional ordering key used by older code paths."""

        return task.get('order')

    def Diff(li1, li2):
        """Return the symmetric difference between two lists."""

        li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
        return li_dif

    def _warn(self, message):
        """Record a warning and optionally print it in debug mode."""

        self.log_file_general_entries.append(message + '\n')
        if self.debug == 'on':
            print(message)

    def _intersect_parameter_lists(self, parameter_lists):
        """Return parameters shared by all candidate parameter lists."""

        if not parameter_lists:
            return []

        common_keys = {
            (param["name"], param.get("type_name"), param.get("type"))
            for param in parameter_lists[0]
        }
        for parameters in parameter_lists[1:]:
            current_keys = {
                (param["name"], param.get("type_name"), param.get("type"))
                for param in parameters
            }
            common_keys &= current_keys

        ordered_parameters = []
        for param in parameter_lists[0]:
            key = (param["name"], param.get("type_name"), param.get("type"))
            if key in common_keys:
                ordered_parameters.append(param)
        return ordered_parameters

    def _infer_parameter_type(self, param, hddl_types):
        """Populate a parameter type from existing types or create a new one."""

        if "type_name" in param:
            return

        if "type" in param:
            for hddl_type in hddl_types:
                if hddl_type["xmi:id"] == param["type"]:
                    param["type_name"] = hddl_type['name']
                    return

        normalized_name = ''.join([character for character in param['name'] if not character.isdigit()])
        for hddl_type in hddl_types:
            if hddl_type['name'] == normalized_name:
                param['type'] = hddl_type['xmi:id']
                param["type_name"] = hddl_type['name']
                return

        type_id = str(uuid.uuid1())
        param['type'] = type_id
        param["type_name"] = param['name']
        hddl_types.append({"name": param['name'], "xmi:id": type_id})
        self._warn('\t\t No predefined type for {}. We added as its own type '.format(param['name']))

    def _collect_hddl_types(self):
        """Collect HDDL type dictionaries from the parsed domain package."""

        return [hddl_type.attrs for hddl_type in self.domain_dictionary['types']]

    def _collect_tasks(self):
        """Collect task dictionaries and attach their owned behaviors."""

        tasks_domain = []
        for task in self.domain_dictionary['tasks']:
            task_data = task.attrs
            for behavior in task.find_all('ownedBehavior'):
                task_data["behavior"] = behavior.attrs
            tasks_domain.append(task_data)
        return tasks_domain

    def _collect_task_parameters(self):
        """Collect task parameter constraints from the parsed domain package."""

        return [parameter.attrs for parameter in self.domain_dictionary['tasks_param']]

    def _build_method_parameters(self, parameter_nodes, hddl_types):
        """Build normalized method parameter dictionaries from XML nodes."""

        parameters = []
        for param in parameter_nodes:
            if not param.has_attr("type"):
                self._infer_parameter_type(param.attrs, hddl_types)
            else:
                self._infer_parameter_type(param.attrs, hddl_types)

            param_data = param.attrs
            if "type_name" not in param_data:
                raise ModelValidationError(
                    f"Could not infer a type for method parameter '{param.get('name', '<unknown>')}'."
                )
            parameters.append(param_data)
        return parameters

    def _extract_actions(self, method):
        """Extract opaque and behavioral actions from a method node."""

        actions = []
        opaque_actions = method.find_all('node', attrs={"xmi:type": "uml:OpaqueAction"})
        behavioral_actions = method.find_all('node', attrs={"xmi:type": "uml:CallBehaviorAction"})

        for action in opaque_actions:
            action_data = action.attrs
            action_data["inputs"] = action.find_all('inputValue')
            action_data["outputs"] = action.find_all('outputValue')
            actions.append(action_data)

        for action in behavioral_actions:
            action_data = action.attrs
            action_data["inputs"] = action.find_all('argument', attrs={"xmi:type": "uml:InputPin"})
            action_data["outputs"] = action.find_all('argument', attrs={"xmi:type": "uml:OutputPin"})
            actions.append(action_data)

        return actions

    def _extract_method_predicates(self, predicate_nodes):
        """Split predicate nodes into method inputs and outputs."""

        input_predicates = []
        output_predicates = []
        for predicate in predicate_nodes:
            if predicate.has_attr('incoming'):
                output_predicates.append(predicate.attrs)
            if predicate.has_attr('outgoing'):
                input_predicates.append(predicate.attrs)
        return input_predicates, output_predicates

    def _infer_actions_order(self, actions, edges):
        """Infer a linear subtask order from control-flow edges."""

        actions_order = []
        actions_partial_order = []
        for edge in edges:
            for action in actions:
                if edge["target"] == action["xmi:id"]:
                    for previous_action in actions:
                        if edge["source"] == previous_action["xmi:id"]:
                            actions_partial_order.append([previous_action["xmi:id"], action["xmi:id"]])

        for index, partial_order in enumerate(actions_partial_order):
            for next_partial_order in actions_partial_order[index::]:
                if partial_order[-1] == next_partial_order[0]:
                    index_next = actions_partial_order.index(next_partial_order)
                    new_index = actions_partial_order.index(partial_order)
                    actions_partial_order.pop(index_next)
                    actions_partial_order.insert(new_index + 1, next_partial_order)

        for partial_order in actions_partial_order:
            for element in partial_order:
                if element not in actions_order:
                    actions_order.append(element)
        return actions_order

    def _build_method_dictionary(self, method, hddl_types):
        """Build the normalized representation used for one HDDL method."""

        method_data = {"method": method.attrs}
        nodes = (
            method.find_all('node', attrs={"xmi:type": "uml:ActivityParameterNode"})
            + method.find_all('node', attrs={"xmi:type": "uml:CentralBufferNode"})
        )
        parameter_nodes = [node for node in nodes if len(node["name"].split()) == 1]
        predicate_nodes = [node for node in nodes if len(node["name"].split()) != 1]

        method_data["parameters"] = self._build_method_parameters(parameter_nodes, hddl_types)
        method_data["task"] = method.parent.attrs
        method_data["actions"] = self._extract_actions(method)
        input_predicates, output_predicates = self._extract_method_predicates(predicate_nodes)
        method_data["input_predicates"] = input_predicates
        method_data["output_predicates"] = output_predicates
        method_data["edges"] = [edge.attrs for edge in method.find_all('edge')]
        method_data["actions_order"] = self._infer_actions_order(method_data["actions"], method_data["edges"])
        return method_data

    def _collect_methods(self, hddl_types):
        """Collect and normalize all methods from the parsed domain package."""

        methods_list = []
        for method in self.domain_dictionary['methods']:
            methods_list.append(self._build_method_dictionary(method, hddl_types))
        return methods_list

    def _build_predicate_list(self, methods_list):
        """Build the HDDL predicate signatures referenced by the methods."""

        final_predicate_list = []
        for predicate_object in self.domain_dictionary['predicates']:
            predicate = predicate_object["name"]
            cleaned_predicate = predicate.replace('(', ' ')
            cleaned_predicate = cleaned_predicate.replace(')', ' ')
            cleaned_predicate = cleaned_predicate.replace('not', ' ')
            cleaned_predicate = cleaned_predicate.replace('_copy', ' ')
            cleaned_predicate = cleaned_predicate.split()
            temporary_predicate = [cleaned_predicate[0]]

            for index_predicate, predicate_atom in enumerate(cleaned_predicate[1::]):
                predicate_atom = predicate_atom.replace('?', ' ').strip()
                for method in methods_list:
                    for method_type in method["parameters"]:
                        if predicate_atom == method_type['name']:
                            predicate_input = '?arg{}-{}'.format(index_predicate, method_type['type_name'])
                            if predicate_input not in temporary_predicate:
                                temporary_predicate.append(predicate_input)

            if len(temporary_predicate) <= 1:
                self._warn(
                    't\t The {} is not used in any method, therefore it is not in the final domain file '.format(
                        predicate
                    )
                )
                continue

            final_predicate = ' '.join(temporary_predicate)
            if final_predicate not in final_predicate_list and '=' not in final_predicate:
                final_predicate_list.append(final_predicate)

        return final_predicate_list

    def _build_opaque_actions(self, methods_list):
        """Build normalized opaque actions with parameters and predicates."""

        final_action_list = []
        for method in methods_list:
            for action in method['actions']:
                if action["xmi:type"] != "uml:OpaqueAction":
                    continue

                action_parameters = []
                action_preconditions = []
                action_postconditions = []
                for edge in method["edges"]:
                    for input_value in action["inputs"]:
                        if edge["target"] == input_value["xmi:id"]:
                            for param in method["parameters"]:
                                if edge["source"] == param["xmi:id"]:
                                    action_parameters.append(param)
                            for input_predicate in method["input_predicates"]:
                                if edge["source"] == input_predicate["xmi:id"]:
                                    action_preconditions.append(input_predicate)

                    for output_value in action["outputs"]:
                        if "source" in edge and edge["source"] == output_value["xmi:id"]:
                            for output_predicate in method["output_predicates"]:
                                if edge["target"] == output_predicate["xmi:id"]:
                                    action_postconditions.append(output_predicate)

                action["parameters"] = action_parameters
                action["preconditions"] = action_preconditions
                action["effects"] = action_postconditions
                final_action_list.append(action)
        return final_action_list

    def _build_behavioral_actions(self, methods_list):
        """Build normalized behavioral subtasks referenced by methods."""

        behavioral_actions = []
        for method in methods_list:
            for action in method['actions']:
                if action["xmi:type"] != "uml:CallBehaviorAction":
                    continue

                action_parameters = []
                action_predicates = []
                for edge in method["edges"]:
                    for input_value in action["inputs"]:
                        if edge["target"] == input_value["xmi:id"]:
                            for param in method["parameters"]:
                                if edge["source"] == param["xmi:id"]:
                                    action_parameters.append(param)
                            for input_predicate in method["input_predicates"]:
                                if "source" in edge and edge["source"] == input_predicate["xmi:id"]:
                                    self._warn(
                                        't\t The {} is a task with precondition. Check if this is intended or not!'.format(
                                            action["name"]
                                        )
                                    )
                                    action_predicates.append(input_predicate)

                action["parameters"] = action_parameters
                action["predicate"] = action_predicates
                behavioral_actions.append(action)

        return behavioral_actions

    def _assign_task_parameters_from_behavior(self, task, behavioral_actions):
        """Infer task parameters from behavioral action calls when available."""

        candidate_parameters = []
        for action in behavioral_actions:
            if action["behavior"] == task["behavior"]["xmi:id"] and "parameters" in action:
                candidate_parameters.append(action["parameters"])

        if candidate_parameters:
            task["parameters"], flag = self.assign_param(candidate_parameters)
            if flag == 1:
                names = [parameter["name"] for parameter in task["parameters"]]
                self._warn(
                    "\t\t {} has {} as parameters - please check if that is the desired outcome ".format(
                        task['name'],
                        names,
                    )
                )

    def _assign_task_parameters_from_constraints(self, task, task_parameters, hddl_types):
        """Infer task parameters from explicit SysML constraint definitions."""

        if "parameters" in task:
            return

        collected_parameters = []
        for param in task_parameters:
            constrained_elements = param.get("constrainedElement", "").split()
            if task["xmi:id"] not in constrained_elements:
                continue

            self._infer_parameter_type(param, hddl_types)
            collected_parameters.append(param)

        if collected_parameters:
            task["parameters"] = collected_parameters

    def _assign_task_parameters_from_methods(self, task, methods_list):
        """Infer task parameters from related methods when no explicit data exists."""

        if "parameters" in task:
            return

        task_parameter_matrix = []
        for method in methods_list:
            if task["xmi:id"] == method["task"]["xmi:id"]:
                task_parameter_matrix.append(method.get("parameters", []))

        if self.task_parameters == 'min':
            task["parameters"] = min(task_parameter_matrix, key=len) if task_parameter_matrix else []
        else:
            task["parameters"] = self._intersect_parameter_lists(task_parameter_matrix)

    def _resolve_task_parameters(self, tasks_domain, behavioral_actions, task_parameters, hddl_types, methods_list):
        """Apply the task-parameter inference strategy to every task."""

        for task in tasks_domain:
            self._assign_task_parameters_from_behavior(task, behavioral_actions)
            self._assign_task_parameters_from_constraints(task, task_parameters, hddl_types)
            self._assign_task_parameters_from_methods(task, methods_list)

    def DomainFileElements(self):
        """Build the normalized domain structure used for HDDL rendering."""

        self.log_file_general_entries.append('------------------------------------------------- \n')
        self.log_file_general_entries.append('Log errors and warnings during the HDDL Domain file element acquisition: \n')
        self.log_file_general_entries.append('------------------------------------------------- \n')

        hddl_types = self._collect_hddl_types()
        tasks_domain = self._collect_tasks()
        task_parameters = self._collect_task_parameters()
        methods_list = self._collect_methods(hddl_types)
        final_predicate_list = self._build_predicate_list(methods_list)
        final_action_list = self._build_opaque_actions(methods_list)
        behavioral_actions_list = self._build_behavioral_actions(methods_list)
        self._resolve_task_parameters(tasks_domain, behavioral_actions_list, task_parameters, hddl_types, methods_list)

        domain_definition_output = {
            "domain_name": self.domain_name,
            "hddl_type_list": hddl_types,
            "predicate_list": final_predicate_list,
            "task_list": tasks_domain,
            "method_list": methods_list,
            "final_action_list": final_action_list,
            "behavioral_actions_list": behavioral_actions_list,
        }
        return domain_definition_output, self.log_file_general_entries

    def assign_param(self, tmp_parameters):
        """Choose the most representative parameter list for a task."""

        param_names = []
        for params in tmp_parameters:
            param_names.append([param["name"] for param in params])

        if len(param_names) == 1:
            return tmp_parameters[0], 1

        repeated_indexes = [index for index, names in enumerate(param_names) if param_names.count(names) > 1]
        if repeated_indexes:
            return tmp_parameters[repeated_indexes[0]], 0

        return tmp_parameters[-1], 1

    def _format_typed_parameters(self, parameters):
        """Format typed parameters in HDDL syntax."""

        return " ".join(
            "?{} - {}".format(param["name"].lower(), param["type_name"].lower())
            for param in parameters
        )

    def _render_types_section(self, hddl_type_list):
        """Render the HDDL ``:types`` section."""

        lines = ['\t (:types  ']
        for hddl_type in hddl_type_list:
            if hddl_type["name"].strip() == 'predicate':
                continue
            if "parent" in hddl_type:
                lines.append('\n\t\t{} - {} '.format(hddl_type["name"].lower(), hddl_type["parent"]))
            else:
                lines.append('\n\t\t{} - object '.format(hddl_type["name"].lower()))
        lines.append(') \n\n')
        return "".join(lines)

    def _render_predicates_section(self, predicates):
        """Render the HDDL ``:predicates`` section."""

        lines = ['\t (:predicates \n']
        for predicate in predicates:
            lines.append('\t\t ({}) \n'.format(predicate).lower())
        lines.append('\t) \n\n')
        return "".join(lines)

    def _render_tasks_section(self, tasks):
        """Render the HDDL task declarations."""

        lines = []
        for task in tasks:
            lines.append('\t (:task {} \n'.format(task["name"]))
            lines.append('\t\t :parameters ({}) \n'.format(self._format_typed_parameters(task["parameters"])))
            lines.append('\t\t :precondition ()\n')
            lines.append('\t\t :effect ()\n')
            lines.append('\t ) \n\n')
        return "".join(lines)

    def _lookup_task_signature(self, task_list, task_id):
        """Return the task name and typed parameters for a method reference."""

        for task in task_list:
            if task['xmi:id'] == task_id:
                return task['name'], self._format_typed_parameters(task["parameters"])
        raise ModelValidationError("Could not find the task referenced by a method while rendering the domain file.")

    def _lookup_subtask_definition(self, action_id, domain_definition_output):
        """Resolve a subtask id to its rendered action or task signature."""

        for opaque_action in domain_definition_output["final_action_list"]:
            if action_id == opaque_action["xmi:id"]:
                return opaque_action['name'], self._format_typed_parameters(opaque_action["parameters"])
        for behavioral_action in domain_definition_output["behavioral_actions_list"]:
            if action_id == behavioral_action["xmi:id"]:
                return behavioral_action['name'], self._format_typed_parameters(behavioral_action["parameters"])
        raise ModelValidationError(
            "Could not match a method subtask to either an opaque action or a behavioral action "
            "while generating the HDDL domain file."
        )

    def _render_method_subtasks(self, method, domain_definition_output):
        """Render a method's subtasks and derived ordering constraints."""

        subtasks = []
        ordering = []
        for index, action_id in enumerate(method["actions_order"]):
            action_name, action_parameters = self._lookup_subtask_definition(action_id, domain_definition_output)
            if action_parameters:
                subtasks.append('task{}({} {})'.format(index, action_name, action_parameters))
            else:
                subtasks.append('task{}({})'.format(index, action_name))

            if index > 0:
                ordering_clause = '(< task{} task{})'.format(index - 1, index)
                if ordering_clause not in ordering:
                    ordering.append(ordering_clause)

        return subtasks, ordering

    def _render_methods_section(self, domain_definition_output):
        """Render the HDDL method declarations."""

        lines = ['\n']
        for method in domain_definition_output["method_list"]:
            lines.append('\t (:method {} \n'.format(method["method"]["name"].lower()))
            lines.append('\t\t :parameters ({}) \n'.format(self._format_typed_parameters(method["parameters"])))

            task_name, task_parameters = self._lookup_task_signature(
                domain_definition_output["task_list"],
                method['task']['xmi:id'],
            )
            lines.append('\t\t :task ({} {}) \n'.format(task_name, task_parameters.lower()))

            if method["input_predicates"]:
                predicates = [predicate["name"].lower() for predicate in method["input_predicates"]]
                lines.append('\t\t :precondition (and \n\t\t\t{} \n\t\t) \n'.format(' \n\t\t\t'.join(predicates)))
            else:
                lines.append('\t\t :precondition ()\n')

            subtasks, ordering = self._render_method_subtasks(method, domain_definition_output)
            if self.flag_ordering_file == 'yes':
                if len(subtasks) > 1:
                    lines.append('\t\t :subtasks (and \n')
                    lines.append('\t\t\t{}\n'.format('\n\t\t\t'.join(subtasks)))
                    lines.append('\t\t ) \n')
                    lines.append('\t\t :ordering (and \n')
                    lines.append('\t\t\t{}\n'.format(' \n\t\t\t'.join(ordering).lower()))
                    lines.append('\t\t ) \n')
                elif len(subtasks) == 1:
                    lines.append('\t\t :subtasks (and \n')
                    lines.append('\t\t\t {}\n'.format(' \n\t\t\t'.join(subtasks)))
                    lines.append('\t\t ) \n')
                else:
                    lines.append('\t\t :subtasks () \n')
            else:
                if len(subtasks) > 1:
                    lines.append('\t\t :ordered-subtasks (and \n')
                    lines.append('\t\t\t{}\n'.format('\n\t\t\t'.join(subtasks)))
                    lines.append('\t\t ) \n')
                elif len(subtasks) == 1:
                    lines.append('\t\t :ordered-subtasks (and \n')
                    lines.append('\t\t\t {}\n'.format(' \n\t\t\t'.join(subtasks)))
                    lines.append('\t\t ) \n')
                else:
                    lines.append('\t\t :ordered-subtasks () \n')

            lines.append('\t ) \n\n')
        return "".join(lines)

    def _render_actions_section(self, final_action_list):
        """Render the HDDL action declarations."""

        lines = ['\n']
        for action in final_action_list:
            lines.append('\t(:action {} \n'.format(action["name"].lower()))
            parameters = self._format_typed_parameters(action["parameters"])
            if parameters:
                lines.append('\t\t :parameters ({}) \n'.format(parameters))
            else:
                lines.append('\t\t :parameters () \n')

            if action["preconditions"]:
                predicates = [predicate["name"].lower() for predicate in action["preconditions"]]
                lines.append('\t\t :precondition (and \n\t\t\t{})\n'.format(' \n\t\t\t'.join(predicates)))
            else:
                lines.append('\t\t :precondition ()\n')

            if action["effects"]:
                effects = [effect["name"].lower() for effect in action["effects"]]
                lines.append('\t\t :effect (and \n\t\t\t{})\n'.format(' \n\t\t\t'.join(effects)))
            else:
                lines.append('\t\t :effect ()\n')

            lines.append('\t) \n\n')
        return "".join(lines)

    def build_domain_text(self, domain_definition_output):
        """Build the full HDDL domain file text."""

        sections = [
            '(define (domain {}) \n'.format(self.domain_name.lower()),
            '\t (:requirements :{}) \n'.format(' :'.join(self.domain_requirements).lower()),
            self._render_types_section(domain_definition_output["hddl_type_list"]),
            self._render_predicates_section(domain_definition_output["predicate_list"]),
            self._render_tasks_section(domain_definition_output["task_list"]),
            self._render_methods_section(domain_definition_output),
            self._render_actions_section(domain_definition_output["final_action_list"]),
            ')',
        ]
        return "".join(sections)

    def DomainFileWriting(self, domain_definition_output):
        """Write the rendered HDDL domain text to disk."""

        self.output_dir.mkdir(parents=True, exist_ok=True)
        output_path = self.output_dir / self.domain_name
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(self.build_domain_text(domain_definition_output))
        return output_path
