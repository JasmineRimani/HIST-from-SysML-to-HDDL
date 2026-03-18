from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from .config import HistConfig, load_config


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config" / "configuration.yaml"
DEFAULT_INPUT_DIR = PROJECT_ROOT / "examples" / "inputs"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "outputs"


@dataclass(frozen=True)
class TranslationResult:
    config: HistConfig
    input_path: Path
    output_dir: Path
    generated_files: tuple[Path, ...]


def _print(verbose: bool, message: str) -> None:
    if verbose:
        print(message)


def run_translation(
    config_path: Path | str = DEFAULT_CONFIG_PATH,
    input_dir: Path | str = DEFAULT_INPUT_DIR,
    output_dir: Path | str = DEFAULT_OUTPUT_DIR,
    verbose: bool = False,
) -> TranslationResult:
    config_path = Path(config_path)
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    config = load_config(config_path)
    papyrus_path = input_dir / config.file_name
    if not papyrus_path.exists():
        raise FileNotFoundError(
            f"Could not find the Papyrus UML input '{papyrus_path}'. "
            "Check --input-dir and the file_name configured in the YAML file."
        )

    from .xml_parsing import XML_parsing

    require_domain = config.generate_domain_file or config.generate_feedback
    require_problem = config.generate_problem_file

    _print(verbose, f"Parsing input file: {papyrus_path.name}")
    parsed_model = XML_parsing(
        papyrus_path.read_text(encoding="utf-8"),
        config.packages.hddl,
        config.packages.domain,
        config.packages.problem,
        debug="off",
    ).parse(require_domain=require_domain, require_problem=require_problem)

    generated_files: list[Path] = []

    if config.generate_domain_file:
        from .domain_creation import Domain
        from .partial_feedback_definition import Simple_FeedbackDefinition

        _print(verbose, "Generating domain file")
        domain_file = Domain(
            config.domain_name,
            parsed_model.sysml_data,
            parsed_model.domain_dictionary,
            list(config.domain_requirements),
            config.task_parameters,
            config.legacy_flag_ordering,
            config.legacy_method_precondition_from_action,
            d_now=PROJECT_ROOT,
            debug="off",
            output_dir=output_dir,
        )
        domain_file_elements, log_file_general_entries = domain_file.DomainFileElements()
        generated_files.append(domain_file.DomainFileWriting(domain_file_elements))

        _print(verbose, "Generating simple feedback file")
        feedback_file = Simple_FeedbackDefinition(
            log_file_general_entries,
            d_now=PROJECT_ROOT,
            debug="off",
            output_dir=output_dir,
        )
        generated_files.append(feedback_file.Simple_FeedbackLogFileWriting())

    if config.generate_problem_file:
        from .problem_creation import ProblemDefinition

        _print(verbose, "Generating problem file")
        problem_file = ProblemDefinition(
            config.domain_name,
            parsed_model.sysml_data,
            parsed_model.missions,
            d_now=PROJECT_ROOT,
            debug="off",
            output_dir=output_dir,
        )
        generated_files.extend(problem_file.write_problem_files())

    if config.generate_feedback:
        _print(verbose, "Detailed feedback generation is not yet implemented in this branch.")

    return TranslationResult(
        config=config,
        input_path=papyrus_path,
        output_dir=output_dir,
        generated_files=tuple(generated_files),
    )


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
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Disable progress messages.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    result = run_translation(
        config_path=args.config,
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        verbose=not args.quiet,
    )
    if not args.quiet:
        if result.generated_files:
            print("Generated files:")
            for file_path in result.generated_files:
                print(f" - {file_path}")
        else:
            print("No files were generated.")
