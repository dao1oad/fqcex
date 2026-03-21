from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CONTROL_PLANE_API = REPO_ROOT / "docs" / "architecture" / "control-plane-api.md"
DATA_MODEL_DOC = REPO_ROOT / "docs" / "architecture" / "DATA_MODEL.md"


def test_control_plane_api_defines_tradeability_and_recovery_read_models() -> None:
    content = CONTROL_PLANE_API.read_text(encoding="utf-8")

    assert "Venue Tradeability Read Model" in content
    assert "Instrument Tradeability Read Model" in content
    assert "Recovery Run Read Model" in content
    assert "`tradeability_states`" in content
    assert "`recovery_runs`" in content
    assert "projection, not a new truth source" in content


def test_data_model_doc_maps_control_plane_read_models_to_existing_truth_tables() -> None:
    content = DATA_MODEL_DOC.read_text(encoding="utf-8")

    assert "Control Plane Read Models" in content
    assert "`tradeability_states`" in content
    assert "`recovery_runs`" in content
    assert "Venue Tradeability Read Model" in content
    assert "Recovery Run Read Model" in content
