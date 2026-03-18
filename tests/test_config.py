from pathlib import Path

import pytest

from hist.config import load_config, load_config_from_mapping, load_config_from_text
from hist.errors import ConfigurationError, NotDefinedRequirements


def test_load_config_normalizes_supported_values():
    config = load_config_from_mapping(
        {
            "file_name": "model.uml",
            "domain_name": "rover_domain",
            "feedback_file_name": "feedback.log",
            "additional_files": ["map.txt"],
            "generate_problem_file": "YES",
            "generate_domain_file": False,
            "generate_feedback": "off",
            "domain_requirements": ["typing", "hierarchy"],
            "method_precondition_from_action": "0",
            "flag_ordering": "true",
            "task_parameters": "MIN",
            "package_HDDL": "HDDLPackage",
            "package_domain": "DomainPackage",
            "package_problem": "ProblemPackage",
            "package_feedback": "FeedbackPackage",
        }
    )

    assert config.file_name == "model.uml"
    assert config.additional_files == ("map.txt",)
    assert config.generate_problem_file is True
    assert config.generate_domain_file is False
    assert config.generate_feedback is False
    assert config.method_precondition_from_action is False
    assert config.use_ordering is True
    assert config.task_parameters == "min"
    assert config.packages.hddl == "HDDLPackage"
    assert config.legacy_generate_problem_file == "yes"
    assert config.legacy_flag_ordering == "yes"


def test_load_config_requires_domain_requirements():
    with pytest.raises(NotDefinedRequirements):
        load_config_from_text(
            """
            file_name: model.uml
            domain_name: rover_domain
            feedback_file_name: feedback.log
            """
        )


def test_load_config_rejects_invalid_task_parameter_mode(tmp_path: Path):
    config_path = tmp_path / "configuration.yaml"
    config_path.write_text(
        """
        file_name: model.uml
        domain_name: rover_domain
        feedback_file_name: feedback.log
        generate_problem_file: "yes"
        domain_requirements:
          - typing
        task_parameters: all
        """,
        encoding="utf-8",
    )

    with pytest.raises(ConfigurationError, match="task_parameters"):
        load_config(config_path)
