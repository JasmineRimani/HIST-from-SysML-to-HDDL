import pytest

from hist.cli import run_translation


def test_run_translation_fails_fast_when_input_file_is_missing(tmp_path):
    config_path = tmp_path / "configuration.yaml"
    input_dir = tmp_path / "inputs"
    output_dir = tmp_path / "outputs"
    input_dir.mkdir()

    config_path.write_text(
        """
        file_name: missing.uml
        domain_name: rover_domain
        feedback_file_name: rover_feedback
        generate_problem_file: "yes"
        generate_domain_file: "no"
        generate_feedback: "no"
        domain_requirements:
          - typing
        task_parameters: common
        """,
        encoding="utf-8",
    )

    with pytest.raises(FileNotFoundError, match="Could not find the Papyrus UML input"):
        run_translation(config_path=config_path, input_dir=input_dir, output_dir=output_dir)
