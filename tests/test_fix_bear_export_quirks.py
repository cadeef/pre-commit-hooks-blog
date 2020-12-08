from pathlib import Path

import pytest  # type: ignore[import]

from pre_commit_hooks_blog.fix_bear_export_quirks import Quirks, run_step

QUIRKS = ("strikethrough", "line_separator", "header_newline")


@pytest.fixture
def quirks():
    """
    Returns an instances of pre_commit_hooks_blog.util.Post
    """
    return Quirks


def test_run_step(shared_datadir):
    # FIXME: Actually implement
    result = run_step(Path(shared_datadir, "good.md"), Quirks().all())
    assert isinstance(result, dict)


def test_quirks_all(quirks):
    assert len(QUIRKS) == len(quirks.all())
    for q in QUIRKS:
        assert q in quirks.all()
