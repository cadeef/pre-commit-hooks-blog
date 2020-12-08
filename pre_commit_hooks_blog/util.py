from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from sys import exit as sys_exit
from typing import Any, Callable, Dict, Iterator, List, Optional, Tuple, Union

import yaml
from click import option, secho


@dataclass
class Hook(object):
    """Minimal hook framework"""

    name: str
    function: Callable
    ansi: bool = True
    verbose: bool = False

    def run(self, files: Tuple[Path, ...], **kwargs) -> None:
        # Pre-run function
        self.pre_run(files)

        results = []
        for file in files:
            # FIXME: file should be a valid Path already
            results.append((file, self.function(Path(file), **kwargs)))

        # Post hook
        self.post_run(results)

    def pre_run(self, files) -> None:
        """Default pre-run function"""
        if self.verbose:
            self.output("Processing Files: {}".format(", ".join(files)))  # type: ignore[arg-type]

    def post_run(self, results) -> None:
        """Default post-run function"""

        for result in results:
            if result[1] or self.verbose:
                self.output("{}:".format(str(result[0])), bold=True)
                for r in result[1]:
                    self.output("\t{}".format(r))

        # Convoluted index check... does the first result have a defined tuple?
        # FIXME: Probably need to use click's context exit instead since it is confused in tests
        if 0 <= 1 < len(results[0][1]):
            sys_exit(1)
        else:
            sys_exit(0)

    def output(self, message: str, **kwargs: Union[str, bool]) -> None:
        if not self.ansi:
            # TODO: Strip any color codes passed in text
            pass
        secho(message, color=self.ansi, **kwargs)  # type: ignore[arg-type]

    def error(self, message: str, exit: Optional[int] = None) -> None:
        self.output("ERROR: {}".format(message), err=True, fg="red")
        if exit:
            sys_exit(exit)


class HookException(Exception):
    pass


@dataclass
class Post(object):
    """Generic post object"""

    meta: Dict[str, Any]
    _body: str
    lines: int

    def body(self, return_type: str = "str") -> Union[str, List[str]]:
        if return_type == "str":
            return self._body
        elif return_type == "list":
            return self._body.splitlines()
        else:
            raise PostException("Invalid body() return_type")

    def body_to_post_line(self, line):
        """Calculate the line position in a file given a position in the body"""
        meta_len = self.lines - len(self.body(return_type="list"))
        return meta_len + line

    def __getattr__(self, key) -> Union[str, Iterator, datetime]:
        """Return meta keys where available"""
        try:
            return self.meta[key]
        except KeyError as e:
            raise AttributeError(e)

    @classmethod
    def load(cls, file: Union[Path, str]):
        if isinstance(file, str):
            # YOLO: Coerce and let Path figure it out
            file = Path(file)
        # Yes it's ugly, but I'm tired
        with file.open() as f:
            meta = ""
            body = ""
            d_cnt = 0
            l_cnt = 1
            while f:
                l = f.readline()
                if not l:
                    break
                elif d_cnt >= 2:
                    body += l
                elif l.startswith("---\n"):
                    d_cnt += 1
                elif d_cnt < 2:
                    meta += l
                l_cnt += 1

        if not meta:
            raise PostException("{}: Doesn't smell like a post...".format(str(file)))

        try:
            meta_yaml = yaml.load(meta, Loader=yaml.FullLoader)
        except Exception as e:
            raise e

        return cls(meta=meta_yaml, _body=body, lines=l_cnt)


class PostException(Exception):
    pass


@dataclass
class Result(object):
    line: int
    content: str

    def __str__(self):
        """Returns LINE_NO: CONTENTS"""
        return "{}: {}".format(self.line, self.content)


# TODO: Make combined decorator work
def default_flags(arg):
    """Decorator that implements default flags for hooks"""

    def inner():
        option(
            "--ansi/--no-ansi", default=True, help="Toggle color output, on by default"
        )
        option(
            "--verbose",
            "-v",
            is_flag=True,
            default=False,
            help="Verbose output, output is typically minimized.",
        )
        print(arg)

    return inner
