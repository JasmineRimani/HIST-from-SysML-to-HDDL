from hist.domain_creation import Domain


def _build_domain(tmp_path, flag_ordering_file="yes", task_parameters="common"):
    return Domain(
        "rover_domain",
        SysML_data=None,
        domain_dictionary={
            "types": [],
            "predicates": [],
            "tasks": [],
            "tasks_param": [],
            "methods": [],
            "actions": [],
            "action_param": [],
        },
        domain_requirements=["typing", "hierarchy"],
        task_parameters=task_parameters,
        flag_ordering_file=flag_ordering_file,
        debug="off",
        output_dir=tmp_path,
    )


def _typed_param(name, type_name):
    return {"name": name, "type_name": type_name, "type": f"{type_name}_id"}


def _domain_definition_output():
    rover = _typed_param("rover", "rover")
    task = {"name": "survey", "xmi:id": "task-1", "parameters": [rover]}
    action = {
        "xmi:id": "action-1",
        "name": "move",
        "parameters": [rover],
        "preconditions": [{"name": "(available ?rover)"}],
        "effects": [{"name": "(visited ?rover)"}],
    }
    method = {
        "method": {"name": "survey_method"},
        "task": {"xmi:id": "task-1"},
        "parameters": [rover],
        "input_predicates": [{"name": "(available ?rover)"}],
        "actions_order": ["action-1"],
    }
    return {
        "hddl_type_list": [
            {"name": "predicate", "xmi:id": "predicate-id"},
            {"name": "rover", "xmi:id": "rover-id"},
        ],
        "predicate_list": ["available ?arg0-rover"],
        "task_list": [task],
        "method_list": [method],
        "final_action_list": [action],
        "behavioral_actions_list": [],
    }


def test_assign_param_returns_flat_list_for_single_candidate(tmp_path):
    domain = _build_domain(tmp_path)
    candidate = [[_typed_param("rover", "rover")]]

    selected, flag = domain.assign_param(candidate)

    assert selected == candidate[0]
    assert flag == 1


def test_assign_param_prefers_repeated_signature(tmp_path):
    domain = _build_domain(tmp_path)
    repeated = [_typed_param("rover", "rover")]
    alternate = [_typed_param("camera", "camera")]

    selected, flag = domain.assign_param([repeated, alternate, repeated])

    assert selected == repeated
    assert flag == 0


def test_intersect_parameter_lists_preserves_first_list_order(tmp_path):
    domain = _build_domain(tmp_path)
    first = [_typed_param("rover", "rover"), _typed_param("camera", "camera")]
    second = [_typed_param("camera", "camera"), _typed_param("rover", "rover")]
    third = [_typed_param("rover", "rover")]

    result = domain._intersect_parameter_lists([first, second, third])

    assert result == [_typed_param("rover", "rover")]


def test_domain_file_writing_renders_expected_sections(tmp_path):
    domain = _build_domain(tmp_path)
    domain_definition_output = _domain_definition_output()

    output_path = domain.DomainFileWriting(domain_definition_output)
    rendered = output_path.read_text(encoding="utf-8")

    assert "(define (domain" in rendered
    assert "(:requirements :typing :hierarchy)" in rendered
    assert "(:task survey" in rendered
    assert "(:method survey_method" in rendered
    assert ":subtasks (and" in rendered
    assert "task0(move ?rover - rover)" in rendered
    assert "(:action move" in rendered


def test_domain_file_writing_supports_ordered_subtasks_mode(tmp_path):
    domain = _build_domain(tmp_path, flag_ordering_file="no")

    rendered = domain.build_domain_text(_domain_definition_output())

    assert ":ordered-subtasks (and" in rendered
    assert ":subtasks (and" not in rendered
