from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Pattern, Tuple

import click

import pre_commit_hooks_blog.util as pcu


@click.command()
@click.argument(
    "files",
    required=True,
    nargs=-1,
    type=click.Path(exists=True),
    metavar="</path(s)/to/fil(e)>",
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
        # Assume that if all is defined anywhere that all are wanted
        if quirks and "all" not in quirks:
            self.quirks = quirks
        else:
            self.quirks = self.all()

    def evaluate(self, file: Path, fix: bool = False) -> Dict[str, Tuple[int, str]]:
        """Evauluate and optionially act on exiting bear quirks, bread an butter of the class"""
        self._fix = fix
        self._file = file

        # Make that magic
        results = {}
        for quirk in self.quirks:
            try:
                results[quirk] = getattr(self, quirk)()
            except AttributeError:
                raise InvalidQuirk("Quirk: {} doesn't exist!".format(quirk))

        return results

    def strikethrough(self):
        """- -> ~~"""
        return Quirk(r"^\b\-([\w\-]+)-\b", r"~~%%MATCH%%~~", fix=self.fix).find(
            self.file
        )

    def line_separator(self):
        """"- - - -"""
        return Quirk(r"^\- \- \- \-\b", r"---", fix=self.fix).find(self.file)

    def header_newline(self):
        pass

    @staticmethod
    def all() -> Tuple[str, ...]:
        # Hokey but works for now
        return tuple(
            q
            for q in dir(Quirks)
            if not q.startswith("__") and q not in ("all", "evaluate")
        )


class InvalidQuirk(Exception):
    # FIXME: Properly define exeption with __str__
    pass


if __name__ == "__main__":
    main()
