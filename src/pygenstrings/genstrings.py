import os
from dataclasses import dataclass
from pathlib import Path
from subprocess import check_call
from tempfile import TemporaryDirectory
from typing import *

import chardet

from .parser import parse


@dataclass(frozen=True, eq=True)
class LocalizableString:
    string: str
    comment: str


@dataclass
class LocalizableStrings:
    strings: Dict[str, LocalizableString]

    @classmethod
    def from_source(cls, source: str):
        return cls(
            {
                key: LocalizableString(string=value, comment=comment)
                for key, value, comment in parse(source)
            }
        )

    def to_source(self) -> str:
        lines = []
        for key, lstring in sorted(self.strings.items()):
            if lstring.comment:
                lines.append(f"/* {lstring.comment} */")
            lines.append(f"{key} = {lstring.string};")
            lines.append("")
        return "\n".join(lines)


def read_file(path: Path) -> Union[str, None]:
    with path.open("rb") as fobj:
        data = fobj.read()
    candidates = ["utf-8"]
    encoding = chardet.detect(data)["encoding"]
    if encoding:
        candidates.append(encoding)
    candidates.append("utf-16-le")
    for candidate in candidates:
        try:
            return data.decode(candidate)
        except UnicodeDecodeError:
            continue
    return None


def read_strings(path: Path) -> LocalizableStrings:
    source = read_file(path)
    if source is None:
        raise Exception(f"Could not read file {path}")
    return LocalizableStrings.from_source(source)


def scantree(
    path: os.PathLike, path_filter: Callable[[os.DirEntry], bool]
) -> Iterable[Path]:
    for entry in os.scandir(path):
        if not path_filter(entry):
            continue
        if entry.is_file() and entry.name.endswith((".m", ".mm", ".swift")):
            yield entry.path
        elif entry.is_dir():
            yield from scantree(entry.path, path_filter)


def generate_strings(
    src: Path, path_filter: Optional[Callable[[os.DirEntry], bool]] = None
) -> LocalizableStrings:
    with TemporaryDirectory() as workspace:
        for entry in scantree(src, path_filter):
            check_call(
                ["genstrings", "-a", "-littleEndian", "-o", workspace, str(entry)]
            )
        return read_strings(Path(workspace) / "Localizable.strings")


def merge_strings(
    strings: LocalizableStrings, translations: LocalizableStrings
) -> LocalizableStrings:
    return LocalizableStrings(
        {
            key: translations.strings.get(key, value)
            for key, value in strings.strings.items()
        }
    )
