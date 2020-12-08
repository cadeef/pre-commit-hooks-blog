import pytest  # type: ignore[import]

import pre_commit_hooks_blog.auto_commit_message
import pre_commit_hooks_blog.check_orphan_tags
import pre_commit_hooks_blog.check_placeholders
import pre_commit_hooks_blog.fix_bear_export_quirks
import pre_commit_hooks_blog.run_markdownlint
import pre_commit_hooks_blog.run_mlc

# TODO: We could do some fancy inspection to get this list, maybe later
SCRIPTS = (
    "auto_commit_message",
    "check_orphan_tags",
    "check_placeholders",
    "fix_bear_export_quirks",
    "run_markdownlint",
    "run_mlc",
)


@pytest.mark.parametrize("script", SCRIPTS)
def test_flag_consistency(cli, shared_datadir, script):
    """
    Verify default options are in the generated help text.

    We test funtion of the flags in unit, just ensure they are there.
    """
    result = cli.invoke(getattr(pre_commit_hooks_blog, script).main, ["--help"])
    assert result.exit_code == 0
    for o in ("--ansi", "--no-ansi", "-v", "--verbose"):
        if o not in result.output:
            pytest.fail("{} not in help output".format(o))


@pytest.mark.parametrize("script", SCRIPTS)
def test_default_no_options(cli, test_files, script):
    # Test good and bad files
    for file in test_files:
        result = cli.invoke(
            getattr(pre_commit_hooks_blog, script).main, [test_files[file]["path"]]
        )
        if result.exit_code != test_files[file]["exit"]:
            pytest.fail(
                "{} file should have exited {} ({})".format(
                    file, test_files[file]["exit"], test_files[file]["path"]
                )
            )
