import os
from io import StringIO
from pathlib import Path

import pytest
from click.testing import CliRunner

from pygenstrings.cli import main, read_config


@pytest.fixture
def tmp_cwd(tmp_path: Path):
    old_cwd = Path.cwd()
    os.chdir(tmp_path)
    try:
        yield tmp_path
    finally:
        os.chdir(old_cwd)


def test_no_translations_yet(tmp_path: Path):
    src = tmp_path / "src"
    src.mkdir()
    dst = tmp_path / "dst"
    dst.mkdir()
    swift = src / "file.swift"
    with swift.open("w") as fobj:
        fobj.write('func test() { NSLocalizedString("msgid", comment:"comment")}')

    runner = CliRunner()
    result = runner.invoke(main, ["-s", str(src), "-d", str(dst), "-l", "ja"])
    assert "Found 1 strings to translate" in result.output
    assert "Wrote ja" in result.output
    assert "Done" in result.output
    assert result.exit_code == 0


def test_config_file(tmp_cwd: Path):
    config = tmp_cwd / "pyproject.toml"
    with config.open("w") as fobj:
        fobj.write('[tool.pygenstrings]\nsources=["bar"]')
    config = read_config(None)
    assert config["sources"] == ["bar"]
    config = tmp_cwd / "pygenstrings.toml"
    with config.open("w") as fobj:
        fobj.write('[pygenstrings]\nsources=["foo"]')
    config = read_config(None)
    assert config["sources"] == ["foo"]
    config = read_config(StringIO('[pygenstrings]\nsources=["baz"]'))
    assert config["sources"] == ["baz"]
