from pathlib import Path
from sys import exit as sys_exit
from typing import Optional

from click import echo, secho


def output(text: str, ansi: bool = True) -> None:
    echo(text)


def error(message: str, exit: Optional[int] = None) -> None:
    secho("ERROR: {}".format(message), fg="red")
    if exit:
        sys_exit(exit)


def output_colorize():
    pass


def load_post(file: Path):
    pass
    # from re import MULTILINE, match
    # import yaml
    # This is super lazy and not very performant, but meh.
    # c = file.read_text()
    # m = match(r"---.*---", c, MULTILINE)
    # if m:
    #     meta = yaml.load(m.group, Loader=yaml.FullLoader)
    # return meta

    # with file.open() as f:
    #     meta = ""
    #     body = ""
    #     d_cnt = 0
    #     while f:
    #         l = f.readline()
    #         if match(r"^---\n$", l):
    #             d_cnt += 1
    #             if d_cnt == 2:
    #                 break
    #         else:
    #             meta += l

    #     meta = yaml.load(meta, Loader=yaml.FullLoader)
    # return meta

    # return {"meta": meta, "body": raw[1]}
