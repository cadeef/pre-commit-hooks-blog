from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Pattern, Tuple

import click

import pre_commit_hooks_blog.util as pcu


@click.command()
@click.argument(
    "files", nargs=-1, type=click.Path(exists=True), metavar="</path/to/file>"
)
@click.option(
    "--fix",
    "-f",
    is_flag=True,
    help="Modify file inline. Default: notify quirks, don't fix",
)
@click.option(
    "--quirk",
    "-q",
    "quirks",
    multiple=True,
    required=False,
    help="Specify quirks. Use multiple times. Default: all",
)
@click.option(
    "--ansi/--no-ansi", default=True, help="Toggle color output. Default: on, if TTY"
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
    fix: bool = False,
    quirks: Optional[Tuple[str, ...]] = None,
    ansi: bool = True,
    verbose: bool = False,
):
    """
    Fix Bear.app export markdown quirks

    Expects a path(s) to a file that exists.
    """
    q = Quirks(quirks)

    if verbose:
        pcu.output("Processing Files: {}".format(", ".join(files)))  # type: ignore[arg-type]
        pcu.output("Quirks: {}".format(", ".join(q.quirks)))

    # Process files serially for simplicity
    for file in files:
        result = q.evaluate(file, fix=fix)
        report(str(file), result, ansi=ansi)


def report(file: str, result: Dict[str, Tuple[int, str]], ansi: bool = True) -> None:
    pass


@dataclass
class Quirk(object):
    """Standard for quirks"""

    pattern: Pattern
    replace: str
    fix: bool = False

    def modify(self) -> Tuple[Tuple[int, str], ...]:
        pass

    def notify(self) -> Tuple[Tuple[int, str], ...]:
        pass

    def find(self, file: Path) -> Tuple[Tuple[int, str], ...]:
        self.file = file
        if self.fix:
            r = self.modify()
        else:
            r = self.notify()
        return r


class Quirks(object):
    """Bear quirks"""

    def __init__(self, quirks: Optional[Tuple[str, ...]] = None) -> None:
        # Verify that we're working with valid quirks
        if quirks and "all" not in quirks:
            for quirk in quirks:
                if quirk not in self.all():
                    raise KeyError("Quirk not found: {}".format(quirk))
            self.quirks = quirks
        else:
            self.quirks = self.all()

    def evaluate(self, file: Path, fix: bool = False) -> Dict[str, Tuple[int, str]]:
        """Evauluate and optionially act on exiting bear quirks, bread an butter of the class"""

        def strikethrough():
            """- -> ~~"""
            return Quirk(r"^\b\-([\w\-]+)-\b", r"~~%%MATCH%%~~", fix=fix).find(file)

        def line_separator():
            """"- - - -"""
            return Quirk(r"^\- \- \- \-\b", r"---", fix=fix).find(file)

        # Make that magic
        results = {}
        for quirk in self.quirks:
            try:
                results[quirk] = eval(quirk)
            except Exception as e:
                raise e

        return results

    @staticmethod
    def all() -> Tuple[str, ...]:
        # FIXME: Need to remember how to list inner functions
        return ("strikethrough", "line_separator")


if __name__ == "__main__":
    main()
