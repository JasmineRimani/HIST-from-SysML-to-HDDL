from pathlib import Path

import pytest


pytest.importorskip("bs4")

from hist.xml_parsing import XML_parsing
from hist.yaml_parsing import YAML_parsing


def test_xml_parsing_extracts_domain_and_problem_elements():
    root = Path(__file__).resolve().parents[1]
    config_path = root / "config" / "configuration.yaml"
    parser = YAML_parsing(config_path.read_text(encoding="utf-8"), debug="off")
    file_name, _, _ = parser.YAML_fileNames()
    package_hddl, package_domain, package_problem, _ = parser.YAML_PackagesNames()

    papyrus_path = root / "examples" / "inputs" / file_name
    xml_parser = XML_parsing(
        papyrus_path.read_text(encoding="utf-8"),
        package_hddl,
        package_domain,
        package_problem,
        debug="off",
    )

    sysml_data, domain_dictionary, missions = xml_parser.Parsing()

    assert sysml_data is not None
    assert domain_dictionary["types"]
    assert domain_dictionary["tasks"]
    assert domain_dictionary["methods"]
    assert missions
