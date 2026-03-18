from __future__ import annotations

import argparse
from pathlib import Path

from .domain_creation import Domain
from .partial_feedback_definition import Simple_FeedbackDefinition
from .problem_creation import ProblemDefinition
from .xml_parsing import XML_parsing
from .yaml_parsing import YAML_parsing


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config" / "configuration.yaml"
DEFAULT_INPUT_DIR = PROJECT_ROOT / "examples" / "inputs"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "outputs"


def run_translation(
    config_path: Path | str = DEFAULT_CONFIG_PATH,
    input_dir: Path | str = DEFAULT_INPUT_DIR,
    output_dir: Path | str = DEFAULT_OUTPUT_DIR,
) -> dict[str, object]:
    config_path = Path(config_path)
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    configuration_file = config_path.read_text(encoding="utf-8")
    yaml_class = YAML_parsing(configuration_file, debug="off")

    file_papyrus, domain_name, feedback_name = yaml_class.YAML_fileNames()
    generate_problem_file, generate_domain_file, generate_feedback_file, domain_requirements = yaml_class.YAML_mainFlags()
    method_precondition_from_action, flag_ordering_file, task_parameters = yaml_class.YAML_otherFlags()
    package_hddl, package_domain, package_problem, _package_feedback = yaml_class.YAML_PackagesNames()

    papyrus_path = input_dir / file_papyrus
    data = papyrus_path.read_text(encoding="utf-8")

    print(f"Parsing input file: {papyrus_path.name}")
    initial_dictionary = XML_parsing(data, package_hddl, package_domain, package_problem, debug="off")
    sysml_data, domain_dictionary, missions = initial_dictionary.Parsing()

    generated_files: list[Path] = []

    if generate_domain_file == "yes":
        print("Generating domain file")
        domain_file = Domain(
            domain_name,
            sysml_data,
            domain_dictionary,
            domain_requirements,
            task_parameters,
            flag_ordering_file,
            method_precondition_from_action,
            d_now=PROJECT_ROOT,
            debug="off",
            output_dir=output_dir,
        )
        domain_file_elements, log_file_general_entries = domain_file.DomainFileElements()
        generated_files.append(domain_file.DomainFileWriting(domain_file_elements))

        print("Generating simple feedback file")
        feedback_file = Simple_FeedbackDefinition(
            log_file_general_entries,
            d_now=PROJECT_ROOT,
            debug="off",
            output_dir=output_dir,
        )
        generated_files.append(feedback_file.Simple_FeedbackLogFileWriting())

    if generate_problem_file == "yes":
        print("Generating problem file")
        problem_file = ProblemDefinition(
            domain_name,
            sysml_data,
            missions,
            d_now=PROJECT_ROOT,
            debug="off",
            output_dir=output_dir,
        )
        generated_files.extend(problem_file.ProblemFileWriting())

    if generate_feedback_file == "yes":
        print("Detailed feedback generation is not yet implemented in this branch.")

    return {
        "config_path": config_path,
        "input_path": papyrus_path,
        "output_dir": output_dir,
        "generated_files": generated_files,
        "feedback_name": feedback_name,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Translate Papyrus SysML MBSE files into HDDL artifacts.")
    parser.add_argument(
        "--config",
        default=str(DEFAULT_CONFIG_PATH),
        help="Path to the YAML configuration file.",
    )
    parser.add_argument(
        "--input-dir",
        default=str(DEFAULT_INPUT_DIR),
        help="Directory containing Papyrus UML inputs.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory where generated HDDL artifacts will be written.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    result = run_translation(
        config_path=args.config,
        input_dir=args.input_dir,
        output_dir=args.output_dir,
    )
    generated_files = result["generated_files"]
    if generated_files:
        print("Generated files:")
        for file_path in generated_files:
            print(f" - {file_path}")
    else:
        print("No files were generated.")
