from sys import exit as sys_exit
from typing import Optional

from click import echo, secho


def output(text: str, ansi: bool = True) -> None:
    echo(text)


def error(message: str, exit: Optional[int] = None) -> None:
    secho("ERROR: {}".format(message), fg="red")
    if exit:
        sys_exit(exit)
