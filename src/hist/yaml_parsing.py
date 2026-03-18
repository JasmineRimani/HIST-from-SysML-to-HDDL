# -*- coding: utf-8 -*-
"""Legacy-compatible YAML parsing helpers for HIST."""

from __future__ import annotations

import yaml

from .config import HistConfig, load_config_from_mapping


class YAML_parsing:
    """Compatibility wrapper around the validated ``HistConfig`` loader."""

    def __init__(self, file, debug='on'):
        self.file = file
        self.debug = debug
        self.input_dictionary = yaml.safe_load(self.file) or {}
        self.config: HistConfig = load_config_from_mapping(self.input_dictionary)
        if self.debug == 'on':
            for key, value in self.input_dictionary.items():
                print(key + " : " + str(value))

    def file_names(self):
        return (
            self.config.file_name,
            self.config.domain_name,
            self.config.feedback_file_name,
        )

    def main_flags(self):
        return (
            self.config.legacy_generate_problem_file,
            self.config.legacy_generate_domain_file,
            self.config.legacy_generate_feedback,
            list(self.config.domain_requirements),
        )

    def other_flags(self):
        return (
            self.config.legacy_method_precondition_from_action,
            self.config.legacy_flag_ordering,
            self.config.task_parameters,
        )

    def package_names(self):
        return (
            self.config.packages.hddl,
            self.config.packages.domain,
            self.config.packages.problem,
            self.config.packages.feedback,
        )

    # Legacy method names retained for backward compatibility with the original code.
    def YAML_fileNames(self):
        return self.file_names()

    def YAML_mainFlags(self):
        return self.main_flags()

    def YAML_otherFlags(self):
        return self.other_flags()

    def YAML_PackagesNames(self):
        return self.package_names()
