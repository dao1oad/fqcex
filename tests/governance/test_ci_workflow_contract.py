from pathlib import Path
import tomllib


REPO_ROOT = Path(__file__).resolve().parents[2]


def read_text(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def test_pyproject_declares_test_dependencies() -> None:
    content = (REPO_ROOT / "pyproject.toml").read_bytes()
    parsed = tomllib.loads(content.decode("utf-8"))

    optional = parsed["project"]["optional-dependencies"]
    assert "test" in optional
    assert any(dep.startswith("pytest") for dep in optional["test"])


def test_ci_workflow_defines_python_check() -> None:
    content = read_text(".github/workflows/ci.yml")

    assert "python-check:" in content


def test_ci_workflow_uses_python_312_and_editable_install() -> None:
    content = read_text(".github/workflows/ci.yml")

    assert 'python-version: "3.12"' in content
    assert "python -m pip install -e '.[test]'" in content


def test_ci_workflow_runs_full_test_suite() -> None:
    content = read_text(".github/workflows/ci.yml")

    assert "python -m pytest tests -q" in content


def test_readme_documents_current_ci_checks() -> None:
    content = read_text("README.md")

    assert "## CI" in content
    assert "governance-check" in content
    assert "python-check" in content
