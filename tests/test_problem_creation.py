import pytest

from hist.errors import UnsupportedFeatureError
from hist.problem_creation import ProblemDefinition


def _build_mission(**overrides):
    mission = {
        "name": "NominalMission",
        "objects": ["rover-rover", "camera1-camera"],
        "initial_conditions": ["(available rover)", "(on_board camera1 rover)"],
        "init_HTN": None,
        "map_File": None,
    }
    mission.update(overrides)
    return mission


def test_problem_creation_writes_valid_problem_file(tmp_path):
    mission = _build_mission()
    problem = ProblemDefinition(
        "Igluna_check",
        SysML_data=None,
        missions=[mission],
        d_now=tmp_path,
        debug="off",
        output_dir=tmp_path,
    )

    problem_text = problem.build_problem_text(mission, 0)

    assert "(problem nominalmission_1)" in problem_text
    assert "(:domain igluna_check)" in problem_text
    assert "(:htn" in problem_text
    assert ":ordering ()" in problem_text
    assert "  )\n  (:init" in problem_text

    generated_files = problem.write_problem_files()
    assert len(generated_files) == 1
    assert generated_files[0].read_text(encoding="utf-8") == problem_text


def test_problem_creation_rejects_custom_initial_htn(tmp_path):
    problem = ProblemDefinition(
        "Igluna_check",
        SysML_data=None,
        missions=[_build_mission(init_HTN="Initial HTN: custom network")],
        d_now=tmp_path,
        debug="off",
        output_dir=tmp_path,
    )

    with pytest.raises(UnsupportedFeatureError, match="Initial HTN"):
        problem.write_problem_files()


def test_problem_creation_rejects_external_map_file(tmp_path):
    problem = ProblemDefinition(
        "Igluna_check",
        SysML_data=None,
        missions=[_build_mission(map_File="Map_file: terrain.txt")],
        d_now=tmp_path,
        debug="off",
        output_dir=tmp_path,
    )

    with pytest.raises(UnsupportedFeatureError, match="Map_file"):
        problem.write_problem_files()
