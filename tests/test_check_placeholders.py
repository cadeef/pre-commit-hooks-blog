from re import IGNORECASE, compile

import pre_commit_hooks_blog.check_placeholders as cp

# import pytest  # type: ignore[import]


def test_run_step(test_files):
    compiled = compile(r"placeholder\-[\w\-]+", IGNORECASE)
    result = cp.run_step(test_files["bad.md"]["path"], compiled)
    assert len(result) == 2
