from pathlib import Path
from typing import Dict, Tuple

import click

from pre_commit_hooks_blog.util import Hook, Post


@click.command()
@click.argument(
    "files",
    required=True,
    nargs=-1,
    type=click.Path(exists=True),
    metavar="</path/to/file>",
)
@click.option(
    "--ansi/--no-ansi", default=True, help="Toggle color output, on by default"
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    default=False,
    help="Verbose output, output is typically minimized.",
)
def main(files: Tuple[Path, ...], ansi: bool = True, verbose: bool = False) -> None:
    """
    Convert post metadata into well formed commits

    Expects a path(s) to a file that exists.
    """

    hook = AutoCommitHook(name=__name__, function=run_step, ansi=ansi, verbose=verbose)
    try:
        hook.run(files)
    except Exception as e:
        hook.error(str(e))


def run_step(file: Path) -> Tuple[int, Dict[str, str]]:
    post = Post.load(file)
    # Return line 0 since we're not linting
    return (0, post.meta)


class AutoCommitHook(Hook):
    """
    AutoCommitHook

    Override post_run since we are creating a commit message rather than linting
    """

    def post_run(self, results):
        commit_msg = "Post:\n\n"
        for result in results:
            meta = result[1][1]
            commit_msg += "* {}, Publish: {} ({})\n".format(
                meta["title"], meta["date"], result[0]
            )
        self.output(commit_msg)


if __name__ == "__main__":
    main()
