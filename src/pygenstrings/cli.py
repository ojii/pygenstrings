import fnmatch
import os
from pathlib import Path
from typing import *

import click

from pygenstrings.genstrings import (
    generate_strings,
    read_strings,
    merge_strings,
    PathFilter,
)


def make_filter(exclude: List[str]) -> PathFilter:
    def fltr(entry: os.DirEntry) -> bool:
        for pat in exclude:
            if fnmatch.fnmatch(entry.path, f"*{pat}"):
                return False
        return True

    return fltr


def find_translations(path: Path, langs: Iterable[str]) -> Iterable[Path]:
    for lang in langs:
        yield path / f"{lang}.lproj" / "Localizable.strings"


@click.command()
@click.argument("src", type=click.Path())
@click.argument("dst", type=click.Path())
@click.argument("langs", nargs=-1)
@click.option("-e", "--exclude", multiple=True)
def main(src: str, dst: str, langs: List[str], exclude: List[str]) -> None:
    path_filter: Optional[PathFilter]
    if exclude:
        path_filter = make_filter(exclude)
    else:
        path_filter = None
    strings = generate_strings(Path(src), path_filter)
    for path in find_translations(Path(dst), langs):
        translation = read_strings(path)
        result = merge_strings(strings, translation)
        with path.open("w", encoding="utf-8") as fobj:
            fobj.write(result.to_source())
