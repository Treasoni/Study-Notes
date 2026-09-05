---
url: "https://docs.astral.sh/uv/guides/tools/"
title: "Using tools | uv"
scraped_at: 2026-09-05T09:31:26+00:00
---

# [Using tools](https://docs.astral.sh/uv/guides/tools/#using-tools)
Many Python packages provide applications that can be used as tools. uv has specialized support for easily invoking and installing tools.
## [Running tools](https://docs.astral.sh/uv/guides/tools/#running-tools)
The `uvx` command invokes a tool without installing it.
For example, to run `ruff`:

```
$ uvxruff

```

Note
This is exactly equivalent to:

```
$ uvtoolrunruff

```

`uvx` is provided as an alias for convenience.
Arguments can be provided after the tool name:

```
$ uvxpycowsayhellofromuv

  -------------
< hello from uv >
  -------------
   \   ^__^
    \  (oo)\_______
       (__)\       )\/\
           ||----w |
           ||     ||

```

Tools are installed into temporary, isolated environments when using `uvx`.
Note
If you are running a tool in a [_project_](https://docs.astral.sh/uv/concepts/projects/) and the tool requires that your project is installed, e.g., when using `pytest` or `mypy`, you'll want to use [`uv run`](https://docs.astral.sh/uv/guides/projects/#running-commands) instead of `uvx`. Otherwise, the tool will be run in a virtual environment that is isolated from your project.
If your project has a flat structure, e.g., instead of using a `src` directory for modules, the project itself does not need to be installed and `uvx` is fine. In this case, using `uv run` is only beneficial if you want to pin the version of the tool in the project's dependencies.
## [Commands with different package names](https://docs.astral.sh/uv/guides/tools/#commands-with-different-package-names)
When `uvx ruff` is invoked, uv installs the `ruff` package which provides the `ruff` command. However, sometimes the package and command names differ.
The `--from` option can be used to invoke a command from a specific package, e.g., `http` which is provided by `httpie`:

```
$ uvx--fromhttpiehttp

```

## [Requesting specific versions](https://docs.astral.sh/uv/guides/tools/#requesting-specific-versions)
To run a tool at a specific version, use `command@<version>`:

```
$ uvx[email protected][](https://docs.astral.sh/cdn-cgi/l/email-protection)check

```

To run a tool at the latest version, use `command@latest`:

```
$ uvxruff@latestcheck

```

The `--from` option can also be used to specify package versions, as above:

```
$ uvx--from'ruff==0.3.0'ruffcheck

```

Or, to constrain to a range of versions:

```
$ uvx--from'ruff>0.2.0,<0.3.0'ruffcheck

```

Note the `@` syntax cannot be used for anything other than an exact version.
## [Requesting extras](https://docs.astral.sh/uv/guides/tools/#requesting-extras)
The `--from` option can be used to run a tool with extras:

```
$ uvx--from'mypy[faster-cache,reports]'mypy--xml-reportmypy_report

```

This can also be combined with version selection:

```
$ uvx--from'mypy[faster-cache,reports]==1.13.0'mypy--xml-reportmypy_report

```

## [Requesting different sources](https://docs.astral.sh/uv/guides/tools/#requesting-different-sources)
The `--from` option can also be used to install from alternative sources.
For example, to pull from git:

```
$ uvx--fromgit+https://github.com/httpie/clihttpie

```

You can also pull the latest commit from a specific named branch:

```
$ uvx--fromgit+https://github.com/httpie/cli@masterhttpie

```

Or pull a specific tag:

```
$ uvx--fromgit+https://github.com/httpie/[email protected][](https://docs.astral.sh/cdn-cgi/l/email-protection)httpie

```

Or even a specific commit:

```
$ uvx--fromgit+https://github.com/httpie/cli@2843b87httpie

```

Or with [Git LFS](https://git-lfs.com) support:

```
$ uvx--lfs--fromgit+https://github.com/astral-sh/lfs-cowsaylfs-cowsay

```

## [Commands with plugins](https://docs.astral.sh/uv/guides/tools/#commands-with-plugins)
Additional dependencies can be included, e.g., to include `mkdocs-material` when running `mkdocs`:

```
$ uvx--withmkdocs-materialmkdocs--help

```

## [Installing tools](https://docs.astral.sh/uv/guides/tools/#installing-tools)
If a tool is used often, it is useful to install it to a persistent environment and add it to the `PATH` instead of invoking `uvx` repeatedly.
Tip
`uvx` is a convenient alias for `uv tool run`. All of the other commands for interacting with tools require the full `uv tool` prefix.
To install `ruff`:

```
$ uvtoolinstallruff

```

When a tool is installed, its executables are placed in a `bin` directory in the `PATH` which allows the tool to be run without uv. If it's not on the `PATH`, a warning will be displayed and `uv tool update-shell` can be used to add it to the `PATH`.
After installing `ruff`, it should be available:

```
$ ruff--version

```

Unlike `uv pip install`, installing a tool does not make its modules available in the current environment. For example, the following command will fail:

```
$ python-c"import ruff"

```

This isolation is important for reducing interactions and conflicts between dependencies of tools, scripts, and projects.
Unlike `uvx`, `uv tool install` operates on a _package_ and will install all executables provided by the tool.
For example, the following will install the `http`, `https`, and `httpie` executables:

```
$ uvtoolinstallhttpie

```

Additionally, package versions can be included without `--from`:

```
$ uvtoolinstall'httpie>0.1.0'

```

And, similarly, for package sources:

```
$ uvtoolinstallgit+https://github.com/httpie/cli

```

Or package sources with [Git LFS](https://git-lfs.com):

```
$ uvtoolinstall--lfsgit+https://github.com/astral-sh/lfs-cowsay

```

As with `uvx`, installations can include additional packages:

```
$ uvtoolinstallmkdocs--withmkdocs-material

```

Multiple related executables can be installed together in the same tool environment, using the `--with-executables-from` flag. For example, the following will install the executables from `ansible`, plus those ones provided by `ansible-core` and `ansible-lint`:

```
$ uvtoolinstall--with-executables-fromansible-core,ansible-lintansible

```

## [Upgrading tools](https://docs.astral.sh/uv/guides/tools/#upgrading-tools)
To upgrade a tool, use `uv tool upgrade`:

```
$ uvtoolupgraderuff

```

Tool upgrades will respect the version constraints provided when installing the tool. For example, `uv tool install ruff >=0.3,<0.4` followed by `uv tool upgrade ruff` will upgrade Ruff to the latest version in the range `>=0.3,<0.4`.
To instead replace the version constraints, re-install the tool with `uv tool install`:

```
$ uvtoolinstallruff>=0.4

```

To instead upgrade all tools:

```
$ uvtoolupgrade--all

```

## [Requesting Python versions](https://docs.astral.sh/uv/guides/tools/#requesting-python-versions)
By default, uv will use your default Python interpreter (the first it finds) when running, installing, or upgrading tools. You can specify the Python interpreter to use with the `--python` option.
For example, to request a specific Python version when running a tool:

```
$ uvx--python3.10ruff

```

Or, when installing a tool:

```
$ uvtoolinstall--python3.10ruff

```

Or, when upgrading a tool:

```
$ uvtoolupgrade--python3.10ruff

```

For more details on requesting Python versions, see the [Python version](https://docs.astral.sh/uv/concepts/python-versions/#requesting-a-version) concept page.
## [Legacy Windows Scripts](https://docs.astral.sh/uv/guides/tools/#legacy-windows-scripts)
Tools also support running [legacy setuptools scripts](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#scripts). These scripts are available via `$(uv tool dir)\<tool-name>\Scripts` when installed.
Currently only legacy scripts with the `.ps1`, `.cmd`, and `.bat` extensions are supported.
For example, below is an example running a Command Prompt script.

```
$ uvtoolrun--fromnuitka==2.6.7nuitka.cmd--version

```

In addition, you don't need to specify the extension. `uvx` will automatically look for files ending in `.ps1`, `.cmd`, and `.bat` in that order of execution on your behalf.

```
$ uvtoolrun--fromnuitka==2.6.7nuitka--version

```

## [Next steps](https://docs.astral.sh/uv/guides/tools/#next-steps)
To learn more about managing tools with uv, see the [Tools concept](https://docs.astral.sh/uv/concepts/tools/) page and the [command reference](https://docs.astral.sh/uv/reference/cli/#uv-tool).
Or, read on to learn how to [work on projects](https://docs.astral.sh/uv/guides/projects/).
Back to top 
