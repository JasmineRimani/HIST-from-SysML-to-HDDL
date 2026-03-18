from pathlib import Path

from hist.yaml_parsing import YAML_parsing


def test_yaml_parsing_reads_project_config():
    config_path = Path(__file__).resolve().parents[1] / "config" / "configuration.yaml"
    parser = YAML_parsing(config_path.read_text(encoding="utf-8"), debug="off")

    file_name, domain_name, feedback_name = parser.YAML_fileNames()
    generate_problem_file, generate_domain_file, generate_feedback_file, domain_requirements = parser.YAML_mainFlags()
    method_precondition_from_action, flag_ordering_file, task_parameters = parser.YAML_otherFlags()
    package_hddl, package_domain, package_problem, package_feedback = parser.YAML_PackagesNames()

    assert file_name == "IGLUNA_model_sample_2.uml"
    assert domain_name == "Igluna_check"
    assert feedback_name == "IGLUNA_model_sample_1_feedback"
    assert generate_problem_file == "yes"
    assert generate_domain_file == "no"
    assert generate_feedback_file == "no"
    assert domain_requirements == ["typing", "hierachie"]
    assert method_precondition_from_action == "no"
    assert flag_ordering_file == "yes"
    assert task_parameters == "common"
    assert package_hddl == "ElementsHDDL"
    assert package_domain == "DomainDefinition"
    assert package_problem == "ProblemDefinition"
    assert package_feedback == "Feedback"
