from pathlib import Path

import pytest  # type: ignore[import]
from click.testing import CliRunner


@pytest.fixture
def cli():
    """
    Returns an instance of click.testing.CliRunner
    """
    return CliRunner()


@pytest.fixture
def test_files(shared_datadir):
    return {
        "good.md": {"exit": 0, "path": Path(shared_datadir, "good.md")},
        "bad.md": {"exit": 1, "path": Path(shared_datadir, "bad.md")},
    }
