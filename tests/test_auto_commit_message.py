# import pytest
from pathlib import Path

from pre_commit_hooks_blog.auto_commit_message import run_step


def test_run_step(shared_datadir):
    # FIXME: Actually implement
    result = run_step(Path(shared_datadir, "good.md"))
    assert isinstance(result, dict)
