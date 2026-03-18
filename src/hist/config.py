from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

import yaml

from .errors import ConfigurationError, NotDefinedRequirements


TRUE_VALUES = {"yes", "true", "1", "on"}
FALSE_VALUES = {"no", "false", "0", "off"}
TASK_PARAMETER_MODES = {"common", "min"}


@dataclass(frozen=True)
class PackageNames:
    hddl: str = "ElementsHDDL"
    domain: str = "DomainDefinition"
    problem: str = "ProblemDefinition"
    feedback: str = "Feedback"


@dataclass(frozen=True)
class HistConfig:
    file_name: str
    domain_name: str
    feedback_file_name: str
    additional_files: tuple[str, ...]
    generate_problem_file: bool
    generate_domain_file: bool
    generate_feedback: bool
    domain_requirements: tuple[str, ...]
    method_precondition_from_action: bool
    use_ordering: bool
    task_parameters: str
    packages: PackageNames

    @property
    def legacy_generate_problem_file(self) -> str:
        return "yes" if self.generate_problem_file else "no"

    @property
    def legacy_generate_domain_file(self) -> str:
        return "yes" if self.generate_domain_file else "no"

    @property
    def legacy_generate_feedback(self) -> str:
        return "yes" if self.generate_feedback else "no"

    @property
    def legacy_method_precondition_from_action(self) -> str:
        return "yes" if self.method_precondition_from_action else "no"

    @property
    def legacy_flag_ordering(self) -> str:
        return "yes" if self.use_ordering else "no"


def _coerce_mapping(data: Any) -> Mapping[str, Any]:
    if not isinstance(data, Mapping):
        raise ConfigurationError("The YAML configuration must define a mapping at the top level.")
    return data


def _coerce_string(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ConfigurationError(f"'{field_name}' must be a non-empty string.")
    return value.strip()


def _coerce_string_sequence(value: Any, field_name: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, list):
        raise ConfigurationError(f"'{field_name}' must be a list of strings.")
    normalized = []
    for item in value:
        normalized.append(_coerce_string(item, field_name))
    return tuple(normalized)


def _coerce_bool(value: Any, field_name: str, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in TRUE_VALUES:
            return True
        if lowered in FALSE_VALUES:
            return False
    raise ConfigurationError(
        f"'{field_name}' must be one of {sorted(TRUE_VALUES | FALSE_VALUES)} or a boolean."
    )


def load_config_from_mapping(data: Mapping[str, Any]) -> HistConfig:
    data = _coerce_mapping(data)

    file_name = _coerce_string(data.get("file_name"), "file_name")
    domain_name = _coerce_string(data.get("domain_name", f"domain_{file_name}"), "domain_name")
    feedback_file_name = _coerce_string(
        data.get("feedback_file_name", f"feedback_{file_name}"),
        "feedback_file_name",
    )

    if "domain_requirements" not in data:
        raise NotDefinedRequirements

    domain_requirements = _coerce_string_sequence(data.get("domain_requirements"), "domain_requirements")
    if not domain_requirements:
        raise NotDefinedRequirements

    task_parameters = _coerce_string(data.get("task_parameters", "common"), "task_parameters").lower()
    if task_parameters not in TASK_PARAMETER_MODES:
        raise ConfigurationError(
            f"'task_parameters' must be one of {sorted(TASK_PARAMETER_MODES)}."
        )

    packages = PackageNames(
        hddl=_coerce_string(data.get("package_HDDL", "ElementsHDDL"), "package_HDDL"),
        domain=_coerce_string(data.get("package_domain", "DomainDefinition"), "package_domain"),
        problem=_coerce_string(data.get("package_problem", "ProblemDefinition"), "package_problem"),
        feedback=_coerce_string(data.get("package_feedback", "Feedback"), "package_feedback"),
    )

    return HistConfig(
        file_name=file_name,
        domain_name=domain_name,
        feedback_file_name=feedback_file_name,
        additional_files=_coerce_string_sequence(data.get("additional_files"), "additional_files"),
        generate_problem_file=_coerce_bool(data.get("generate_problem_file"), "generate_problem_file", False),
        generate_domain_file=_coerce_bool(data.get("generate_domain_file"), "generate_domain_file", False),
        generate_feedback=_coerce_bool(data.get("generate_feedback"), "generate_feedback", False),
        domain_requirements=domain_requirements,
        method_precondition_from_action=_coerce_bool(
            data.get("method_precondition_from_action"),
            "method_precondition_from_action",
            True,
        ),
        use_ordering=_coerce_bool(data.get("flag_ordering"), "flag_ordering", True),
        task_parameters=task_parameters,
        packages=packages,
    )


def load_config_from_text(text: str) -> HistConfig:
    return load_config_from_mapping(yaml.safe_load(text) or {})


def load_config(config_path: str | Path) -> HistConfig:
    config_path = Path(config_path)
    return load_config_from_text(config_path.read_text(encoding="utf-8"))
