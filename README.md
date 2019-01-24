# pygenstrings

Simplifies managing localization files for ObjC/Swift projects.

## Installation

`pip install pygenstrings` or your preferred way of installing Python packages.

## Usage

### With a config file

Create a config file `pygenstrings.toml`. This uses the [TOML](https://github.com/toml-lang/toml)
format. All configuration values are under the `[pygenstrings]` key. Alternatively you can use
the key `[tool.pygenstrings]` in your `pyproject.toml`

Available configuration options are:

* `sources`: A list of paths to search for strings in.
* `languages`: A list of languages for which to generate string files.
* `destination`: Root folder for the output of the files. Defaults to the current directory.
* `exclude`: List of glob-like filters for which paths to exclude.

Now simply run `pygenstrings` in the same directory as the config file.

### Using command line arguments

Command line arguments override any values in the config file when given. The following options are supported:

* `-s`/`--src`: Path to search for strings in. Can be provided multiple times.
* `-l`/`--lang`: Language to generate string files for. Can be provided multiple times.
* `-d`/`--dst`: Root folder for the output of files. Defaults to current directory.
* `-e`/`--exclude`: Glob-like filter of paths to exclude. Can be provided multiple times.
* `-c`/`--config-file`: Alternative configuration file to use.
