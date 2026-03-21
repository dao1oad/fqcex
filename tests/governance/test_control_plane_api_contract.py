from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CONTROL_PLANE_API = REPO_ROOT / "docs" / "architecture" / "control-plane-api.md"
ARCHITECTURE_DOC = REPO_ROOT / "docs" / "architecture" / "ARCHITECTURE.md"


def test_control_plane_api_doc_defines_minimal_resource_surface() -> None:
    assert CONTROL_PLANE_API.exists(), "control-plane-api.md must exist"

    content = CONTROL_PLANE_API.read_text(encoding="utf-8")

    assert "Venue Tradeability" in content
    assert "Instrument Tradeability" in content
    assert "Recovery Runs" in content
    assert "Checker Signals" in content
    assert "Operator Actions" in content
    assert "projection layer" in content
    assert "不是新的 truth source" in content
    assert "延后到 `#68`" in content
    assert "延后到 `#69`" in content


def test_architecture_doc_mentions_control_plane_component() -> None:
    content = ARCHITECTURE_DOC.read_text(encoding="utf-8")

    assert "Control Plane" in content
    assert "without taking truth ownership" in content
