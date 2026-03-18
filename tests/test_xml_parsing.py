import builtins
import importlib.util
from pathlib import Path

import pytest

from hist.errors import DependencyError, MissingModelPackageError, ModelValidationError
from hist.xml_parsing import XML_parsing
from hist.yaml_parsing import YAML_parsing


BS4_AVAILABLE = importlib.util.find_spec("bs4") is not None


def test_xml_parsing_reports_missing_dependency(monkeypatch):
    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "bs4":
            raise ImportError("mocked missing dependency")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    parser = XML_parsing(
        "<xmi:XMI xmlns:xmi='http://www.omg.org/XMI'></xmi:XMI>",
        "ElementsHDDL",
        "DomainDefinition",
        "ProblemDefinition",
        debug="off",
    )

    with pytest.raises(DependencyError, match="beautifulsoup4"):
        parser.parse()


@pytest.mark.skipif(not BS4_AVAILABLE, reason="beautifulsoup4 is not installed")
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


@pytest.mark.skipif(not BS4_AVAILABLE, reason="beautifulsoup4 is not installed")
def test_xml_parsing_raises_for_missing_hddl_package():
    parser = XML_parsing(
        """
        <xmi:XMI xmlns:xmi="http://www.omg.org/XMI">
          <packagedElement xmi:type="uml:Package" name="DomainDefinition" />
        </xmi:XMI>
        """,
        "ElementsHDDL",
        "DomainDefinition",
        "ProblemDefinition",
        debug="off",
    )

    with pytest.raises(MissingModelPackageError, match="ElementsHDDL"):
        parser.parse(require_domain=False, require_problem=True)


@pytest.mark.skipif(not BS4_AVAILABLE, reason="beautifulsoup4 is not installed")
def test_xml_parsing_validates_mission_objects():
    parser = XML_parsing(
        """
        <xmi:XMI xmlns:xmi="http://www.omg.org/XMI">
          <packagedElement xmi:type="uml:Package" name="ElementsHDDL" />
          <packagedElement xmi:type="uml:Package" name="ProblemDefinition">
            <packagedElement xmi:type="uml:Package" name="ProblemFilesDefinition">
              <packagedElement xmi:type="uml:Package" name="NominalMission">
                <packagedElement xmi:type="uml:Class" name="Rover" />
              </packagedElement>
            </packagedElement>
          </packagedElement>
        </xmi:XMI>
        """,
        "ElementsHDDL",
        "DomainDefinition",
        "ProblemDefinition",
        debug="off",
    )

    with pytest.raises(ModelValidationError, match="ownedAttribute"):
        parser.parse(require_domain=False, require_problem=True)
