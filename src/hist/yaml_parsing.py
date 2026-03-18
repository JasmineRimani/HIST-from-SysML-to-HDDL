# -*- coding: utf-8 -*-
"""Legacy-compatible YAML parsing helpers for HIST."""

from __future__ import annotations

import yaml

from .config import HistConfig, load_config_from_mapping


class YAML_parsing:
    """Compatibility wrapper around the validated ``HistConfig`` loader."""

    def __init__(self, file, debug='on'):
        """Parse YAML text and expose the legacy helper interface."""

        self.file = file
        self.debug = debug
        self.input_dictionary = yaml.safe_load(self.file) or {}
        self.config: HistConfig = load_config_from_mapping(self.input_dictionary)
        if self.debug == 'on':
            for key, value in self.input_dictionary.items():
                print(key + " : " + str(value))

    def file_names(self):
        """Return the configured input, domain, and feedback file names."""

        return (
            self.config.file_name,
            self.config.domain_name,
            self.config.feedback_file_name,
        )

    def main_flags(self):
        """Return the legacy main yes/no flags and domain requirements."""

        return (
            self.config.legacy_generate_problem_file,
            self.config.legacy_generate_domain_file,
            self.config.legacy_generate_feedback,
            list(self.config.domain_requirements),
        )

    def other_flags(self):
        """Return the legacy auxiliary flags for ordering and task handling."""

        return (
            self.config.legacy_method_precondition_from_action,
            self.config.legacy_flag_ordering,
            self.config.task_parameters,
        )

    def package_names(self):
        """Return the configured Papyrus package names."""

        return (
            self.config.packages.hddl,
            self.config.packages.domain,
            self.config.packages.problem,
            self.config.packages.feedback,
        )

    # Legacy method names retained for backward compatibility with the original code.
    def YAML_fileNames(self):
        """Backward-compatible alias for :meth:`file_names`."""

        return self.file_names()

    def YAML_mainFlags(self):
        """Backward-compatible alias for :meth:`main_flags`."""

        return self.main_flags()

    def YAML_otherFlags(self):
        """Backward-compatible alias for :meth:`other_flags`."""

        return self.other_flags()

    def YAML_PackagesNames(self):
        """Backward-compatible alias for :meth:`package_names`."""

        return self.package_names()
