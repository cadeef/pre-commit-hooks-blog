from pathlib import Path
from re import IGNORECASE, compile
from typing import List, Tuple

import click

from pre_commit_hooks_blog.util import Hook, HookException, Post, Result


@click.command()
@click.argument(
    "files",
    required=True,
    nargs=-1,
    type=click.Path(exists=True),
    metavar="</path/to/file>",
)
@click.option(
    "--remove/--no-remove",
    default=False,
    help="Remove tags represented in metadata from body, off by default",
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
def main(
    files: Tuple[Path, ...],
    remove: bool = False,
    ansi: bool = True,
    verbose: bool = False,
) -> None:
    hook = Hook(name=__name__, function=run_step, ansi=ansi, verbose=verbose)
    try:
        hook.run(files)
    except HookException as e:
        raise e


def run_step(file: Path) -> List[Result]:
    post = Post.load(file)

    compiled = compile(r"(^|\s)+#[\w\-/]+\b", IGNORECASE)

    results = []
    for i, l in enumerate(post.body(return_type="list")):
        matches = compiled.findall(l)
        # FIXME: matches doesn't have strings of matches, come back with fresh eyes
        if matches:
            content = ""
            for m in matches:
                if m in post.tags:
                    content += "{} (in meta) ".format(m)
                else:
                    content += "{} (not in meta) ".format(m)
            results.append(Result(post.body_to_post_line(i), content))
    return results


if __name__ == "__main__":
    main()
