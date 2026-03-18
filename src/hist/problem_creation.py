"""Problem-file generation utilities for HIST."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from .errors import UnsupportedFeatureError


class ProblemDefinition:
    """Generate HDDL problem files from parsed mission data."""

    def __init__(self, domain_name, SysML_data, missions, d_now=None, debug='on', output_dir=None):
        """Store the parsed mission data and output location for problem generation."""

        self.problem_name = datetime.now().strftime("%Y_%m_%d-%I_%M_%S") + '_' + domain_name + '_' + '_problem.hddl'
        self.domain_name = domain_name
        self.overall_data = SysML_data
        self.mission_dictionary = missions
        self.debug = debug
        self.d_now = Path(d_now) if d_now is not None else Path.cwd()
        self.output_dir = Path(output_dir) if output_dir is not None else self.d_now / 'outputs'
        self.log_file_general_entries = []

    def get_order(task):
        """Return the optional ordering key used by older code paths."""

        return task.get('order')

    def ProblemFileElements(self):
        """Initialize the legacy problem-generation log entries."""

        self.log_file_general_entries.append('------------------------------------------------- \n')
        self.log_file_general_entries.append('Log errors and warnings during the HDDL Problem file element acquisition: \n')
        self.log_file_general_entries.append('------------------------------------------------- \n')

    def _render_objects(self, mission):
        """Render the HDDL objects section for a mission."""

        lines = ["  (:objects"]
        for object_name in mission["objects"]:
            lines.append(f"    {object_name.lower()}")
        lines.append("  )")
        return "\n".join(lines)

    def _render_htn(self, mission):
        """Render the HDDL HTN section for a mission."""

        if mission["init_HTN"] is not None:
            raise UnsupportedFeatureError(
                "Problem-file generation for custom 'Initial HTN' comments is not implemented yet."
            )
        return "\n".join(
            [
                "  (:htn",
                "    :parameters ()",
                "    :subtasks ()",
                "    :ordering ()",
                "  )",
            ]
        )

    def _render_init(self, mission):
        """Render the initial conditions section for a mission."""

        if mission["map_File"] is not None:
            raise UnsupportedFeatureError(
                "Problem-file generation using external 'Map_file' comments is not implemented yet."
            )

        lines = ["  (:init"]
        for condition in mission["initial_conditions"]:
            lines.append(f"    {condition.lower()}")
        lines.append("  )")
        return "\n".join(lines)

    def build_problem_text(self, mission, index):
        """Build the full HDDL problem text for a single mission."""

        sections = [
            "(define",
            f"  (problem {mission['name'].lower()}_{index + 1})",
            f"  (:domain {self.domain_name.lower()})",
            self._render_objects(mission),
            self._render_htn(mission),
            self._render_init(mission),
            ")",
        ]
        return "\n".join(sections) + "\n"

    def write_problem_files(self):
        """Write one HDDL problem file per parsed mission."""

        self.output_dir.mkdir(parents=True, exist_ok=True)
        generated_files = []
        for index, mission in enumerate(self.mission_dictionary):
            output_path = self.output_dir / f'{mission["name"]}_problem.hddl'
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(self.build_problem_text(mission, index))
            generated_files.append(output_path)
        return generated_files

    # Legacy public method retained.
    def ProblemFileWriting(self):
        """Backward-compatible alias for :meth:`write_problem_files`."""

        return self.write_problem_files()
