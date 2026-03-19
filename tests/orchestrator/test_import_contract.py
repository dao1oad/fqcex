def test_orchestrator_modules_import() -> None:
    from perp_platform.orchestrator import (
        dispatcher,
        github_state,
        models,
        runtime_state,
        sequence,
    )

    assert dispatcher is not None
    assert github_state is not None
    assert models is not None
    assert runtime_state is not None
    assert sequence is not None
