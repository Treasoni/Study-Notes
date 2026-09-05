---
url: "https://docs.astral.sh/uv/reference/cli/"
title: "Commands | uv"
scraped_at: 2026-09-05T09:31:26+00:00
---

# [CLI Reference](https://docs.astral.sh/uv/reference/cli/#cli-reference)
An extremely fast Python package manager.
### Usage

```
uv [OPTIONS] <COMMAND>

```

### Commands     
Manage authentication     
Run a command or script     
Create a new project     
Add dependencies to the project     
Remove dependencies from the project     
Read or update the project's version     
Update the project's environment     
Update the project's lockfile     
Export the project's lockfile to an alternate format     
Display the project's dependency tree     
Format Python code in the project     
Run checks on the project     
Audit the project's dependencies     
Run and install commands provided by Python packages     
Manage Python versions and installations     
Manage Python packages with a pip-compatible interface     
Create a virtual environment     
Build Python packages into source distributions and wheels     
Upload distributions to an index     
Inspect uv workspaces     
Manage uv's cache     
Manage the uv executable     
Display documentation for a command
## [uv auth](https://docs.astral.sh/uv/reference/cli/#uv-auth)
Manage authentication
### Usage

```
uv auth [OPTIONS] <COMMAND>

```

### Commands     
Login to a service     
Logout of a service     
Show the authentication token for a service     
Show the path to the uv credentials directory
### [uv auth login](https://docs.astral.sh/uv/reference/cli/#uv-auth-login)
Login to a service
### Usage

```
uv auth login [OPTIONS] <SERVICE>

```

### Arguments     
The domain or URL of the service to log into
### Options 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-auth-login--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-auth-login--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-auth-login--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-auth-login--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-auth-login--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable.     
Display the concise help for this command 

[`--keyring-provider`](https://docs.astral.sh/uv/reference/cli/#uv-auth-login--keyring-provider) _keyring-provider_ 
    
The keyring provider to use for storage of credentials.
Only `--keyring-provider native` is supported for `login`, which uses the system keyring via an integration built into uv.
May also be set with the `UV_KEYRING_PROVIDER` environment variable.
Possible values:
  * `disabled`: Do not use keyring for credential lookup
  * `subprocess`: Use the `keyring` command for credential lookup

    
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-auth-login--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable. 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-auth-login--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-auth-login--no-python-downloads)
    
Disable automatic downloads of Python.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--password`](https://docs.astral.sh/uv/reference/cli/#uv-auth-login--password) _password_ 
    
The password to use for the service.
Use `-` to read the password from stdin. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-auth-login--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store. 

[`--token`](https://docs.astral.sh/uv/reference/cli/#uv-auth-login--token), `-t` _token_ 
    
The token to use for the service.
The username will be set to `__token__`.
Use `-` to read the token from stdin. 

[`--username`](https://docs.astral.sh/uv/reference/cli/#uv-auth-login--username), `-u` _username_ 
    
The username to use for the service     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
### [uv auth logout](https://docs.astral.sh/uv/reference/cli/#uv-auth-logout)
Logout of a service
### Usage

```
uv auth logout [OPTIONS] <SERVICE>

```

### Arguments     
The domain or URL of the service to logout from
### Options 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-auth-logout--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-auth-logout--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-auth-logout--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-auth-logout--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-auth-logout--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable.     
Display the concise help for this command 

[`--keyring-provider`](https://docs.astral.sh/uv/reference/cli/#uv-auth-logout--keyring-provider) _keyring-provider_ 
    
The keyring provider to use for storage of credentials.
Only `--keyring-provider native` is supported for `logout`, which uses the system keyring via an integration built into uv.
May also be set with the `UV_KEYRING_PROVIDER` environment variable.
Possible values:
  * `disabled`: Do not use keyring for credential lookup
  * `subprocess`: Use the `keyring` command for credential lookup

    
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-auth-logout--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable. 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-auth-logout--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-auth-logout--no-python-downloads)
    
Disable automatic downloads of Python.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-auth-logout--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store. 

[`--username`](https://docs.astral.sh/uv/reference/cli/#uv-auth-logout--username), `-u` _username_ 
    
The username to logout     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
### [uv auth token](https://docs.astral.sh/uv/reference/cli/#uv-auth-token)
Show the authentication token for a service
### Usage

```
uv auth token [OPTIONS] <SERVICE>

```

### Arguments     
The domain or URL of the service to lookup
### Options 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-auth-token--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-auth-token--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-auth-token--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-auth-token--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-auth-token--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable.     
Display the concise help for this command 

[`--keyring-provider`](https://docs.astral.sh/uv/reference/cli/#uv-auth-token--keyring-provider) _keyring-provider_ 
    
The keyring provider to use for reading credentials
May also be set with the `UV_KEYRING_PROVIDER` environment variable.
Possible values:
  * `disabled`: Do not use keyring for credential lookup
  * `subprocess`: Use the `keyring` command for credential lookup

    
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-auth-token--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable. 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-auth-token--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-auth-token--no-python-downloads)
    
Disable automatic downloads of Python.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-auth-token--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store. 

[`--username`](https://docs.astral.sh/uv/reference/cli/#uv-auth-token--username), `-u` _username_ 
    
The username to lookup     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
### [uv auth dir](https://docs.astral.sh/uv/reference/cli/#uv-auth-dir)
Show the path to the uv credentials directory.
By default, credentials are stored in the uv data directory at `$XDG_DATA_HOME/uv/credentials` or `$HOME/.local/share/uv/credentials` on Unix and `%APPDATA%\uv\data\credentials` on Windows.
The credentials directory may be overridden with `$UV_CREDENTIALS_DIR`.
Credentials are only stored in this directory when the plaintext backend is used, as opposed to the native backend, which uses the system keyring.
### Usage

```
uv auth dir [OPTIONS]

```

### Options 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-auth-dir--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-auth-dir--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-auth-dir--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-auth-dir--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-auth-dir--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable.     
Display the concise help for this command     
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-auth-dir--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable. 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-auth-dir--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-auth-dir--no-python-downloads)
    
Disable automatic downloads of Python.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-auth-dir--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store.     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
Run a command or script.
Ensures that the command runs in a Python environment.
When used with a file ending in `.py` or an HTTP(S) URL, the file will be treated as a script and run with a Python interpreter, i.e., `uv run file.py` is equivalent to `uv run python file.py`. For URLs, the script is temporarily downloaded before execution. If the script contains inline dependency metadata, it will be installed into an isolated, ephemeral environment. When used with `-`, the input will be read from stdin, and treated as a Python script.
When used in a project, the project environment will be created and updated before invoking the command.
When used outside a project, if a virtual environment can be found in the current directory or a parent directory, the command will be run in that environment. Otherwise, the command will be run in the environment of the discovered interpreter.
When running a script, the project or workspace is discovered from the script's directory. Otherwise, the project or workspace is discovered from the current working directory.
Arguments following the command (or script) are not interpreted as arguments to uv. All options to uv must be provided before the command, e.g., `uv run --verbose foo`. A `--` can be used to separate the command from uv options for clarity, e.g., `uv run --python 3.12 -- python`.
### Usage

```
uv run [OPTIONS] [COMMAND]

```

### Options     
Prefer the active virtual environment over the project's virtual environment.
If the project virtual environment is active or no virtual environment is active, this has no effect.     
Include all optional dependencies.
This option is only available when running in a project.     
Include dependencies from all dependency groups.
`--no-group` can be used to exclude specific groups.     
Run the command with all workspace members installed.
The workspace's environment (`.venv`) is updated to include all workspace members.
Any extras or groups specified via `--extra`, `--group`, or related options will be applied to all workspace members. 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-run--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-run--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-run--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--compile-bytecode`](https://docs.astral.sh/uv/reference/cli/#uv-run--compile-bytecode), `--compile` 
    
Compile Python files to bytecode after installation.
By default, uv does not compile Python (`.py`) files to bytecode (`__pycache__/*.pyc`); instead, compilation is performed lazily the first time a module is imported. For use-cases in which start time is critical, such as CLI applications and Docker containers, this option can be enabled to trade longer installation times for faster start times.
When enabled, install operations (e.g., `uv pip install`) will compile installed or reinstalled Python files. Commands that perform a sync operation (e.g., `uv sync` or `uv run`) will process the entire site-packages directory including packages that are not being modified.
May also be set with the `UV_COMPILE_BYTECODE` environment variable. 

[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-run--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--config-setting`](https://docs.astral.sh/uv/reference/cli/#uv-run--config-setting), `--config-settings`, `-C` _config-setting_ 
    
Settings to pass to the PEP 517 build backend, specified as `KEY=VALUE` pairs 

[`--config-settings-package`](https://docs.astral.sh/uv/reference/cli/#uv-run--config-settings-package), `--config-settings-package` _config-settings-package_ 
    
Settings to pass to the PEP 517 build backend for a specific package, specified as `PACKAGE:KEY=VALUE` pairs 

[`--default-index`](https://docs.astral.sh/uv/reference/cli/#uv-run--default-index) _default-index_ 
    
The default package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--index` flag.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
May also be set with the `UV_DEFAULT_INDEX` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-run--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable. 

[`--env-file`](https://docs.astral.sh/uv/reference/cli/#uv-run--env-file) _env-file_ 
    
Load environment variables from a `.env` file.
Can be provided multiple times, with subsequent files overriding values defined in previous files.
May also be set with the `UV_ENV_FILE` environment variable.     
Perform an exact sync, removing extraneous packages.
When enabled, uv will remove any extraneous packages from the environment. By default, `uv run` will make the minimum necessary changes to satisfy the requirements. 

[`--exclude-newer`](https://docs.astral.sh/uv/reference/cli/#uv-run--exclude-newer) _exclude-newer_ 
    
Limit candidate packages to those that were uploaded prior to the given date.
The date is compared against the upload time of each individual distribution artifact (i.e., when each file was uploaded to the package index), not the release date of the package version.
Accepts RFC 3339 timestamps (e.g., `2006-12-02T02:07:43Z`), local dates in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Use `false` to disable `exclude-newer`.
May also be set with the `UV_EXCLUDE_NEWER` environment variable. 

[`--exclude-newer-package`](https://docs.astral.sh/uv/reference/cli/#uv-run--exclude-newer-package) _exclude-newer-package_ 
    
Limit candidate packages for specific packages to those that were uploaded prior to the given date.
Accepts package-date pairs in the format `PACKAGE=DATE`, where `DATE` is an RFC 3339 timestamp (e.g., `2006-12-02T02:07:43Z`), a local date in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Can be provided multiple times for different packages. 

[`--extra`](https://docs.astral.sh/uv/reference/cli/#uv-run--extra) _extra_ 
    
Include optional dependencies from the specified extra name.
May be provided more than once.
This option is only available when running in a project. 

[`--extra-index-url`](https://docs.astral.sh/uv/reference/cli/#uv-run--extra-index-url) _extra-index-url_ 
    
(Deprecated: use `--index` instead) Extra URLs of package indexes to use, in addition to `--index-url`.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--index-url` (which defaults to PyPI). When multiple `--extra-index-url` flags are provided, earlier values take priority.
May also be set with the `UV_EXTRA_INDEX_URL` environment variable. 

[`--find-links`](https://docs.astral.sh/uv/reference/cli/#uv-run--find-links), `-f` _find-links_ 
    
Locations to search for candidate distributions, in addition to those found in the registry indexes.
If a path, the target must be a directory that contains packages as wheel files (`.whl`) or source distributions (e.g., `.tar.gz` or `.zip`) at the top level.
If a URL, the page must contain a flat list of links to package files adhering to the formats described above.
May also be set with the `UV_FIND_LINKS` environment variable. 

[`--fork-strategy`](https://docs.astral.sh/uv/reference/cli/#uv-run--fork-strategy) _fork-strategy_ 
    
The strategy to use when selecting multiple versions of a given package across Python versions and platforms.
By default, uv will optimize for selecting the latest version of each package for each supported Python version (`requires-python`), while minimizing the number of selected versions across platforms.
Under `fewest`, uv will minimize the number of selected versions for each package, preferring older versions that are compatible with a wider range of supported Python versions or platforms.
May also be set with the `UV_FORK_STRATEGY` environment variable.
Possible values:
  * `fewest`: Optimize for selecting the fewest number of versions for each package. Older versions may be preferred if they are compatible with a wider range of supported Python versions or platforms
  * `requires-python`: Optimize for selecting latest supported version of each package, for each supported Python version

    
Run without updating the `uv.lock` file [env: UV_FROZEN=]
Instead of checking if the lockfile is up-to-date, uses the versions in the lockfile as the source of truth. If the lockfile is missing, uv will exit with an error. If the `pyproject.toml` includes changes to dependencies that have not been included in the lockfile yet, they will not be present in the environment. 

[`--group`](https://docs.astral.sh/uv/reference/cli/#uv-run--group) _group_ 
    
Include dependencies from the specified dependency group.
May be provided multiple times.     
Run the given path as a Python GUI script.
Using `--gui-script` will attempt to parse the path as a PEP 723 script and run it with `pythonw.exe`, irrespective of its extension. Only available on Windows.     
Display the concise help for this command 

[`--index`](https://docs.astral.sh/uv/reference/cli/#uv-run--index) _index_ 
    
The indexes to use when resolving dependencies, in addition to the default index.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--default-index` (which defaults to PyPI). When multiple `--index` flags are provided, earlier values take priority.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
Relative paths can be disambiguated from index names with `./` or `../` on Unix or `.\\`, `..\\`, `./` or `../` on Windows.
May also be set with the `UV_INDEX` environment variable. 

[`--index-strategy`](https://docs.astral.sh/uv/reference/cli/#uv-run--index-strategy) _index-strategy_ 
    
The strategy to use when resolving against multiple index URLs.
By default, uv will stop at the first index on which a given package is available, and limit resolutions to those present on that first index (`first-index`). This prevents "dependency confusion" attacks, whereby an attacker can upload a malicious package under the same name to an alternate index.
May also be set with the `UV_INDEX_STRATEGY` environment variable.
Possible values:
  * `first-index`: Only use results from the first index that returns a match for a given package name
  * `unsafe-first-match`: Search for every package name across all indexes, exhausting the versions from the first index before moving on to the next
  * `unsafe-best-match`: Search for every package name across all indexes, preferring the "best" version found. If a package version is in multiple indexes, only look at the entry for the first index



[`--index-url`](https://docs.astral.sh/uv/reference/cli/#uv-run--index-url), `-i` _index-url_ 
    
(Deprecated: use `--default-index` instead) The URL of the Python package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--extra-index-url` flag.
May also be set with the `UV_INDEX_URL` environment variable.     
Run the command in an isolated virtual environment [env: UV_ISOLATED=]
Usually, the project environment is reused for performance. This option forces a fresh environment to be used for the project, enforcing strict isolation between dependencies and declaration of requirements.
An editable installation is still used for the project.
When used with `--with` or `--with-requirements`, the additional dependencies will still be layered in a second environment. 

[`--keyring-provider`](https://docs.astral.sh/uv/reference/cli/#uv-run--keyring-provider) _keyring-provider_ 
    
Attempt to use `keyring` for authentication for index URLs.
At present, only `--keyring-provider subprocess` is supported, which configures uv to use the `keyring` CLI to handle authentication.
Defaults to `disabled`.
May also be set with the `UV_KEYRING_PROVIDER` environment variable.
Possible values:
  * `disabled`: Do not use keyring for credential lookup
  * `subprocess`: Use the `keyring` command for credential lookup



[`--link-mode`](https://docs.astral.sh/uv/reference/cli/#uv-run--link-mode) _link-mode_ 
    
The method to use when installing packages from the global cache.
Defaults to `clone` (also known as Copy-on-Write) on macOS and Linux, and `hardlink` on Windows.
WARNING: The use of symlink link mode is discouraged, as they create tight coupling between the cache and the target environment. For example, clearing the cache (`uv cache clean`) will break all installed packages by way of removing the underlying source files. Use symlinks with caution.
May also be set with the `UV_LINK_MODE` environment variable.
Possible values:
  * `clone`: Clone (i.e., copy-on-write) packages from the source into the destination
  * `copy`: Copy packages from the source into the destination
  * `hardlink`: Hard link packages from the source into the destination
  * `symlink`: Symbolically link packages from the source into the destination

    
Assert that the `uv.lock` will remain unchanged [env: UV_LOCKED=]
Requires that the lockfile is up-to-date. If the lockfile is missing or needs to be updated, uv will exit with an error.     
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions.     
Run a Python module.
Equivalent to `python -m <module>`.     
Don't install pre-built wheels.
The given packages will be built and installed from source. The resolver will still use pre-built wheels to extract package metadata, if available.
May also be set with the `UV_NO_BINARY` environment variable. 

[`--no-binary-package`](https://docs.astral.sh/uv/reference/cli/#uv-run--no-binary-package) _no-binary-package_ 
    
Don't install pre-built wheels for a specific package [env: `UV_NO_BINARY_PACKAGE`=]     
Don't build source distributions.
When enabled, uv will reuse cached wheels from previously built source distributions, but operations that require building a source distribution will exit with an error. First-party packages, such as projects in the workspace, will still be built. uv will also still build editable requirements, and their build backends may run arbitrary Python code.
May also be set with the `UV_NO_BUILD` environment variable. 

[`--no-build-isolation`](https://docs.astral.sh/uv/reference/cli/#uv-run--no-build-isolation)
    
Disable isolation when building source distributions.
Assumes that build dependencies specified by PEP 518 are already installed.
May also be set with the `UV_NO_BUILD_ISOLATION` environment variable. 

[`--no-build-isolation-package`](https://docs.astral.sh/uv/reference/cli/#uv-run--no-build-isolation-package) _no-build-isolation-package_ 
    
Disable isolation when building source distributions for a specific package.
Assumes that the packages' build dependencies specified by PEP 518 are already installed. 

[`--no-build-package`](https://docs.astral.sh/uv/reference/cli/#uv-run--no-build-package) _no-build-package_ 
    
Don't build source distributions for a specific package [env: `UV_NO_BUILD_PACKAGE`=]
First-party packages, such as projects in the workspace, will still be built. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-run--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable. 

[`--no-default-groups`](https://docs.astral.sh/uv/reference/cli/#uv-run--no-default-groups)
    
Ignore the default dependency groups.
uv includes the groups defined in `tool.uv.default-groups` by default. This disables that option, however, specific groups can still be included with `--group`.
May also be set with the `UV_NO_DEFAULT_GROUPS` environment variable.     
Disable the development dependency group [env: UV_NO_DEV=]
This option is an alias of `--no-group dev`. See `--no-default-groups` to disable all default groups instead.
This option is only available when running in a project.     
Install any editable dependencies, including the project and any workspace members, as non-editable [env: UV_NO_EDITABLE=] 

[`--no-editable-package`](https://docs.astral.sh/uv/reference/cli/#uv-run--no-editable-package) _no-editable-package_ 
    
Install the specified editable packages as non-editable     
Avoid reading environment variables from a `.env` file [env: UV_NO_ENV_FILE=] 

[`--no-extra`](https://docs.astral.sh/uv/reference/cli/#uv-run--no-extra) _no-extra_ 
    
Exclude the specified optional dependencies, if `--all-extras` is supplied.
May be provided multiple times. 

[`--no-group`](https://docs.astral.sh/uv/reference/cli/#uv-run--no-group) _no-group_ 
    
Disable the specified dependency group [env: `UV_NO_GROUP`=]
This option always takes precedence over default groups, `--all-groups`, and `--group`.
May be provided multiple times.     
Ignore the registry index (e.g., PyPI), instead relying on direct URL dependencies and those provided via `--find-links` 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-run--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-project`](https://docs.astral.sh/uv/reference/cli/#uv-run--no-project), `--no_workspace` 
    
Avoid discovering the project or workspace.
Instead of searching for projects in the current directory and parent directories, run in an isolated, ephemeral environment populated by the `--with` requirements.
If a virtual environment is active or found in a current or parent directory, it will be used as if there was no project or workspace.
May also be set with the `UV_NO_PROJECT` environment variable. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-run--no-python-downloads)
    
Disable automatic downloads of Python.     
Ignore the `tool.uv.sources` table when resolving dependencies. Used to lock against the standards-compliant, publishable package metadata, as opposed to using any workspace, Git, URL, or local path sources
May also be set with the `UV_NO_SOURCES` environment variable. 

[`--no-sources-package`](https://docs.astral.sh/uv/reference/cli/#uv-run--no-sources-package) _no-sources-package_ 
    
Don't use sources from the `tool.uv.sources` table for the specified packages [env: `UV_NO_SOURCES_PACKAGE`=]     
Avoid syncing the virtual environment [env: UV_NO_SYNC=]
Implies `--frozen`, as the project dependencies will be ignored (i.e., the lockfile will not be updated, since the environment will not be synced regardless).     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files.     
Only include the development dependency group.
The project and its dependencies will be omitted.
This option is an alias for `--only-group dev`. Implies `--no-default-groups`. 

[`--only-group`](https://docs.astral.sh/uv/reference/cli/#uv-run--only-group) _only-group_ 
    
Only include dependencies from the specified dependency group.
The project and its dependencies will be omitted.
May be provided multiple times. Implies `--no-default-groups`. 

[`--package`](https://docs.astral.sh/uv/reference/cli/#uv-run--package) _package_ 
    
Run the command in a specific package in the workspace.
If the workspace member does not exist, uv will exit with an error. 

[`--prerelease`](https://docs.astral.sh/uv/reference/cli/#uv-run--prerelease) _prerelease_ 
    
The strategy to use when considering pre-release versions.
By default, uv will prefer stable candidates, falling back to pre-releases only after every stable candidate that satisfies the active constraints is rejected (`if-necessary`).
May also be set with the `UV_PRERELEASE` environment variable.
Possible values:
  * `disallow`: Disallow all pre-release versions
  * `allow`: Allow all pre-release versions
  * `if-necessary`: Prefer stable versions, falling back to pre-release versions when necessary
  * `explicit`: Prefer stable versions for first-party packages with explicit pre-release specifiers, falling back to pre-release versions when necessary. Disallow pre-release versions for all other packages
  * `if-necessary-or-explicit`: Deprecated alias for `if-necessary`



[`--prerelease-package`](https://docs.astral.sh/uv/reference/cli/#uv-run--prerelease-package) _prerelease-package_ 
    
The strategy to use when considering pre-release versions for a specific package.
Accepts package-mode pairs in the format `PACKAGE=MODE`, where `MODE` is any value accepted by `--prerelease`.
May be provided multiple times for different packages. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-run--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable. 

[`--python`](https://docs.astral.sh/uv/reference/cli/#uv-run--python), `-p` _python_ 
    
The Python interpreter to use for the run environment.
If the interpreter request is satisfied by a discovered environment, the environment will be used.
See [uv python](https://docs.astral.sh/uv/reference/cli/#uv-python) to view supported request formats.
May also be set with the `UV_PYTHON` environment variable. 

[`--python-platform`](https://docs.astral.sh/uv/reference/cli/#uv-run--python-platform) _python-platform_ 
    
The platform for which requirements should be installed.
Represented as a "target triple", a string that describes the target platform in terms of its CPU, vendor, and operating system name, like `x86_64-unknown-linux-gnu` or `aarch64-apple-darwin`.
When targeting macOS (Darwin), the default minimum version is `13.0`. Use `MACOSX_DEPLOYMENT_TARGET` to specify a different minimum version, e.g., `14.0`.
When targeting iOS, the default minimum version is `13.0`. Use `IPHONEOS_DEPLOYMENT_TARGET` to specify a different minimum version, e.g., `14.0`.
When targeting Android, the default minimum Android API level is `24`. Use `ANDROID_API_LEVEL` to specify a different minimum version, e.g., `26`.
WARNING: When specified, uv will select wheels that are compatible with the _target_ platform; as a result, the installed distributions may not be compatible with the _current_ platform. Conversely, any distributions that are built from source may be incompatible with the _target_ platform, as they will be built for the _current_ platform. The `--python-platform` option is intended for advanced use cases.
Possible values:
  * `windows`: An alias for `x86_64-pc-windows-msvc`, the default target for Windows
  * `linux`: An alias for `x86_64-unknown-linux-gnu`, the default target for Linux
  * `macos`: An alias for `aarch64-apple-darwin`, the default target for macOS
  * `x86_64-pc-windows-msvc`: A 64-bit x86 Windows target
  * `aarch64-pc-windows-msvc`: An ARM64 Windows target
  * `i686-pc-windows-msvc`: A 32-bit x86 Windows target
  * `x86_64-unknown-linux-gnu`: An x86 Linux target. Equivalent to `x86_64-manylinux_2_28`
  * `aarch64-apple-darwin`: An ARM-based macOS target, as seen on Apple Silicon devices
  * `x86_64-apple-darwin`: An x86 macOS target
  * `aarch64-unknown-linux-gnu`: An ARM64 Linux target. Equivalent to `aarch64-manylinux_2_28`
  * `aarch64-unknown-linux-musl`: An ARM64 Linux target
  * `x86_64-unknown-linux-musl`: An `x86_64` Linux target
  * `riscv64-unknown-linux`: A RISCV64 Linux target
  * `x86_64-manylinux2014`: An `x86_64` target for the `manylinux2014` platform. Equivalent to `x86_64-manylinux_2_17`
  * `x86_64-manylinux_2_17`: An `x86_64` target for the `manylinux_2_17` platform
  * `x86_64-manylinux_2_28`: An `x86_64` target for the `manylinux_2_28` platform
  * `x86_64-manylinux_2_31`: An `x86_64` target for the `manylinux_2_31` platform
  * `x86_64-manylinux_2_32`: An `x86_64` target for the `manylinux_2_32` platform
  * `x86_64-manylinux_2_33`: An `x86_64` target for the `manylinux_2_33` platform
  * `x86_64-manylinux_2_34`: An `x86_64` target for the `manylinux_2_34` platform
  * `x86_64-manylinux_2_35`: An `x86_64` target for the `manylinux_2_35` platform
  * `x86_64-manylinux_2_36`: An `x86_64` target for the `manylinux_2_36` platform
  * `x86_64-manylinux_2_37`: An `x86_64` target for the `manylinux_2_37` platform
  * `x86_64-manylinux_2_38`: An `x86_64` target for the `manylinux_2_38` platform
  * `x86_64-manylinux_2_39`: An `x86_64` target for the `manylinux_2_39` platform
  * `x86_64-manylinux_2_40`: An `x86_64` target for the `manylinux_2_40` platform
  * `aarch64-manylinux2014`: An ARM64 target for the `manylinux2014` platform. Equivalent to `aarch64-manylinux_2_17`
  * `aarch64-manylinux_2_17`: An ARM64 target for the `manylinux_2_17` platform
  * `aarch64-manylinux_2_28`: An ARM64 target for the `manylinux_2_28` platform
  * `aarch64-manylinux_2_31`: An ARM64 target for the `manylinux_2_31` platform
  * `aarch64-manylinux_2_32`: An ARM64 target for the `manylinux_2_32` platform
  * `aarch64-manylinux_2_33`: An ARM64 target for the `manylinux_2_33` platform
  * `aarch64-manylinux_2_34`: An ARM64 target for the `manylinux_2_34` platform
  * `aarch64-manylinux_2_35`: An ARM64 target for the `manylinux_2_35` platform
  * `aarch64-manylinux_2_36`: An ARM64 target for the `manylinux_2_36` platform
  * `aarch64-manylinux_2_37`: An ARM64 target for the `manylinux_2_37` platform
  * `aarch64-manylinux_2_38`: An ARM64 target for the `manylinux_2_38` platform
  * `aarch64-manylinux_2_39`: An ARM64 target for the `manylinux_2_39` platform
  * `aarch64-manylinux_2_40`: An ARM64 target for the `manylinux_2_40` platform
  * `aarch64-linux-android`: An ARM64 Android target
  * `x86_64-linux-android`: An `x86_64` Android target
  * `wasm32-pyodide2024`: A wasm32 target using the Pyodide 2024 platform. Meant for use with Python 3.12. See <https://pyodide.org/en/stable/development/abi/312.html>
  * `wasm32-pyodide2025`: A wasm32 target using the Pyodide 2025 platform. Meant for use with Python 3.13. See <https://pyodide.org/en/stable/development/abi/313.html>
  * `arm64-apple-ios`: An ARM64 target for iOS device
  * `arm64-apple-ios-simulator`: An ARM64 target for iOS simulator
  * `x86_64-apple-ios-simulator`: An `x86_64` target for iOS simulator

    
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Refresh all cached data 

[`--refresh-package`](https://docs.astral.sh/uv/reference/cli/#uv-run--refresh-package) _refresh-package_ 
    
Refresh cached data for a specific package 

[`--reinstall`](https://docs.astral.sh/uv/reference/cli/#uv-run--reinstall), `--force-reinstall` 
    
Reinstall all packages, regardless of whether they're already installed. Implies `--refresh` 

[`--reinstall-package`](https://docs.astral.sh/uv/reference/cli/#uv-run--reinstall-package) _reinstall-package_ 
    
Reinstall a specific package, regardless of whether it's already installed. Implies `--refresh-package` 

[`--resolution`](https://docs.astral.sh/uv/reference/cli/#uv-run--resolution) _resolution_ 
    
The strategy to use when selecting between the different compatible versions for a given package requirement.
By default, uv will use the latest compatible version of each package (`highest`).
May also be set with the `UV_RESOLUTION` environment variable.
Possible values:
  * `highest`: Resolve the highest compatible version of each package
  * `lowest`: Resolve the lowest compatible version of each package
  * `lowest-direct`: Resolve the lowest compatible version of any direct dependencies, and the highest compatible version of any transitive dependencies

    
Run the given path as a Python script.
Using `--script` will attempt to parse the path as a PEP 723 script, irrespective of its extension.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store.     
Allow package upgrades, ignoring pinned versions in any existing output file. Implies `--refresh` 

[`--upgrade-group`](https://docs.astral.sh/uv/reference/cli/#uv-run--upgrade-group) _upgrade-group_ 
    
Allow upgrades for all packages in a dependency group, ignoring pinned versions in any existing output file 

[`--upgrade-package`](https://docs.astral.sh/uv/reference/cli/#uv-run--upgrade-package), `-P` _upgrade-package_ 
    
Allow upgrades for a specific package, ignoring pinned versions in any existing output file. Implies `--refresh-package`     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>) 

[`--with`](https://docs.astral.sh/uv/reference/cli/#uv-run--with), `-w` _with_ 
    
Run with the given packages installed.
When used in a project, these dependencies will be layered on top of the project environment in a separate, ephemeral environment. These dependencies are allowed to conflict with those specified by the project. 

[`--with-editable`](https://docs.astral.sh/uv/reference/cli/#uv-run--with-editable) _with-editable_ 
    
Run with the given packages installed in editable mode.
When used in a project, these dependencies will be layered on top of the project environment in a separate, ephemeral environment. These dependencies are allowed to conflict with those specified by the project. 

[`--with-requirements`](https://docs.astral.sh/uv/reference/cli/#uv-run--with-requirements) _with-requirements_ 
    
Run with the packages listed in the given files.
The following formats are supported: `requirements.txt`, `.py` files with inline metadata, and `pylock.toml`.
The same environment semantics as `--with` apply.
Using `pyproject.toml`, `setup.py`, or `setup.cfg` files is not allowed.
## [uv init](https://docs.astral.sh/uv/reference/cli/#uv-init)
Create a new project.
Follows the `pyproject.toml` specification.
If a `pyproject.toml` already exists at the target, uv will exit with an error.
If a `pyproject.toml` is found in any of the parent directories of the target path, the project will be added as a workspace member of the parent.
Some project state is not created until needed, e.g., the project virtual environment (`.venv`) and lockfile (`uv.lock`) are lazily created during the first sync.
### Usage

```
uv init [OPTIONS] [PATH]

```

### Arguments     
The path to use for the project/script.
Defaults to the current working directory when initializing an app or library; required when initializing a script. Accepts relative and absolute paths.
If a `pyproject.toml` is found in any of the parent directories of the target path, the project will be added as a workspace member of the parent, unless `--no-workspace` is provided.
### Options 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-init--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--app`](https://docs.astral.sh/uv/reference/cli/#uv-init--app), `--application` 
    
Create a project for an application.
This project kind is for web servers, scripts, and command-line interfaces.
Applications are packaged by default. Use `--no-package` to create an unpackaged application. 

[`--author-from`](https://docs.astral.sh/uv/reference/cli/#uv-init--author-from) _author-from_ 
    
Fill in the `authors` field in the `pyproject.toml`.
By default, uv will attempt to infer the author information from some sources (e.g., Git) (`auto`). Use `--author-from git` to only infer from Git configuration. Use `--author-from none` to avoid inferring the author information.
Possible values:
  * `auto`: Fetch the author information from some sources (e.g., Git) automatically
  * `git`: Fetch the author information from Git configuration only
  * `none`: Do not infer the author information

    
Only create a `pyproject.toml`.
Disables creating extra files like `README.md`, the `src/` tree, `.python-version` files, etc.
A `[build-system]` table is only created with `--package` or `--build-backend`.
When combined with `--script`, the script will only contain the inline metadata header. 

[`--build-backend`](https://docs.astral.sh/uv/reference/cli/#uv-init--build-backend) _build-backend_ 
    
Initialize a build-backend of choice for the project.
Implicitly sets `--package`.
May also be set with the `UV_INIT_BUILD_BACKEND` environment variable.
Possible values:
  * `uv`: Use uv as the project build backend
  * `hatch`: Use [hatchling](https://pypi.org/project/hatchling) as the project build backend
  * `flit`: Use [flit-core](https://pypi.org/project/flit-core) as the project build backend
  * `pdm`: Use [pdm-backend](https://pypi.org/project/pdm-backend) as the project build backend
  * `poetry`: Use [poetry-core](https://pypi.org/project/poetry-core) as the project build backend
  * `setuptools`: Use [setuptools](https://pypi.org/project/setuptools) as the project build backend
  * `maturin`: Use [maturin](https://pypi.org/project/maturin) as the project build backend
  * `scikit`: Use [scikit-build-core](https://pypi.org/project/scikit-build-core) as the project build backend



[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-init--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-init--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-init--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--description`](https://docs.astral.sh/uv/reference/cli/#uv-init--description) _description_ 
    
Set the project description 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-init--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable.     
Display the concise help for this command 

[`--lib`](https://docs.astral.sh/uv/reference/cli/#uv-init--lib), `--library` 
    
Create a project for a library.
A library is a project that is intended to be built and distributed as a Python package.     
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions. 

[`--name`](https://docs.astral.sh/uv/reference/cli/#uv-init--name) _name_ 
    
The name of the project.
Defaults to the name of the directory. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-init--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable.     
Disable the description for the project 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-init--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Do not set up the project to be built as a Python package.
This option creates the project structure as a flat directory that is not importable as a module and has no `[build-system]` entry. It can be used for applications that are not expected to be distributed as a package.     
Do not create a `.python-version` file for the project.
By default, uv will create a `.python-version` file containing the minor version of the discovered Python interpreter, which will cause subsequent uv commands to use that version.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-init--no-python-downloads)
    
Disable automatic downloads of Python.     
Do not create a `README.md` file 

[`--no-workspace`](https://docs.astral.sh/uv/reference/cli/#uv-init--no-workspace), `--no-project` 
    
Avoid discovering a workspace and create a standalone project.
By default, uv searches for workspaces in the current directory or any parent directory.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files.     
Set up the project to be built as a Python package.
Defines a `[build-system]` for the project.
This is the default behavior. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-init--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable. 

[`--python`](https://docs.astral.sh/uv/reference/cli/#uv-init--python), `-p` _python_ 
    
The Python interpreter to use to determine the minimum supported Python version.
See [uv python](https://docs.astral.sh/uv/reference/cli/#uv-python) to view supported request formats.
May also be set with the `UV_PYTHON` environment variable.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Create a script.
A script is a standalone file with embedded metadata enumerating its dependencies, along with any Python version requirements, as defined in the PEP 723 specification.
PEP 723 scripts can be executed directly with `uv run`.
By default, adds a requirement on the system Python version; use `--python` to specify an alternative Python version requirement.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store.     
Initialize a version control system for the project.
By default, uv will initialize a Git repository (`git`). Use `--vcs none` to explicitly avoid initializing a version control system.
Possible values:
  * `git`: Use Git for version control
  * `none`: Do not use any version control system

    
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
Add dependencies to the project.
Dependencies are added to the project's `pyproject.toml` file.
If a given dependency exists already, it will be updated to the new version specifier unless it includes markers that differ from the existing specifier in which case another entry for the dependency will be added.
The lockfile and project environment will be updated to reflect the added dependencies. To skip updating the lockfile, use `--frozen`. To skip updating the environment, use `--no-sync`.
If any of the requested dependencies cannot be found, uv will exit with an error, unless the `--frozen` flag is provided, in which case uv will add the dependencies verbatim without checking that they exist or are compatible with the project.
uv will search for a project in the current directory or any parent directory. If a project cannot be found, uv will exit with an error.
### Usage

```
uv add [OPTIONS] <PACKAGES|--requirements <REQUIREMENTS>>

```

### Arguments     
The packages to add, as PEP 508 requirements (e.g., `ruff==0.5.0`)
### Options     
Prefer the active virtual environment over the project's virtual environment.
If the project virtual environment is active or no virtual environment is active, this has no effect. 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-add--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--bounds`](https://docs.astral.sh/uv/reference/cli/#uv-add--bounds) _bounds_ 
    
The kind of version specifier to use when adding dependencies.
When adding a dependency to the project, if no constraint or URL is provided, a constraint is added based on the latest compatible version of the package. By default, a lower bound constraint is used, e.g., `>=1.2.3`.
When `--frozen` is provided, no resolution is performed, and dependencies are always added without constraints.
This option is in preview and may change in any future release.
Possible values:
  * `lower`: Only a lower bound, e.g., `>=1.2.3`
  * `major`: Allow the same major version, similar to the semver caret, e.g., `>=1.2.3, <2.0.0`
  * `minor`: Allow the same minor version, similar to the semver tilde, e.g., `>=1.2.3, <1.3.0`
  * `exact`: Pin the exact version, e.g., `==1.2.3`



[`--branch`](https://docs.astral.sh/uv/reference/cli/#uv-add--branch) _branch_ 
    
Branch to use when adding a dependency from Git 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-add--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-add--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--compile-bytecode`](https://docs.astral.sh/uv/reference/cli/#uv-add--compile-bytecode), `--compile` 
    
Compile Python files to bytecode after installation.
By default, uv does not compile Python (`.py`) files to bytecode (`__pycache__/*.pyc`); instead, compilation is performed lazily the first time a module is imported. For use-cases in which start time is critical, such as CLI applications and Docker containers, this option can be enabled to trade longer installation times for faster start times.
When enabled, install operations (e.g., `uv pip install`) will compile installed or reinstalled Python files. Commands that perform a sync operation (e.g., `uv sync` or `uv run`) will process the entire site-packages directory including packages that are not being modified.
May also be set with the `UV_COMPILE_BYTECODE` environment variable. 

[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-add--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--config-setting`](https://docs.astral.sh/uv/reference/cli/#uv-add--config-setting), `--config-settings`, `-C` _config-setting_ 
    
Settings to pass to the PEP 517 build backend, specified as `KEY=VALUE` pairs 

[`--config-settings-package`](https://docs.astral.sh/uv/reference/cli/#uv-add--config-settings-package), `--config-settings-package` _config-settings-package_ 
    
Settings to pass to the PEP 517 build backend for a specific package, specified as `PACKAGE:KEY=VALUE` pairs 

[`--constraints`](https://docs.astral.sh/uv/reference/cli/#uv-add--constraints), `--constraint`, `-c` _constraints_ 
    
Constrain versions using the given requirements files.
Constraints files are `requirements.txt`-like files that only control the _version_ of a requirement that's installed. The constraints will _not_ be added to the project's `pyproject.toml` file, but _will_ be respected during dependency resolution.
This is equivalent to pip's `--constraint` option.
May also be set with the `UV_CONSTRAINT` environment variable. 

[`--default-index`](https://docs.astral.sh/uv/reference/cli/#uv-add--default-index) _default-index_ 
    
The default package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--index` flag.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
May also be set with the `UV_DEFAULT_INDEX` environment variable.     
Add the requirements to the development dependency group [env: UV_DEV=]
This option is an alias for `--group dev`. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-add--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable.     
Add the requirements as editable 

[`--exclude-newer`](https://docs.astral.sh/uv/reference/cli/#uv-add--exclude-newer) _exclude-newer_ 
    
Limit candidate packages to those that were uploaded prior to the given date.
The date is compared against the upload time of each individual distribution artifact (i.e., when each file was uploaded to the package index), not the release date of the package version.
Accepts RFC 3339 timestamps (e.g., `2006-12-02T02:07:43Z`), local dates in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Use `false` to disable `exclude-newer`.
May also be set with the `UV_EXCLUDE_NEWER` environment variable. 

[`--exclude-newer-package`](https://docs.astral.sh/uv/reference/cli/#uv-add--exclude-newer-package) _exclude-newer-package_ 
    
Limit candidate packages for specific packages to those that were uploaded prior to the given date.
Accepts package-date pairs in the format `PACKAGE=DATE`, where `DATE` is an RFC 3339 timestamp (e.g., `2006-12-02T02:07:43Z`), a local date in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Can be provided multiple times for different packages. 

[`--extra`](https://docs.astral.sh/uv/reference/cli/#uv-add--extra) _extra_ 
    
Extras to enable for the dependency.
May be provided more than once.
To add this dependency to an optional extra instead, see `--optional`. 

[`--extra-index-url`](https://docs.astral.sh/uv/reference/cli/#uv-add--extra-index-url) _extra-index-url_ 
    
(Deprecated: use `--index` instead) Extra URLs of package indexes to use, in addition to `--index-url`.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--index-url` (which defaults to PyPI). When multiple `--extra-index-url` flags are provided, earlier values take priority.
May also be set with the `UV_EXTRA_INDEX_URL` environment variable. 

[`--find-links`](https://docs.astral.sh/uv/reference/cli/#uv-add--find-links), `-f` _find-links_ 
    
Locations to search for candidate distributions, in addition to those found in the registry indexes.
If a path, the target must be a directory that contains packages as wheel files (`.whl`) or source distributions (e.g., `.tar.gz` or `.zip`) at the top level.
If a URL, the page must contain a flat list of links to package files adhering to the formats described above.
May also be set with the `UV_FIND_LINKS` environment variable. 

[`--fork-strategy`](https://docs.astral.sh/uv/reference/cli/#uv-add--fork-strategy) _fork-strategy_ 
    
The strategy to use when selecting multiple versions of a given package across Python versions and platforms.
By default, uv will optimize for selecting the latest version of each package for each supported Python version (`requires-python`), while minimizing the number of selected versions across platforms.
Under `fewest`, uv will minimize the number of selected versions for each package, preferring older versions that are compatible with a wider range of supported Python versions or platforms.
May also be set with the `UV_FORK_STRATEGY` environment variable.
Possible values:
  * `fewest`: Optimize for selecting the fewest number of versions for each package. Older versions may be preferred if they are compatible with a wider range of supported Python versions or platforms
  * `requires-python`: Optimize for selecting latest supported version of each package, for each supported Python version

    
Add dependencies without re-locking the project [env: UV_FROZEN=]
The project environment will not be synced. 

[`--group`](https://docs.astral.sh/uv/reference/cli/#uv-add--group) _group_ 
    
Add the requirements to the specified dependency group.
These requirements will not be included in the published metadata for the project.     
Display the concise help for this command 

[`--index`](https://docs.astral.sh/uv/reference/cli/#uv-add--index) _index_ 
    
The indexes to use when resolving dependencies, in addition to the default index.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--default-index` (which defaults to PyPI). When multiple `--index` flags are provided, earlier values take priority.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
Relative paths can be disambiguated from index names with `./` or `../` on Unix or `.\\`, `..\\`, `./` or `../` on Windows.
May also be set with the `UV_INDEX` environment variable. 

[`--index-strategy`](https://docs.astral.sh/uv/reference/cli/#uv-add--index-strategy) _index-strategy_ 
    
The strategy to use when resolving against multiple index URLs.
By default, uv will stop at the first index on which a given package is available, and limit resolutions to those present on that first index (`first-index`). This prevents "dependency confusion" attacks, whereby an attacker can upload a malicious package under the same name to an alternate index.
May also be set with the `UV_INDEX_STRATEGY` environment variable.
Possible values:
  * `first-index`: Only use results from the first index that returns a match for a given package name
  * `unsafe-first-match`: Search for every package name across all indexes, exhausting the versions from the first index before moving on to the next
  * `unsafe-best-match`: Search for every package name across all indexes, preferring the "best" version found. If a package version is in multiple indexes, only look at the entry for the first index



[`--index-url`](https://docs.astral.sh/uv/reference/cli/#uv-add--index-url), `-i` _index-url_ 
    
(Deprecated: use `--default-index` instead) The URL of the Python package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--extra-index-url` flag.
May also be set with the `UV_INDEX_URL` environment variable. 

[`--keyring-provider`](https://docs.astral.sh/uv/reference/cli/#uv-add--keyring-provider) _keyring-provider_ 
    
Attempt to use `keyring` for authentication for index URLs.
At present, only `--keyring-provider subprocess` is supported, which configures uv to use the `keyring` CLI to handle authentication.
Defaults to `disabled`.
May also be set with the `UV_KEYRING_PROVIDER` environment variable.
Possible values:
  * `disabled`: Do not use keyring for credential lookup
  * `subprocess`: Use the `keyring` command for credential lookup

    
Whether to use Git LFS when adding a dependency from Git 

[`--link-mode`](https://docs.astral.sh/uv/reference/cli/#uv-add--link-mode) _link-mode_ 
    
The method to use when installing packages from the global cache.
Defaults to `clone` (also known as Copy-on-Write) on macOS and Linux, and `hardlink` on Windows.
WARNING: The use of symlink link mode is discouraged, as they create tight coupling between the cache and the target environment. For example, clearing the cache (`uv cache clean`) will break all installed packages by way of removing the underlying source files. Use symlinks with caution.
May also be set with the `UV_LINK_MODE` environment variable.
Possible values:
  * `clone`: Clone (i.e., copy-on-write) packages from the source into the destination
  * `copy`: Copy packages from the source into the destination
  * `hardlink`: Hard link packages from the source into the destination
  * `symlink`: Symbolically link packages from the source into the destination

    
Assert that the `uv.lock` will remain unchanged [env: UV_LOCKED=]
Requires that the lockfile is up-to-date. If the lockfile is missing or needs to be updated, uv will exit with an error.     
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions. 

[`--marker`](https://docs.astral.sh/uv/reference/cli/#uv-add--marker), `-m` _marker_ 
    
Apply this marker to all added packages     
Don't install pre-built wheels.
The given packages will be built and installed from source. The resolver will still use pre-built wheels to extract package metadata, if available.
May also be set with the `UV_NO_BINARY` environment variable. 

[`--no-binary-package`](https://docs.astral.sh/uv/reference/cli/#uv-add--no-binary-package) _no-binary-package_ 
    
Don't install pre-built wheels for a specific package [env: `UV_NO_BINARY_PACKAGE`=]     
Don't build source distributions.
When enabled, uv will reuse cached wheels from previously built source distributions, but operations that require building a source distribution will exit with an error. First-party packages, such as projects in the workspace, will still be built. uv will also still build editable requirements, and their build backends may run arbitrary Python code.
May also be set with the `UV_NO_BUILD` environment variable. 

[`--no-build-isolation`](https://docs.astral.sh/uv/reference/cli/#uv-add--no-build-isolation)
    
Disable isolation when building source distributions.
Assumes that build dependencies specified by PEP 518 are already installed.
May also be set with the `UV_NO_BUILD_ISOLATION` environment variable. 

[`--no-build-isolation-package`](https://docs.astral.sh/uv/reference/cli/#uv-add--no-build-isolation-package) _no-build-isolation-package_ 
    
Disable isolation when building source distributions for a specific package.
Assumes that the packages' build dependencies specified by PEP 518 are already installed. 

[`--no-build-package`](https://docs.astral.sh/uv/reference/cli/#uv-add--no-build-package) _no-build-package_ 
    
Don't build source distributions for a specific package [env: `UV_NO_BUILD_PACKAGE`=]
First-party packages, such as projects in the workspace, will still be built. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-add--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable.     
Ignore the registry index (e.g., PyPI), instead relying on direct URL dependencies and those provided via `--find-links` 

[`--no-install-local`](https://docs.astral.sh/uv/reference/cli/#uv-add--no-install-local)
    
Do not install local path dependencies [env: UV_NO_INSTALL_LOCAL=]
Skips the current project, workspace members, and any other local (path or editable) packages. Only remote/indexed dependencies are installed. Useful in Docker builds to cache heavy third-party dependencies first and layer local packages separately.
The inverse `--only-install-local` can be used to install _only_ local packages, excluding all remote dependencies. 

[`--no-install-package`](https://docs.astral.sh/uv/reference/cli/#uv-add--no-install-package) _no-install-package_ 
    
Do not install the given package(s).
By default, all project's dependencies are installed into the environment. The `--no-install-package` option allows exclusion of specific packages. Note this can result in a broken environment, and should be used with caution.
The inverse `--only-install-package` can be used to install _only_ the specified packages, excluding all others. 

[`--no-install-project`](https://docs.astral.sh/uv/reference/cli/#uv-add--no-install-project)
    
Do not install the current project [env: UV_NO_INSTALL_PROJECT=]
By default, the current project is installed into the environment with all of its dependencies. The `--no-install-project` option allows the project to be excluded, but all of its dependencies are still installed. This is particularly useful in situations like building Docker images where installing the project separately from its dependencies allows optimal layer caching.
The inverse `--only-install-project` can be used to install _only_ the project itself, excluding all dependencies. 

[`--no-install-workspace`](https://docs.astral.sh/uv/reference/cli/#uv-add--no-install-workspace)
    
Do not install any workspace members, including the current project [env: UV_NO_INSTALL_WORKSPACE=]
By default, all workspace members and their dependencies are installed into the environment. The `--no-install-workspace` option allows exclusion of all the workspace members while retaining their dependencies. This is particularly useful in situations like building Docker images where installing the workspace separately from its dependencies allows optimal layer caching.
The inverse `--only-install-workspace` can be used to install _only_ workspace members, excluding all other dependencies. 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-add--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-add--no-python-downloads)
    
Disable automatic downloads of Python.     
Ignore the `tool.uv.sources` table when resolving dependencies. Used to lock against the standards-compliant, publishable package metadata, as opposed to using any workspace, Git, URL, or local path sources
May also be set with the `UV_NO_SOURCES` environment variable. 

[`--no-sources-package`](https://docs.astral.sh/uv/reference/cli/#uv-add--no-sources-package) _no-sources-package_ 
    
Don't use sources from the `tool.uv.sources` table for the specified packages [env: `UV_NO_SOURCES_PACKAGE`=]     
Avoid syncing the virtual environment [env: UV_NO_SYNC=]     
Don't add the dependency as a workspace member.
By default, when adding a dependency that's a local path and is within the workspace directory, uv will add it as a workspace member; pass `--no-workspace` to add the package as direct path dependency instead.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--optional`](https://docs.astral.sh/uv/reference/cli/#uv-add--optional) _optional_ 
    
Add the requirements to the package's optional dependencies for the specified extra.
The group may then be activated when installing the project with the `--extra` flag.
To enable an optional extra for this requirement instead, see `--extra`. 

[`--package`](https://docs.astral.sh/uv/reference/cli/#uv-add--package) _package_ 
    
Add the dependency to a specific package in the workspace 

[`--prerelease`](https://docs.astral.sh/uv/reference/cli/#uv-add--prerelease) _prerelease_ 
    
The strategy to use when considering pre-release versions.
By default, uv will prefer stable candidates, falling back to pre-releases only after every stable candidate that satisfies the active constraints is rejected (`if-necessary`).
May also be set with the `UV_PRERELEASE` environment variable.
Possible values:
  * `disallow`: Disallow all pre-release versions
  * `allow`: Allow all pre-release versions
  * `if-necessary`: Prefer stable versions, falling back to pre-release versions when necessary
  * `explicit`: Prefer stable versions for first-party packages with explicit pre-release specifiers, falling back to pre-release versions when necessary. Disallow pre-release versions for all other packages
  * `if-necessary-or-explicit`: Deprecated alias for `if-necessary`



[`--prerelease-package`](https://docs.astral.sh/uv/reference/cli/#uv-add--prerelease-package) _prerelease-package_ 
    
The strategy to use when considering pre-release versions for a specific package.
Accepts package-mode pairs in the format `PACKAGE=MODE`, where `MODE` is any value accepted by `--prerelease`.
May be provided multiple times for different packages. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-add--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable. 

[`--python`](https://docs.astral.sh/uv/reference/cli/#uv-add--python), `-p` _python_ 
    
The Python interpreter to use for resolving and syncing.
See [uv python](https://docs.astral.sh/uv/reference/cli/#uv-python) for details on Python discovery and supported request formats.
May also be set with the `UV_PYTHON` environment variable.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout. 

[`--raw`](https://docs.astral.sh/uv/reference/cli/#uv-add--raw), `--raw-sources` 
    
Add a dependency as provided.
By default, uv will use the `tool.uv.sources` section to record source information for Git, local, editable, and direct URL requirements. When `--raw` is provided, uv will add source requirements to `project.dependencies`, rather than `tool.uv.sources`.
Additionally, by default, uv will add bounds to your dependency, e.g., `foo>=1.0.0`. When `--raw` is provided, uv will add the dependency without bounds.     
Refresh all cached data 

[`--refresh-package`](https://docs.astral.sh/uv/reference/cli/#uv-add--refresh-package) _refresh-package_ 
    
Refresh cached data for a specific package 

[`--reinstall`](https://docs.astral.sh/uv/reference/cli/#uv-add--reinstall), `--force-reinstall` 
    
Reinstall all packages, regardless of whether they're already installed. Implies `--refresh` 

[`--reinstall-package`](https://docs.astral.sh/uv/reference/cli/#uv-add--reinstall-package) _reinstall-package_ 
    
Reinstall a specific package, regardless of whether it's already installed. Implies `--refresh-package` 

[`--requirements`](https://docs.astral.sh/uv/reference/cli/#uv-add--requirements), `--requirement`, `-r` _requirements_ 
    
Add the packages listed in the given files.
The following formats are supported: `requirements.txt`, `.py` files with inline metadata, `pylock.toml`, `pyproject.toml`, `setup.py`, and `setup.cfg`. 

[`--resolution`](https://docs.astral.sh/uv/reference/cli/#uv-add--resolution) _resolution_ 
    
The strategy to use when selecting between the different compatible versions for a given package requirement.
By default, uv will use the latest compatible version of each package (`highest`).
May also be set with the `UV_RESOLUTION` environment variable.
Possible values:
  * `highest`: Resolve the highest compatible version of each package
  * `lowest`: Resolve the lowest compatible version of each package
  * `lowest-direct`: Resolve the lowest compatible version of any direct dependencies, and the highest compatible version of any transitive dependencies

    
Commit to use when adding a dependency from Git 

[`--script`](https://docs.astral.sh/uv/reference/cli/#uv-add--script) _script_ 
    
Add the dependency to the specified Python script, rather than to a project.
If provided, uv will add the dependency to the script's inline metadata table, in adherence with PEP 723. If no such inline metadata table is present, a new one will be created and added to the script. When executed via `uv run`, uv will create a temporary environment for the script with all inline dependencies installed.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store.     
Tag to use when adding a dependency from Git     
Allow package upgrades, ignoring pinned versions in any existing output file. Implies `--refresh` 

[`--upgrade-group`](https://docs.astral.sh/uv/reference/cli/#uv-add--upgrade-group) _upgrade-group_ 
    
Allow upgrades for all packages in a dependency group, ignoring pinned versions in any existing output file 

[`--upgrade-package`](https://docs.astral.sh/uv/reference/cli/#uv-add--upgrade-package), `-P` _upgrade-package_ 
    
Allow upgrades for a specific package, ignoring pinned versions in any existing output file. Implies `--refresh-package`     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)     
Add the dependency as a workspace member.
By default, uv will add path dependencies that are within the workspace directory as workspace members. When used with a path dependency, the package will be added to the workspace's `members` list in the root `pyproject.toml` file.
## [uv remove](https://docs.astral.sh/uv/reference/cli/#uv-remove)
Remove dependencies from the project.
Dependencies are removed from the project's `pyproject.toml` file.
If multiple entries exist for a given dependency, i.e., each with different markers, all of the entries will be removed.
The lockfile and project environment will be updated to reflect the removed dependencies. To skip updating the lockfile, use `--frozen`. To skip updating the environment, use `--no-sync`.
If any of the requested dependencies are not present in the project, uv will exit with an error.
If a package has been manually installed in the environment, i.e., with `uv pip install`, it will not be removed by `uv remove`.
uv will search for a project in the current directory or any parent directory. If a project cannot be found, uv will exit with an error.
### Usage

```
uv remove [OPTIONS] <PACKAGES>...

```

### Arguments     
The names of the dependencies to remove (e.g., `ruff`)
### Options     
Prefer the active virtual environment over the project's virtual environment.
If the project virtual environment is active or no virtual environment is active, this has no effect. 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-remove--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-remove--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-remove--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--compile-bytecode`](https://docs.astral.sh/uv/reference/cli/#uv-remove--compile-bytecode), `--compile` 
    
Compile Python files to bytecode after installation.
By default, uv does not compile Python (`.py`) files to bytecode (`__pycache__/*.pyc`); instead, compilation is performed lazily the first time a module is imported. For use-cases in which start time is critical, such as CLI applications and Docker containers, this option can be enabled to trade longer installation times for faster start times.
When enabled, install operations (e.g., `uv pip install`) will compile installed or reinstalled Python files. Commands that perform a sync operation (e.g., `uv sync` or `uv run`) will process the entire site-packages directory including packages that are not being modified.
May also be set with the `UV_COMPILE_BYTECODE` environment variable. 

[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-remove--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--config-setting`](https://docs.astral.sh/uv/reference/cli/#uv-remove--config-setting), `--config-settings`, `-C` _config-setting_ 
    
Settings to pass to the PEP 517 build backend, specified as `KEY=VALUE` pairs 

[`--config-settings-package`](https://docs.astral.sh/uv/reference/cli/#uv-remove--config-settings-package), `--config-settings-package` _config-settings-package_ 
    
Settings to pass to the PEP 517 build backend for a specific package, specified as `PACKAGE:KEY=VALUE` pairs 

[`--default-index`](https://docs.astral.sh/uv/reference/cli/#uv-remove--default-index) _default-index_ 
    
The default package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--index` flag.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
May also be set with the `UV_DEFAULT_INDEX` environment variable.     
Remove the packages from the development dependency group [env: UV_DEV=]
This option is an alias for `--group dev`. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-remove--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable. 

[`--exclude-newer`](https://docs.astral.sh/uv/reference/cli/#uv-remove--exclude-newer) _exclude-newer_ 
    
Limit candidate packages to those that were uploaded prior to the given date.
The date is compared against the upload time of each individual distribution artifact (i.e., when each file was uploaded to the package index), not the release date of the package version.
Accepts RFC 3339 timestamps (e.g., `2006-12-02T02:07:43Z`), local dates in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Use `false` to disable `exclude-newer`.
May also be set with the `UV_EXCLUDE_NEWER` environment variable. 

[`--exclude-newer-package`](https://docs.astral.sh/uv/reference/cli/#uv-remove--exclude-newer-package) _exclude-newer-package_ 
    
Limit candidate packages for specific packages to those that were uploaded prior to the given date.
Accepts package-date pairs in the format `PACKAGE=DATE`, where `DATE` is an RFC 3339 timestamp (e.g., `2006-12-02T02:07:43Z`), a local date in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Can be provided multiple times for different packages. 

[`--extra-index-url`](https://docs.astral.sh/uv/reference/cli/#uv-remove--extra-index-url) _extra-index-url_ 
    
(Deprecated: use `--index` instead) Extra URLs of package indexes to use, in addition to `--index-url`.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--index-url` (which defaults to PyPI). When multiple `--extra-index-url` flags are provided, earlier values take priority.
May also be set with the `UV_EXTRA_INDEX_URL` environment variable. 

[`--find-links`](https://docs.astral.sh/uv/reference/cli/#uv-remove--find-links), `-f` _find-links_ 
    
Locations to search for candidate distributions, in addition to those found in the registry indexes.
If a path, the target must be a directory that contains packages as wheel files (`.whl`) or source distributions (e.g., `.tar.gz` or `.zip`) at the top level.
If a URL, the page must contain a flat list of links to package files adhering to the formats described above.
May also be set with the `UV_FIND_LINKS` environment variable. 

[`--fork-strategy`](https://docs.astral.sh/uv/reference/cli/#uv-remove--fork-strategy) _fork-strategy_ 
    
The strategy to use when selecting multiple versions of a given package across Python versions and platforms.
By default, uv will optimize for selecting the latest version of each package for each supported Python version (`requires-python`), while minimizing the number of selected versions across platforms.
Under `fewest`, uv will minimize the number of selected versions for each package, preferring older versions that are compatible with a wider range of supported Python versions or platforms.
May also be set with the `UV_FORK_STRATEGY` environment variable.
Possible values:
  * `fewest`: Optimize for selecting the fewest number of versions for each package. Older versions may be preferred if they are compatible with a wider range of supported Python versions or platforms
  * `requires-python`: Optimize for selecting latest supported version of each package, for each supported Python version

    
Remove dependencies without re-locking the project [env: UV_FROZEN=]
The project environment will not be synced. 

[`--group`](https://docs.astral.sh/uv/reference/cli/#uv-remove--group) _group_ 
    
Remove the packages from the specified dependency group     
Display the concise help for this command 

[`--index`](https://docs.astral.sh/uv/reference/cli/#uv-remove--index) _index_ 
    
The indexes to use when resolving dependencies, in addition to the default index.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--default-index` (which defaults to PyPI). When multiple `--index` flags are provided, earlier values take priority.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
Relative paths can be disambiguated from index names with `./` or `../` on Unix or `.\\`, `..\\`, `./` or `../` on Windows.
May also be set with the `UV_INDEX` environment variable. 

[`--index-strategy`](https://docs.astral.sh/uv/reference/cli/#uv-remove--index-strategy) _index-strategy_ 
    
The strategy to use when resolving against multiple index URLs.
By default, uv will stop at the first index on which a given package is available, and limit resolutions to those present on that first index (`first-index`). This prevents "dependency confusion" attacks, whereby an attacker can upload a malicious package under the same name to an alternate index.
May also be set with the `UV_INDEX_STRATEGY` environment variable.
Possible values:
  * `first-index`: Only use results from the first index that returns a match for a given package name
  * `unsafe-first-match`: Search for every package name across all indexes, exhausting the versions from the first index before moving on to the next
  * `unsafe-best-match`: Search for every package name across all indexes, preferring the "best" version found. If a package version is in multiple indexes, only look at the entry for the first index



[`--index-url`](https://docs.astral.sh/uv/reference/cli/#uv-remove--index-url), `-i` _index-url_ 
    
(Deprecated: use `--default-index` instead) The URL of the Python package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--extra-index-url` flag.
May also be set with the `UV_INDEX_URL` environment variable. 

[`--keyring-provider`](https://docs.astral.sh/uv/reference/cli/#uv-remove--keyring-provider) _keyring-provider_ 
    
Attempt to use `keyring` for authentication for index URLs.
At present, only `--keyring-provider subprocess` is supported, which configures uv to use the `keyring` CLI to handle authentication.
Defaults to `disabled`.
May also be set with the `UV_KEYRING_PROVIDER` environment variable.
Possible values:
  * `disabled`: Do not use keyring for credential lookup
  * `subprocess`: Use the `keyring` command for credential lookup



[`--link-mode`](https://docs.astral.sh/uv/reference/cli/#uv-remove--link-mode) _link-mode_ 
    
The method to use when installing packages from the global cache.
Defaults to `clone` (also known as Copy-on-Write) on macOS and Linux, and `hardlink` on Windows.
WARNING: The use of symlink link mode is discouraged, as they create tight coupling between the cache and the target environment. For example, clearing the cache (`uv cache clean`) will break all installed packages by way of removing the underlying source files. Use symlinks with caution.
May also be set with the `UV_LINK_MODE` environment variable.
Possible values:
  * `clone`: Clone (i.e., copy-on-write) packages from the source into the destination
  * `copy`: Copy packages from the source into the destination
  * `hardlink`: Hard link packages from the source into the destination
  * `symlink`: Symbolically link packages from the source into the destination

    
Assert that the `uv.lock` will remain unchanged [env: UV_LOCKED=]
Requires that the lockfile is up-to-date. If the lockfile is missing or needs to be updated, uv will exit with an error.     
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions.     
Don't install pre-built wheels.
The given packages will be built and installed from source. The resolver will still use pre-built wheels to extract package metadata, if available.
May also be set with the `UV_NO_BINARY` environment variable. 

[`--no-binary-package`](https://docs.astral.sh/uv/reference/cli/#uv-remove--no-binary-package) _no-binary-package_ 
    
Don't install pre-built wheels for a specific package [env: `UV_NO_BINARY_PACKAGE`=]     
Don't build source distributions.
When enabled, uv will reuse cached wheels from previously built source distributions, but operations that require building a source distribution will exit with an error. First-party packages, such as projects in the workspace, will still be built. uv will also still build editable requirements, and their build backends may run arbitrary Python code.
May also be set with the `UV_NO_BUILD` environment variable. 

[`--no-build-isolation`](https://docs.astral.sh/uv/reference/cli/#uv-remove--no-build-isolation)
    
Disable isolation when building source distributions.
Assumes that build dependencies specified by PEP 518 are already installed.
May also be set with the `UV_NO_BUILD_ISOLATION` environment variable. 

[`--no-build-isolation-package`](https://docs.astral.sh/uv/reference/cli/#uv-remove--no-build-isolation-package) _no-build-isolation-package_ 
    
Disable isolation when building source distributions for a specific package.
Assumes that the packages' build dependencies specified by PEP 518 are already installed. 

[`--no-build-package`](https://docs.astral.sh/uv/reference/cli/#uv-remove--no-build-package) _no-build-package_ 
    
Don't build source distributions for a specific package [env: `UV_NO_BUILD_PACKAGE`=]
First-party packages, such as projects in the workspace, will still be built. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-remove--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable.     
Ignore the registry index (e.g., PyPI), instead relying on direct URL dependencies and those provided via `--find-links` 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-remove--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-remove--no-python-downloads)
    
Disable automatic downloads of Python.     
Ignore the `tool.uv.sources` table when resolving dependencies. Used to lock against the standards-compliant, publishable package metadata, as opposed to using any workspace, Git, URL, or local path sources
May also be set with the `UV_NO_SOURCES` environment variable. 

[`--no-sources-package`](https://docs.astral.sh/uv/reference/cli/#uv-remove--no-sources-package) _no-sources-package_ 
    
Don't use sources from the `tool.uv.sources` table for the specified packages [env: `UV_NO_SOURCES_PACKAGE`=]     
Avoid syncing the virtual environment after re-locking the project [env: UV_NO_SYNC=]     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--optional`](https://docs.astral.sh/uv/reference/cli/#uv-remove--optional) _optional_ 
    
Remove the packages from the project's optional dependencies for the specified extra 

[`--package`](https://docs.astral.sh/uv/reference/cli/#uv-remove--package) _package_ 
    
Remove the dependencies from a specific package in the workspace 

[`--prerelease`](https://docs.astral.sh/uv/reference/cli/#uv-remove--prerelease) _prerelease_ 
    
The strategy to use when considering pre-release versions.
By default, uv will prefer stable candidates, falling back to pre-releases only after every stable candidate that satisfies the active constraints is rejected (`if-necessary`).
May also be set with the `UV_PRERELEASE` environment variable.
Possible values:
  * `disallow`: Disallow all pre-release versions
  * `allow`: Allow all pre-release versions
  * `if-necessary`: Prefer stable versions, falling back to pre-release versions when necessary
  * `explicit`: Prefer stable versions for first-party packages with explicit pre-release specifiers, falling back to pre-release versions when necessary. Disallow pre-release versions for all other packages
  * `if-necessary-or-explicit`: Deprecated alias for `if-necessary`



[`--prerelease-package`](https://docs.astral.sh/uv/reference/cli/#uv-remove--prerelease-package) _prerelease-package_ 
    
The strategy to use when considering pre-release versions for a specific package.
Accepts package-mode pairs in the format `PACKAGE=MODE`, where `MODE` is any value accepted by `--prerelease`.
May be provided multiple times for different packages. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-remove--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable. 

[`--python`](https://docs.astral.sh/uv/reference/cli/#uv-remove--python), `-p` _python_ 
    
The Python interpreter to use for resolving and syncing.
See [uv python](https://docs.astral.sh/uv/reference/cli/#uv-python) for details on Python discovery and supported request formats.
May also be set with the `UV_PYTHON` environment variable.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Refresh all cached data 

[`--refresh-package`](https://docs.astral.sh/uv/reference/cli/#uv-remove--refresh-package) _refresh-package_ 
    
Refresh cached data for a specific package 

[`--reinstall`](https://docs.astral.sh/uv/reference/cli/#uv-remove--reinstall), `--force-reinstall` 
    
Reinstall all packages, regardless of whether they're already installed. Implies `--refresh` 

[`--reinstall-package`](https://docs.astral.sh/uv/reference/cli/#uv-remove--reinstall-package) _reinstall-package_ 
    
Reinstall a specific package, regardless of whether it's already installed. Implies `--refresh-package` 

[`--resolution`](https://docs.astral.sh/uv/reference/cli/#uv-remove--resolution) _resolution_ 
    
The strategy to use when selecting between the different compatible versions for a given package requirement.
By default, uv will use the latest compatible version of each package (`highest`).
May also be set with the `UV_RESOLUTION` environment variable.
Possible values:
  * `highest`: Resolve the highest compatible version of each package
  * `lowest`: Resolve the lowest compatible version of each package
  * `lowest-direct`: Resolve the lowest compatible version of any direct dependencies, and the highest compatible version of any transitive dependencies



[`--script`](https://docs.astral.sh/uv/reference/cli/#uv-remove--script) _script_ 
    
Remove the dependency from the specified Python script, rather than from a project.
If provided, uv will remove the dependency from the script's inline metadata table, in adherence with PEP 723.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store.     
Allow package upgrades, ignoring pinned versions in any existing output file. Implies `--refresh` 

[`--upgrade-group`](https://docs.astral.sh/uv/reference/cli/#uv-remove--upgrade-group) _upgrade-group_ 
    
Allow upgrades for all packages in a dependency group, ignoring pinned versions in any existing output file 

[`--upgrade-package`](https://docs.astral.sh/uv/reference/cli/#uv-remove--upgrade-package), `-P` _upgrade-package_ 
    
Allow upgrades for a specific package, ignoring pinned versions in any existing output file. Implies `--refresh-package`     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
## [uv version](https://docs.astral.sh/uv/reference/cli/#uv-version)
Read or update the project's version
### Usage

```
uv version [OPTIONS] [VALUE]

```

### Arguments     
Set the project version to this value
To update the project using semantic versioning components instead, use `--bump`.
### Options     
Prefer the active virtual environment over the project's virtual environment.
If the project virtual environment is active or no virtual environment is active, this has no effect. 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-version--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--bump`](https://docs.astral.sh/uv/reference/cli/#uv-version--bump) _bump[=value]_ 
    
Update the project version using the given semantics
This flag can be passed multiple times.
Possible values:
  * `major`: Increase the major version (e.g., 1.2.3 => 2.0.0)
  * `minor`: Increase the minor version (e.g., 1.2.3 => 1.3.0)
  * `patch`: Increase the patch version (e.g., 1.2.3 => 1.2.4)
  * `stable`: Move from a pre-release to stable version (e.g., 1.2.3b4.post5.dev6 => 1.2.3)
  * `alpha`: Increase the alpha version (e.g., 1.2.3a4 => 1.2.3a5)
  * `beta`: Increase the beta version (e.g., 1.2.3b4 => 1.2.3b5)
  * `rc`: Increase the rc version (e.g., 1.2.3rc4 => 1.2.3rc5)
  * `post`: Increase the post version (e.g., 1.2.3.post5 => 1.2.3.post6)
  * `dev`: Increase the dev version (e.g., 1.2.3a4.dev6 => 1.2.3.dev7)



[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-version--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-version--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--compile-bytecode`](https://docs.astral.sh/uv/reference/cli/#uv-version--compile-bytecode), `--compile` 
    
Compile Python files to bytecode after installation.
By default, uv does not compile Python (`.py`) files to bytecode (`__pycache__/*.pyc`); instead, compilation is performed lazily the first time a module is imported. For use-cases in which start time is critical, such as CLI applications and Docker containers, this option can be enabled to trade longer installation times for faster start times.
When enabled, install operations (e.g., `uv pip install`) will compile installed or reinstalled Python files. Commands that perform a sync operation (e.g., `uv sync` or `uv run`) will process the entire site-packages directory including packages that are not being modified.
May also be set with the `UV_COMPILE_BYTECODE` environment variable. 

[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-version--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--config-setting`](https://docs.astral.sh/uv/reference/cli/#uv-version--config-setting), `--config-settings`, `-C` _config-setting_ 
    
Settings to pass to the PEP 517 build backend, specified as `KEY=VALUE` pairs 

[`--config-settings-package`](https://docs.astral.sh/uv/reference/cli/#uv-version--config-settings-package), `--config-settings-package` _config-settings-package_ 
    
Settings to pass to the PEP 517 build backend for a specific package, specified as `PACKAGE:KEY=VALUE` pairs 

[`--default-index`](https://docs.astral.sh/uv/reference/cli/#uv-version--default-index) _default-index_ 
    
The default package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--index` flag.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
May also be set with the `UV_DEFAULT_INDEX` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-version--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable.     
Don't write a new version to the `pyproject.toml`
Instead, the version will be displayed. 

[`--exclude-newer`](https://docs.astral.sh/uv/reference/cli/#uv-version--exclude-newer) _exclude-newer_ 
    
Limit candidate packages to those that were uploaded prior to the given date.
The date is compared against the upload time of each individual distribution artifact (i.e., when each file was uploaded to the package index), not the release date of the package version.
Accepts RFC 3339 timestamps (e.g., `2006-12-02T02:07:43Z`), local dates in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Use `false` to disable `exclude-newer`.
May also be set with the `UV_EXCLUDE_NEWER` environment variable. 

[`--exclude-newer-package`](https://docs.astral.sh/uv/reference/cli/#uv-version--exclude-newer-package) _exclude-newer-package_ 
    
Limit candidate packages for specific packages to those that were uploaded prior to the given date.
Accepts package-date pairs in the format `PACKAGE=DATE`, where `DATE` is an RFC 3339 timestamp (e.g., `2006-12-02T02:07:43Z`), a local date in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Can be provided multiple times for different packages. 

[`--extra-index-url`](https://docs.astral.sh/uv/reference/cli/#uv-version--extra-index-url) _extra-index-url_ 
    
(Deprecated: use `--index` instead) Extra URLs of package indexes to use, in addition to `--index-url`.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--index-url` (which defaults to PyPI). When multiple `--extra-index-url` flags are provided, earlier values take priority.
May also be set with the `UV_EXTRA_INDEX_URL` environment variable. 

[`--find-links`](https://docs.astral.sh/uv/reference/cli/#uv-version--find-links), `-f` _find-links_ 
    
Locations to search for candidate distributions, in addition to those found in the registry indexes.
If a path, the target must be a directory that contains packages as wheel files (`.whl`) or source distributions (e.g., `.tar.gz` or `.zip`) at the top level.
If a URL, the page must contain a flat list of links to package files adhering to the formats described above.
May also be set with the `UV_FIND_LINKS` environment variable. 

[`--fork-strategy`](https://docs.astral.sh/uv/reference/cli/#uv-version--fork-strategy) _fork-strategy_ 
    
The strategy to use when selecting multiple versions of a given package across Python versions and platforms.
By default, uv will optimize for selecting the latest version of each package for each supported Python version (`requires-python`), while minimizing the number of selected versions across platforms.
Under `fewest`, uv will minimize the number of selected versions for each package, preferring older versions that are compatible with a wider range of supported Python versions or platforms.
May also be set with the `UV_FORK_STRATEGY` environment variable.
Possible values:
  * `fewest`: Optimize for selecting the fewest number of versions for each package. Older versions may be preferred if they are compatible with a wider range of supported Python versions or platforms
  * `requires-python`: Optimize for selecting latest supported version of each package, for each supported Python version

    
Update the version without re-locking the project [env: UV_FROZEN=]
The project environment will not be synced.     
Display the concise help for this command 

[`--index`](https://docs.astral.sh/uv/reference/cli/#uv-version--index) _index_ 
    
The indexes to use when resolving dependencies, in addition to the default index.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--default-index` (which defaults to PyPI). When multiple `--index` flags are provided, earlier values take priority.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
Relative paths can be disambiguated from index names with `./` or `../` on Unix or `.\\`, `..\\`, `./` or `../` on Windows.
May also be set with the `UV_INDEX` environment variable. 

[`--index-strategy`](https://docs.astral.sh/uv/reference/cli/#uv-version--index-strategy) _index-strategy_ 
    
The strategy to use when resolving against multiple index URLs.
By default, uv will stop at the first index on which a given package is available, and limit resolutions to those present on that first index (`first-index`). This prevents "dependency confusion" attacks, whereby an attacker can upload a malicious package under the same name to an alternate index.
May also be set with the `UV_INDEX_STRATEGY` environment variable.
Possible values:
  * `first-index`: Only use results from the first index that returns a match for a given package name
  * `unsafe-first-match`: Search for every package name across all indexes, exhausting the versions from the first index before moving on to the next
  * `unsafe-best-match`: Search for every package name across all indexes, preferring the "best" version found. If a package version is in multiple indexes, only look at the entry for the first index



[`--index-url`](https://docs.astral.sh/uv/reference/cli/#uv-version--index-url), `-i` _index-url_ 
    
(Deprecated: use `--default-index` instead) The URL of the Python package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--extra-index-url` flag.
May also be set with the `UV_INDEX_URL` environment variable. 

[`--keyring-provider`](https://docs.astral.sh/uv/reference/cli/#uv-version--keyring-provider) _keyring-provider_ 
    
Attempt to use `keyring` for authentication for index URLs.
At present, only `--keyring-provider subprocess` is supported, which configures uv to use the `keyring` CLI to handle authentication.
Defaults to `disabled`.
May also be set with the `UV_KEYRING_PROVIDER` environment variable.
Possible values:
  * `disabled`: Do not use keyring for credential lookup
  * `subprocess`: Use the `keyring` command for credential lookup



[`--link-mode`](https://docs.astral.sh/uv/reference/cli/#uv-version--link-mode) _link-mode_ 
    
The method to use when installing packages from the global cache.
Defaults to `clone` (also known as Copy-on-Write) on macOS and Linux, and `hardlink` on Windows.
WARNING: The use of symlink link mode is discouraged, as they create tight coupling between the cache and the target environment. For example, clearing the cache (`uv cache clean`) will break all installed packages by way of removing the underlying source files. Use symlinks with caution.
May also be set with the `UV_LINK_MODE` environment variable.
Possible values:
  * `clone`: Clone (i.e., copy-on-write) packages from the source into the destination
  * `copy`: Copy packages from the source into the destination
  * `hardlink`: Hard link packages from the source into the destination
  * `symlink`: Symbolically link packages from the source into the destination

    
Assert that the `uv.lock` will remain unchanged [env: UV_LOCKED=]
Requires that the lockfile is up-to-date. If the lockfile is missing or needs to be updated, uv will exit with an error.     
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions.     
Don't install pre-built wheels.
The given packages will be built and installed from source. The resolver will still use pre-built wheels to extract package metadata, if available.
May also be set with the `UV_NO_BINARY` environment variable. 

[`--no-binary-package`](https://docs.astral.sh/uv/reference/cli/#uv-version--no-binary-package) _no-binary-package_ 
    
Don't install pre-built wheels for a specific package [env: `UV_NO_BINARY_PACKAGE`=]     
Don't build source distributions.
When enabled, uv will reuse cached wheels from previously built source distributions, but operations that require building a source distribution will exit with an error. First-party packages, such as projects in the workspace, will still be built. uv will also still build editable requirements, and their build backends may run arbitrary Python code.
May also be set with the `UV_NO_BUILD` environment variable. 

[`--no-build-isolation`](https://docs.astral.sh/uv/reference/cli/#uv-version--no-build-isolation)
    
Disable isolation when building source distributions.
Assumes that build dependencies specified by PEP 518 are already installed.
May also be set with the `UV_NO_BUILD_ISOLATION` environment variable. 

[`--no-build-isolation-package`](https://docs.astral.sh/uv/reference/cli/#uv-version--no-build-isolation-package) _no-build-isolation-package_ 
    
Disable isolation when building source distributions for a specific package.
Assumes that the packages' build dependencies specified by PEP 518 are already installed. 

[`--no-build-package`](https://docs.astral.sh/uv/reference/cli/#uv-version--no-build-package) _no-build-package_ 
    
Don't build source distributions for a specific package [env: `UV_NO_BUILD_PACKAGE`=]
First-party packages, such as projects in the workspace, will still be built. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-version--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable.     
Ignore the registry index (e.g., PyPI), instead relying on direct URL dependencies and those provided via `--find-links` 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-version--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-version--no-python-downloads)
    
Disable automatic downloads of Python.     
Ignore the `tool.uv.sources` table when resolving dependencies. Used to lock against the standards-compliant, publishable package metadata, as opposed to using any workspace, Git, URL, or local path sources
May also be set with the `UV_NO_SOURCES` environment variable. 

[`--no-sources-package`](https://docs.astral.sh/uv/reference/cli/#uv-version--no-sources-package) _no-sources-package_ 
    
Don't use sources from the `tool.uv.sources` table for the specified packages [env: `UV_NO_SOURCES_PACKAGE`=]     
Avoid syncing the virtual environment after re-locking the project [env: UV_NO_SYNC=]     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--output-format`](https://docs.astral.sh/uv/reference/cli/#uv-version--output-format) _output-format_ 
    
The format of the output
[default: text]
Possible values:
  * `text`: Display the version as plain text
  * `json`: Display the version as JSON



[`--package`](https://docs.astral.sh/uv/reference/cli/#uv-version--package) _package_ 
    
Update the version of a specific package in the workspace 

[`--prerelease`](https://docs.astral.sh/uv/reference/cli/#uv-version--prerelease) _prerelease_ 
    
The strategy to use when considering pre-release versions.
By default, uv will prefer stable candidates, falling back to pre-releases only after every stable candidate that satisfies the active constraints is rejected (`if-necessary`).
May also be set with the `UV_PRERELEASE` environment variable.
Possible values:
  * `disallow`: Disallow all pre-release versions
  * `allow`: Allow all pre-release versions
  * `if-necessary`: Prefer stable versions, falling back to pre-release versions when necessary
  * `explicit`: Prefer stable versions for first-party packages with explicit pre-release specifiers, falling back to pre-release versions when necessary. Disallow pre-release versions for all other packages
  * `if-necessary-or-explicit`: Deprecated alias for `if-necessary`



[`--prerelease-package`](https://docs.astral.sh/uv/reference/cli/#uv-version--prerelease-package) _prerelease-package_ 
    
The strategy to use when considering pre-release versions for a specific package.
Accepts package-mode pairs in the format `PACKAGE=MODE`, where `MODE` is any value accepted by `--prerelease`.
May be provided multiple times for different packages. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-version--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable. 

[`--python`](https://docs.astral.sh/uv/reference/cli/#uv-version--python), `-p` _python_ 
    
The Python interpreter to use for resolving and syncing.
See [uv python](https://docs.astral.sh/uv/reference/cli/#uv-python) for details on Python discovery and supported request formats.
May also be set with the `UV_PYTHON` environment variable.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Refresh all cached data 

[`--refresh-package`](https://docs.astral.sh/uv/reference/cli/#uv-version--refresh-package) _refresh-package_ 
    
Refresh cached data for a specific package 

[`--reinstall`](https://docs.astral.sh/uv/reference/cli/#uv-version--reinstall), `--force-reinstall` 
    
Reinstall all packages, regardless of whether they're already installed. Implies `--refresh` 

[`--reinstall-package`](https://docs.astral.sh/uv/reference/cli/#uv-version--reinstall-package) _reinstall-package_ 
    
Reinstall a specific package, regardless of whether it's already installed. Implies `--refresh-package` 

[`--resolution`](https://docs.astral.sh/uv/reference/cli/#uv-version--resolution) _resolution_ 
    
The strategy to use when selecting between the different compatible versions for a given package requirement.
By default, uv will use the latest compatible version of each package (`highest`).
May also be set with the `UV_RESOLUTION` environment variable.
Possible values:
  * `highest`: Resolve the highest compatible version of each package
  * `lowest`: Resolve the lowest compatible version of each package
  * `lowest-direct`: Resolve the lowest compatible version of any direct dependencies, and the highest compatible version of any transitive dependencies

    
Only show the version
By default, uv will show the project name before the version.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store.     
Allow package upgrades, ignoring pinned versions in any existing output file. Implies `--refresh` 

[`--upgrade-group`](https://docs.astral.sh/uv/reference/cli/#uv-version--upgrade-group) _upgrade-group_ 
    
Allow upgrades for all packages in a dependency group, ignoring pinned versions in any existing output file 

[`--upgrade-package`](https://docs.astral.sh/uv/reference/cli/#uv-version--upgrade-package), `-P` _upgrade-package_ 
    
Allow upgrades for a specific package, ignoring pinned versions in any existing output file. Implies `--refresh-package`     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
## [uv sync](https://docs.astral.sh/uv/reference/cli/#uv-sync)
Update the project's environment.
Syncing ensures that all project dependencies are installed and up-to-date with the lockfile.
By default, an exact sync is performed: uv removes packages that are not declared as dependencies of the project. Use the `--inexact` flag to keep extraneous packages. Note that if an extraneous package conflicts with a project dependency, it will still be removed. Additionally, if `--no-build-isolation` is used, uv will not remove extraneous packages to avoid removing possible build dependencies.
If the project virtual environment (`.venv`) does not exist, it will be created.
The project is re-locked before syncing unless the `--locked` or `--frozen` flag is provided.
uv will search for a project in the current directory or any parent directory. If a project cannot be found, uv will exit with an error.
Note that, when installing from a lockfile, uv will not provide warnings for yanked package versions.
### Usage

```
uv sync [OPTIONS]

```

### Options     
Sync dependencies to the active virtual environment.
Instead of creating or updating the virtual environment for the project or script, the active virtual environment will be preferred, if the `VIRTUAL_ENV` environment variable is set.     
Include all optional dependencies.
When two or more extras are declared as conflicting in `tool.uv.conflicts`, using this flag will always result in an error.
Note that all optional dependencies are always included in the resolution; this option only affects the selection of packages to install.     
Include dependencies from all dependency groups.
`--no-group` can be used to exclude specific groups.     
Sync all packages in the workspace.
The workspace's environment (`.venv`) is updated to include all workspace members.
Any extras or groups specified via `--extra`, `--group`, or related options will be applied to all workspace members. 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-sync--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-sync--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable.     
Check if the Python environment is synchronized with the project.
If the environment is not up to date, uv will exit with an error. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-sync--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--compile-bytecode`](https://docs.astral.sh/uv/reference/cli/#uv-sync--compile-bytecode), `--compile` 
    
Compile Python files to bytecode after installation.
By default, uv does not compile Python (`.py`) files to bytecode (`__pycache__/*.pyc`); instead, compilation is performed lazily the first time a module is imported. For use-cases in which start time is critical, such as CLI applications and Docker containers, this option can be enabled to trade longer installation times for faster start times.
When enabled, install operations (e.g., `uv pip install`) will compile installed or reinstalled Python files. Commands that perform a sync operation (e.g., `uv sync` or `uv run`) will process the entire site-packages directory including packages that are not being modified.
May also be set with the `UV_COMPILE_BYTECODE` environment variable. 

[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-sync--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--config-setting`](https://docs.astral.sh/uv/reference/cli/#uv-sync--config-setting), `--config-settings`, `-C` _config-setting_ 
    
Settings to pass to the PEP 517 build backend, specified as `KEY=VALUE` pairs 

[`--config-settings-package`](https://docs.astral.sh/uv/reference/cli/#uv-sync--config-settings-package), `--config-settings-package` _config-settings-package_ 
    
Settings to pass to the PEP 517 build backend for a specific package, specified as `PACKAGE:KEY=VALUE` pairs 

[`--default-index`](https://docs.astral.sh/uv/reference/cli/#uv-sync--default-index) _default-index_ 
    
The default package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--index` flag.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
May also be set with the `UV_DEFAULT_INDEX` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-sync--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable.     
Perform a dry run, without writing the lockfile or modifying the project environment.
In dry-run mode, uv will resolve the project's dependencies and report on the resulting changes to both the lockfile and the project environment, but will not modify either. 

[`--exclude-newer`](https://docs.astral.sh/uv/reference/cli/#uv-sync--exclude-newer) _exclude-newer_ 
    
Limit candidate packages to those that were uploaded prior to the given date.
The date is compared against the upload time of each individual distribution artifact (i.e., when each file was uploaded to the package index), not the release date of the package version.
Accepts RFC 3339 timestamps (e.g., `2006-12-02T02:07:43Z`), local dates in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Use `false` to disable `exclude-newer`.
May also be set with the `UV_EXCLUDE_NEWER` environment variable. 

[`--exclude-newer-package`](https://docs.astral.sh/uv/reference/cli/#uv-sync--exclude-newer-package) _exclude-newer-package_ 
    
Limit candidate packages for specific packages to those that were uploaded prior to the given date.
Accepts package-date pairs in the format `PACKAGE=DATE`, where `DATE` is an RFC 3339 timestamp (e.g., `2006-12-02T02:07:43Z`), a local date in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Can be provided multiple times for different packages. 

[`--extra`](https://docs.astral.sh/uv/reference/cli/#uv-sync--extra) _extra_ 
    
Include optional dependencies from the specified extra name.
May be provided more than once.
When multiple extras or groups are specified that appear in `tool.uv.conflicts`, uv will report an error.
Note that all optional dependencies are always included in the resolution; this option only affects the selection of packages to install. 

[`--extra-index-url`](https://docs.astral.sh/uv/reference/cli/#uv-sync--extra-index-url) _extra-index-url_ 
    
(Deprecated: use `--index` instead) Extra URLs of package indexes to use, in addition to `--index-url`.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--index-url` (which defaults to PyPI). When multiple `--extra-index-url` flags are provided, earlier values take priority.
May also be set with the `UV_EXTRA_INDEX_URL` environment variable. 

[`--find-links`](https://docs.astral.sh/uv/reference/cli/#uv-sync--find-links), `-f` _find-links_ 
    
Locations to search for candidate distributions, in addition to those found in the registry indexes.
If a path, the target must be a directory that contains packages as wheel files (`.whl`) or source distributions (e.g., `.tar.gz` or `.zip`) at the top level.
If a URL, the page must contain a flat list of links to package files adhering to the formats described above.
May also be set with the `UV_FIND_LINKS` environment variable. 

[`--fork-strategy`](https://docs.astral.sh/uv/reference/cli/#uv-sync--fork-strategy) _fork-strategy_ 
    
The strategy to use when selecting multiple versions of a given package across Python versions and platforms.
By default, uv will optimize for selecting the latest version of each package for each supported Python version (`requires-python`), while minimizing the number of selected versions across platforms.
Under `fewest`, uv will minimize the number of selected versions for each package, preferring older versions that are compatible with a wider range of supported Python versions or platforms.
May also be set with the `UV_FORK_STRATEGY` environment variable.
Possible values:
  * `fewest`: Optimize for selecting the fewest number of versions for each package. Older versions may be preferred if they are compatible with a wider range of supported Python versions or platforms
  * `requires-python`: Optimize for selecting latest supported version of each package, for each supported Python version

    
Sync without updating the `uv.lock` file [env: UV_FROZEN=]
Instead of checking if the lockfile is up-to-date, uses the versions in the lockfile as the source of truth. If the lockfile is missing, uv will exit with an error. If the `pyproject.toml` includes changes to dependencies that have not been included in the lockfile yet, they will not be present in the environment. 

[`--group`](https://docs.astral.sh/uv/reference/cli/#uv-sync--group) _group_ 
    
Include dependencies from the specified dependency group.
When multiple extras or groups are specified that appear in `tool.uv.conflicts`, uv will report an error.
May be provided multiple times.     
Display the concise help for this command 

[`--index`](https://docs.astral.sh/uv/reference/cli/#uv-sync--index) _index_ 
    
The indexes to use when resolving dependencies, in addition to the default index.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--default-index` (which defaults to PyPI). When multiple `--index` flags are provided, earlier values take priority.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
Relative paths can be disambiguated from index names with `./` or `../` on Unix or `.\\`, `..\\`, `./` or `../` on Windows.
May also be set with the `UV_INDEX` environment variable. 

[`--index-strategy`](https://docs.astral.sh/uv/reference/cli/#uv-sync--index-strategy) _index-strategy_ 
    
The strategy to use when resolving against multiple index URLs.
By default, uv will stop at the first index on which a given package is available, and limit resolutions to those present on that first index (`first-index`). This prevents "dependency confusion" attacks, whereby an attacker can upload a malicious package under the same name to an alternate index.
May also be set with the `UV_INDEX_STRATEGY` environment variable.
Possible values:
  * `first-index`: Only use results from the first index that returns a match for a given package name
  * `unsafe-first-match`: Search for every package name across all indexes, exhausting the versions from the first index before moving on to the next
  * `unsafe-best-match`: Search for every package name across all indexes, preferring the "best" version found. If a package version is in multiple indexes, only look at the entry for the first index



[`--index-url`](https://docs.astral.sh/uv/reference/cli/#uv-sync--index-url), `-i` _index-url_ 
    
(Deprecated: use `--default-index` instead) The URL of the Python package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--extra-index-url` flag.
May also be set with the `UV_INDEX_URL` environment variable. 

[`--inexact`](https://docs.astral.sh/uv/reference/cli/#uv-sync--inexact), `--no-exact` 
    
Do not remove extraneous packages present in the environment.
When enabled, uv will make the minimum necessary changes to satisfy the requirements. By default, syncing will remove any extraneous packages from the environment 

[`--keyring-provider`](https://docs.astral.sh/uv/reference/cli/#uv-sync--keyring-provider) _keyring-provider_ 
    
Attempt to use `keyring` for authentication for index URLs.
At present, only `--keyring-provider subprocess` is supported, which configures uv to use the `keyring` CLI to handle authentication.
Defaults to `disabled`.
May also be set with the `UV_KEYRING_PROVIDER` environment variable.
Possible values:
  * `disabled`: Do not use keyring for credential lookup
  * `subprocess`: Use the `keyring` command for credential lookup



[`--link-mode`](https://docs.astral.sh/uv/reference/cli/#uv-sync--link-mode) _link-mode_ 
    
The method to use when installing packages from the global cache.
Defaults to `clone` (also known as Copy-on-Write) on macOS and Linux, and `hardlink` on Windows.
WARNING: The use of symlink link mode is discouraged, as they create tight coupling between the cache and the target environment. For example, clearing the cache (`uv cache clean`) will break all installed packages by way of removing the underlying source files. Use symlinks with caution.
May also be set with the `UV_LINK_MODE` environment variable.
Possible values:
  * `clone`: Clone (i.e., copy-on-write) packages from the source into the destination
  * `copy`: Copy packages from the source into the destination
  * `hardlink`: Hard link packages from the source into the destination
  * `symlink`: Symbolically link packages from the source into the destination

    
Assert that the `uv.lock` will remain unchanged [env: UV_LOCKED=]
Requires that the lockfile is up-to-date. If the lockfile is missing or needs to be updated, uv will exit with an error.     
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions.     
Don't install pre-built wheels.
The given packages will be built and installed from source. The resolver will still use pre-built wheels to extract package metadata, if available.
May also be set with the `UV_NO_BINARY` environment variable. 

[`--no-binary-package`](https://docs.astral.sh/uv/reference/cli/#uv-sync--no-binary-package) _no-binary-package_ 
    
Don't install pre-built wheels for a specific package [env: `UV_NO_BINARY_PACKAGE`=]     
Don't build source distributions.
When enabled, uv will reuse cached wheels from previously built source distributions, but operations that require building a source distribution will exit with an error. First-party packages, such as projects in the workspace, will still be built. uv will also still build editable requirements, and their build backends may run arbitrary Python code.
May also be set with the `UV_NO_BUILD` environment variable. 

[`--no-build-isolation`](https://docs.astral.sh/uv/reference/cli/#uv-sync--no-build-isolation)
    
Disable isolation when building source distributions.
Assumes that build dependencies specified by PEP 518 are already installed.
May also be set with the `UV_NO_BUILD_ISOLATION` environment variable. 

[`--no-build-isolation-package`](https://docs.astral.sh/uv/reference/cli/#uv-sync--no-build-isolation-package) _no-build-isolation-package_ 
    
Disable isolation when building source distributions for a specific package.
Assumes that the packages' build dependencies specified by PEP 518 are already installed. 

[`--no-build-package`](https://docs.astral.sh/uv/reference/cli/#uv-sync--no-build-package) _no-build-package_ 
    
Don't build source distributions for a specific package [env: `UV_NO_BUILD_PACKAGE`=]
First-party packages, such as projects in the workspace, will still be built. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-sync--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable. 

[`--no-default-groups`](https://docs.astral.sh/uv/reference/cli/#uv-sync--no-default-groups)
    
Ignore the default dependency groups.
uv includes the groups defined in `tool.uv.default-groups` by default. This disables that option, however, specific groups can still be included with `--group`.
May also be set with the `UV_NO_DEFAULT_GROUPS` environment variable.     
Disable the development dependency group [env: UV_NO_DEV=]
This option is an alias of `--no-group dev`. See `--no-default-groups` to disable all default groups instead.
This option is only available when running in a project.     
Install any editable dependencies, including the project and any workspace members, as non-editable [env: UV_NO_EDITABLE=] 

[`--no-editable-package`](https://docs.astral.sh/uv/reference/cli/#uv-sync--no-editable-package) _no-editable-package_ 
    
Install the specified editable packages as non-editable 

[`--no-extra`](https://docs.astral.sh/uv/reference/cli/#uv-sync--no-extra) _no-extra_ 
    
Exclude the specified optional dependencies, if `--all-extras` is supplied.
May be provided multiple times. 

[`--no-group`](https://docs.astral.sh/uv/reference/cli/#uv-sync--no-group) _no-group_ 
    
Disable the specified dependency group [env: `UV_NO_GROUP`=]
This option always takes precedence over default groups, `--all-groups`, and `--group`.
May be provided multiple times.     
Ignore the registry index (e.g., PyPI), instead relying on direct URL dependencies and those provided via `--find-links` 

[`--no-install-local`](https://docs.astral.sh/uv/reference/cli/#uv-sync--no-install-local)
    
Do not install local path dependencies [env: UV_NO_INSTALL_LOCAL=]
Skips the current project, workspace members, and any other local (path or editable) packages. Only remote/indexed dependencies are installed. Useful in Docker builds to cache heavy third-party dependencies first and layer local packages separately.
The inverse `--only-install-local` can be used to install _only_ local packages, excluding all remote dependencies. 

[`--no-install-package`](https://docs.astral.sh/uv/reference/cli/#uv-sync--no-install-package) _no-install-package_ 
    
Do not install the given package(s).
By default, all of the project's dependencies are installed into the environment. The `--no-install-package` option allows exclusion of specific packages. Note this can result in a broken environment, and should be used with caution.
The inverse `--only-install-package` can be used to install _only_ the specified packages, excluding all others. 

[`--no-install-project`](https://docs.astral.sh/uv/reference/cli/#uv-sync--no-install-project)
    
Do not install the current project [env: UV_NO_INSTALL_PROJECT=]
By default, the current project is installed into the environment with all of its dependencies. The `--no-install-project` option allows the project to be excluded, but all of its dependencies are still installed. This is particularly useful in situations like building Docker images where installing the project separately from its dependencies allows optimal layer caching.
The inverse `--only-install-project` can be used to install _only_ the project itself, excluding all dependencies. 

[`--no-install-workspace`](https://docs.astral.sh/uv/reference/cli/#uv-sync--no-install-workspace)
    
Do not install any workspace members, including the root project [env: UV_NO_INSTALL_WORKSPACE=]
By default, all workspace members and their dependencies are installed into the environment. The `--no-install-workspace` option allows exclusion of all the workspace members while retaining their dependencies. This is particularly useful in situations like building Docker images where installing the workspace separately from its dependencies allows optimal layer caching.
The inverse `--only-install-workspace` can be used to install _only_ workspace members, excluding all other dependencies. 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-sync--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-sync--no-python-downloads)
    
Disable automatic downloads of Python.     
Ignore the `tool.uv.sources` table when resolving dependencies. Used to lock against the standards-compliant, publishable package metadata, as opposed to using any workspace, Git, URL, or local path sources
May also be set with the `UV_NO_SOURCES` environment variable. 

[`--no-sources-package`](https://docs.astral.sh/uv/reference/cli/#uv-sync--no-sources-package) _no-sources-package_ 
    
Don't use sources from the `tool.uv.sources` table for the specified packages [env: `UV_NO_SOURCES_PACKAGE`=]     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files.     
Only include the development dependency group.
The project and its dependencies will be omitted.
This option is an alias for `--only-group dev`. Implies `--no-default-groups`. 

[`--only-group`](https://docs.astral.sh/uv/reference/cli/#uv-sync--only-group) _only-group_ 
    
Only include dependencies from the specified dependency group.
The project and its dependencies will be omitted.
May be provided multiple times. Implies `--no-default-groups`. 

[`--output-format`](https://docs.astral.sh/uv/reference/cli/#uv-sync--output-format) _output-format_ 
    
Select the output format
[default: text]
Possible values:
  * `text`: Display the result in a human-readable format
  * `json`: Display the result in JSON format



[`--package`](https://docs.astral.sh/uv/reference/cli/#uv-sync--package) _package_ 
    
Sync for specific packages in the workspace.
The workspace's environment (`.venv`) is updated to reflect the subset of dependencies declared by the specified workspace member packages.
If any workspace member does not exist, uv will exit with an error. 

[`--prerelease`](https://docs.astral.sh/uv/reference/cli/#uv-sync--prerelease) _prerelease_ 
    
The strategy to use when considering pre-release versions.
By default, uv will prefer stable candidates, falling back to pre-releases only after every stable candidate that satisfies the active constraints is rejected (`if-necessary`).
May also be set with the `UV_PRERELEASE` environment variable.
Possible values:
  * `disallow`: Disallow all pre-release versions
  * `allow`: Allow all pre-release versions
  * `if-necessary`: Prefer stable versions, falling back to pre-release versions when necessary
  * `explicit`: Prefer stable versions for first-party packages with explicit pre-release specifiers, falling back to pre-release versions when necessary. Disallow pre-release versions for all other packages
  * `if-necessary-or-explicit`: Deprecated alias for `if-necessary`



[`--prerelease-package`](https://docs.astral.sh/uv/reference/cli/#uv-sync--prerelease-package) _prerelease-package_ 
    
The strategy to use when considering pre-release versions for a specific package.
Accepts package-mode pairs in the format `PACKAGE=MODE`, where `MODE` is any value accepted by `--prerelease`.
May be provided multiple times for different packages. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-sync--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable. 

[`--python`](https://docs.astral.sh/uv/reference/cli/#uv-sync--python), `-p` _python_ 
    
The Python interpreter to use for the project environment.
By default, the first interpreter that meets the project's `requires-python` constraint is used.
If a Python interpreter in a virtual environment is provided, the packages will not be synced to the given environment. The interpreter will be used to create a virtual environment in the project.
See [uv python](https://docs.astral.sh/uv/reference/cli/#uv-python) for details on Python discovery and supported request formats.
May also be set with the `UV_PYTHON` environment variable. 

[`--python-platform`](https://docs.astral.sh/uv/reference/cli/#uv-sync--python-platform) _python-platform_ 
    
The platform for which requirements should be installed.
Represented as a "target triple", a string that describes the target platform in terms of its CPU, vendor, and operating system name, like `x86_64-unknown-linux-gnu` or `aarch64-apple-darwin`.
When targeting macOS (Darwin), the default minimum version is `13.0`. Use `MACOSX_DEPLOYMENT_TARGET` to specify a different minimum version, e.g., `14.0`.
When targeting iOS, the default minimum version is `13.0`. Use `IPHONEOS_DEPLOYMENT_TARGET` to specify a different minimum version, e.g., `14.0`.
When targeting Android, the default minimum Android API level is `24`. Use `ANDROID_API_LEVEL` to specify a different minimum version, e.g., `26`.
WARNING: When specified, uv will select wheels that are compatible with the _target_ platform; as a result, the installed distributions may not be compatible with the _current_ platform. Conversely, any distributions that are built from source may be incompatible with the _target_ platform, as they will be built for the _current_ platform. The `--python-platform` option is intended for advanced use cases.
Possible values:
  * `windows`: An alias for `x86_64-pc-windows-msvc`, the default target for Windows
  * `linux`: An alias for `x86_64-unknown-linux-gnu`, the default target for Linux
  * `macos`: An alias for `aarch64-apple-darwin`, the default target for macOS
  * `x86_64-pc-windows-msvc`: A 64-bit x86 Windows target
  * `aarch64-pc-windows-msvc`: An ARM64 Windows target
  * `i686-pc-windows-msvc`: A 32-bit x86 Windows target
  * `x86_64-unknown-linux-gnu`: An x86 Linux target. Equivalent to `x86_64-manylinux_2_28`
  * `aarch64-apple-darwin`: An ARM-based macOS target, as seen on Apple Silicon devices
  * `x86_64-apple-darwin`: An x86 macOS target
  * `aarch64-unknown-linux-gnu`: An ARM64 Linux target. Equivalent to `aarch64-manylinux_2_28`
  * `aarch64-unknown-linux-musl`: An ARM64 Linux target
  * `x86_64-unknown-linux-musl`: An `x86_64` Linux target
  * `riscv64-unknown-linux`: A RISCV64 Linux target
  * `x86_64-manylinux2014`: An `x86_64` target for the `manylinux2014` platform. Equivalent to `x86_64-manylinux_2_17`
  * `x86_64-manylinux_2_17`: An `x86_64` target for the `manylinux_2_17` platform
  * `x86_64-manylinux_2_28`: An `x86_64` target for the `manylinux_2_28` platform
  * `x86_64-manylinux_2_31`: An `x86_64` target for the `manylinux_2_31` platform
  * `x86_64-manylinux_2_32`: An `x86_64` target for the `manylinux_2_32` platform
  * `x86_64-manylinux_2_33`: An `x86_64` target for the `manylinux_2_33` platform
  * `x86_64-manylinux_2_34`: An `x86_64` target for the `manylinux_2_34` platform
  * `x86_64-manylinux_2_35`: An `x86_64` target for the `manylinux_2_35` platform
  * `x86_64-manylinux_2_36`: An `x86_64` target for the `manylinux_2_36` platform
  * `x86_64-manylinux_2_37`: An `x86_64` target for the `manylinux_2_37` platform
  * `x86_64-manylinux_2_38`: An `x86_64` target for the `manylinux_2_38` platform
  * `x86_64-manylinux_2_39`: An `x86_64` target for the `manylinux_2_39` platform
  * `x86_64-manylinux_2_40`: An `x86_64` target for the `manylinux_2_40` platform
  * `aarch64-manylinux2014`: An ARM64 target for the `manylinux2014` platform. Equivalent to `aarch64-manylinux_2_17`
  * `aarch64-manylinux_2_17`: An ARM64 target for the `manylinux_2_17` platform
  * `aarch64-manylinux_2_28`: An ARM64 target for the `manylinux_2_28` platform
  * `aarch64-manylinux_2_31`: An ARM64 target for the `manylinux_2_31` platform
  * `aarch64-manylinux_2_32`: An ARM64 target for the `manylinux_2_32` platform
  * `aarch64-manylinux_2_33`: An ARM64 target for the `manylinux_2_33` platform
  * `aarch64-manylinux_2_34`: An ARM64 target for the `manylinux_2_34` platform
  * `aarch64-manylinux_2_35`: An ARM64 target for the `manylinux_2_35` platform
  * `aarch64-manylinux_2_36`: An ARM64 target for the `manylinux_2_36` platform
  * `aarch64-manylinux_2_37`: An ARM64 target for the `manylinux_2_37` platform
  * `aarch64-manylinux_2_38`: An ARM64 target for the `manylinux_2_38` platform
  * `aarch64-manylinux_2_39`: An ARM64 target for the `manylinux_2_39` platform
  * `aarch64-manylinux_2_40`: An ARM64 target for the `manylinux_2_40` platform
  * `aarch64-linux-android`: An ARM64 Android target
  * `x86_64-linux-android`: An `x86_64` Android target
  * `wasm32-pyodide2024`: A wasm32 target using the Pyodide 2024 platform. Meant for use with Python 3.12. See <https://pyodide.org/en/stable/development/abi/312.html>
  * `wasm32-pyodide2025`: A wasm32 target using the Pyodide 2025 platform. Meant for use with Python 3.13. See <https://pyodide.org/en/stable/development/abi/313.html>
  * `arm64-apple-ios`: An ARM64 target for iOS device
  * `arm64-apple-ios-simulator`: An ARM64 target for iOS simulator
  * `x86_64-apple-ios-simulator`: An `x86_64` target for iOS simulator

    
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Refresh all cached data 

[`--refresh-package`](https://docs.astral.sh/uv/reference/cli/#uv-sync--refresh-package) _refresh-package_ 
    
Refresh cached data for a specific package 

[`--reinstall`](https://docs.astral.sh/uv/reference/cli/#uv-sync--reinstall), `--force-reinstall` 
    
Reinstall all packages, regardless of whether they're already installed. Implies `--refresh` 

[`--reinstall-package`](https://docs.astral.sh/uv/reference/cli/#uv-sync--reinstall-package) _reinstall-package_ 
    
Reinstall a specific package, regardless of whether it's already installed. Implies `--refresh-package` 

[`--resolution`](https://docs.astral.sh/uv/reference/cli/#uv-sync--resolution) _resolution_ 
    
The strategy to use when selecting between the different compatible versions for a given package requirement.
By default, uv will use the latest compatible version of each package (`highest`).
May also be set with the `UV_RESOLUTION` environment variable.
Possible values:
  * `highest`: Resolve the highest compatible version of each package
  * `lowest`: Resolve the lowest compatible version of each package
  * `lowest-direct`: Resolve the lowest compatible version of any direct dependencies, and the highest compatible version of any transitive dependencies



[`--script`](https://docs.astral.sh/uv/reference/cli/#uv-sync--script) _script_ 
    
Sync the environment for a Python script, rather than the current project.
If provided, uv will sync the dependencies based on the script's inline metadata table, in adherence with PEP 723.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store.     
Allow package upgrades, ignoring pinned versions in any existing output file. Implies `--refresh` 

[`--upgrade-group`](https://docs.astral.sh/uv/reference/cli/#uv-sync--upgrade-group) _upgrade-group_ 
    
Allow upgrades for all packages in a dependency group, ignoring pinned versions in any existing output file 

[`--upgrade-package`](https://docs.astral.sh/uv/reference/cli/#uv-sync--upgrade-package), `-P` _upgrade-package_ 
    
Allow upgrades for a specific package, ignoring pinned versions in any existing output file. Implies `--refresh-package`     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
## [uv lock](https://docs.astral.sh/uv/reference/cli/#uv-lock)
Update the project's lockfile.
If the project lockfile (`uv.lock`) does not exist, it will be created. If a lockfile is present, its contents will be used as preferences for the resolution.
If there are no changes to the project's dependencies, locking will have no effect unless the `--upgrade` flag is provided.
### Usage

```
uv lock [OPTIONS]

```

### Options 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-lock--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-lock--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable.     
Check if the lockfile is up-to-date.
Asserts that the `uv.lock` would remain unchanged after a resolution. If the lockfile is missing or needs to be updated, uv will exit with an error.
Equivalent to `--locked`.     
Assert that a `uv.lock` exists without checking if it is up-to-date [env: UV_FROZEN=]
Equivalent to `--frozen`. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-lock--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-lock--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--config-setting`](https://docs.astral.sh/uv/reference/cli/#uv-lock--config-setting), `--config-settings`, `-C` _config-setting_ 
    
Settings to pass to the PEP 517 build backend, specified as `KEY=VALUE` pairs 

[`--config-settings-package`](https://docs.astral.sh/uv/reference/cli/#uv-lock--config-settings-package), `--config-settings-package` _config-settings-package_ 
    
Settings to pass to the PEP 517 build backend for a specific package, specified as `PACKAGE:KEY=VALUE` pairs 

[`--default-index`](https://docs.astral.sh/uv/reference/cli/#uv-lock--default-index) _default-index_ 
    
The default package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--index` flag.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
May also be set with the `UV_DEFAULT_INDEX` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-lock--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable.     
Perform a dry run, without writing the lockfile.
In dry-run mode, uv will resolve the project's dependencies and report on the resulting changes, but will not write the lockfile to disk. 

[`--exclude-newer`](https://docs.astral.sh/uv/reference/cli/#uv-lock--exclude-newer) _exclude-newer_ 
    
Limit candidate packages to those that were uploaded prior to the given date.
The date is compared against the upload time of each individual distribution artifact (i.e., when each file was uploaded to the package index), not the release date of the package version.
Accepts RFC 3339 timestamps (e.g., `2006-12-02T02:07:43Z`), local dates in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Use `false` to disable `exclude-newer`.
May also be set with the `UV_EXCLUDE_NEWER` environment variable. 

[`--exclude-newer-package`](https://docs.astral.sh/uv/reference/cli/#uv-lock--exclude-newer-package) _exclude-newer-package_ 
    
Limit candidate packages for specific packages to those that were uploaded prior to the given date.
Accepts package-date pairs in the format `PACKAGE=DATE`, where `DATE` is an RFC 3339 timestamp (e.g., `2006-12-02T02:07:43Z`), a local date in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Can be provided multiple times for different packages. 

[`--extra-index-url`](https://docs.astral.sh/uv/reference/cli/#uv-lock--extra-index-url) _extra-index-url_ 
    
(Deprecated: use `--index` instead) Extra URLs of package indexes to use, in addition to `--index-url`.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--index-url` (which defaults to PyPI). When multiple `--extra-index-url` flags are provided, earlier values take priority.
May also be set with the `UV_EXTRA_INDEX_URL` environment variable. 

[`--find-links`](https://docs.astral.sh/uv/reference/cli/#uv-lock--find-links), `-f` _find-links_ 
    
Locations to search for candidate distributions, in addition to those found in the registry indexes.
If a path, the target must be a directory that contains packages as wheel files (`.whl`) or source distributions (e.g., `.tar.gz` or `.zip`) at the top level.
If a URL, the page must contain a flat list of links to package files adhering to the formats described above.
May also be set with the `UV_FIND_LINKS` environment variable. 

[`--fork-strategy`](https://docs.astral.sh/uv/reference/cli/#uv-lock--fork-strategy) _fork-strategy_ 
    
The strategy to use when selecting multiple versions of a given package across Python versions and platforms.
By default, uv will optimize for selecting the latest version of each package for each supported Python version (`requires-python`), while minimizing the number of selected versions across platforms.
Under `fewest`, uv will minimize the number of selected versions for each package, preferring older versions that are compatible with a wider range of supported Python versions or platforms.
May also be set with the `UV_FORK_STRATEGY` environment variable.
Possible values:
  * `fewest`: Optimize for selecting the fewest number of versions for each package. Older versions may be preferred if they are compatible with a wider range of supported Python versions or platforms
  * `requires-python`: Optimize for selecting latest supported version of each package, for each supported Python version

    
Display the concise help for this command 

[`--index`](https://docs.astral.sh/uv/reference/cli/#uv-lock--index) _index_ 
    
The indexes to use when resolving dependencies, in addition to the default index.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--default-index` (which defaults to PyPI). When multiple `--index` flags are provided, earlier values take priority.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
Relative paths can be disambiguated from index names with `./` or `../` on Unix or `.\\`, `..\\`, `./` or `../` on Windows.
May also be set with the `UV_INDEX` environment variable. 

[`--index-strategy`](https://docs.astral.sh/uv/reference/cli/#uv-lock--index-strategy) _index-strategy_ 
    
The strategy to use when resolving against multiple index URLs.
By default, uv will stop at the first index on which a given package is available, and limit resolutions to those present on that first index (`first-index`). This prevents "dependency confusion" attacks, whereby an attacker can upload a malicious package under the same name to an alternate index.
May also be set with the `UV_INDEX_STRATEGY` environment variable.
Possible values:
  * `first-index`: Only use results from the first index that returns a match for a given package name
  * `unsafe-first-match`: Search for every package name across all indexes, exhausting the versions from the first index before moving on to the next
  * `unsafe-best-match`: Search for every package name across all indexes, preferring the "best" version found. If a package version is in multiple indexes, only look at the entry for the first index



[`--index-url`](https://docs.astral.sh/uv/reference/cli/#uv-lock--index-url), `-i` _index-url_ 
    
(Deprecated: use `--default-index` instead) The URL of the Python package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--extra-index-url` flag.
May also be set with the `UV_INDEX_URL` environment variable. 

[`--keyring-provider`](https://docs.astral.sh/uv/reference/cli/#uv-lock--keyring-provider) _keyring-provider_ 
    
Attempt to use `keyring` for authentication for index URLs.
At present, only `--keyring-provider subprocess` is supported, which configures uv to use the `keyring` CLI to handle authentication.
Defaults to `disabled`.
May also be set with the `UV_KEYRING_PROVIDER` environment variable.
Possible values:
  * `disabled`: Do not use keyring for credential lookup
  * `subprocess`: Use the `keyring` command for credential lookup



[`--link-mode`](https://docs.astral.sh/uv/reference/cli/#uv-lock--link-mode) _link-mode_ 
    
The method to use when installing packages from the global cache.
This option is only used when building source distributions.
Defaults to `clone` (also known as Copy-on-Write) on macOS and Linux, and `hardlink` on Windows.
WARNING: The use of symlink link mode is discouraged, as they create tight coupling between the cache and the target environment. For example, clearing the cache (`uv cache clean`) will break all installed packages by way of removing the underlying source files. Use symlinks with caution.
May also be set with the `UV_LINK_MODE` environment variable.
Possible values:
  * `clone`: Clone (i.e., copy-on-write) packages from the source into the destination
  * `copy`: Copy packages from the source into the destination
  * `hardlink`: Hard link packages from the source into the destination
  * `symlink`: Symbolically link packages from the source into the destination

    
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions.     
Don't install pre-built wheels.
The given packages will be built and installed from source. The resolver will still use pre-built wheels to extract package metadata, if available.
May also be set with the `UV_NO_BINARY` environment variable. 

[`--no-binary-package`](https://docs.astral.sh/uv/reference/cli/#uv-lock--no-binary-package) _no-binary-package_ 
    
Don't install pre-built wheels for a specific package [env: `UV_NO_BINARY_PACKAGE`=]     
Don't build source distributions.
When enabled, uv will reuse cached wheels from previously built source distributions, but operations that require building a source distribution will exit with an error. First-party packages, such as projects in the workspace, will still be built. uv will also still build editable requirements, and their build backends may run arbitrary Python code.
May also be set with the `UV_NO_BUILD` environment variable. 

[`--no-build-isolation`](https://docs.astral.sh/uv/reference/cli/#uv-lock--no-build-isolation)
    
Disable isolation when building source distributions.
Assumes that build dependencies specified by PEP 518 are already installed.
May also be set with the `UV_NO_BUILD_ISOLATION` environment variable. 

[`--no-build-isolation-package`](https://docs.astral.sh/uv/reference/cli/#uv-lock--no-build-isolation-package) _no-build-isolation-package_ 
    
Disable isolation when building source distributions for a specific package.
Assumes that the packages' build dependencies specified by PEP 518 are already installed. 

[`--no-build-package`](https://docs.astral.sh/uv/reference/cli/#uv-lock--no-build-package) _no-build-package_ 
    
Don't build source distributions for a specific package [env: `UV_NO_BUILD_PACKAGE`=]
First-party packages, such as projects in the workspace, will still be built. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-lock--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable.     
Ignore the registry index (e.g., PyPI), instead relying on direct URL dependencies and those provided via `--find-links` 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-lock--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-lock--no-python-downloads)
    
Disable automatic downloads of Python.     
Ignore the `tool.uv.sources` table when resolving dependencies. Used to lock against the standards-compliant, publishable package metadata, as opposed to using any workspace, Git, URL, or local path sources
May also be set with the `UV_NO_SOURCES` environment variable. 

[`--no-sources-package`](https://docs.astral.sh/uv/reference/cli/#uv-lock--no-sources-package) _no-sources-package_ 
    
Don't use sources from the `tool.uv.sources` table for the specified packages [env: `UV_NO_SOURCES_PACKAGE`=]     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--prerelease`](https://docs.astral.sh/uv/reference/cli/#uv-lock--prerelease) _prerelease_ 
    
The strategy to use when considering pre-release versions.
By default, uv will prefer stable candidates, falling back to pre-releases only after every stable candidate that satisfies the active constraints is rejected (`if-necessary`).
May also be set with the `UV_PRERELEASE` environment variable.
Possible values:
  * `disallow`: Disallow all pre-release versions
  * `allow`: Allow all pre-release versions
  * `if-necessary`: Prefer stable versions, falling back to pre-release versions when necessary
  * `explicit`: Prefer stable versions for first-party packages with explicit pre-release specifiers, falling back to pre-release versions when necessary. Disallow pre-release versions for all other packages
  * `if-necessary-or-explicit`: Deprecated alias for `if-necessary`



[`--prerelease-package`](https://docs.astral.sh/uv/reference/cli/#uv-lock--prerelease-package) _prerelease-package_ 
    
The strategy to use when considering pre-release versions for a specific package.
Accepts package-mode pairs in the format `PACKAGE=MODE`, where `MODE` is any value accepted by `--prerelease`.
May be provided multiple times for different packages. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-lock--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable. 

[`--python`](https://docs.astral.sh/uv/reference/cli/#uv-lock--python), `-p` _python_ 
    
The Python interpreter to use during resolution.
A Python interpreter is required for building source distributions to determine package metadata when there are not wheels.
The interpreter is also used as the fallback value for the minimum Python version if `requires-python` is not set.
See [uv python](https://docs.astral.sh/uv/reference/cli/#uv-python) for details on Python discovery and supported request formats.
May also be set with the `UV_PYTHON` environment variable.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Refresh all cached data 

[`--refresh-package`](https://docs.astral.sh/uv/reference/cli/#uv-lock--refresh-package) _refresh-package_ 
    
Refresh cached data for a specific package 

[`--resolution`](https://docs.astral.sh/uv/reference/cli/#uv-lock--resolution) _resolution_ 
    
The strategy to use when selecting between the different compatible versions for a given package requirement.
By default, uv will use the latest compatible version of each package (`highest`).
May also be set with the `UV_RESOLUTION` environment variable.
Possible values:
  * `highest`: Resolve the highest compatible version of each package
  * `lowest`: Resolve the lowest compatible version of each package
  * `lowest-direct`: Resolve the lowest compatible version of any direct dependencies, and the highest compatible version of any transitive dependencies



[`--script`](https://docs.astral.sh/uv/reference/cli/#uv-lock--script) _script_ 
    
Lock the specified Python script, rather than the current project.
If provided, uv will lock the script (based on its inline metadata table, in adherence with PEP 723) to a `.lock` file adjacent to the script itself.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store.     
Allow package upgrades, ignoring pinned versions in any existing output file. Implies `--refresh` 

[`--upgrade-group`](https://docs.astral.sh/uv/reference/cli/#uv-lock--upgrade-group) _upgrade-group_ 
    
Allow upgrades for all packages in a dependency group, ignoring pinned versions in any existing output file 

[`--upgrade-package`](https://docs.astral.sh/uv/reference/cli/#uv-lock--upgrade-package), `-P` _upgrade-package_ 
    
Allow upgrades for a specific package, ignoring pinned versions in any existing output file. Implies `--refresh-package`     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
## [uv export](https://docs.astral.sh/uv/reference/cli/#uv-export)
Export the project's lockfile to an alternate format.
At present, `requirements.txt`, `pylock.toml` (PEP 751) and CycloneDX v1.5 JSON output formats are supported.
The project is re-locked before exporting unless the `--locked` or `--frozen` flag is provided.
uv will search for a project in the current directory or any parent directory. If a project cannot be found, uv will exit with an error.
If operating in a workspace, the root will be exported by default; however, specific members can be selected using the `--package` option.
### Usage

```
uv export [OPTIONS]

```

### Options     
Include all optional dependencies     
Include dependencies from all dependency groups.
`--no-group` can be used to exclude specific groups.     
Export the entire workspace.
The dependencies for all workspace members will be included in the exported requirements file.
Any extras or groups specified via `--extra`, `--group`, or related options will be applied to all workspace members. 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-export--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-export--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-export--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-export--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--config-setting`](https://docs.astral.sh/uv/reference/cli/#uv-export--config-setting), `--config-settings`, `-C` _config-setting_ 
    
Settings to pass to the PEP 517 build backend, specified as `KEY=VALUE` pairs 

[`--config-settings-package`](https://docs.astral.sh/uv/reference/cli/#uv-export--config-settings-package), `--config-settings-package` _config-settings-package_ 
    
Settings to pass to the PEP 517 build backend for a specific package, specified as `PACKAGE:KEY=VALUE` pairs 

[`--default-index`](https://docs.astral.sh/uv/reference/cli/#uv-export--default-index) _default-index_ 
    
The default package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--index` flag.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
May also be set with the `UV_DEFAULT_INDEX` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-export--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable. 

[`--emit-find-links`](https://docs.astral.sh/uv/reference/cli/#uv-export--emit-find-links)
    
Include `--find-links` entries in the generated output file     
Include `--index-url` and `--extra-index-url` entries in the generated output file 

[`--exclude-newer`](https://docs.astral.sh/uv/reference/cli/#uv-export--exclude-newer) _exclude-newer_ 
    
Limit candidate packages to those that were uploaded prior to the given date.
The date is compared against the upload time of each individual distribution artifact (i.e., when each file was uploaded to the package index), not the release date of the package version.
Accepts RFC 3339 timestamps (e.g., `2006-12-02T02:07:43Z`), local dates in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Use `false` to disable `exclude-newer`.
May also be set with the `UV_EXCLUDE_NEWER` environment variable. 

[`--exclude-newer-package`](https://docs.astral.sh/uv/reference/cli/#uv-export--exclude-newer-package) _exclude-newer-package_ 
    
Limit candidate packages for specific packages to those that were uploaded prior to the given date.
Accepts package-date pairs in the format `PACKAGE=DATE`, where `DATE` is an RFC 3339 timestamp (e.g., `2006-12-02T02:07:43Z`), a local date in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Can be provided multiple times for different packages. 

[`--extra`](https://docs.astral.sh/uv/reference/cli/#uv-export--extra) _extra_ 
    
Include optional dependencies from the specified extra name.
May be provided more than once. 

[`--extra-index-url`](https://docs.astral.sh/uv/reference/cli/#uv-export--extra-index-url) _extra-index-url_ 
    
(Deprecated: use `--index` instead) Extra URLs of package indexes to use, in addition to `--index-url`.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--index-url` (which defaults to PyPI). When multiple `--extra-index-url` flags are provided, earlier values take priority.
May also be set with the `UV_EXTRA_INDEX_URL` environment variable. 

[`--find-links`](https://docs.astral.sh/uv/reference/cli/#uv-export--find-links), `-f` _find-links_ 
    
Locations to search for candidate distributions, in addition to those found in the registry indexes.
If a path, the target must be a directory that contains packages as wheel files (`.whl`) or source distributions (e.g., `.tar.gz` or `.zip`) at the top level.
If a URL, the page must contain a flat list of links to package files adhering to the formats described above.
May also be set with the `UV_FIND_LINKS` environment variable. 

[`--fork-strategy`](https://docs.astral.sh/uv/reference/cli/#uv-export--fork-strategy) _fork-strategy_ 
    
The strategy to use when selecting multiple versions of a given package across Python versions and platforms.
By default, uv will optimize for selecting the latest version of each package for each supported Python version (`requires-python`), while minimizing the number of selected versions across platforms.
Under `fewest`, uv will minimize the number of selected versions for each package, preferring older versions that are compatible with a wider range of supported Python versions or platforms.
May also be set with the `UV_FORK_STRATEGY` environment variable.
Possible values:
  * `fewest`: Optimize for selecting the fewest number of versions for each package. Older versions may be preferred if they are compatible with a wider range of supported Python versions or platforms
  * `requires-python`: Optimize for selecting latest supported version of each package, for each supported Python version



[`--format`](https://docs.astral.sh/uv/reference/cli/#uv-export--format) _format_ 
    
The format to which `uv.lock` should be exported.
Supports `requirements.txt`, `pylock.toml` (PEP 751) and CycloneDX v1.5 JSON output formats.
uv will infer the output format from the file extension of the output file, if provided. Otherwise, defaults to `requirements.txt`.
Possible values:
  * `requirements.txt`: Export in `requirements.txt` format
  * `pylock.toml`: Export in `pylock.toml` format
  * `cyclonedx1.5`: Export in `CycloneDX` v1.5 JSON format

    
Do not update the `uv.lock` before exporting [env: UV_FROZEN=]
If a `uv.lock` does not exist, uv will exit with an error. 

[`--group`](https://docs.astral.sh/uv/reference/cli/#uv-export--group) _group_ 
    
Include dependencies from the specified dependency group.
May be provided multiple times.     
Display the concise help for this command 

[`--index`](https://docs.astral.sh/uv/reference/cli/#uv-export--index) _index_ 
    
The indexes to use when resolving dependencies, in addition to the default index.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--default-index` (which defaults to PyPI). When multiple `--index` flags are provided, earlier values take priority.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
Relative paths can be disambiguated from index names with `./` or `../` on Unix or `.\\`, `..\\`, `./` or `../` on Windows.
May also be set with the `UV_INDEX` environment variable. 

[`--index-strategy`](https://docs.astral.sh/uv/reference/cli/#uv-export--index-strategy) _index-strategy_ 
    
The strategy to use when resolving against multiple index URLs.
By default, uv will stop at the first index on which a given package is available, and limit resolutions to those present on that first index (`first-index`). This prevents "dependency confusion" attacks, whereby an attacker can upload a malicious package under the same name to an alternate index.
May also be set with the `UV_INDEX_STRATEGY` environment variable.
Possible values:
  * `first-index`: Only use results from the first index that returns a match for a given package name
  * `unsafe-first-match`: Search for every package name across all indexes, exhausting the versions from the first index before moving on to the next
  * `unsafe-best-match`: Search for every package name across all indexes, preferring the "best" version found. If a package version is in multiple indexes, only look at the entry for the first index



[`--index-url`](https://docs.astral.sh/uv/reference/cli/#uv-export--index-url), `-i` _index-url_ 
    
(Deprecated: use `--default-index` instead) The URL of the Python package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--extra-index-url` flag.
May also be set with the `UV_INDEX_URL` environment variable. 

[`--keyring-provider`](https://docs.astral.sh/uv/reference/cli/#uv-export--keyring-provider) _keyring-provider_ 
    
Attempt to use `keyring` for authentication for index URLs.
At present, only `--keyring-provider subprocess` is supported, which configures uv to use the `keyring` CLI to handle authentication.
Defaults to `disabled`.
May also be set with the `UV_KEYRING_PROVIDER` environment variable.
Possible values:
  * `disabled`: Do not use keyring for credential lookup
  * `subprocess`: Use the `keyring` command for credential lookup



[`--link-mode`](https://docs.astral.sh/uv/reference/cli/#uv-export--link-mode) _link-mode_ 
    
The method to use when installing packages from the global cache.
This option is only used when building source distributions.
Defaults to `clone` (also known as Copy-on-Write) on macOS and Linux, and `hardlink` on Windows.
WARNING: The use of symlink link mode is discouraged, as they create tight coupling between the cache and the target environment. For example, clearing the cache (`uv cache clean`) will break all installed packages by way of removing the underlying source files. Use symlinks with caution.
May also be set with the `UV_LINK_MODE` environment variable.
Possible values:
  * `clone`: Clone (i.e., copy-on-write) packages from the source into the destination
  * `copy`: Copy packages from the source into the destination
  * `hardlink`: Hard link packages from the source into the destination
  * `symlink`: Symbolically link packages from the source into the destination

    
Assert that the `uv.lock` will remain unchanged [env: UV_LOCKED=]
Requires that the lockfile is up-to-date. If the lockfile is missing or needs to be updated, uv will exit with an error.     
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions.     
Exclude comment annotations indicating the source of each package     
Don't install pre-built wheels.
The given packages will be built and installed from source. The resolver will still use pre-built wheels to extract package metadata, if available.
May also be set with the `UV_NO_BINARY` environment variable. 

[`--no-binary-package`](https://docs.astral.sh/uv/reference/cli/#uv-export--no-binary-package) _no-binary-package_ 
    
Don't install pre-built wheels for a specific package [env: `UV_NO_BINARY_PACKAGE`=]     
Don't build source distributions.
When enabled, uv will reuse cached wheels from previously built source distributions, but operations that require building a source distribution will exit with an error. First-party packages, such as projects in the workspace, will still be built. uv will also still build editable requirements, and their build backends may run arbitrary Python code.
May also be set with the `UV_NO_BUILD` environment variable. 

[`--no-build-isolation`](https://docs.astral.sh/uv/reference/cli/#uv-export--no-build-isolation)
    
Disable isolation when building source distributions.
Assumes that build dependencies specified by PEP 518 are already installed.
May also be set with the `UV_NO_BUILD_ISOLATION` environment variable. 

[`--no-build-isolation-package`](https://docs.astral.sh/uv/reference/cli/#uv-export--no-build-isolation-package) _no-build-isolation-package_ 
    
Disable isolation when building source distributions for a specific package.
Assumes that the packages' build dependencies specified by PEP 518 are already installed. 

[`--no-build-package`](https://docs.astral.sh/uv/reference/cli/#uv-export--no-build-package) _no-build-package_ 
    
Don't build source distributions for a specific package [env: `UV_NO_BUILD_PACKAGE`=]
First-party packages, such as projects in the workspace, will still be built. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-export--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable. 

[`--no-default-groups`](https://docs.astral.sh/uv/reference/cli/#uv-export--no-default-groups)
    
Ignore the default dependency groups.
uv includes the groups defined in `tool.uv.default-groups` by default. This disables that option, however, specific groups can still be included with `--group`.
May also be set with the `UV_NO_DEFAULT_GROUPS` environment variable.     
Disable the development dependency group [env: UV_NO_DEV=]
This option is an alias of `--no-group dev`. See `--no-default-groups` to disable all default groups instead.
This option is only available when running in a project.     
Export any editable dependencies, including the project and any workspace members, as non-editable [env: UV_NO_EDITABLE=] 

[`--no-editable-package`](https://docs.astral.sh/uv/reference/cli/#uv-export--no-editable-package) _no-editable-package_ 
    
Export the specified editable packages as non-editable 

[`--no-emit-local`](https://docs.astral.sh/uv/reference/cli/#uv-export--no-emit-local), `--no-install-local` 
    
Do not include local path dependencies in the exported requirements.
Omits the current project, workspace members, and any other local (path or editable) packages from the export. Only remote/indexed dependencies are written. Useful for Docker and CI flows that want to export and cache third-party dependencies first.
The inverse `--only-emit-local` can be used to emit _only_ local packages, excluding all remote dependencies. 

[`--no-emit-package`](https://docs.astral.sh/uv/reference/cli/#uv-export--no-emit-package), `--no-install-package` _no-emit-package_ 
    
Do not emit the given package(s).
By default, all project's dependencies are included in the exported requirements file. The `--no-emit-package` option allows exclusion of specific packages.
The inverse `--only-emit-package` can be used to emit _only_ the specified packages, excluding all others. 

[`--no-emit-project`](https://docs.astral.sh/uv/reference/cli/#uv-export--no-emit-project), `--no-install-project` 
    
Do not emit the current project.
By default, the current project is included in the exported requirements file with all of its dependencies. The `--no-emit-project` option allows the project to be excluded, but all of its dependencies to remain included.
The inverse `--only-emit-project` can be used to emit _only_ the project itself, excluding all dependencies. 

[`--no-emit-workspace`](https://docs.astral.sh/uv/reference/cli/#uv-export--no-emit-workspace), `--no-install-workspace` 
    
Do not emit any workspace members, including the root project.
By default, all workspace members and their dependencies are included in the exported requirements file, with all of their dependencies. The `--no-emit-workspace` option allows exclusion of all the workspace members while retaining their dependencies.
The inverse `--only-emit-workspace` can be used to emit _only_ workspace members, excluding all other dependencies. 

[`--no-extra`](https://docs.astral.sh/uv/reference/cli/#uv-export--no-extra) _no-extra_ 
    
Exclude the specified optional dependencies, if `--all-extras` is supplied.
May be provided multiple times. 

[`--no-group`](https://docs.astral.sh/uv/reference/cli/#uv-export--no-group) _no-group_ 
    
Disable the specified dependency group [env: `UV_NO_GROUP`=]
This option always takes precedence over default groups, `--all-groups`, and `--group`.
May be provided multiple times.     
Omit hashes in the generated output     
Exclude the comment header at the top of the generated output file     
Ignore the registry index (e.g., PyPI), instead relying on direct URL dependencies and those provided via `--find-links` 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-export--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-export--no-python-downloads)
    
Disable automatic downloads of Python.     
Ignore the `tool.uv.sources` table when resolving dependencies. Used to lock against the standards-compliant, publishable package metadata, as opposed to using any workspace, Git, URL, or local path sources
May also be set with the `UV_NO_SOURCES` environment variable. 

[`--no-sources-package`](https://docs.astral.sh/uv/reference/cli/#uv-export--no-sources-package) _no-sources-package_ 
    
Don't use sources from the `tool.uv.sources` table for the specified packages [env: `UV_NO_SOURCES_PACKAGE`=]     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files.     
Only include the development dependency group.
The project and its dependencies will be omitted.
This option is an alias for `--only-group dev`. Implies `--no-default-groups`. 

[`--only-group`](https://docs.astral.sh/uv/reference/cli/#uv-export--only-group) _only-group_ 
    
Only include dependencies from the specified dependency group.
The project and its dependencies will be omitted.
May be provided multiple times. Implies `--no-default-groups`. 

[`--output-file`](https://docs.astral.sh/uv/reference/cli/#uv-export--output-file), `-o` _output-file_ 
    
Write the exported requirements to the given file 

[`--package`](https://docs.astral.sh/uv/reference/cli/#uv-export--package) _package_ 
    
Export the dependencies for specific packages in the workspace.
If any workspace member does not exist, uv will exit with an error. 

[`--prerelease`](https://docs.astral.sh/uv/reference/cli/#uv-export--prerelease) _prerelease_ 
    
The strategy to use when considering pre-release versions.
By default, uv will prefer stable candidates, falling back to pre-releases only after every stable candidate that satisfies the active constraints is rejected (`if-necessary`).
May also be set with the `UV_PRERELEASE` environment variable.
Possible values:
  * `disallow`: Disallow all pre-release versions
  * `allow`: Allow all pre-release versions
  * `if-necessary`: Prefer stable versions, falling back to pre-release versions when necessary
  * `explicit`: Prefer stable versions for first-party packages with explicit pre-release specifiers, falling back to pre-release versions when necessary. Disallow pre-release versions for all other packages
  * `if-necessary-or-explicit`: Deprecated alias for `if-necessary`



[`--prerelease-package`](https://docs.astral.sh/uv/reference/cli/#uv-export--prerelease-package) _prerelease-package_ 
    
The strategy to use when considering pre-release versions for a specific package.
Accepts package-mode pairs in the format `PACKAGE=MODE`, where `MODE` is any value accepted by `--prerelease`.
May be provided multiple times for different packages. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-export--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable. 

[`--prune`](https://docs.astral.sh/uv/reference/cli/#uv-export--prune) _package_ 
    
Prune the given package from the dependency tree.
Pruned packages will be excluded from the exported requirements file, as will any dependencies that are no longer required after the pruned package is removed. 

[`--python`](https://docs.astral.sh/uv/reference/cli/#uv-export--python), `-p` _python_ 
    
The Python interpreter to use during resolution.
A Python interpreter is required for building source distributions to determine package metadata when there are not wheels.
The interpreter is also used as the fallback value for the minimum Python version if `requires-python` is not set.
See [uv python](https://docs.astral.sh/uv/reference/cli/#uv-python) for details on Python discovery and supported request formats.
May also be set with the `UV_PYTHON` environment variable.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Refresh all cached data 

[`--refresh-package`](https://docs.astral.sh/uv/reference/cli/#uv-export--refresh-package) _refresh-package_ 
    
Refresh cached data for a specific package 

[`--resolution`](https://docs.astral.sh/uv/reference/cli/#uv-export--resolution) _resolution_ 
    
The strategy to use when selecting between the different compatible versions for a given package requirement.
By default, uv will use the latest compatible version of each package (`highest`).
May also be set with the `UV_RESOLUTION` environment variable.
Possible values:
  * `highest`: Resolve the highest compatible version of each package
  * `lowest`: Resolve the lowest compatible version of each package
  * `lowest-direct`: Resolve the lowest compatible version of any direct dependencies, and the highest compatible version of any transitive dependencies



[`--script`](https://docs.astral.sh/uv/reference/cli/#uv-export--script) _script_ 
    
Export the dependencies for the specified PEP 723 Python script, rather than the current project.
If provided, uv will resolve the dependencies based on its inline metadata table, in adherence with PEP 723.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store.     
Allow package upgrades, ignoring pinned versions in any existing output file. Implies `--refresh` 

[`--upgrade-group`](https://docs.astral.sh/uv/reference/cli/#uv-export--upgrade-group) _upgrade-group_ 
    
Allow upgrades for all packages in a dependency group, ignoring pinned versions in any existing output file 

[`--upgrade-package`](https://docs.astral.sh/uv/reference/cli/#uv-export--upgrade-package), `-P` _upgrade-package_ 
    
Allow upgrades for a specific package, ignoring pinned versions in any existing output file. Implies `--refresh-package`     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
## [uv tree](https://docs.astral.sh/uv/reference/cli/#uv-tree)
Display the project's dependency tree
### Usage

```
uv tree [OPTIONS]

```

### Options     
Include dependencies from all dependency groups.
`--no-group` can be used to exclude specific groups. 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-tree--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-tree--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-tree--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-tree--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--config-setting`](https://docs.astral.sh/uv/reference/cli/#uv-tree--config-setting), `--config-settings`, `-C` _config-setting_ 
    
Settings to pass to the PEP 517 build backend, specified as `KEY=VALUE` pairs 

[`--config-settings-package`](https://docs.astral.sh/uv/reference/cli/#uv-tree--config-settings-package), `--config-settings-package` _config-settings-package_ 
    
Settings to pass to the PEP 517 build backend for a specific package, specified as `PACKAGE:KEY=VALUE` pairs 

[`--default-index`](https://docs.astral.sh/uv/reference/cli/#uv-tree--default-index) _default-index_ 
    
The default package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--index` flag.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
May also be set with the `UV_DEFAULT_INDEX` environment variable. 

[`--depth`](https://docs.astral.sh/uv/reference/cli/#uv-tree--depth), `-d` _depth_ 
    
Maximum display depth of the dependency tree
[default: 255] 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-tree--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable. 

[`--exclude-newer`](https://docs.astral.sh/uv/reference/cli/#uv-tree--exclude-newer) _exclude-newer_ 
    
Limit candidate packages to those that were uploaded prior to the given date.
The date is compared against the upload time of each individual distribution artifact (i.e., when each file was uploaded to the package index), not the release date of the package version.
Accepts RFC 3339 timestamps (e.g., `2006-12-02T02:07:43Z`), local dates in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Use `false` to disable `exclude-newer`.
May also be set with the `UV_EXCLUDE_NEWER` environment variable. 

[`--exclude-newer-package`](https://docs.astral.sh/uv/reference/cli/#uv-tree--exclude-newer-package) _exclude-newer-package_ 
    
Limit candidate packages for specific packages to those that were uploaded prior to the given date.
Accepts package-date pairs in the format `PACKAGE=DATE`, where `DATE` is an RFC 3339 timestamp (e.g., `2006-12-02T02:07:43Z`), a local date in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Can be provided multiple times for different packages. 

[`--extra-index-url`](https://docs.astral.sh/uv/reference/cli/#uv-tree--extra-index-url) _extra-index-url_ 
    
(Deprecated: use `--index` instead) Extra URLs of package indexes to use, in addition to `--index-url`.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--index-url` (which defaults to PyPI). When multiple `--extra-index-url` flags are provided, earlier values take priority.
May also be set with the `UV_EXTRA_INDEX_URL` environment variable. 

[`--find-links`](https://docs.astral.sh/uv/reference/cli/#uv-tree--find-links), `-f` _find-links_ 
    
Locations to search for candidate distributions, in addition to those found in the registry indexes.
If a path, the target must be a directory that contains packages as wheel files (`.whl`) or source distributions (e.g., `.tar.gz` or `.zip`) at the top level.
If a URL, the page must contain a flat list of links to package files adhering to the formats described above.
May also be set with the `UV_FIND_LINKS` environment variable. 

[`--fork-strategy`](https://docs.astral.sh/uv/reference/cli/#uv-tree--fork-strategy) _fork-strategy_ 
    
The strategy to use when selecting multiple versions of a given package across Python versions and platforms.
By default, uv will optimize for selecting the latest version of each package for each supported Python version (`requires-python`), while minimizing the number of selected versions across platforms.
Under `fewest`, uv will minimize the number of selected versions for each package, preferring older versions that are compatible with a wider range of supported Python versions or platforms.
May also be set with the `UV_FORK_STRATEGY` environment variable.
Possible values:
  * `fewest`: Optimize for selecting the fewest number of versions for each package. Older versions may be preferred if they are compatible with a wider range of supported Python versions or platforms
  * `requires-python`: Optimize for selecting latest supported version of each package, for each supported Python version



[`--format`](https://docs.astral.sh/uv/reference/cli/#uv-tree--format) _format_ 
    
The format in which to display the dependency graph
[default: text]
Possible values:
  * `text`: Display the dependency graph as a human-readable tree
  * `json`: Display the dependency graph as JSON

    
Display the requirements without locking the project [env: UV_FROZEN=]
If the lockfile is missing, uv will exit with an error. 

[`--group`](https://docs.astral.sh/uv/reference/cli/#uv-tree--group) _group_ 
    
Include dependencies from the specified dependency group.
May be provided multiple times.     
Display the concise help for this command 

[`--index`](https://docs.astral.sh/uv/reference/cli/#uv-tree--index) _index_ 
    
The indexes to use when resolving dependencies, in addition to the default index.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--default-index` (which defaults to PyPI). When multiple `--index` flags are provided, earlier values take priority.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
Relative paths can be disambiguated from index names with `./` or `../` on Unix or `.\\`, `..\\`, `./` or `../` on Windows.
May also be set with the `UV_INDEX` environment variable. 

[`--index-strategy`](https://docs.astral.sh/uv/reference/cli/#uv-tree--index-strategy) _index-strategy_ 
    
The strategy to use when resolving against multiple index URLs.
By default, uv will stop at the first index on which a given package is available, and limit resolutions to those present on that first index (`first-index`). This prevents "dependency confusion" attacks, whereby an attacker can upload a malicious package under the same name to an alternate index.
May also be set with the `UV_INDEX_STRATEGY` environment variable.
Possible values:
  * `first-index`: Only use results from the first index that returns a match for a given package name
  * `unsafe-first-match`: Search for every package name across all indexes, exhausting the versions from the first index before moving on to the next
  * `unsafe-best-match`: Search for every package name across all indexes, preferring the "best" version found. If a package version is in multiple indexes, only look at the entry for the first index



[`--index-url`](https://docs.astral.sh/uv/reference/cli/#uv-tree--index-url), `-i` _index-url_ 
    
(Deprecated: use `--default-index` instead) The URL of the Python package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--extra-index-url` flag.
May also be set with the `UV_INDEX_URL` environment variable. 

[`--invert`](https://docs.astral.sh/uv/reference/cli/#uv-tree--invert), `--reverse` 
    
Show the reverse dependencies for the given package. This flag will invert the tree and display the packages that depend on the given package 

[`--keyring-provider`](https://docs.astral.sh/uv/reference/cli/#uv-tree--keyring-provider) _keyring-provider_ 
    
Attempt to use `keyring` for authentication for index URLs.
At present, only `--keyring-provider subprocess` is supported, which configures uv to use the `keyring` CLI to handle authentication.
Defaults to `disabled`.
May also be set with the `UV_KEYRING_PROVIDER` environment variable.
Possible values:
  * `disabled`: Do not use keyring for credential lookup
  * `subprocess`: Use the `keyring` command for credential lookup



[`--link-mode`](https://docs.astral.sh/uv/reference/cli/#uv-tree--link-mode) _link-mode_ 
    
The method to use when installing packages from the global cache.
This option is only used when building source distributions.
Defaults to `clone` (also known as Copy-on-Write) on macOS and Linux, and `hardlink` on Windows.
WARNING: The use of symlink link mode is discouraged, as they create tight coupling between the cache and the target environment. For example, clearing the cache (`uv cache clean`) will break all installed packages by way of removing the underlying source files. Use symlinks with caution.
May also be set with the `UV_LINK_MODE` environment variable.
Possible values:
  * `clone`: Clone (i.e., copy-on-write) packages from the source into the destination
  * `copy`: Copy packages from the source into the destination
  * `hardlink`: Hard link packages from the source into the destination
  * `symlink`: Symbolically link packages from the source into the destination

    
Assert that the `uv.lock` will remain unchanged [env: UV_LOCKED=]
Requires that the lockfile is up-to-date. If the lockfile is missing or needs to be updated, uv will exit with an error.     
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions.     
Don't install pre-built wheels.
The given packages will be built and installed from source. The resolver will still use pre-built wheels to extract package metadata, if available.
May also be set with the `UV_NO_BINARY` environment variable. 

[`--no-binary-package`](https://docs.astral.sh/uv/reference/cli/#uv-tree--no-binary-package) _no-binary-package_ 
    
Don't install pre-built wheels for a specific package [env: `UV_NO_BINARY_PACKAGE`=]     
Don't build source distributions.
When enabled, uv will reuse cached wheels from previously built source distributions, but operations that require building a source distribution will exit with an error. First-party packages, such as projects in the workspace, will still be built. uv will also still build editable requirements, and their build backends may run arbitrary Python code.
May also be set with the `UV_NO_BUILD` environment variable. 

[`--no-build-isolation`](https://docs.astral.sh/uv/reference/cli/#uv-tree--no-build-isolation)
    
Disable isolation when building source distributions.
Assumes that build dependencies specified by PEP 518 are already installed.
May also be set with the `UV_NO_BUILD_ISOLATION` environment variable. 

[`--no-build-isolation-package`](https://docs.astral.sh/uv/reference/cli/#uv-tree--no-build-isolation-package) _no-build-isolation-package_ 
    
Disable isolation when building source distributions for a specific package.
Assumes that the packages' build dependencies specified by PEP 518 are already installed. 

[`--no-build-package`](https://docs.astral.sh/uv/reference/cli/#uv-tree--no-build-package) _no-build-package_ 
    
Don't build source distributions for a specific package [env: `UV_NO_BUILD_PACKAGE`=]
First-party packages, such as projects in the workspace, will still be built. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-tree--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable.     
Do not de-duplicate repeated dependencies. Usually, when a package has already displayed its dependencies, further occurrences will not re-display its dependencies, and will include a (*) to indicate it has already been shown. This flag will cause those duplicates to be repeated 

[`--no-default-groups`](https://docs.astral.sh/uv/reference/cli/#uv-tree--no-default-groups)
    
Ignore the default dependency groups.
uv includes the groups defined in `tool.uv.default-groups` by default. This disables that option, however, specific groups can still be included with `--group`.
May also be set with the `UV_NO_DEFAULT_GROUPS` environment variable.     
Disable the development dependency group [env: UV_NO_DEV=]
This option is an alias of `--no-group dev`. See `--no-default-groups` to disable all default groups instead.
This option is only available when running in a project. 

[`--no-group`](https://docs.astral.sh/uv/reference/cli/#uv-tree--no-group) _no-group_ 
    
Disable the specified dependency group [env: `UV_NO_GROUP`=]
This option always takes precedence over default groups, `--all-groups`, and `--group`.
May be provided multiple times.     
Ignore the registry index (e.g., PyPI), instead relying on direct URL dependencies and those provided via `--find-links` 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-tree--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-tree--no-python-downloads)
    
Disable automatic downloads of Python.     
Ignore the `tool.uv.sources` table when resolving dependencies. Used to lock against the standards-compliant, publishable package metadata, as opposed to using any workspace, Git, URL, or local path sources
May also be set with the `UV_NO_SOURCES` environment variable. 

[`--no-sources-package`](https://docs.astral.sh/uv/reference/cli/#uv-tree--no-sources-package) _no-sources-package_ 
    
Don't use sources from the `tool.uv.sources` table for the specified packages [env: `UV_NO_SOURCES_PACKAGE`=]     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files.     
Only include the development dependency group.
The project and its dependencies will be omitted.
This option is an alias for `--only-group dev`. Implies `--no-default-groups`. 

[`--only-group`](https://docs.astral.sh/uv/reference/cli/#uv-tree--only-group) _only-group_ 
    
Only include dependencies from the specified dependency group.
The project and its dependencies will be omitted.
May be provided multiple times. Implies `--no-default-groups`.     
Show the latest available version of each package in the tree 

[`--package`](https://docs.astral.sh/uv/reference/cli/#uv-tree--package) _package_ 
    
Display only the specified packages 

[`--prerelease`](https://docs.astral.sh/uv/reference/cli/#uv-tree--prerelease) _prerelease_ 
    
The strategy to use when considering pre-release versions.
By default, uv will prefer stable candidates, falling back to pre-releases only after every stable candidate that satisfies the active constraints is rejected (`if-necessary`).
May also be set with the `UV_PRERELEASE` environment variable.
Possible values:
  * `disallow`: Disallow all pre-release versions
  * `allow`: Allow all pre-release versions
  * `if-necessary`: Prefer stable versions, falling back to pre-release versions when necessary
  * `explicit`: Prefer stable versions for first-party packages with explicit pre-release specifiers, falling back to pre-release versions when necessary. Disallow pre-release versions for all other packages
  * `if-necessary-or-explicit`: Deprecated alias for `if-necessary`



[`--prerelease-package`](https://docs.astral.sh/uv/reference/cli/#uv-tree--prerelease-package) _prerelease-package_ 
    
The strategy to use when considering pre-release versions for a specific package.
Accepts package-mode pairs in the format `PACKAGE=MODE`, where `MODE` is any value accepted by `--prerelease`.
May be provided multiple times for different packages. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-tree--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable. 

[`--prune`](https://docs.astral.sh/uv/reference/cli/#uv-tree--prune) _prune_ 
    
Prune the given package from the display of the dependency tree 

[`--python`](https://docs.astral.sh/uv/reference/cli/#uv-tree--python), `-p` _python_ 
    
The Python interpreter to use for locking and filtering.
By default, the tree is filtered to match the platform as reported by the Python interpreter. Use `--universal` to display the tree for all platforms, or use `--python-version` or `--python-platform` to override a subset of markers.
See [uv python](https://docs.astral.sh/uv/reference/cli/#uv-python) for details on Python discovery and supported request formats.
May also be set with the `UV_PYTHON` environment variable. 

[`--python-platform`](https://docs.astral.sh/uv/reference/cli/#uv-tree--python-platform) _python-platform_ 
    
The platform to use when filtering the tree.
For example, pass `--platform windows` to display the dependencies that would be included when installing on Windows.
Represented as a "target triple", a string that describes the target platform in terms of its CPU, vendor, and operating system name, like `x86_64-unknown-linux-gnu` or `aarch64-apple-darwin`.
Possible values:
  * `windows`: An alias for `x86_64-pc-windows-msvc`, the default target for Windows
  * `linux`: An alias for `x86_64-unknown-linux-gnu`, the default target for Linux
  * `macos`: An alias for `aarch64-apple-darwin`, the default target for macOS
  * `x86_64-pc-windows-msvc`: A 64-bit x86 Windows target
  * `aarch64-pc-windows-msvc`: An ARM64 Windows target
  * `i686-pc-windows-msvc`: A 32-bit x86 Windows target
  * `x86_64-unknown-linux-gnu`: An x86 Linux target. Equivalent to `x86_64-manylinux_2_28`
  * `aarch64-apple-darwin`: An ARM-based macOS target, as seen on Apple Silicon devices
  * `x86_64-apple-darwin`: An x86 macOS target
  * `aarch64-unknown-linux-gnu`: An ARM64 Linux target. Equivalent to `aarch64-manylinux_2_28`
  * `aarch64-unknown-linux-musl`: An ARM64 Linux target
  * `x86_64-unknown-linux-musl`: An `x86_64` Linux target
  * `riscv64-unknown-linux`: A RISCV64 Linux target
  * `x86_64-manylinux2014`: An `x86_64` target for the `manylinux2014` platform. Equivalent to `x86_64-manylinux_2_17`
  * `x86_64-manylinux_2_17`: An `x86_64` target for the `manylinux_2_17` platform
  * `x86_64-manylinux_2_28`: An `x86_64` target for the `manylinux_2_28` platform
  * `x86_64-manylinux_2_31`: An `x86_64` target for the `manylinux_2_31` platform
  * `x86_64-manylinux_2_32`: An `x86_64` target for the `manylinux_2_32` platform
  * `x86_64-manylinux_2_33`: An `x86_64` target for the `manylinux_2_33` platform
  * `x86_64-manylinux_2_34`: An `x86_64` target for the `manylinux_2_34` platform
  * `x86_64-manylinux_2_35`: An `x86_64` target for the `manylinux_2_35` platform
  * `x86_64-manylinux_2_36`: An `x86_64` target for the `manylinux_2_36` platform
  * `x86_64-manylinux_2_37`: An `x86_64` target for the `manylinux_2_37` platform
  * `x86_64-manylinux_2_38`: An `x86_64` target for the `manylinux_2_38` platform
  * `x86_64-manylinux_2_39`: An `x86_64` target for the `manylinux_2_39` platform
  * `x86_64-manylinux_2_40`: An `x86_64` target for the `manylinux_2_40` platform
  * `aarch64-manylinux2014`: An ARM64 target for the `manylinux2014` platform. Equivalent to `aarch64-manylinux_2_17`
  * `aarch64-manylinux_2_17`: An ARM64 target for the `manylinux_2_17` platform
  * `aarch64-manylinux_2_28`: An ARM64 target for the `manylinux_2_28` platform
  * `aarch64-manylinux_2_31`: An ARM64 target for the `manylinux_2_31` platform
  * `aarch64-manylinux_2_32`: An ARM64 target for the `manylinux_2_32` platform
  * `aarch64-manylinux_2_33`: An ARM64 target for the `manylinux_2_33` platform
  * `aarch64-manylinux_2_34`: An ARM64 target for the `manylinux_2_34` platform
  * `aarch64-manylinux_2_35`: An ARM64 target for the `manylinux_2_35` platform
  * `aarch64-manylinux_2_36`: An ARM64 target for the `manylinux_2_36` platform
  * `aarch64-manylinux_2_37`: An ARM64 target for the `manylinux_2_37` platform
  * `aarch64-manylinux_2_38`: An ARM64 target for the `manylinux_2_38` platform
  * `aarch64-manylinux_2_39`: An ARM64 target for the `manylinux_2_39` platform
  * `aarch64-manylinux_2_40`: An ARM64 target for the `manylinux_2_40` platform
  * `aarch64-linux-android`: An ARM64 Android target
  * `x86_64-linux-android`: An `x86_64` Android target
  * `wasm32-pyodide2024`: A wasm32 target using the Pyodide 2024 platform. Meant for use with Python 3.12. See <https://pyodide.org/en/stable/development/abi/312.html>
  * `wasm32-pyodide2025`: A wasm32 target using the Pyodide 2025 platform. Meant for use with Python 3.13. See <https://pyodide.org/en/stable/development/abi/313.html>
  * `arm64-apple-ios`: An ARM64 target for iOS device
  * `arm64-apple-ios-simulator`: An ARM64 target for iOS simulator
  * `x86_64-apple-ios-simulator`: An `x86_64` target for iOS simulator



[`--python-version`](https://docs.astral.sh/uv/reference/cli/#uv-tree--python-version) _python-version_ 
    
The Python version to use when filtering the tree.
For example, pass `--python-version 3.10` to display the dependencies that would be included when installing on Python 3.10.
Defaults to the version of the discovered Python interpreter.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout. 

[`--resolution`](https://docs.astral.sh/uv/reference/cli/#uv-tree--resolution) _resolution_ 
    
The strategy to use when selecting between the different compatible versions for a given package requirement.
By default, uv will use the latest compatible version of each package (`highest`).
May also be set with the `UV_RESOLUTION` environment variable.
Possible values:
  * `highest`: Resolve the highest compatible version of each package
  * `lowest`: Resolve the lowest compatible version of each package
  * `lowest-direct`: Resolve the lowest compatible version of any direct dependencies, and the highest compatible version of any transitive dependencies



[`--script`](https://docs.astral.sh/uv/reference/cli/#uv-tree--script) _script_ 
    
Show the dependency tree the specified PEP 723 Python script, rather than the current project.
If provided, uv will resolve the dependencies based on its inline metadata table, in adherence with PEP 723.     
Show compressed wheel sizes for packages in the tree     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store.     
Show a platform-independent dependency tree.
Shows resolved package versions for all Python versions and platforms, rather than filtering to those that are relevant for the current environment.
Multiple versions may be shown for a each package.     
Allow package upgrades, ignoring pinned versions in any existing output file. Implies `--refresh` 

[`--upgrade-group`](https://docs.astral.sh/uv/reference/cli/#uv-tree--upgrade-group) _upgrade-group_ 
    
Allow upgrades for all packages in a dependency group, ignoring pinned versions in any existing output file 

[`--upgrade-package`](https://docs.astral.sh/uv/reference/cli/#uv-tree--upgrade-package), `-P` _upgrade-package_ 
    
Allow upgrades for a specific package, ignoring pinned versions in any existing output file. Implies `--refresh-package`     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
## [uv format](https://docs.astral.sh/uv/reference/cli/#uv-format)
Format Python code in the project.
Formats Python code using the Ruff formatter. By default, all Python files in the project are formatted. This command has the same behavior as running `ruff format` in the project root.
To check if files are formatted without modifying them, use `--check`. To see a diff of formatting changes, use `--diff`.
Additional arguments can be passed to Ruff after `--`.
### Usage

```
uv format [OPTIONS] [-- <EXTRA_ARGS>...]

```

### Arguments     
Additional arguments to pass to Ruff.
For example, use `uv format -- --line-length 100` to set the line length or `uv format -- src/module/foo.py` to format a specific file.
### Options 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-format--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-format--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable.     
Check if files are formatted without applying changes 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-format--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-format--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable.     
Show a diff of formatting changes without applying them.
Implies `--check`. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-format--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable. 

[`--exclude-newer`](https://docs.astral.sh/uv/reference/cli/#uv-format--exclude-newer) _exclude-newer_ 
    
Limit candidate Ruff versions to those released prior to the given date.
Accepts a superset of [RFC 3339](https://www.rfc-editor.org/rfc/rfc3339.html) (e.g., `2006-12-02T02:07:43Z`) or local date in the same format (e.g. `2006-12-02`), as well as durations relative to "now" (e.g., `-1 week`).
Use `false` to disable `exclude-newer`.
May also be set with the `UV_EXCLUDE_NEWER` environment variable.     
Display the concise help for this command     
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-format--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable. 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-format--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars.     
Avoid discovering a project or workspace.
Instead of running the formatter in the context of the current project, run it in the context of the current directory. This is useful when the current directory is not a project.
May also be set with the `UV_NO_PROJECT` environment variable. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-format--no-python-downloads)
    
Disable automatic downloads of Python.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-format--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store.     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>) 

[`--version`](https://docs.astral.sh/uv/reference/cli/#uv-format--version) _version_ 
    
The version of Ruff to use for formatting.
Accepts either a version (e.g., `0.8.2`) which will be treated as an exact pin, a version specifier (e.g., `>=0.8.0`), or `latest` to use the latest available version.
By default, a constrained version range of Ruff will be used (e.g., `>=0.15,<0.16`).
## [uv check](https://docs.astral.sh/uv/reference/cli/#uv-check)
Run checks on the project.
Currently, this type checks Python code using ty. By default, all Python files in the project are checked.
To apply safe fixes to type-checking errors, use `--fix`.
### Usage

```
uv check [OPTIONS]

```

### Options     
Include all optional dependencies.
When two or more extras are declared as conflicting in `tool.uv.conflicts`, using this flag will always result in an error.
Note that all optional dependencies are always included in the resolution; this option only affects the selection of packages to install.     
Include dependencies from all dependency groups.
`--no-group` can be used to exclude specific groups.     
Check all packages in the workspace.
The workspace's environment is synchronized to include all workspace members, and files in every member are checked. 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-check--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-check--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-check--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--compile-bytecode`](https://docs.astral.sh/uv/reference/cli/#uv-check--compile-bytecode), `--compile` 
    
Compile Python files to bytecode after installation.
By default, uv does not compile Python (`.py`) files to bytecode (`__pycache__/*.pyc`); instead, compilation is performed lazily the first time a module is imported. For use-cases in which start time is critical, such as CLI applications and Docker containers, this option can be enabled to trade longer installation times for faster start times.
When enabled, install operations (e.g., `uv pip install`) will compile installed or reinstalled Python files. Commands that perform a sync operation (e.g., `uv sync` or `uv run`) will process the entire site-packages directory including packages that are not being modified.
May also be set with the `UV_COMPILE_BYTECODE` environment variable. 

[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-check--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--config-setting`](https://docs.astral.sh/uv/reference/cli/#uv-check--config-setting), `--config-settings`, `-C` _config-setting_ 
    
Settings to pass to the PEP 517 build backend, specified as `KEY=VALUE` pairs 

[`--config-settings-package`](https://docs.astral.sh/uv/reference/cli/#uv-check--config-settings-package), `--config-settings-package` _config-settings-package_ 
    
Settings to pass to the PEP 517 build backend for a specific package, specified as `PACKAGE:KEY=VALUE` pairs 

[`--default-index`](https://docs.astral.sh/uv/reference/cli/#uv-check--default-index) _default-index_ 
    
The default package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--index` flag.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
May also be set with the `UV_DEFAULT_INDEX` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-check--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable. 

[`--exclude-newer`](https://docs.astral.sh/uv/reference/cli/#uv-check--exclude-newer) _exclude-newer_ 
    
Limit candidate packages to those that were uploaded prior to the given date.
The date is compared against the upload time of each individual distribution artifact (i.e., when each file was uploaded to the package index), not the release date of the package version.
Accepts RFC 3339 timestamps (e.g., `2006-12-02T02:07:43Z`), local dates in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Use `false` to disable `exclude-newer`.
May also be set with the `UV_EXCLUDE_NEWER` environment variable. 

[`--exclude-newer-package`](https://docs.astral.sh/uv/reference/cli/#uv-check--exclude-newer-package) _exclude-newer-package_ 
    
Limit candidate packages for specific packages to those that were uploaded prior to the given date.
Accepts package-date pairs in the format `PACKAGE=DATE`, where `DATE` is an RFC 3339 timestamp (e.g., `2006-12-02T02:07:43Z`), a local date in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Can be provided multiple times for different packages. 

[`--extra`](https://docs.astral.sh/uv/reference/cli/#uv-check--extra) _extra_ 
    
Include optional dependencies from the specified extra name.
May be provided more than once.
When multiple extras or groups are specified that appear in `tool.uv.conflicts`, uv will report an error.
Note that all optional dependencies are always included in the resolution; this option only affects the selection of packages to install. 

[`--extra-index-url`](https://docs.astral.sh/uv/reference/cli/#uv-check--extra-index-url) _extra-index-url_ 
    
(Deprecated: use `--index` instead) Extra URLs of package indexes to use, in addition to `--index-url`.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--index-url` (which defaults to PyPI). When multiple `--extra-index-url` flags are provided, earlier values take priority.
May also be set with the `UV_EXTRA_INDEX_URL` environment variable. 

[`--find-links`](https://docs.astral.sh/uv/reference/cli/#uv-check--find-links), `-f` _find-links_ 
    
Locations to search for candidate distributions, in addition to those found in the registry indexes.
If a path, the target must be a directory that contains packages as wheel files (`.whl`) or source distributions (e.g., `.tar.gz` or `.zip`) at the top level.
If a URL, the page must contain a flat list of links to package files adhering to the formats described above.
May also be set with the `UV_FIND_LINKS` environment variable.     
Apply safe fixes to resolve type-checking errors 

[`--fork-strategy`](https://docs.astral.sh/uv/reference/cli/#uv-check--fork-strategy) _fork-strategy_ 
    
The strategy to use when selecting multiple versions of a given package across Python versions and platforms.
By default, uv will optimize for selecting the latest version of each package for each supported Python version (`requires-python`), while minimizing the number of selected versions across platforms.
Under `fewest`, uv will minimize the number of selected versions for each package, preferring older versions that are compatible with a wider range of supported Python versions or platforms.
May also be set with the `UV_FORK_STRATEGY` environment variable.
Possible values:
  * `fewest`: Optimize for selecting the fewest number of versions for each package. Older versions may be preferred if they are compatible with a wider range of supported Python versions or platforms
  * `requires-python`: Optimize for selecting latest supported version of each package, for each supported Python version

    
Sync without updating the `uv.lock` file [env: UV_FROZEN=]
Instead of checking if the lockfile is up-to-date, uses the versions in the lockfile as the source of truth. If the lockfile is missing, uv will exit with an error. If the `pyproject.toml` includes changes to dependencies that have not been included in the lockfile yet, they will not be present in the environment. 

[`--group`](https://docs.astral.sh/uv/reference/cli/#uv-check--group) _group_ 
    
Include dependencies from the specified dependency group.
When multiple extras or groups are specified that appear in `tool.uv.conflicts`, uv will report an error.
May be provided multiple times.     
Display the concise help for this command 

[`--index`](https://docs.astral.sh/uv/reference/cli/#uv-check--index) _index_ 
    
The indexes to use when resolving dependencies, in addition to the default index.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--default-index` (which defaults to PyPI). When multiple `--index` flags are provided, earlier values take priority.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
Relative paths can be disambiguated from index names with `./` or `../` on Unix or `.\\`, `..\\`, `./` or `../` on Windows.
May also be set with the `UV_INDEX` environment variable. 

[`--index-strategy`](https://docs.astral.sh/uv/reference/cli/#uv-check--index-strategy) _index-strategy_ 
    
The strategy to use when resolving against multiple index URLs.
By default, uv will stop at the first index on which a given package is available, and limit resolutions to those present on that first index (`first-index`). This prevents "dependency confusion" attacks, whereby an attacker can upload a malicious package under the same name to an alternate index.
May also be set with the `UV_INDEX_STRATEGY` environment variable.
Possible values:
  * `first-index`: Only use results from the first index that returns a match for a given package name
  * `unsafe-first-match`: Search for every package name across all indexes, exhausting the versions from the first index before moving on to the next
  * `unsafe-best-match`: Search for every package name across all indexes, preferring the "best" version found. If a package version is in multiple indexes, only look at the entry for the first index



[`--index-url`](https://docs.astral.sh/uv/reference/cli/#uv-check--index-url), `-i` _index-url_ 
    
(Deprecated: use `--default-index` instead) The URL of the Python package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--extra-index-url` flag.
May also be set with the `UV_INDEX_URL` environment variable.     
Run checks without mutating project state [env: UV_ISOLATED=]
Uses a temporary virtual environment and leaves existing environments and the project lockfile unchanged. Declared project requirements are resolved and installed into the temporary environment. 

[`--keyring-provider`](https://docs.astral.sh/uv/reference/cli/#uv-check--keyring-provider) _keyring-provider_ 
    
Attempt to use `keyring` for authentication for index URLs.
At present, only `--keyring-provider subprocess` is supported, which configures uv to use the `keyring` CLI to handle authentication.
Defaults to `disabled`.
May also be set with the `UV_KEYRING_PROVIDER` environment variable.
Possible values:
  * `disabled`: Do not use keyring for credential lookup
  * `subprocess`: Use the `keyring` command for credential lookup



[`--link-mode`](https://docs.astral.sh/uv/reference/cli/#uv-check--link-mode) _link-mode_ 
    
The method to use when installing packages from the global cache.
Defaults to `clone` (also known as Copy-on-Write) on macOS and Linux, and `hardlink` on Windows.
WARNING: The use of symlink link mode is discouraged, as they create tight coupling between the cache and the target environment. For example, clearing the cache (`uv cache clean`) will break all installed packages by way of removing the underlying source files. Use symlinks with caution.
May also be set with the `UV_LINK_MODE` environment variable.
Possible values:
  * `clone`: Clone (i.e., copy-on-write) packages from the source into the destination
  * `copy`: Copy packages from the source into the destination
  * `hardlink`: Hard link packages from the source into the destination
  * `symlink`: Symbolically link packages from the source into the destination

    
Assert that the `uv.lock` will remain unchanged [env: UV_LOCKED=]
Requires that the lockfile is up-to-date. If the lockfile is missing or needs to be updated, uv will exit with an error.     
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions.     
Don't install pre-built wheels.
The given packages will be built and installed from source. The resolver will still use pre-built wheels to extract package metadata, if available.
May also be set with the `UV_NO_BINARY` environment variable. 

[`--no-binary-package`](https://docs.astral.sh/uv/reference/cli/#uv-check--no-binary-package) _no-binary-package_ 
    
Don't install pre-built wheels for a specific package [env: `UV_NO_BINARY_PACKAGE`=]     
Don't build source distributions.
When enabled, uv will reuse cached wheels from previously built source distributions, but operations that require building a source distribution will exit with an error. First-party packages, such as projects in the workspace, will still be built. uv will also still build editable requirements, and their build backends may run arbitrary Python code.
May also be set with the `UV_NO_BUILD` environment variable. 

[`--no-build-isolation`](https://docs.astral.sh/uv/reference/cli/#uv-check--no-build-isolation)
    
Disable isolation when building source distributions.
Assumes that build dependencies specified by PEP 518 are already installed.
May also be set with the `UV_NO_BUILD_ISOLATION` environment variable. 

[`--no-build-isolation-package`](https://docs.astral.sh/uv/reference/cli/#uv-check--no-build-isolation-package) _no-build-isolation-package_ 
    
Disable isolation when building source distributions for a specific package.
Assumes that the packages' build dependencies specified by PEP 518 are already installed. 

[`--no-build-package`](https://docs.astral.sh/uv/reference/cli/#uv-check--no-build-package) _no-build-package_ 
    
Don't build source distributions for a specific package [env: `UV_NO_BUILD_PACKAGE`=]
First-party packages, such as projects in the workspace, will still be built. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-check--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable. 

[`--no-default-groups`](https://docs.astral.sh/uv/reference/cli/#uv-check--no-default-groups)
    
Ignore the default dependency groups.
uv includes the groups defined in `tool.uv.default-groups` by default. This disables that option, however, specific groups can still be included with `--group`.
May also be set with the `UV_NO_DEFAULT_GROUPS` environment variable.     
Disable the development dependency group [env: UV_NO_DEV=]
This option is an alias of `--no-group dev`. See `--no-default-groups` to disable all default groups instead.
This option is only available when running in a project. 

[`--no-extra`](https://docs.astral.sh/uv/reference/cli/#uv-check--no-extra) _no-extra_ 
    
Exclude the specified optional dependencies, if `--all-extras` is supplied.
May be provided multiple times. 

[`--no-group`](https://docs.astral.sh/uv/reference/cli/#uv-check--no-group) _no-group_ 
    
Disable the specified dependency group [env: `UV_NO_GROUP`=]
This option always takes precedence over default groups, `--all-groups`, and `--group`.
May be provided multiple times.     
Ignore the registry index (e.g., PyPI), instead relying on direct URL dependencies and those provided via `--find-links` 

[`--no-install-project`](https://docs.astral.sh/uv/reference/cli/#uv-check--no-install-project)
    
Do not install the current project [env: UV_NO_INSTALL_PROJECT=]
By default, the current project is installed into the environment with all of its dependencies. The `--no-install-project` option excludes the project itself while still installing its dependencies, which is useful when the project can be type-checked from its source tree without building native extensions. 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-check--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars.     
Avoid discovering a project or workspace.
Instead of running checks in the context of the current project, run them in the context of the current directory. This is useful when the current directory is not a project.
May also be set with the `UV_NO_PROJECT` environment variable. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-check--no-python-downloads)
    
Disable automatic downloads of Python.     
Ignore the `tool.uv.sources` table when resolving dependencies. Used to lock against the standards-compliant, publishable package metadata, as opposed to using any workspace, Git, URL, or local path sources
May also be set with the `UV_NO_SOURCES` environment variable. 

[`--no-sources-package`](https://docs.astral.sh/uv/reference/cli/#uv-check--no-sources-package) _no-sources-package_ 
    
Don't use sources from the `tool.uv.sources` table for the specified packages [env: `UV_NO_SOURCES_PACKAGE`=]     
Avoid syncing the virtual environment [env: UV_NO_SYNC=]     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files.     
Only include the development dependency group.
The project and its dependencies will be omitted.
This option is an alias for `--only-group dev`. Implies `--no-default-groups`. 

[`--only-group`](https://docs.astral.sh/uv/reference/cli/#uv-check--only-group) _only-group_ 
    
Only include dependencies from the specified dependency group.
The project and its dependencies will be omitted.
May be provided multiple times. Implies `--no-default-groups`. 

[`--package`](https://docs.astral.sh/uv/reference/cli/#uv-check--package) _package_ 
    
Check specific packages in the workspace.
The workspace's environment is synchronized to include the selected members and their dependencies. Only files owned by the selected members are checked. 

[`--prerelease`](https://docs.astral.sh/uv/reference/cli/#uv-check--prerelease) _prerelease_ 
    
The strategy to use when considering pre-release versions.
By default, uv will prefer stable candidates, falling back to pre-releases only after every stable candidate that satisfies the active constraints is rejected (`if-necessary`).
May also be set with the `UV_PRERELEASE` environment variable.
Possible values:
  * `disallow`: Disallow all pre-release versions
  * `allow`: Allow all pre-release versions
  * `if-necessary`: Prefer stable versions, falling back to pre-release versions when necessary
  * `explicit`: Prefer stable versions for first-party packages with explicit pre-release specifiers, falling back to pre-release versions when necessary. Disallow pre-release versions for all other packages
  * `if-necessary-or-explicit`: Deprecated alias for `if-necessary`



[`--prerelease-package`](https://docs.astral.sh/uv/reference/cli/#uv-check--prerelease-package) _prerelease-package_ 
    
The strategy to use when considering pre-release versions for a specific package.
Accepts package-mode pairs in the format `PACKAGE=MODE`, where `MODE` is any value accepted by `--prerelease`.
May be provided multiple times for different packages. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-check--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable. 

[`--python`](https://docs.astral.sh/uv/reference/cli/#uv-check--python), `-p` _python_ 
    
The Python interpreter to use for the project environment.
By default, the first interpreter that meets the project's `requires-python` constraint is used.
See `uv python` for more details on Python discovery and requests.
May also be set with the `UV_PYTHON` environment variable.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Refresh all cached data 

[`--refresh-package`](https://docs.astral.sh/uv/reference/cli/#uv-check--refresh-package) _refresh-package_ 
    
Refresh cached data for a specific package 

[`--reinstall`](https://docs.astral.sh/uv/reference/cli/#uv-check--reinstall), `--force-reinstall` 
    
Reinstall all packages, regardless of whether they're already installed. Implies `--refresh` 

[`--reinstall-package`](https://docs.astral.sh/uv/reference/cli/#uv-check--reinstall-package) _reinstall-package_ 
    
Reinstall a specific package, regardless of whether it's already installed. Implies `--refresh-package` 

[`--resolution`](https://docs.astral.sh/uv/reference/cli/#uv-check--resolution) _resolution_ 
    
The strategy to use when selecting between the different compatible versions for a given package requirement.
By default, uv will use the latest compatible version of each package (`highest`).
May also be set with the `UV_RESOLUTION` environment variable.
Possible values:
  * `highest`: Resolve the highest compatible version of each package
  * `lowest`: Resolve the lowest compatible version of each package
  * `lowest-direct`: Resolve the lowest compatible version of any direct dependencies, and the highest compatible version of any transitive dependencies



[`--script`](https://docs.astral.sh/uv/reference/cli/#uv-check--script) _script_ 
    
Run checks for the specified PEP 723 Python script, rather than the current project.
If provided, uv will use the dependencies based on the script's inline metadata table, in adherence with PEP 723.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store. 

[`--ty-version`](https://docs.astral.sh/uv/reference/cli/#uv-check--ty-version) _ty-version_ 
    
The version of ty to use for type checking.
Accepts either a version (e.g., `0.0.1`) which will be treated as an exact pin, a version specifier (e.g., `>=0.0.1`), or `latest` to use the latest available version.
By default, the exact version resolved in `uv.lock` will be used when `ty` is a project dependency or a dependency in the project's `dev` group. Otherwise, a constrained version range of ty will be used (e.g., `>=0.0,<0.1`).     
Allow package upgrades, ignoring pinned versions in any existing output file. Implies `--refresh` 

[`--upgrade-group`](https://docs.astral.sh/uv/reference/cli/#uv-check--upgrade-group) _upgrade-group_ 
    
Allow upgrades for all packages in a dependency group, ignoring pinned versions in any existing output file 

[`--upgrade-package`](https://docs.astral.sh/uv/reference/cli/#uv-check--upgrade-package), `-P` _upgrade-package_ 
    
Allow upgrades for a specific package, ignoring pinned versions in any existing output file. Implies `--refresh-package`     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
## [uv audit](https://docs.astral.sh/uv/reference/cli/#uv-audit)
Audit the project's dependencies.
Dependencies are audited for known vulnerabilities, as well as 'adverse' statuses such as deprecation and quarantine.
By default, all extras and groups within the project are audited. To exclude extras and/or groups from the audit, use the `--no-extra`, `--no-group`, and related options.
### Usage

```
uv audit [OPTIONS]

```

### Options 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-audit--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-audit--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-audit--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-audit--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--config-setting`](https://docs.astral.sh/uv/reference/cli/#uv-audit--config-setting), `--config-settings`, `-C` _config-setting_ 
    
Settings to pass to the PEP 517 build backend, specified as `KEY=VALUE` pairs 

[`--config-settings-package`](https://docs.astral.sh/uv/reference/cli/#uv-audit--config-settings-package), `--config-settings-package` _config-settings-package_ 
    
Settings to pass to the PEP 517 build backend for a specific package, specified as `PACKAGE:KEY=VALUE` pairs 

[`--default-index`](https://docs.astral.sh/uv/reference/cli/#uv-audit--default-index) _default-index_ 
    
The default package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--index` flag.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
May also be set with the `UV_DEFAULT_INDEX` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-audit--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable. 

[`--exclude-newer`](https://docs.astral.sh/uv/reference/cli/#uv-audit--exclude-newer) _exclude-newer_ 
    
Limit candidate packages to those that were uploaded prior to the given date.
The date is compared against the upload time of each individual distribution artifact (i.e., when each file was uploaded to the package index), not the release date of the package version.
Accepts RFC 3339 timestamps (e.g., `2006-12-02T02:07:43Z`), local dates in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Use `false` to disable `exclude-newer`.
May also be set with the `UV_EXCLUDE_NEWER` environment variable. 

[`--exclude-newer-package`](https://docs.astral.sh/uv/reference/cli/#uv-audit--exclude-newer-package) _exclude-newer-package_ 
    
Limit candidate packages for specific packages to those that were uploaded prior to the given date.
Accepts package-date pairs in the format `PACKAGE=DATE`, where `DATE` is an RFC 3339 timestamp (e.g., `2006-12-02T02:07:43Z`), a local date in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Can be provided multiple times for different packages. 

[`--extra-index-url`](https://docs.astral.sh/uv/reference/cli/#uv-audit--extra-index-url) _extra-index-url_ 
    
(Deprecated: use `--index` instead) Extra URLs of package indexes to use, in addition to `--index-url`.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--index-url` (which defaults to PyPI). When multiple `--extra-index-url` flags are provided, earlier values take priority.
May also be set with the `UV_EXTRA_INDEX_URL` environment variable. 

[`--find-links`](https://docs.astral.sh/uv/reference/cli/#uv-audit--find-links), `-f` _find-links_ 
    
Locations to search for candidate distributions, in addition to those found in the registry indexes.
If a path, the target must be a directory that contains packages as wheel files (`.whl`) or source distributions (e.g., `.tar.gz` or `.zip`) at the top level.
If a URL, the page must contain a flat list of links to package files adhering to the formats described above.
May also be set with the `UV_FIND_LINKS` environment variable. 

[`--fork-strategy`](https://docs.astral.sh/uv/reference/cli/#uv-audit--fork-strategy) _fork-strategy_ 
    
The strategy to use when selecting multiple versions of a given package across Python versions and platforms.
By default, uv will optimize for selecting the latest version of each package for each supported Python version (`requires-python`), while minimizing the number of selected versions across platforms.
Under `fewest`, uv will minimize the number of selected versions for each package, preferring older versions that are compatible with a wider range of supported Python versions or platforms.
May also be set with the `UV_FORK_STRATEGY` environment variable.
Possible values:
  * `fewest`: Optimize for selecting the fewest number of versions for each package. Older versions may be preferred if they are compatible with a wider range of supported Python versions or platforms
  * `requires-python`: Optimize for selecting latest supported version of each package, for each supported Python version

    
Audit the requirements without locking the project [env: UV_FROZEN=]
If the lockfile is missing, uv will exit with an error.     
Display the concise help for this command 

[`--ignore`](https://docs.astral.sh/uv/reference/cli/#uv-audit--ignore) _ignore_ 
    
Ignore a vulnerability by ID.
Vulnerabilities matching any of the provided IDs (including aliases) will be excluded from the audit results.
May be provided multiple times. 

[`--ignore-until-fixed`](https://docs.astral.sh/uv/reference/cli/#uv-audit--ignore-until-fixed) _ignore-until-fixed_ 
    
Ignore a vulnerability by ID, but only while no fix is available.
Vulnerabilities matching any of the provided IDs (including aliases) will be excluded from the audit results as long as they have no known fix versions. Once a fix version becomes available, the vulnerability will be reported again.
May be provided multiple times. 

[`--index`](https://docs.astral.sh/uv/reference/cli/#uv-audit--index) _index_ 
    
The indexes to use when resolving dependencies, in addition to the default index.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--default-index` (which defaults to PyPI). When multiple `--index` flags are provided, earlier values take priority.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
Relative paths can be disambiguated from index names with `./` or `../` on Unix or `.\\`, `..\\`, `./` or `../` on Windows.
May also be set with the `UV_INDEX` environment variable. 

[`--index-strategy`](https://docs.astral.sh/uv/reference/cli/#uv-audit--index-strategy) _index-strategy_ 
    
The strategy to use when resolving against multiple index URLs.
By default, uv will stop at the first index on which a given package is available, and limit resolutions to those present on that first index (`first-index`). This prevents "dependency confusion" attacks, whereby an attacker can upload a malicious package under the same name to an alternate index.
May also be set with the `UV_INDEX_STRATEGY` environment variable.
Possible values:
  * `first-index`: Only use results from the first index that returns a match for a given package name
  * `unsafe-first-match`: Search for every package name across all indexes, exhausting the versions from the first index before moving on to the next
  * `unsafe-best-match`: Search for every package name across all indexes, preferring the "best" version found. If a package version is in multiple indexes, only look at the entry for the first index



[`--index-url`](https://docs.astral.sh/uv/reference/cli/#uv-audit--index-url), `-i` _index-url_ 
    
(Deprecated: use `--default-index` instead) The URL of the Python package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--extra-index-url` flag.
May also be set with the `UV_INDEX_URL` environment variable. 

[`--keyring-provider`](https://docs.astral.sh/uv/reference/cli/#uv-audit--keyring-provider) _keyring-provider_ 
    
Attempt to use `keyring` for authentication for index URLs.
At present, only `--keyring-provider subprocess` is supported, which configures uv to use the `keyring` CLI to handle authentication.
Defaults to `disabled`.
May also be set with the `UV_KEYRING_PROVIDER` environment variable.
Possible values:
  * `disabled`: Do not use keyring for credential lookup
  * `subprocess`: Use the `keyring` command for credential lookup



[`--link-mode`](https://docs.astral.sh/uv/reference/cli/#uv-audit--link-mode) _link-mode_ 
    
The method to use when installing packages from the global cache.
This option is only used when building source distributions.
Defaults to `clone` (also known as Copy-on-Write) on macOS and Linux, and `hardlink` on Windows.
WARNING: The use of symlink link mode is discouraged, as they create tight coupling between the cache and the target environment. For example, clearing the cache (`uv cache clean`) will break all installed packages by way of removing the underlying source files. Use symlinks with caution.
May also be set with the `UV_LINK_MODE` environment variable.
Possible values:
  * `clone`: Clone (i.e., copy-on-write) packages from the source into the destination
  * `copy`: Copy packages from the source into the destination
  * `hardlink`: Hard link packages from the source into the destination
  * `symlink`: Symbolically link packages from the source into the destination

    
Assert that the `uv.lock` will remain unchanged [env: UV_LOCKED=]
Requires that the lockfile is up-to-date. If the lockfile is missing or needs to be updated, uv will exit with an error.     
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions.     
Don't install pre-built wheels.
The given packages will be built and installed from source. The resolver will still use pre-built wheels to extract package metadata, if available.
May also be set with the `UV_NO_BINARY` environment variable. 

[`--no-binary-package`](https://docs.astral.sh/uv/reference/cli/#uv-audit--no-binary-package) _no-binary-package_ 
    
Don't install pre-built wheels for a specific package [env: `UV_NO_BINARY_PACKAGE`=]     
Don't build source distributions.
When enabled, uv will reuse cached wheels from previously built source distributions, but operations that require building a source distribution will exit with an error. First-party packages, such as projects in the workspace, will still be built. uv will also still build editable requirements, and their build backends may run arbitrary Python code.
May also be set with the `UV_NO_BUILD` environment variable. 

[`--no-build-isolation`](https://docs.astral.sh/uv/reference/cli/#uv-audit--no-build-isolation)
    
Disable isolation when building source distributions.
Assumes that build dependencies specified by PEP 518 are already installed.
May also be set with the `UV_NO_BUILD_ISOLATION` environment variable. 

[`--no-build-isolation-package`](https://docs.astral.sh/uv/reference/cli/#uv-audit--no-build-isolation-package) _no-build-isolation-package_ 
    
Disable isolation when building source distributions for a specific package.
Assumes that the packages' build dependencies specified by PEP 518 are already installed. 

[`--no-build-package`](https://docs.astral.sh/uv/reference/cli/#uv-audit--no-build-package) _no-build-package_ 
    
Don't build source distributions for a specific package [env: `UV_NO_BUILD_PACKAGE`=]
First-party packages, such as projects in the workspace, will still be built. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-audit--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable. 

[`--no-default-groups`](https://docs.astral.sh/uv/reference/cli/#uv-audit--no-default-groups)
    
Don't audit the default dependency groups
May also be set with the `UV_NO_DEFAULT_GROUPS` environment variable.     
Don't audit the development dependency group [env: UV_NO_DEV=]
This option is an alias of `--no-group dev`. See `--no-default-groups` to exclude all default groups instead.
This option is only available when running in a project. 

[`--no-extra`](https://docs.astral.sh/uv/reference/cli/#uv-audit--no-extra) _no-extra_ 
    
Don't audit the specified optional dependencies.
May be provided multiple times. 

[`--no-group`](https://docs.astral.sh/uv/reference/cli/#uv-audit--no-group) _no-group_ 
    
Don't audit the specified dependency group [env: `UV_NO_GROUP`=]
May be provided multiple times.     
Ignore the registry index (e.g., PyPI), instead relying on direct URL dependencies and those provided via `--find-links` 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-audit--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-audit--no-python-downloads)
    
Disable automatic downloads of Python.     
Ignore the `tool.uv.sources` table when resolving dependencies. Used to lock against the standards-compliant, publishable package metadata, as opposed to using any workspace, Git, URL, or local path sources
May also be set with the `UV_NO_SOURCES` environment variable. 

[`--no-sources-package`](https://docs.astral.sh/uv/reference/cli/#uv-audit--no-sources-package) _no-sources-package_ 
    
Don't use sources from the `tool.uv.sources` table for the specified packages [env: `UV_NO_SOURCES_PACKAGE`=]     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files.     
Only audit the development dependency group.
The project and its dependencies will be omitted.
This option is an alias for `--only-group dev`. Implies `--no-default-groups`. 

[`--only-group`](https://docs.astral.sh/uv/reference/cli/#uv-audit--only-group) _only-group_ 
    
Only audit dependencies from the specified dependency group.
The project and its dependencies will be omitted.
May be provided multiple times. Implies `--no-default-groups`. 

[`--output-format`](https://docs.astral.sh/uv/reference/cli/#uv-audit--output-format) _output-format_ 
    
Select the output format
[default: text]
Possible values:
  * `text`: Display the result in a human-readable format
  * `json`: Display the result in JSON format
  * `sarif`: Display the result in SARIF format



[`--prerelease`](https://docs.astral.sh/uv/reference/cli/#uv-audit--prerelease) _prerelease_ 
    
The strategy to use when considering pre-release versions.
By default, uv will prefer stable candidates, falling back to pre-releases only after every stable candidate that satisfies the active constraints is rejected (`if-necessary`).
May also be set with the `UV_PRERELEASE` environment variable.
Possible values:
  * `disallow`: Disallow all pre-release versions
  * `allow`: Allow all pre-release versions
  * `if-necessary`: Prefer stable versions, falling back to pre-release versions when necessary
  * `explicit`: Prefer stable versions for first-party packages with explicit pre-release specifiers, falling back to pre-release versions when necessary. Disallow pre-release versions for all other packages
  * `if-necessary-or-explicit`: Deprecated alias for `if-necessary`



[`--prerelease-package`](https://docs.astral.sh/uv/reference/cli/#uv-audit--prerelease-package) _prerelease-package_ 
    
The strategy to use when considering pre-release versions for a specific package.
Accepts package-mode pairs in the format `PACKAGE=MODE`, where `MODE` is any value accepted by `--prerelease`.
May be provided multiple times for different packages. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-audit--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable. 

[`--python-platform`](https://docs.astral.sh/uv/reference/cli/#uv-audit--python-platform) _python-platform_ 
    
The platform to use when auditing.
For example, pass `--platform windows` to audit the dependencies that would be included when installing on Windows.
Represented as a "target triple", a string that describes the target platform in terms of its CPU, vendor, and operating system name, like `x86_64-unknown-linux-gnu` or `aarch64-apple-darwin`.
Possible values:
  * `windows`: An alias for `x86_64-pc-windows-msvc`, the default target for Windows
  * `linux`: An alias for `x86_64-unknown-linux-gnu`, the default target for Linux
  * `macos`: An alias for `aarch64-apple-darwin`, the default target for macOS
  * `x86_64-pc-windows-msvc`: A 64-bit x86 Windows target
  * `aarch64-pc-windows-msvc`: An ARM64 Windows target
  * `i686-pc-windows-msvc`: A 32-bit x86 Windows target
  * `x86_64-unknown-linux-gnu`: An x86 Linux target. Equivalent to `x86_64-manylinux_2_28`
  * `aarch64-apple-darwin`: An ARM-based macOS target, as seen on Apple Silicon devices
  * `x86_64-apple-darwin`: An x86 macOS target
  * `aarch64-unknown-linux-gnu`: An ARM64 Linux target. Equivalent to `aarch64-manylinux_2_28`
  * `aarch64-unknown-linux-musl`: An ARM64 Linux target
  * `x86_64-unknown-linux-musl`: An `x86_64` Linux target
  * `riscv64-unknown-linux`: A RISCV64 Linux target
  * `x86_64-manylinux2014`: An `x86_64` target for the `manylinux2014` platform. Equivalent to `x86_64-manylinux_2_17`
  * `x86_64-manylinux_2_17`: An `x86_64` target for the `manylinux_2_17` platform
  * `x86_64-manylinux_2_28`: An `x86_64` target for the `manylinux_2_28` platform
  * `x86_64-manylinux_2_31`: An `x86_64` target for the `manylinux_2_31` platform
  * `x86_64-manylinux_2_32`: An `x86_64` target for the `manylinux_2_32` platform
  * `x86_64-manylinux_2_33`: An `x86_64` target for the `manylinux_2_33` platform
  * `x86_64-manylinux_2_34`: An `x86_64` target for the `manylinux_2_34` platform
  * `x86_64-manylinux_2_35`: An `x86_64` target for the `manylinux_2_35` platform
  * `x86_64-manylinux_2_36`: An `x86_64` target for the `manylinux_2_36` platform
  * `x86_64-manylinux_2_37`: An `x86_64` target for the `manylinux_2_37` platform
  * `x86_64-manylinux_2_38`: An `x86_64` target for the `manylinux_2_38` platform
  * `x86_64-manylinux_2_39`: An `x86_64` target for the `manylinux_2_39` platform
  * `x86_64-manylinux_2_40`: An `x86_64` target for the `manylinux_2_40` platform
  * `aarch64-manylinux2014`: An ARM64 target for the `manylinux2014` platform. Equivalent to `aarch64-manylinux_2_17`
  * `aarch64-manylinux_2_17`: An ARM64 target for the `manylinux_2_17` platform
  * `aarch64-manylinux_2_28`: An ARM64 target for the `manylinux_2_28` platform
  * `aarch64-manylinux_2_31`: An ARM64 target for the `manylinux_2_31` platform
  * `aarch64-manylinux_2_32`: An ARM64 target for the `manylinux_2_32` platform
  * `aarch64-manylinux_2_33`: An ARM64 target for the `manylinux_2_33` platform
  * `aarch64-manylinux_2_34`: An ARM64 target for the `manylinux_2_34` platform
  * `aarch64-manylinux_2_35`: An ARM64 target for the `manylinux_2_35` platform
  * `aarch64-manylinux_2_36`: An ARM64 target for the `manylinux_2_36` platform
  * `aarch64-manylinux_2_37`: An ARM64 target for the `manylinux_2_37` platform
  * `aarch64-manylinux_2_38`: An ARM64 target for the `manylinux_2_38` platform
  * `aarch64-manylinux_2_39`: An ARM64 target for the `manylinux_2_39` platform
  * `aarch64-manylinux_2_40`: An ARM64 target for the `manylinux_2_40` platform
  * `aarch64-linux-android`: An ARM64 Android target
  * `x86_64-linux-android`: An `x86_64` Android target
  * `wasm32-pyodide2024`: A wasm32 target using the Pyodide 2024 platform. Meant for use with Python 3.12. See <https://pyodide.org/en/stable/development/abi/312.html>
  * `wasm32-pyodide2025`: A wasm32 target using the Pyodide 2025 platform. Meant for use with Python 3.13. See <https://pyodide.org/en/stable/development/abi/313.html>
  * `arm64-apple-ios`: An ARM64 target for iOS device
  * `arm64-apple-ios-simulator`: An ARM64 target for iOS simulator
  * `x86_64-apple-ios-simulator`: An `x86_64` target for iOS simulator



[`--python-version`](https://docs.astral.sh/uv/reference/cli/#uv-audit--python-version) _python-version_ 
    
The Python version to use when auditing.
For example, pass `--python-version 3.10` to audit the dependencies that would be included when installing on Python 3.10.
Defaults to the version of the discovered Python interpreter.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout. 

[`--resolution`](https://docs.astral.sh/uv/reference/cli/#uv-audit--resolution) _resolution_ 
    
The strategy to use when selecting between the different compatible versions for a given package requirement.
By default, uv will use the latest compatible version of each package (`highest`).
May also be set with the `UV_RESOLUTION` environment variable.
Possible values:
  * `highest`: Resolve the highest compatible version of each package
  * `lowest`: Resolve the lowest compatible version of each package
  * `lowest-direct`: Resolve the lowest compatible version of any direct dependencies, and the highest compatible version of any transitive dependencies



[`--script`](https://docs.astral.sh/uv/reference/cli/#uv-audit--script) _script_ 
    
Audit the specified PEP 723 Python script, rather than the current project.
The specified script must be locked, i.e. with `uv lock --script <script>` before it can be audited. 

[`--service-format`](https://docs.astral.sh/uv/reference/cli/#uv-audit--service-format) _service-format_ 
    
The service format to use for vulnerability lookups.
Each service format has a default URL, which can be changed with `--service-url`. The defaults are:
  * OSV: <https://api.osv.dev/>


[default: osv]
Possible values:
  * `osv`



[`--service-url`](https://docs.astral.sh/uv/reference/cli/#uv-audit--service-url) _service-url_ 
    
The URL to vulnerability service API endpoint.
If not provided, the default URL for the selected service will be used.
The service needs to use the OSV protocol, unless a different format was requested by `--service-format`.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store.     
Allow package upgrades, ignoring pinned versions in any existing output file. Implies `--refresh` 

[`--upgrade-group`](https://docs.astral.sh/uv/reference/cli/#uv-audit--upgrade-group) _upgrade-group_ 
    
Allow upgrades for all packages in a dependency group, ignoring pinned versions in any existing output file 

[`--upgrade-package`](https://docs.astral.sh/uv/reference/cli/#uv-audit--upgrade-package), `-P` _upgrade-package_ 
    
Allow upgrades for a specific package, ignoring pinned versions in any existing output file. Implies `--refresh-package`     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
## [uv tool](https://docs.astral.sh/uv/reference/cli/#uv-tool)
Run and install commands provided by Python packages
### Usage

```
uv tool [OPTIONS] <COMMAND>

```

### Commands     
Run a command provided by a Python package     
Install commands provided by a Python package     
Upgrade installed tools     
List installed tools     
Audit installed tools and their dependencies 

[`uv tool uninstall`](https://docs.astral.sh/uv/reference/cli/#uv-tool-uninstall)
    
Uninstall a tool 

[`uv tool update-shell`](https://docs.astral.sh/uv/reference/cli/#uv-tool-update-shell)
    
Ensure that the tool executable directory is on the `PATH`     
Show the path to the uv tools directory
### [uv tool run](https://docs.astral.sh/uv/reference/cli/#uv-tool-run)
Run a command provided by a Python package.
By default, the package to install is assumed to match the command name.
The name of the command can include an exact version in the format `<package>@<version>`, e.g., `uv tool run [email protected][](https://docs.astral.sh/cdn-cgi/l/email-protection)`. If more complex version specification is desired or if the command is provided by a different package, use `--from`.
`uvx` can be used to invoke Python, e.g., with `uvx python` or `uvx python@<version>`. A Python interpreter will be started in an isolated virtual environment.
If the tool was previously installed, i.e., via `uv tool install`, the installed version will be used unless a version is requested or the `--isolated` flag is used.
`uvx` is provided as a convenient alias for `uv tool run`, their behavior is identical.
If no command is provided, the installed tools are displayed.
Packages are installed into an ephemeral virtual environment in the uv cache directory.
### Usage

```
uv tool run [OPTIONS] [COMMAND]

```

### Options 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--build-constraints`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--build-constraints), `--build-constraint`, `-b` _build-constraints_ 
    
Constrain build dependencies using the given requirements files when building source distributions.
Constraints files are `requirements.txt`-like files that only control the _version_ of a requirement that's installed. However, including a package in a constraints file will _not_ trigger the installation of that package.
May also be set with the `UV_BUILD_CONSTRAINT` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--compile-bytecode`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--compile-bytecode), `--compile` 
    
Compile Python files to bytecode after installation.
By default, uv does not compile Python (`.py`) files to bytecode (`__pycache__/*.pyc`); instead, compilation is performed lazily the first time a module is imported. For use-cases in which start time is critical, such as CLI applications and Docker containers, this option can be enabled to trade longer installation times for faster start times.
When enabled, install operations (e.g., `uv pip install`) will compile installed or reinstalled Python files. Commands that perform a sync operation (e.g., `uv sync` or `uv run`) will process the entire site-packages directory including packages that are not being modified.
May also be set with the `UV_COMPILE_BYTECODE` environment variable. 

[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--config-setting`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--config-setting), `--config-settings`, `-C` _config-setting_ 
    
Settings to pass to the PEP 517 build backend, specified as `KEY=VALUE` pairs 

[`--config-settings-package`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--config-settings-package), `--config-settings-package` _config-settings-package_ 
    
Settings to pass to the PEP 517 build backend for a specific package, specified as `PACKAGE:KEY=VALUE` pairs 

[`--constraints`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--constraints), `--constraint`, `-c` _constraints_ 
    
Constrain versions using the given requirements files.
Constraints files are `requirements.txt`-like files that only control the _version_ of a requirement that's installed. However, including a package in a constraints file will _not_ trigger the installation of that package.
This is equivalent to pip's `--constraint` option.
May also be set with the `UV_CONSTRAINT` environment variable. 

[`--default-index`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--default-index) _default-index_ 
    
The default package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--index` flag.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
May also be set with the `UV_DEFAULT_INDEX` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable. 

[`--env-file`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--env-file) _env-file_ 
    
Load environment variables from a `.env` file.
Can be provided multiple times, with subsequent files overriding values defined in previous files.
May also be set with the `UV_ENV_FILE` environment variable. 

[`--exclude-newer`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--exclude-newer) _exclude-newer_ 
    
Limit candidate packages to those that were uploaded prior to the given date.
The date is compared against the upload time of each individual distribution artifact (i.e., when each file was uploaded to the package index), not the release date of the package version.
Accepts RFC 3339 timestamps (e.g., `2006-12-02T02:07:43Z`), local dates in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Use `false` to disable `exclude-newer`.
May also be set with the `UV_EXCLUDE_NEWER` environment variable. 

[`--exclude-newer-package`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--exclude-newer-package) _exclude-newer-package_ 
    
Limit candidate packages for specific packages to those that were uploaded prior to the given date.
Accepts package-date pairs in the format `PACKAGE=DATE`, where `DATE` is an RFC 3339 timestamp (e.g., `2006-12-02T02:07:43Z`), a local date in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Can be provided multiple times for different packages. 

[`--extra-index-url`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--extra-index-url) _extra-index-url_ 
    
(Deprecated: use `--index` instead) Extra URLs of package indexes to use, in addition to `--index-url`.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--index-url` (which defaults to PyPI). When multiple `--extra-index-url` flags are provided, earlier values take priority.
May also be set with the `UV_EXTRA_INDEX_URL` environment variable. 

[`--find-links`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--find-links), `-f` _find-links_ 
    
Locations to search for candidate distributions, in addition to those found in the registry indexes.
If a path, the target must be a directory that contains packages as wheel files (`.whl`) or source distributions (e.g., `.tar.gz` or `.zip`) at the top level.
If a URL, the page must contain a flat list of links to package files adhering to the formats described above.
May also be set with the `UV_FIND_LINKS` environment variable. 

[`--fork-strategy`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--fork-strategy) _fork-strategy_ 
    
The strategy to use when selecting multiple versions of a given package across Python versions and platforms.
By default, uv will optimize for selecting the latest version of each package for each supported Python version (`requires-python`), while minimizing the number of selected versions across platforms.
Under `fewest`, uv will minimize the number of selected versions for each package, preferring older versions that are compatible with a wider range of supported Python versions or platforms.
May also be set with the `UV_FORK_STRATEGY` environment variable.
Possible values:
  * `fewest`: Optimize for selecting the fewest number of versions for each package. Older versions may be preferred if they are compatible with a wider range of supported Python versions or platforms
  * `requires-python`: Optimize for selecting latest supported version of each package, for each supported Python version



[`--from`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--from) _from_ 
    
Use the given package to provide the command.
By default, the package name is assumed to match the command name.     
Display the concise help for this command 

[`--index`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--index) _index_ 
    
The indexes to use when resolving dependencies, in addition to the default index.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--default-index` (which defaults to PyPI). When multiple `--index` flags are provided, earlier values take priority.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
Relative paths can be disambiguated from index names with `./` or `../` on Unix or `.\\`, `..\\`, `./` or `../` on Windows.
May also be set with the `UV_INDEX` environment variable. 

[`--index-strategy`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--index-strategy) _index-strategy_ 
    
The strategy to use when resolving against multiple index URLs.
By default, uv will stop at the first index on which a given package is available, and limit resolutions to those present on that first index (`first-index`). This prevents "dependency confusion" attacks, whereby an attacker can upload a malicious package under the same name to an alternate index.
May also be set with the `UV_INDEX_STRATEGY` environment variable.
Possible values:
  * `first-index`: Only use results from the first index that returns a match for a given package name
  * `unsafe-first-match`: Search for every package name across all indexes, exhausting the versions from the first index before moving on to the next
  * `unsafe-best-match`: Search for every package name across all indexes, preferring the "best" version found. If a package version is in multiple indexes, only look at the entry for the first index



[`--index-url`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--index-url), `-i` _index-url_ 
    
(Deprecated: use `--default-index` instead) The URL of the Python package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--extra-index-url` flag.
May also be set with the `UV_INDEX_URL` environment variable.     
Run the tool in an isolated virtual environment, ignoring any already-installed tools [env: UV_ISOLATED=] 

[`--keyring-provider`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--keyring-provider) _keyring-provider_ 
    
Attempt to use `keyring` for authentication for index URLs.
At present, only `--keyring-provider subprocess` is supported, which configures uv to use the `keyring` CLI to handle authentication.
Defaults to `disabled`.
May also be set with the `UV_KEYRING_PROVIDER` environment variable.
Possible values:
  * `disabled`: Do not use keyring for credential lookup
  * `subprocess`: Use the `keyring` command for credential lookup

    
Whether to use Git LFS when adding a dependency from Git 

[`--link-mode`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--link-mode) _link-mode_ 
    
The method to use when installing packages from the global cache.
Defaults to `clone` (also known as Copy-on-Write) on macOS and Linux, and `hardlink` on Windows.
WARNING: The use of symlink link mode is discouraged, as they create tight coupling between the cache and the target environment. For example, clearing the cache (`uv cache clean`) will break all installed packages by way of removing the underlying source files. Use symlinks with caution.
May also be set with the `UV_LINK_MODE` environment variable.
Possible values:
  * `clone`: Clone (i.e., copy-on-write) packages from the source into the destination
  * `copy`: Copy packages from the source into the destination
  * `hardlink`: Hard link packages from the source into the destination
  * `symlink`: Symbolically link packages from the source into the destination

    
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions.     
Don't install pre-built wheels.
The given packages will be built and installed from source. The resolver will still use pre-built wheels to extract package metadata, if available.
May also be set with the `UV_NO_BINARY` environment variable. 

[`--no-binary-package`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--no-binary-package) _no-binary-package_ 
    
Don't install pre-built wheels for a specific package [env: `UV_NO_BINARY_PACKAGE`=]     
Don't build source distributions.
When enabled, uv will reuse cached wheels from previously built source distributions, but operations that require building a source distribution will exit with an error. First-party packages, such as projects in the workspace, will still be built. uv will also still build editable requirements, and their build backends may run arbitrary Python code.
May also be set with the `UV_NO_BUILD` environment variable. 

[`--no-build-isolation`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--no-build-isolation)
    
Disable isolation when building source distributions.
Assumes that build dependencies specified by PEP 518 are already installed.
May also be set with the `UV_NO_BUILD_ISOLATION` environment variable. 

[`--no-build-isolation-package`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--no-build-isolation-package) _no-build-isolation-package_ 
    
Disable isolation when building source distributions for a specific package.
Assumes that the packages' build dependencies specified by PEP 518 are already installed. 

[`--no-build-package`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--no-build-package) _no-build-package_ 
    
Don't build source distributions for a specific package [env: `UV_NO_BUILD_PACKAGE`=]
First-party packages, such as projects in the workspace, will still be built. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable.     
Avoid reading environment variables from a `.env` file [env: UV_NO_ENV_FILE=]     
Ignore the registry index (e.g., PyPI), instead relying on direct URL dependencies and those provided via `--find-links` 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--no-python-downloads)
    
Disable automatic downloads of Python.     
Ignore the `tool.uv.sources` table when resolving dependencies. Used to lock against the standards-compliant, publishable package metadata, as opposed to using any workspace, Git, URL, or local path sources
May also be set with the `UV_NO_SOURCES` environment variable. 

[`--no-sources-package`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--no-sources-package) _no-sources-package_ 
    
Don't use sources from the `tool.uv.sources` table for the specified packages [env: `UV_NO_SOURCES_PACKAGE`=]     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--overrides`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--overrides), `--override` _overrides_ 
    
Override versions using the given requirements files.
Overrides files are `requirements.txt`-like files that force a specific version of a requirement to be installed, regardless of the requirements declared by any constituent package, and regardless of whether this would be considered an invalid resolution.
While constraints are _additive_ , in that they're combined with the requirements of the constituent packages, overrides are _absolute_ , in that they completely replace the requirements of the constituent packages.
May also be set with the `UV_OVERRIDE` environment variable. 

[`--prerelease`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--prerelease) _prerelease_ 
    
The strategy to use when considering pre-release versions.
By default, uv will prefer stable candidates, falling back to pre-releases only after every stable candidate that satisfies the active constraints is rejected (`if-necessary`).
May also be set with the `UV_PRERELEASE` environment variable.
Possible values:
  * `disallow`: Disallow all pre-release versions
  * `allow`: Allow all pre-release versions
  * `if-necessary`: Prefer stable versions, falling back to pre-release versions when necessary
  * `explicit`: Prefer stable versions for first-party packages with explicit pre-release specifiers, falling back to pre-release versions when necessary. Disallow pre-release versions for all other packages
  * `if-necessary-or-explicit`: Deprecated alias for `if-necessary`



[`--prerelease-package`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--prerelease-package) _prerelease-package_ 
    
The strategy to use when considering pre-release versions for a specific package.
Accepts package-mode pairs in the format `PACKAGE=MODE`, where `MODE` is any value accepted by `--prerelease`.
May be provided multiple times for different packages. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable. 

[`--python`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--python), `-p` _python_ 
    
The Python interpreter to use to build the run environment.
See [uv python](https://docs.astral.sh/uv/reference/cli/#uv-python) for details on Python discovery and supported request formats.
May also be set with the `UV_PYTHON` environment variable. 

[`--python-platform`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--python-platform) _python-platform_ 
    
The platform for which requirements should be installed.
Represented as a "target triple", a string that describes the target platform in terms of its CPU, vendor, and operating system name, like `x86_64-unknown-linux-gnu` or `aarch64-apple-darwin`.
When targeting macOS (Darwin), the default minimum version is `13.0`. Use `MACOSX_DEPLOYMENT_TARGET` to specify a different minimum version, e.g., `14.0`.
When targeting iOS, the default minimum version is `13.0`. Use `IPHONEOS_DEPLOYMENT_TARGET` to specify a different minimum version, e.g., `14.0`.
When targeting Android, the default minimum Android API level is `24`. Use `ANDROID_API_LEVEL` to specify a different minimum version, e.g., `26`.
WARNING: When specified, uv will select wheels that are compatible with the _target_ platform; as a result, the installed distributions may not be compatible with the _current_ platform. Conversely, any distributions that are built from source may be incompatible with the _target_ platform, as they will be built for the _current_ platform. The `--python-platform` option is intended for advanced use cases.
Possible values:
  * `windows`: An alias for `x86_64-pc-windows-msvc`, the default target for Windows
  * `linux`: An alias for `x86_64-unknown-linux-gnu`, the default target for Linux
  * `macos`: An alias for `aarch64-apple-darwin`, the default target for macOS
  * `x86_64-pc-windows-msvc`: A 64-bit x86 Windows target
  * `aarch64-pc-windows-msvc`: An ARM64 Windows target
  * `i686-pc-windows-msvc`: A 32-bit x86 Windows target
  * `x86_64-unknown-linux-gnu`: An x86 Linux target. Equivalent to `x86_64-manylinux_2_28`
  * `aarch64-apple-darwin`: An ARM-based macOS target, as seen on Apple Silicon devices
  * `x86_64-apple-darwin`: An x86 macOS target
  * `aarch64-unknown-linux-gnu`: An ARM64 Linux target. Equivalent to `aarch64-manylinux_2_28`
  * `aarch64-unknown-linux-musl`: An ARM64 Linux target
  * `x86_64-unknown-linux-musl`: An `x86_64` Linux target
  * `riscv64-unknown-linux`: A RISCV64 Linux target
  * `x86_64-manylinux2014`: An `x86_64` target for the `manylinux2014` platform. Equivalent to `x86_64-manylinux_2_17`
  * `x86_64-manylinux_2_17`: An `x86_64` target for the `manylinux_2_17` platform
  * `x86_64-manylinux_2_28`: An `x86_64` target for the `manylinux_2_28` platform
  * `x86_64-manylinux_2_31`: An `x86_64` target for the `manylinux_2_31` platform
  * `x86_64-manylinux_2_32`: An `x86_64` target for the `manylinux_2_32` platform
  * `x86_64-manylinux_2_33`: An `x86_64` target for the `manylinux_2_33` platform
  * `x86_64-manylinux_2_34`: An `x86_64` target for the `manylinux_2_34` platform
  * `x86_64-manylinux_2_35`: An `x86_64` target for the `manylinux_2_35` platform
  * `x86_64-manylinux_2_36`: An `x86_64` target for the `manylinux_2_36` platform
  * `x86_64-manylinux_2_37`: An `x86_64` target for the `manylinux_2_37` platform
  * `x86_64-manylinux_2_38`: An `x86_64` target for the `manylinux_2_38` platform
  * `x86_64-manylinux_2_39`: An `x86_64` target for the `manylinux_2_39` platform
  * `x86_64-manylinux_2_40`: An `x86_64` target for the `manylinux_2_40` platform
  * `aarch64-manylinux2014`: An ARM64 target for the `manylinux2014` platform. Equivalent to `aarch64-manylinux_2_17`
  * `aarch64-manylinux_2_17`: An ARM64 target for the `manylinux_2_17` platform
  * `aarch64-manylinux_2_28`: An ARM64 target for the `manylinux_2_28` platform
  * `aarch64-manylinux_2_31`: An ARM64 target for the `manylinux_2_31` platform
  * `aarch64-manylinux_2_32`: An ARM64 target for the `manylinux_2_32` platform
  * `aarch64-manylinux_2_33`: An ARM64 target for the `manylinux_2_33` platform
  * `aarch64-manylinux_2_34`: An ARM64 target for the `manylinux_2_34` platform
  * `aarch64-manylinux_2_35`: An ARM64 target for the `manylinux_2_35` platform
  * `aarch64-manylinux_2_36`: An ARM64 target for the `manylinux_2_36` platform
  * `aarch64-manylinux_2_37`: An ARM64 target for the `manylinux_2_37` platform
  * `aarch64-manylinux_2_38`: An ARM64 target for the `manylinux_2_38` platform
  * `aarch64-manylinux_2_39`: An ARM64 target for the `manylinux_2_39` platform
  * `aarch64-manylinux_2_40`: An ARM64 target for the `manylinux_2_40` platform
  * `aarch64-linux-android`: An ARM64 Android target
  * `x86_64-linux-android`: An `x86_64` Android target
  * `wasm32-pyodide2024`: A wasm32 target using the Pyodide 2024 platform. Meant for use with Python 3.12. See <https://pyodide.org/en/stable/development/abi/312.html>
  * `wasm32-pyodide2025`: A wasm32 target using the Pyodide 2025 platform. Meant for use with Python 3.13. See <https://pyodide.org/en/stable/development/abi/313.html>
  * `arm64-apple-ios`: An ARM64 target for iOS device
  * `arm64-apple-ios-simulator`: An ARM64 target for iOS simulator
  * `x86_64-apple-ios-simulator`: An `x86_64` target for iOS simulator

    
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Refresh all cached data 

[`--refresh-package`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--refresh-package) _refresh-package_ 
    
Refresh cached data for a specific package 

[`--reinstall`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--reinstall), `--force-reinstall` 
    
Reinstall all packages, regardless of whether they're already installed. Implies `--refresh` 

[`--reinstall-package`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--reinstall-package) _reinstall-package_ 
    
Reinstall a specific package, regardless of whether it's already installed. Implies `--refresh-package` 

[`--resolution`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--resolution) _resolution_ 
    
The strategy to use when selecting between the different compatible versions for a given package requirement.
By default, uv will use the latest compatible version of each package (`highest`).
May also be set with the `UV_RESOLUTION` environment variable.
Possible values:
  * `highest`: Resolve the highest compatible version of each package
  * `lowest`: Resolve the lowest compatible version of each package
  * `lowest-direct`: Resolve the lowest compatible version of any direct dependencies, and the highest compatible version of any transitive dependencies

    
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store. 

[`--torch-backend`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--torch-backend) _torch-backend_ 
    
The backend to use when fetching packages in the PyTorch ecosystem (e.g., `cpu`, `cu126`, or `auto`)
When set, uv will ignore the configured index URLs for packages in the PyTorch ecosystem, and will instead use the defined backend.
For example, when set to `cpu`, uv will use the CPU-only PyTorch index; when set to `cu126`, uv will use the PyTorch index for CUDA 12.6.
The `auto` mode will attempt to detect the appropriate PyTorch index based on the currently installed CUDA drivers.
This option is in preview and may change in any future release.
May also be set with the `UV_TORCH_BACKEND` environment variable.
Possible values:
  * `auto`: Select the appropriate PyTorch index based on the operating system and CUDA driver version
  * `cpu`: Use the CPU-only PyTorch index
  * `cu132`: Use the PyTorch index for CUDA 13.2
  * `cu130`: Use the PyTorch index for CUDA 13.0
  * `cu129`: Use the PyTorch index for CUDA 12.9
  * `cu128`: Use the PyTorch index for CUDA 12.8
  * `cu126`: Use the PyTorch index for CUDA 12.6
  * `cu125`: Use the PyTorch index for CUDA 12.5
  * `cu124`: Use the PyTorch index for CUDA 12.4
  * `cu123`: Use the PyTorch index for CUDA 12.3
  * `cu122`: Use the PyTorch index for CUDA 12.2
  * `cu121`: Use the PyTorch index for CUDA 12.1
  * `cu120`: Use the PyTorch index for CUDA 12.0
  * `cu118`: Use the PyTorch index for CUDA 11.8
  * `cu117`: Use the PyTorch index for CUDA 11.7
  * `cu116`: Use the PyTorch index for CUDA 11.6
  * `cu115`: Use the PyTorch index for CUDA 11.5
  * `cu114`: Use the PyTorch index for CUDA 11.4
  * `cu113`: Use the PyTorch index for CUDA 11.3
  * `cu112`: Use the PyTorch index for CUDA 11.2
  * `cu111`: Use the PyTorch index for CUDA 11.1
  * `cu110`: Use the PyTorch index for CUDA 11.0
  * `cu102`: Use the PyTorch index for CUDA 10.2
  * `cu101`: Use the PyTorch index for CUDA 10.1
  * `cu100`: Use the PyTorch index for CUDA 10.0
  * `cu92`: Use the PyTorch index for CUDA 9.2
  * `cu91`: Use the PyTorch index for CUDA 9.1
  * `cu90`: Use the PyTorch index for CUDA 9.0
  * `cu80`: Use the PyTorch index for CUDA 8.0
  * `rocm7.2`: Use the PyTorch index for ROCm 7.2
  * `rocm7.1`: Use the PyTorch index for ROCm 7.1
  * `rocm7.0`: Use the PyTorch index for ROCm 7.0
  * `rocm6.4`: Use the PyTorch index for ROCm 6.4
  * `rocm6.3`: Use the PyTorch index for ROCm 6.3
  * `rocm6.2.4`: Use the PyTorch index for ROCm 6.2.4
  * `rocm6.2`: Use the PyTorch index for ROCm 6.2
  * `rocm6.1`: Use the PyTorch index for ROCm 6.1
  * `rocm6.0`: Use the PyTorch index for ROCm 6.0
  * `rocm5.7`: Use the PyTorch index for ROCm 5.7
  * `rocm5.6`: Use the PyTorch index for ROCm 5.6
  * `rocm5.5`: Use the PyTorch index for ROCm 5.5
  * `rocm5.4.2`: Use the PyTorch index for ROCm 5.4.2
  * `rocm5.4`: Use the PyTorch index for ROCm 5.4
  * `rocm5.3`: Use the PyTorch index for ROCm 5.3
  * `rocm5.2`: Use the PyTorch index for ROCm 5.2
  * `rocm5.1.1`: Use the PyTorch index for ROCm 5.1.1
  * `rocm4.2`: Use the PyTorch index for ROCm 4.2
  * `rocm4.1`: Use the PyTorch index for ROCm 4.1
  * `rocm4.0.1`: Use the PyTorch index for ROCm 4.0.1
  * `xpu`: Use the PyTorch index for Intel XPU

    
Allow package upgrades, ignoring pinned versions in any existing output file. Implies `--refresh` 

[`--upgrade-group`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--upgrade-group) _upgrade-group_ 
    
Allow upgrades for all packages in a dependency group, ignoring pinned versions in any existing output file 

[`--upgrade-package`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--upgrade-package), `-P` _upgrade-package_ 
    
Allow upgrades for a specific package, ignoring pinned versions in any existing output file. Implies `--refresh-package`     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>) 

[`--with`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--with), `-w` _with_ 
    
Run with the given packages installed 

[`--with-editable`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--with-editable) _with-editable_ 
    
Run with the given packages installed in editable mode
When used in a project, these dependencies will be layered on top of the uv tool's environment in a separate, ephemeral environment. These dependencies are allowed to conflict with those specified. 

[`--with-requirements`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run--with-requirements) _with-requirements_ 
    
Run with the packages listed in the given files.
The following formats are supported: `requirements.txt`, `.py` files with inline metadata, and `pylock.toml`.
### [uv tool install](https://docs.astral.sh/uv/reference/cli/#uv-tool-install)
Install commands provided by a Python package.
Packages are installed into an isolated virtual environment in the uv tools directory. The executables are linked the tool executable directory, which is determined according to the XDG standard and can be retrieved with `uv tool dir --bin`.
If the tool was previously installed, the existing tool will generally be replaced.
### Usage

```
uv tool install [OPTIONS] <PACKAGE>

```

### Arguments     
The package to install commands from
### Options 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--build-constraints`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--build-constraints), `--build-constraint`, `-b` _build-constraints_ 
    
Constrain build dependencies using the given requirements files when building source distributions.
Constraints files are `requirements.txt`-like files that only control the _version_ of a requirement that's installed. However, including a package in a constraints file will _not_ trigger the installation of that package.
May also be set with the `UV_BUILD_CONSTRAINT` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--compile-bytecode`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--compile-bytecode), `--compile` 
    
Compile Python files to bytecode after installation.
By default, uv does not compile Python (`.py`) files to bytecode (`__pycache__/*.pyc`); instead, compilation is performed lazily the first time a module is imported. For use-cases in which start time is critical, such as CLI applications and Docker containers, this option can be enabled to trade longer installation times for faster start times.
When enabled, install operations (e.g., `uv pip install`) will compile installed or reinstalled Python files. Commands that perform a sync operation (e.g., `uv sync` or `uv run`) will process the entire site-packages directory including packages that are not being modified.
May also be set with the `UV_COMPILE_BYTECODE` environment variable. 

[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--config-setting`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--config-setting), `--config-settings`, `-C` _config-setting_ 
    
Settings to pass to the PEP 517 build backend, specified as `KEY=VALUE` pairs 

[`--config-settings-package`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--config-settings-package), `--config-settings-package` _config-settings-package_ 
    
Settings to pass to the PEP 517 build backend for a specific package, specified as `PACKAGE:KEY=VALUE` pairs 

[`--constraints`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--constraints), `--constraint`, `-c` _constraints_ 
    
Constrain versions using the given requirements files.
Constraints files are `requirements.txt`-like files that only control the _version_ of a requirement that's installed. However, including a package in a constraints file will _not_ trigger the installation of that package.
This is equivalent to pip's `--constraint` option.
May also be set with the `UV_CONSTRAINT` environment variable. 

[`--default-index`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--default-index) _default-index_ 
    
The default package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--index` flag.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
May also be set with the `UV_DEFAULT_INDEX` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable.     
Install the target package in editable mode, such that changes in the package's source directory are reflected without reinstallation 

[`--exclude-newer`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--exclude-newer) _exclude-newer_ 
    
Limit candidate packages to those that were uploaded prior to the given date.
The date is compared against the upload time of each individual distribution artifact (i.e., when each file was uploaded to the package index), not the release date of the package version.
Accepts RFC 3339 timestamps (e.g., `2006-12-02T02:07:43Z`), local dates in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Use `false` to disable `exclude-newer`.
May also be set with the `UV_EXCLUDE_NEWER` environment variable. 

[`--exclude-newer-package`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--exclude-newer-package) _exclude-newer-package_ 
    
Limit candidate packages for specific packages to those that were uploaded prior to the given date.
Accepts package-date pairs in the format `PACKAGE=DATE`, where `DATE` is an RFC 3339 timestamp (e.g., `2006-12-02T02:07:43Z`), a local date in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Can be provided multiple times for different packages. 

[`--excludes`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--excludes), `--exclude` _excludes_ 
    
Exclude packages from resolution using the given requirements files.
Excludes files are `requirements.txt`-like files that specify packages to exclude from the resolution. When a package is excluded, it will be omitted from the dependency list entirely and its own dependencies will be ignored during the resolution phase. Excludes are unconditional in that requirement specifiers and markers are ignored; any package listed in the provided file will be omitted from all resolved environments.
May also be set with the `UV_EXCLUDE` environment variable. 

[`--extra-index-url`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--extra-index-url) _extra-index-url_ 
    
(Deprecated: use `--index` instead) Extra URLs of package indexes to use, in addition to `--index-url`.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--index-url` (which defaults to PyPI). When multiple `--extra-index-url` flags are provided, earlier values take priority.
May also be set with the `UV_EXTRA_INDEX_URL` environment variable. 

[`--find-links`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--find-links), `-f` _find-links_ 
    
Locations to search for candidate distributions, in addition to those found in the registry indexes.
If a path, the target must be a directory that contains packages as wheel files (`.whl`) or source distributions (e.g., `.tar.gz` or `.zip`) at the top level.
If a URL, the page must contain a flat list of links to package files adhering to the formats described above.
May also be set with the `UV_FIND_LINKS` environment variable.     
Force installation of the tool.
Will recreate any existing environment for the tool and replace any existing entry points with the same name in the executable directory. 

[`--fork-strategy`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--fork-strategy) _fork-strategy_ 
    
The strategy to use when selecting multiple versions of a given package across Python versions and platforms.
By default, uv will optimize for selecting the latest version of each package for each supported Python version (`requires-python`), while minimizing the number of selected versions across platforms.
Under `fewest`, uv will minimize the number of selected versions for each package, preferring older versions that are compatible with a wider range of supported Python versions or platforms.
May also be set with the `UV_FORK_STRATEGY` environment variable.
Possible values:
  * `fewest`: Optimize for selecting the fewest number of versions for each package. Older versions may be preferred if they are compatible with a wider range of supported Python versions or platforms
  * `requires-python`: Optimize for selecting latest supported version of each package, for each supported Python version

    
Display the concise help for this command 

[`--index`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--index) _index_ 
    
The indexes to use when resolving dependencies, in addition to the default index.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--default-index` (which defaults to PyPI). When multiple `--index` flags are provided, earlier values take priority.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
Relative paths can be disambiguated from index names with `./` or `../` on Unix or `.\\`, `..\\`, `./` or `../` on Windows.
May also be set with the `UV_INDEX` environment variable. 

[`--index-strategy`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--index-strategy) _index-strategy_ 
    
The strategy to use when resolving against multiple index URLs.
By default, uv will stop at the first index on which a given package is available, and limit resolutions to those present on that first index (`first-index`). This prevents "dependency confusion" attacks, whereby an attacker can upload a malicious package under the same name to an alternate index.
May also be set with the `UV_INDEX_STRATEGY` environment variable.
Possible values:
  * `first-index`: Only use results from the first index that returns a match for a given package name
  * `unsafe-first-match`: Search for every package name across all indexes, exhausting the versions from the first index before moving on to the next
  * `unsafe-best-match`: Search for every package name across all indexes, preferring the "best" version found. If a package version is in multiple indexes, only look at the entry for the first index



[`--index-url`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--index-url), `-i` _index-url_ 
    
(Deprecated: use `--default-index` instead) The URL of the Python package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--extra-index-url` flag.
May also be set with the `UV_INDEX_URL` environment variable. 

[`--keyring-provider`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--keyring-provider) _keyring-provider_ 
    
Attempt to use `keyring` for authentication for index URLs.
At present, only `--keyring-provider subprocess` is supported, which configures uv to use the `keyring` CLI to handle authentication.
Defaults to `disabled`.
May also be set with the `UV_KEYRING_PROVIDER` environment variable.
Possible values:
  * `disabled`: Do not use keyring for credential lookup
  * `subprocess`: Use the `keyring` command for credential lookup

    
Whether to use Git LFS when adding a dependency from Git 

[`--link-mode`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--link-mode) _link-mode_ 
    
The method to use when installing packages from the global cache.
Defaults to `clone` (also known as Copy-on-Write) on macOS and Linux, and `hardlink` on Windows.
WARNING: The use of symlink link mode is discouraged, as they create tight coupling between the cache and the target environment. For example, clearing the cache (`uv cache clean`) will break all installed packages by way of removing the underlying source files. Use symlinks with caution.
May also be set with the `UV_LINK_MODE` environment variable.
Possible values:
  * `clone`: Clone (i.e., copy-on-write) packages from the source into the destination
  * `copy`: Copy packages from the source into the destination
  * `hardlink`: Hard link packages from the source into the destination
  * `symlink`: Symbolically link packages from the source into the destination

    
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions.     
Don't install pre-built wheels.
The given packages will be built and installed from source. The resolver will still use pre-built wheels to extract package metadata, if available.
May also be set with the `UV_NO_BINARY` environment variable. 

[`--no-binary-package`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--no-binary-package) _no-binary-package_ 
    
Don't install pre-built wheels for a specific package [env: `UV_NO_BINARY_PACKAGE`=]     
Don't build source distributions.
When enabled, uv will reuse cached wheels from previously built source distributions, but operations that require building a source distribution will exit with an error. First-party packages, such as projects in the workspace, will still be built. uv will also still build editable requirements, and their build backends may run arbitrary Python code.
May also be set with the `UV_NO_BUILD` environment variable. 

[`--no-build-isolation`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--no-build-isolation)
    
Disable isolation when building source distributions.
Assumes that build dependencies specified by PEP 518 are already installed.
May also be set with the `UV_NO_BUILD_ISOLATION` environment variable. 

[`--no-build-isolation-package`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--no-build-isolation-package) _no-build-isolation-package_ 
    
Disable isolation when building source distributions for a specific package.
Assumes that the packages' build dependencies specified by PEP 518 are already installed. 

[`--no-build-package`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--no-build-package) _no-build-package_ 
    
Don't build source distributions for a specific package [env: `UV_NO_BUILD_PACKAGE`=]
First-party packages, such as projects in the workspace, will still be built. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable.     
Ignore the registry index (e.g., PyPI), instead relying on direct URL dependencies and those provided via `--find-links` 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--no-python-downloads)
    
Disable automatic downloads of Python.     
Ignore the `tool.uv.sources` table when resolving dependencies. Used to lock against the standards-compliant, publishable package metadata, as opposed to using any workspace, Git, URL, or local path sources
May also be set with the `UV_NO_SOURCES` environment variable. 

[`--no-sources-package`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--no-sources-package) _no-sources-package_ 
    
Don't use sources from the `tool.uv.sources` table for the specified packages [env: `UV_NO_SOURCES_PACKAGE`=]     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--overrides`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--overrides), `--override` _overrides_ 
    
Override versions using the given requirements files.
Overrides files are `requirements.txt`-like files that force a specific version of a requirement to be installed, regardless of the requirements declared by any constituent package, and regardless of whether this would be considered an invalid resolution.
While constraints are _additive_ , in that they're combined with the requirements of the constituent packages, overrides are _absolute_ , in that they completely replace the requirements of the constituent packages.
May also be set with the `UV_OVERRIDE` environment variable. 

[`--prerelease`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--prerelease) _prerelease_ 
    
The strategy to use when considering pre-release versions.
By default, uv will prefer stable candidates, falling back to pre-releases only after every stable candidate that satisfies the active constraints is rejected (`if-necessary`).
May also be set with the `UV_PRERELEASE` environment variable.
Possible values:
  * `disallow`: Disallow all pre-release versions
  * `allow`: Allow all pre-release versions
  * `if-necessary`: Prefer stable versions, falling back to pre-release versions when necessary
  * `explicit`: Prefer stable versions for first-party packages with explicit pre-release specifiers, falling back to pre-release versions when necessary. Disallow pre-release versions for all other packages
  * `if-necessary-or-explicit`: Deprecated alias for `if-necessary`



[`--prerelease-package`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--prerelease-package) _prerelease-package_ 
    
The strategy to use when considering pre-release versions for a specific package.
Accepts package-mode pairs in the format `PACKAGE=MODE`, where `MODE` is any value accepted by `--prerelease`.
May be provided multiple times for different packages. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable. 

[`--python`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--python), `-p` _python_ 
    
The Python interpreter to use to build the tool environment.
See [uv python](https://docs.astral.sh/uv/reference/cli/#uv-python) for details on Python discovery and supported request formats.
May also be set with the `UV_PYTHON` environment variable. 

[`--python-platform`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--python-platform) _python-platform_ 
    
The platform for which requirements should be installed.
Represented as a "target triple", a string that describes the target platform in terms of its CPU, vendor, and operating system name, like `x86_64-unknown-linux-gnu` or `aarch64-apple-darwin`.
When targeting macOS (Darwin), the default minimum version is `13.0`. Use `MACOSX_DEPLOYMENT_TARGET` to specify a different minimum version, e.g., `14.0`.
When targeting iOS, the default minimum version is `13.0`. Use `IPHONEOS_DEPLOYMENT_TARGET` to specify a different minimum version, e.g., `14.0`.
When targeting Android, the default minimum Android API level is `24`. Use `ANDROID_API_LEVEL` to specify a different minimum version, e.g., `26`.
WARNING: When specified, uv will select wheels that are compatible with the _target_ platform; as a result, the installed distributions may not be compatible with the _current_ platform. Conversely, any distributions that are built from source may be incompatible with the _target_ platform, as they will be built for the _current_ platform. The `--python-platform` option is intended for advanced use cases.
Possible values:
  * `windows`: An alias for `x86_64-pc-windows-msvc`, the default target for Windows
  * `linux`: An alias for `x86_64-unknown-linux-gnu`, the default target for Linux
  * `macos`: An alias for `aarch64-apple-darwin`, the default target for macOS
  * `x86_64-pc-windows-msvc`: A 64-bit x86 Windows target
  * `aarch64-pc-windows-msvc`: An ARM64 Windows target
  * `i686-pc-windows-msvc`: A 32-bit x86 Windows target
  * `x86_64-unknown-linux-gnu`: An x86 Linux target. Equivalent to `x86_64-manylinux_2_28`
  * `aarch64-apple-darwin`: An ARM-based macOS target, as seen on Apple Silicon devices
  * `x86_64-apple-darwin`: An x86 macOS target
  * `aarch64-unknown-linux-gnu`: An ARM64 Linux target. Equivalent to `aarch64-manylinux_2_28`
  * `aarch64-unknown-linux-musl`: An ARM64 Linux target
  * `x86_64-unknown-linux-musl`: An `x86_64` Linux target
  * `riscv64-unknown-linux`: A RISCV64 Linux target
  * `x86_64-manylinux2014`: An `x86_64` target for the `manylinux2014` platform. Equivalent to `x86_64-manylinux_2_17`
  * `x86_64-manylinux_2_17`: An `x86_64` target for the `manylinux_2_17` platform
  * `x86_64-manylinux_2_28`: An `x86_64` target for the `manylinux_2_28` platform
  * `x86_64-manylinux_2_31`: An `x86_64` target for the `manylinux_2_31` platform
  * `x86_64-manylinux_2_32`: An `x86_64` target for the `manylinux_2_32` platform
  * `x86_64-manylinux_2_33`: An `x86_64` target for the `manylinux_2_33` platform
  * `x86_64-manylinux_2_34`: An `x86_64` target for the `manylinux_2_34` platform
  * `x86_64-manylinux_2_35`: An `x86_64` target for the `manylinux_2_35` platform
  * `x86_64-manylinux_2_36`: An `x86_64` target for the `manylinux_2_36` platform
  * `x86_64-manylinux_2_37`: An `x86_64` target for the `manylinux_2_37` platform
  * `x86_64-manylinux_2_38`: An `x86_64` target for the `manylinux_2_38` platform
  * `x86_64-manylinux_2_39`: An `x86_64` target for the `manylinux_2_39` platform
  * `x86_64-manylinux_2_40`: An `x86_64` target for the `manylinux_2_40` platform
  * `aarch64-manylinux2014`: An ARM64 target for the `manylinux2014` platform. Equivalent to `aarch64-manylinux_2_17`
  * `aarch64-manylinux_2_17`: An ARM64 target for the `manylinux_2_17` platform
  * `aarch64-manylinux_2_28`: An ARM64 target for the `manylinux_2_28` platform
  * `aarch64-manylinux_2_31`: An ARM64 target for the `manylinux_2_31` platform
  * `aarch64-manylinux_2_32`: An ARM64 target for the `manylinux_2_32` platform
  * `aarch64-manylinux_2_33`: An ARM64 target for the `manylinux_2_33` platform
  * `aarch64-manylinux_2_34`: An ARM64 target for the `manylinux_2_34` platform
  * `aarch64-manylinux_2_35`: An ARM64 target for the `manylinux_2_35` platform
  * `aarch64-manylinux_2_36`: An ARM64 target for the `manylinux_2_36` platform
  * `aarch64-manylinux_2_37`: An ARM64 target for the `manylinux_2_37` platform
  * `aarch64-manylinux_2_38`: An ARM64 target for the `manylinux_2_38` platform
  * `aarch64-manylinux_2_39`: An ARM64 target for the `manylinux_2_39` platform
  * `aarch64-manylinux_2_40`: An ARM64 target for the `manylinux_2_40` platform
  * `aarch64-linux-android`: An ARM64 Android target
  * `x86_64-linux-android`: An `x86_64` Android target
  * `wasm32-pyodide2024`: A wasm32 target using the Pyodide 2024 platform. Meant for use with Python 3.12. See <https://pyodide.org/en/stable/development/abi/312.html>
  * `wasm32-pyodide2025`: A wasm32 target using the Pyodide 2025 platform. Meant for use with Python 3.13. See <https://pyodide.org/en/stable/development/abi/313.html>
  * `arm64-apple-ios`: An ARM64 target for iOS device
  * `arm64-apple-ios-simulator`: An ARM64 target for iOS simulator
  * `x86_64-apple-ios-simulator`: An `x86_64` target for iOS simulator

    
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Refresh all cached data 

[`--refresh-package`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--refresh-package) _refresh-package_ 
    
Refresh cached data for a specific package 

[`--reinstall`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--reinstall), `--force-reinstall` 
    
Reinstall all packages, regardless of whether they're already installed. Implies `--refresh` 

[`--reinstall-package`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--reinstall-package) _reinstall-package_ 
    
Reinstall a specific package, regardless of whether it's already installed. Implies `--refresh-package` 

[`--resolution`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--resolution) _resolution_ 
    
The strategy to use when selecting between the different compatible versions for a given package requirement.
By default, uv will use the latest compatible version of each package (`highest`).
May also be set with the `UV_RESOLUTION` environment variable.
Possible values:
  * `highest`: Resolve the highest compatible version of each package
  * `lowest`: Resolve the lowest compatible version of each package
  * `lowest-direct`: Resolve the lowest compatible version of any direct dependencies, and the highest compatible version of any transitive dependencies

    
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store. 

[`--torch-backend`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--torch-backend) _torch-backend_ 
    
The backend to use when fetching packages in the PyTorch ecosystem (e.g., `cpu`, `cu126`, or `auto`)
When set, uv will ignore the configured index URLs for packages in the PyTorch ecosystem, and will instead use the defined backend.
For example, when set to `cpu`, uv will use the CPU-only PyTorch index; when set to `cu126`, uv will use the PyTorch index for CUDA 12.6.
The `auto` mode will attempt to detect the appropriate PyTorch index based on the currently installed CUDA drivers.
This option is in preview and may change in any future release.
May also be set with the `UV_TORCH_BACKEND` environment variable.
Possible values:
  * `auto`: Select the appropriate PyTorch index based on the operating system and CUDA driver version
  * `cpu`: Use the CPU-only PyTorch index
  * `cu132`: Use the PyTorch index for CUDA 13.2
  * `cu130`: Use the PyTorch index for CUDA 13.0
  * `cu129`: Use the PyTorch index for CUDA 12.9
  * `cu128`: Use the PyTorch index for CUDA 12.8
  * `cu126`: Use the PyTorch index for CUDA 12.6
  * `cu125`: Use the PyTorch index for CUDA 12.5
  * `cu124`: Use the PyTorch index for CUDA 12.4
  * `cu123`: Use the PyTorch index for CUDA 12.3
  * `cu122`: Use the PyTorch index for CUDA 12.2
  * `cu121`: Use the PyTorch index for CUDA 12.1
  * `cu120`: Use the PyTorch index for CUDA 12.0
  * `cu118`: Use the PyTorch index for CUDA 11.8
  * `cu117`: Use the PyTorch index for CUDA 11.7
  * `cu116`: Use the PyTorch index for CUDA 11.6
  * `cu115`: Use the PyTorch index for CUDA 11.5
  * `cu114`: Use the PyTorch index for CUDA 11.4
  * `cu113`: Use the PyTorch index for CUDA 11.3
  * `cu112`: Use the PyTorch index for CUDA 11.2
  * `cu111`: Use the PyTorch index for CUDA 11.1
  * `cu110`: Use the PyTorch index for CUDA 11.0
  * `cu102`: Use the PyTorch index for CUDA 10.2
  * `cu101`: Use the PyTorch index for CUDA 10.1
  * `cu100`: Use the PyTorch index for CUDA 10.0
  * `cu92`: Use the PyTorch index for CUDA 9.2
  * `cu91`: Use the PyTorch index for CUDA 9.1
  * `cu90`: Use the PyTorch index for CUDA 9.0
  * `cu80`: Use the PyTorch index for CUDA 8.0
  * `rocm7.2`: Use the PyTorch index for ROCm 7.2
  * `rocm7.1`: Use the PyTorch index for ROCm 7.1
  * `rocm7.0`: Use the PyTorch index for ROCm 7.0
  * `rocm6.4`: Use the PyTorch index for ROCm 6.4
  * `rocm6.3`: Use the PyTorch index for ROCm 6.3
  * `rocm6.2.4`: Use the PyTorch index for ROCm 6.2.4
  * `rocm6.2`: Use the PyTorch index for ROCm 6.2
  * `rocm6.1`: Use the PyTorch index for ROCm 6.1
  * `rocm6.0`: Use the PyTorch index for ROCm 6.0
  * `rocm5.7`: Use the PyTorch index for ROCm 5.7
  * `rocm5.6`: Use the PyTorch index for ROCm 5.6
  * `rocm5.5`: Use the PyTorch index for ROCm 5.5
  * `rocm5.4.2`: Use the PyTorch index for ROCm 5.4.2
  * `rocm5.4`: Use the PyTorch index for ROCm 5.4
  * `rocm5.3`: Use the PyTorch index for ROCm 5.3
  * `rocm5.2`: Use the PyTorch index for ROCm 5.2
  * `rocm5.1.1`: Use the PyTorch index for ROCm 5.1.1
  * `rocm4.2`: Use the PyTorch index for ROCm 4.2
  * `rocm4.1`: Use the PyTorch index for ROCm 4.1
  * `rocm4.0.1`: Use the PyTorch index for ROCm 4.0.1
  * `xpu`: Use the PyTorch index for Intel XPU

    
Allow package upgrades, ignoring pinned versions in any existing output file. Implies `--refresh` 

[`--upgrade-group`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--upgrade-group) _upgrade-group_ 
    
Allow upgrades for all packages in a dependency group, ignoring pinned versions in any existing output file 

[`--upgrade-package`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--upgrade-package), `-P` _upgrade-package_ 
    
Allow upgrades for a specific package, ignoring pinned versions in any existing output file. Implies `--refresh-package`     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>) 

[`--with`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--with), `-w` _with_ 
    
Include the following additional requirements 

[`--with-editable`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--with-editable) _with-editable_ 
    
Include the given packages in editable mode 

[`--with-executables-from`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--with-executables-from) _with-executables-from_ 
    
Install executables from the following packages 

[`--with-requirements`](https://docs.astral.sh/uv/reference/cli/#uv-tool-install--with-requirements) _with-requirements_ 
    
Run with the packages listed in the given files.
The following formats are supported: `requirements.txt`, `.py` files with inline metadata, and `pylock.toml`.
### [uv tool upgrade](https://docs.astral.sh/uv/reference/cli/#uv-tool-upgrade)
Upgrade installed tools.
If a tool was installed with version constraints, they will be respected on upgrade — to upgrade a tool beyond the originally provided constraints, use `uv tool install` again.
If a tool was installed with specific settings, they will be respected on upgraded. For example, if `--prereleases allow` was provided during installation, it will continue to be respected in upgrades.
### Usage

```
uv tool upgrade [OPTIONS] <NAME>...

```

### Arguments     
The name of the tool to upgrade, along with an optional version specifier
### Options     
Upgrade all tools 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-tool-upgrade--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-tool-upgrade--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-tool-upgrade--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--compile-bytecode`](https://docs.astral.sh/uv/reference/cli/#uv-tool-upgrade--compile-bytecode), `--compile` 
    
Compile Python files to bytecode after installation.
By default, uv does not compile Python (`.py`) files to bytecode (`__pycache__/*.pyc`); instead, compilation is performed lazily the first time a module is imported. For use-cases in which start time is critical, such as CLI applications and Docker containers, this option can be enabled to trade longer installation times for faster start times.
When enabled, install operations (e.g., `uv pip install`) will compile installed or reinstalled Python files. Commands that perform a sync operation (e.g., `uv sync` or `uv run`) will process the entire site-packages directory including packages that are not being modified.
May also be set with the `UV_COMPILE_BYTECODE` environment variable. 

[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-tool-upgrade--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--config-setting`](https://docs.astral.sh/uv/reference/cli/#uv-tool-upgrade--config-setting), `--config-settings`, `-C` _config-setting_ 
    
Settings to pass to the PEP 517 build backend, specified as `KEY=VALUE` pairs 

[`--config-setting-package`](https://docs.astral.sh/uv/reference/cli/#uv-tool-upgrade--config-setting-package), `--config-settings-package` _config-setting-package_ 
    
Settings to pass to the PEP 517 build backend for a specific package, specified as `PACKAGE:KEY=VALUE` pairs 

[`--default-index`](https://docs.astral.sh/uv/reference/cli/#uv-tool-upgrade--default-index) _default-index_ 
    
The default package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--index` flag.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
May also be set with the `UV_DEFAULT_INDEX` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-tool-upgrade--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable. 

[`--exclude-newer`](https://docs.astral.sh/uv/reference/cli/#uv-tool-upgrade--exclude-newer) _exclude-newer_ 
    
Limit candidate packages to those that were uploaded prior to the given date.
The date is compared against the upload time of each individual distribution artifact (i.e., when each file was uploaded to the package index), not the release date of the package version.
Accepts RFC 3339 timestamps (e.g., `2006-12-02T02:07:43Z`), local dates in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Use `false` to disable `exclude-newer`.
May also be set with the `UV_EXCLUDE_NEWER` environment variable. 

[`--exclude-newer-package`](https://docs.astral.sh/uv/reference/cli/#uv-tool-upgrade--exclude-newer-package) _exclude-newer-package_ 
    
Limit candidate packages for specific packages to those that were uploaded prior to the given date.
Accepts package-date pairs in the format `PACKAGE=DATE`, where `DATE` is an RFC 3339 timestamp (e.g., `2006-12-02T02:07:43Z`), a local date in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Can be provided multiple times for different packages. 

[`--extra-index-url`](https://docs.astral.sh/uv/reference/cli/#uv-tool-upgrade--extra-index-url) _extra-index-url_ 
    
(Deprecated: use `--index` instead) Extra URLs of package indexes to use, in addition to `--index-url`.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--index-url` (which defaults to PyPI). When multiple `--extra-index-url` flags are provided, earlier values take priority.
May also be set with the `UV_EXTRA_INDEX_URL` environment variable. 

[`--find-links`](https://docs.astral.sh/uv/reference/cli/#uv-tool-upgrade--find-links), `-f` _find-links_ 
    
Locations to search for candidate distributions, in addition to those found in the registry indexes.
If a path, the target must be a directory that contains packages as wheel files (`.whl`) or source distributions (e.g., `.tar.gz` or `.zip`) at the top level.
If a URL, the page must contain a flat list of links to package files adhering to the formats described above.
May also be set with the `UV_FIND_LINKS` environment variable. 

[`--fork-strategy`](https://docs.astral.sh/uv/reference/cli/#uv-tool-upgrade--fork-strategy) _fork-strategy_ 
    
The strategy to use when selecting multiple versions of a given package across Python versions and platforms.
By default, uv will optimize for selecting the latest version of each package for each supported Python version (`requires-python`), while minimizing the number of selected versions across platforms.
Under `fewest`, uv will minimize the number of selected versions for each package, preferring older versions that are compatible with a wider range of supported Python versions or platforms.
May also be set with the `UV_FORK_STRATEGY` environment variable.
Possible values:
  * `fewest`: Optimize for selecting the fewest number of versions for each package. Older versions may be preferred if they are compatible with a wider range of supported Python versions or platforms
  * `requires-python`: Optimize for selecting latest supported version of each package, for each supported Python version

    
Display the concise help for this command 

[`--index`](https://docs.astral.sh/uv/reference/cli/#uv-tool-upgrade--index) _index_ 
    
The indexes to use when resolving dependencies, in addition to the default index.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--default-index` (which defaults to PyPI). When multiple `--index` flags are provided, earlier values take priority.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
Relative paths can be disambiguated from index names with `./` or `../` on Unix or `.\\`, `..\\`, `./` or `../` on Windows.
May also be set with the `UV_INDEX` environment variable. 

[`--index-strategy`](https://docs.astral.sh/uv/reference/cli/#uv-tool-upgrade--index-strategy) _index-strategy_ 
    
The strategy to use when resolving against multiple index URLs.
By default, uv will stop at the first index on which a given package is available, and limit resolutions to those present on that first index (`first-index`). This prevents "dependency confusion" attacks, whereby an attacker can upload a malicious package under the same name to an alternate index.
May also be set with the `UV_INDEX_STRATEGY` environment variable.
Possible values:
  * `first-index`: Only use results from the first index that returns a match for a given package name
  * `unsafe-first-match`: Search for every package name across all indexes, exhausting the versions from the first index before moving on to the next
  * `unsafe-best-match`: Search for every package name across all indexes, preferring the "best" version found. If a package version is in multiple indexes, only look at the entry for the first index



[`--index-url`](https://docs.astral.sh/uv/reference/cli/#uv-tool-upgrade--index-url), `-i` _index-url_ 
    
(Deprecated: use `--default-index` instead) The URL of the Python package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--extra-index-url` flag.
May also be set with the `UV_INDEX_URL` environment variable. 

[`--keyring-provider`](https://docs.astral.sh/uv/reference/cli/#uv-tool-upgrade--keyring-provider) _keyring-provider_ 
    
Attempt to use `keyring` for authentication for index URLs.
At present, only `--keyring-provider subprocess` is supported, which configures uv to use the `keyring` CLI to handle authentication.
Defaults to `disabled`.
May also be set with the `UV_KEYRING_PROVIDER` environment variable.
Possible values:
  * `disabled`: Do not use keyring for credential lookup
  * `subprocess`: Use the `keyring` command for credential lookup



[`--link-mode`](https://docs.astral.sh/uv/reference/cli/#uv-tool-upgrade--link-mode) _link-mode_ 
    
The method to use when installing packages from the global cache.
Defaults to `clone` (also known as Copy-on-Write) on macOS and Linux, and `hardlink` on Windows.
WARNING: The use of symlink link mode is discouraged, as they create tight coupling between the cache and the target environment. For example, clearing the cache (`uv cache clean`) will break all installed packages by way of removing the underlying source files. Use symlinks with caution.
May also be set with the `UV_LINK_MODE` environment variable.
Possible values:
  * `clone`: Clone (i.e., copy-on-write) packages from the source into the destination
  * `copy`: Copy packages from the source into the destination
  * `hardlink`: Hard link packages from the source into the destination
  * `symlink`: Symbolically link packages from the source into the destination

    
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions.     
Don't install pre-built wheels.
The given packages will be built and installed from source. The resolver will still use pre-built wheels to extract package metadata, if available.
May also be set with the `UV_NO_BINARY` environment variable. 

[`--no-binary-package`](https://docs.astral.sh/uv/reference/cli/#uv-tool-upgrade--no-binary-package) _no-binary-package_ 
    
Don't install pre-built wheels for a specific package [env: `UV_NO_BINARY_PACKAGE`=]     
Don't build source distributions.
When enabled, uv will reuse cached wheels from previously built source distributions, but operations that require building a source distribution will exit with an error. First-party packages, such as projects in the workspace, will still be built. uv will also still build editable requirements, and their build backends may run arbitrary Python code.
May also be set with the `UV_NO_BUILD` environment variable. 

[`--no-build-isolation`](https://docs.astral.sh/uv/reference/cli/#uv-tool-upgrade--no-build-isolation)
    
Disable isolation when building source distributions.
Assumes that build dependencies specified by PEP 518 are already installed.
May also be set with the `UV_NO_BUILD_ISOLATION` environment variable. 

[`--no-build-isolation-package`](https://docs.astral.sh/uv/reference/cli/#uv-tool-upgrade--no-build-isolation-package) _no-build-isolation-package_ 
    
Disable isolation when building source distributions for a specific package.
Assumes that the packages' build dependencies specified by PEP 518 are already installed. 

[`--no-build-package`](https://docs.astral.sh/uv/reference/cli/#uv-tool-upgrade--no-build-package) _no-build-package_ 
    
Don't build source distributions for a specific package [env: `UV_NO_BUILD_PACKAGE`=]
First-party packages, such as projects in the workspace, will still be built. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-tool-upgrade--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable.     
Ignore the registry index (e.g., PyPI), instead relying on direct URL dependencies and those provided via `--find-links` 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-tool-upgrade--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-tool-upgrade--no-python-downloads)
    
Disable automatic downloads of Python.     
Ignore the `tool.uv.sources` table when resolving dependencies. Used to lock against the standards-compliant, publishable package metadata, as opposed to using any workspace, Git, URL, or local path sources
May also be set with the `UV_NO_SOURCES` environment variable. 

[`--no-sources-package`](https://docs.astral.sh/uv/reference/cli/#uv-tool-upgrade--no-sources-package) _no-sources-package_ 
    
Don't use sources from the `tool.uv.sources` table for the specified packages [env: `UV_NO_SOURCES_PACKAGE`=]     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--prerelease`](https://docs.astral.sh/uv/reference/cli/#uv-tool-upgrade--prerelease) _prerelease_ 
    
The strategy to use when considering pre-release versions.
By default, uv will prefer stable candidates, falling back to pre-releases only after every stable candidate that satisfies the active constraints is rejected (`if-necessary`).
May also be set with the `UV_PRERELEASE` environment variable.
Possible values:
  * `disallow`: Disallow all pre-release versions
  * `allow`: Allow all pre-release versions
  * `if-necessary`: Prefer stable versions, falling back to pre-release versions when necessary
  * `explicit`: Prefer stable versions for first-party packages with explicit pre-release specifiers, falling back to pre-release versions when necessary. Disallow pre-release versions for all other packages
  * `if-necessary-or-explicit`: Deprecated alias for `if-necessary`



[`--prerelease-package`](https://docs.astral.sh/uv/reference/cli/#uv-tool-upgrade--prerelease-package) _prerelease-package_ 
    
The strategy to use when considering pre-release versions for a specific package.
Accepts package-mode pairs in the format `PACKAGE=MODE`, where `MODE` is any value accepted by `--prerelease`.
May be provided multiple times for different packages. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-tool-upgrade--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable. 

[`--python`](https://docs.astral.sh/uv/reference/cli/#uv-tool-upgrade--python), `-p` _python_ 
    
Upgrade a tool, and specify it to use the given Python interpreter to build its environment. Use with `--all` to apply to all tools.
See [uv python](https://docs.astral.sh/uv/reference/cli/#uv-python) for details on Python discovery and supported request formats.
May also be set with the `UV_PYTHON` environment variable. 

[`--python-platform`](https://docs.astral.sh/uv/reference/cli/#uv-tool-upgrade--python-platform) _python-platform_ 
    
The platform for which requirements should be installed.
Represented as a "target triple", a string that describes the target platform in terms of its CPU, vendor, and operating system name, like `x86_64-unknown-linux-gnu` or `aarch64-apple-darwin`.
When targeting macOS (Darwin), the default minimum version is `13.0`. Use `MACOSX_DEPLOYMENT_TARGET` to specify a different minimum version, e.g., `14.0`.
When targeting iOS, the default minimum version is `13.0`. Use `IPHONEOS_DEPLOYMENT_TARGET` to specify a different minimum version, e.g., `14.0`.
When targeting Android, the default minimum Android API level is `24`. Use `ANDROID_API_LEVEL` to specify a different minimum version, e.g., `26`.
WARNING: When specified, uv will select wheels that are compatible with the _target_ platform; as a result, the installed distributions may not be compatible with the _current_ platform. Conversely, any distributions that are built from source may be incompatible with the _target_ platform, as they will be built for the _current_ platform. The `--python-platform` option is intended for advanced use cases.
Possible values:
  * `windows`: An alias for `x86_64-pc-windows-msvc`, the default target for Windows
  * `linux`: An alias for `x86_64-unknown-linux-gnu`, the default target for Linux
  * `macos`: An alias for `aarch64-apple-darwin`, the default target for macOS
  * `x86_64-pc-windows-msvc`: A 64-bit x86 Windows target
  * `aarch64-pc-windows-msvc`: An ARM64 Windows target
  * `i686-pc-windows-msvc`: A 32-bit x86 Windows target
  * `x86_64-unknown-linux-gnu`: An x86 Linux target. Equivalent to `x86_64-manylinux_2_28`
  * `aarch64-apple-darwin`: An ARM-based macOS target, as seen on Apple Silicon devices
  * `x86_64-apple-darwin`: An x86 macOS target
  * `aarch64-unknown-linux-gnu`: An ARM64 Linux target. Equivalent to `aarch64-manylinux_2_28`
  * `aarch64-unknown-linux-musl`: An ARM64 Linux target
  * `x86_64-unknown-linux-musl`: An `x86_64` Linux target
  * `riscv64-unknown-linux`: A RISCV64 Linux target
  * `x86_64-manylinux2014`: An `x86_64` target for the `manylinux2014` platform. Equivalent to `x86_64-manylinux_2_17`
  * `x86_64-manylinux_2_17`: An `x86_64` target for the `manylinux_2_17` platform
  * `x86_64-manylinux_2_28`: An `x86_64` target for the `manylinux_2_28` platform
  * `x86_64-manylinux_2_31`: An `x86_64` target for the `manylinux_2_31` platform
  * `x86_64-manylinux_2_32`: An `x86_64` target for the `manylinux_2_32` platform
  * `x86_64-manylinux_2_33`: An `x86_64` target for the `manylinux_2_33` platform
  * `x86_64-manylinux_2_34`: An `x86_64` target for the `manylinux_2_34` platform
  * `x86_64-manylinux_2_35`: An `x86_64` target for the `manylinux_2_35` platform
  * `x86_64-manylinux_2_36`: An `x86_64` target for the `manylinux_2_36` platform
  * `x86_64-manylinux_2_37`: An `x86_64` target for the `manylinux_2_37` platform
  * `x86_64-manylinux_2_38`: An `x86_64` target for the `manylinux_2_38` platform
  * `x86_64-manylinux_2_39`: An `x86_64` target for the `manylinux_2_39` platform
  * `x86_64-manylinux_2_40`: An `x86_64` target for the `manylinux_2_40` platform
  * `aarch64-manylinux2014`: An ARM64 target for the `manylinux2014` platform. Equivalent to `aarch64-manylinux_2_17`
  * `aarch64-manylinux_2_17`: An ARM64 target for the `manylinux_2_17` platform
  * `aarch64-manylinux_2_28`: An ARM64 target for the `manylinux_2_28` platform
  * `aarch64-manylinux_2_31`: An ARM64 target for the `manylinux_2_31` platform
  * `aarch64-manylinux_2_32`: An ARM64 target for the `manylinux_2_32` platform
  * `aarch64-manylinux_2_33`: An ARM64 target for the `manylinux_2_33` platform
  * `aarch64-manylinux_2_34`: An ARM64 target for the `manylinux_2_34` platform
  * `aarch64-manylinux_2_35`: An ARM64 target for the `manylinux_2_35` platform
  * `aarch64-manylinux_2_36`: An ARM64 target for the `manylinux_2_36` platform
  * `aarch64-manylinux_2_37`: An ARM64 target for the `manylinux_2_37` platform
  * `aarch64-manylinux_2_38`: An ARM64 target for the `manylinux_2_38` platform
  * `aarch64-manylinux_2_39`: An ARM64 target for the `manylinux_2_39` platform
  * `aarch64-manylinux_2_40`: An ARM64 target for the `manylinux_2_40` platform
  * `aarch64-linux-android`: An ARM64 Android target
  * `x86_64-linux-android`: An `x86_64` Android target
  * `wasm32-pyodide2024`: A wasm32 target using the Pyodide 2024 platform. Meant for use with Python 3.12. See <https://pyodide.org/en/stable/development/abi/312.html>
  * `wasm32-pyodide2025`: A wasm32 target using the Pyodide 2025 platform. Meant for use with Python 3.13. See <https://pyodide.org/en/stable/development/abi/313.html>
  * `arm64-apple-ios`: An ARM64 target for iOS device
  * `arm64-apple-ios-simulator`: An ARM64 target for iOS simulator
  * `x86_64-apple-ios-simulator`: An `x86_64` target for iOS simulator

    
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout. 

[`--reinstall`](https://docs.astral.sh/uv/reference/cli/#uv-tool-upgrade--reinstall), `--force-reinstall` 
    
Reinstall all packages, regardless of whether they're already installed. Implies `--refresh` 

[`--reinstall-package`](https://docs.astral.sh/uv/reference/cli/#uv-tool-upgrade--reinstall-package) _reinstall-package_ 
    
Reinstall a specific package, regardless of whether it's already installed. Implies `--refresh-package` 

[`--resolution`](https://docs.astral.sh/uv/reference/cli/#uv-tool-upgrade--resolution) _resolution_ 
    
The strategy to use when selecting between the different compatible versions for a given package requirement.
By default, uv will use the latest compatible version of each package (`highest`).
May also be set with the `UV_RESOLUTION` environment variable.
Possible values:
  * `highest`: Resolve the highest compatible version of each package
  * `lowest`: Resolve the lowest compatible version of each package
  * `lowest-direct`: Resolve the lowest compatible version of any direct dependencies, and the highest compatible version of any transitive dependencies

    
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store.     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
### [uv tool list](https://docs.astral.sh/uv/reference/cli/#uv-tool-list)
List installed tools
### Usage

```
uv tool list [OPTIONS]

```

### Options 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-tool-list--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-tool-list--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-tool-list--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-tool-list--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-tool-list--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable. 

[`--exclude-newer`](https://docs.astral.sh/uv/reference/cli/#uv-tool-list--exclude-newer) _exclude-newer_ 
    
Limit candidate packages to those that were uploaded prior to the given date.
The date is compared against the upload time of each individual distribution artifact (i.e., when each file was uploaded to the package index), not the release date of the package version.
Accepts RFC 3339 timestamps (e.g., `2006-12-02T02:07:43Z`), local dates in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Use `false` to disable `exclude-newer`.
May also be set with the `UV_EXCLUDE_NEWER` environment variable. 

[`--exclude-newer-package`](https://docs.astral.sh/uv/reference/cli/#uv-tool-list--exclude-newer-package) _exclude-newer-package_ 
    
Limit candidate packages for specific packages to those that were uploaded prior to the given date.
Accepts package-date pairs in the format `PACKAGE=DATE`, where `DATE` is an RFC 3339 timestamp (e.g., `2006-12-02T02:07:43Z`), a local date in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Can be provided multiple times for different packages.     
Display the concise help for this command     
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-tool-list--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable. 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-tool-list--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files.     
List outdated tools.
The latest version of each tool will be shown alongside the installed version. Up-to-date tools will be omitted from the output. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-tool-list--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Whether to display the extra requirements installed with each tool     
Whether to display the path to each tool environment and installed executable     
Whether to display the Python version associated with each tool 

[`--show-version-specifiers`](https://docs.astral.sh/uv/reference/cli/#uv-tool-list--show-version-specifiers)
    
Whether to display the version specifier(s) used to install each tool     
Whether to display the additional requirements installed with each tool     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store.     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
### [uv tool audit](https://docs.astral.sh/uv/reference/cli/#uv-tool-audit)
Audit installed tools and their dependencies
### Usage

```
uv tool audit [OPTIONS] <NAME>...

```

### Arguments     
The names of the installed tools to audit
### Options     
Audit all installed tools 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-tool-audit--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-tool-audit--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-tool-audit--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-tool-audit--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-tool-audit--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable.     
Display the concise help for this command 

[`--ignore`](https://docs.astral.sh/uv/reference/cli/#uv-tool-audit--ignore) _ignore_ 
    
Ignore a vulnerability by ID.
Vulnerabilities matching any of the provided IDs (including aliases) will be excluded from the audit results.
May be provided multiple times. 

[`--ignore-until-fixed`](https://docs.astral.sh/uv/reference/cli/#uv-tool-audit--ignore-until-fixed) _ignore-until-fixed_ 
    
Ignore a vulnerability by ID, but only while no fix is available.
Vulnerabilities matching any of the provided IDs (including aliases) will be excluded from the audit results as long as they have no known fix versions. Once a fix version becomes available, the vulnerability will be reported again.
May be provided multiple times.     
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-tool-audit--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable. 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-tool-audit--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-tool-audit--no-python-downloads)
    
Disable automatic downloads of Python.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--output-format`](https://docs.astral.sh/uv/reference/cli/#uv-tool-audit--output-format) _output-format_ 
    
Select the output format
[default: text]
Possible values:
  * `text`: Display the result in a human-readable format
  * `json`: Display the result in JSON format
  * `sarif`: Display the result in SARIF format



[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-tool-audit--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout. 

[`--service-format`](https://docs.astral.sh/uv/reference/cli/#uv-tool-audit--service-format) _service-format_ 
    
The service format to use for vulnerability lookups.
Each service format has a default URL, which can be changed with `--service-url`. The defaults are:
  * OSV: <https://api.osv.dev/>


[default: osv]
Possible values:
  * `osv`



[`--service-url`](https://docs.astral.sh/uv/reference/cli/#uv-tool-audit--service-url) _service-url_ 
    
The URL to vulnerability service API endpoint.
If not provided, the default URL for the selected service will be used.
The service needs to use the OSV protocol, unless a different format was requested by `--service-format`.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store.     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
### [uv tool uninstall](https://docs.astral.sh/uv/reference/cli/#uv-tool-uninstall)
Uninstall a tool
### Usage

```
uv tool uninstall [OPTIONS] <NAME>...

```

### Arguments     
The name of the tool to uninstall
### Options     
Uninstall all tools 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-tool-uninstall--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-tool-uninstall--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-tool-uninstall--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-tool-uninstall--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-tool-uninstall--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable.     
Display the concise help for this command     
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-tool-uninstall--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable. 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-tool-uninstall--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-tool-uninstall--no-python-downloads)
    
Disable automatic downloads of Python.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-tool-uninstall--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store.     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
### [uv tool update-shell](https://docs.astral.sh/uv/reference/cli/#uv-tool-update-shell)
Ensure that the tool executable directory is on the `PATH`.
If the tool executable directory is not present on the `PATH`, uv will attempt to add it to the relevant shell configuration files.
If the shell configuration files already include a blurb to add the executable directory to the path, but the directory is not present on the `PATH`, uv will exit with an error.
The tool executable directory is determined according to the XDG standard and can be retrieved with `uv tool dir --bin`.
### Usage

```
uv tool update-shell [OPTIONS]

```

### Options 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-tool-update-shell--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-tool-update-shell--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-tool-update-shell--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-tool-update-shell--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-tool-update-shell--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable.     
Display the concise help for this command     
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-tool-update-shell--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable. 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-tool-update-shell--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-tool-update-shell--no-python-downloads)
    
Disable automatic downloads of Python.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-tool-update-shell--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store.     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
### [uv tool dir](https://docs.astral.sh/uv/reference/cli/#uv-tool-dir)
Show the path to the uv tools directory.
The tools directory is used to store environments and metadata for installed tools.
By default, tools are stored in the uv data directory at `$XDG_DATA_HOME/uv/tools` or `$HOME/.local/share/uv/tools` on Unix and `%APPDATA%\uv\data\tools` on Windows.
The tool installation directory may be overridden with `$UV_TOOL_DIR`.
To instead view the directory uv installs executables into, use the `--bin` flag.
### Usage

```
uv tool dir [OPTIONS]

```

### Options 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-tool-dir--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable.     
Show the directory into which `uv tool` will install executables.
By default, `uv tool dir` shows the directory into which the tool Python environments themselves are installed, rather than the directory containing the linked executables.
The tool executable directory is determined according to the XDG standard and is derived from the following environment variables, in order of preference:
  * `$UV_TOOL_BIN_DIR`
  * `$XDG_BIN_HOME`
  * `$XDG_DATA_HOME/../bin`
  * `$HOME/.local/bin`



[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-tool-dir--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-tool-dir--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-tool-dir--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-tool-dir--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable.     
Display the concise help for this command     
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-tool-dir--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable. 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-tool-dir--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-tool-dir--no-python-downloads)
    
Disable automatic downloads of Python.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-tool-dir--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store.     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
## [uv python](https://docs.astral.sh/uv/reference/cli/#uv-python)
Manage Python versions and installations
Generally, uv first searches for Python in a virtual environment, either active or in a `.venv` directory in the current working directory or any parent directory. If a virtual environment is not required, uv will then search for a Python interpreter. Python interpreters are found by searching for Python executables in the `PATH` environment variable.
On Windows, the registry is also searched for Python executables.
By default, uv will download Python if a version cannot be found. This behavior can be disabled with the `--no-python-downloads` flag or the `python-downloads` setting.
The `--python` option allows requesting a different interpreter.
The following Python version request formats are supported:
  * `<version>` e.g. `3`, `3.12`, `3.12.3`
  * `<version-specifier>` e.g. `>=3.12,<3.13`
  * `<version><short-variant>` (e.g., `3.13t`, `3.12.0d`)
  * `<version>+<variant>` (e.g., `3.13+freethreaded`, `3.12.0+debug`)
  * `<implementation>` e.g. `cpython` or `cp`
  * `<implementation>@<version>` e.g. 
  * `<implementation><version>` e.g. `cpython3.12` or `cp312`
  * `<implementation><version-specifier>` e.g. `cpython>=3.12,<3.13`
  * `<implementation>-<version>-<os>-<arch>-<libc>` e.g. `cpython-3.12.3-macos-aarch64-none`


Additionally, a specific system Python interpreter can often be requested with:
  * `<executable-path>` e.g. `/opt/homebrew/bin/python3`
  * `<executable-name>` e.g. `mypython3`
  * `<install-dir>` e.g. `/some/environment/`


When the `--python` option is used, normal discovery rules apply but discovered interpreters are checked for compatibility with the request, e.g., if `pypy` is requested, uv will first check if the virtual environment contains a PyPy interpreter then check if each executable in the path is a PyPy interpreter.
uv supports discovering CPython, PyPy, and GraalPy interpreters. Unsupported interpreters will be skipped during discovery. If an unsupported interpreter implementation is requested, uv will exit with an error.
### Usage

```
uv python [OPTIONS] <COMMAND>

```

### Commands     
List the available Python installations 

[`uv python install`](https://docs.astral.sh/uv/reference/cli/#uv-python-install)
    
Download and install Python versions 

[`uv python upgrade`](https://docs.astral.sh/uv/reference/cli/#uv-python-upgrade)
    
Upgrade installed Python versions     
Search for a Python installation     
Pin to a specific Python version     
Show the uv Python installation directory 

[`uv python uninstall`](https://docs.astral.sh/uv/reference/cli/#uv-python-uninstall)
    
Uninstall Python versions 

[`uv python update-shell`](https://docs.astral.sh/uv/reference/cli/#uv-python-update-shell)
    
Ensure that the Python executable directory is on the `PATH`
### [uv python list](https://docs.astral.sh/uv/reference/cli/#uv-python-list)
List the available Python installations.
By default, installed Python versions and the downloads for latest available patch version of each supported Python major version are shown.
Use `--managed-python` to view only managed Python versions.
Use `--no-managed-python` to omit managed Python versions.
Use `--all-versions` to view all available patch versions.
Use `--only-installed` to omit available downloads.
### Usage

```
uv python list [OPTIONS] [REQUEST]

```

### Arguments     
A Python request to filter by.
See [uv python](https://docs.astral.sh/uv/reference/cli/#uv-python) to view supported request formats.
### Options 

[`--all-arches`](https://docs.astral.sh/uv/reference/cli/#uv-python-list--all-arches), `--all_architectures` 
    
List Python downloads for all architectures.
By default, only downloads for the current architecture are shown.     
List Python downloads for all platforms.
By default, only downloads for the current platform are shown.     
List all Python versions, including old patch versions.
By default, only the latest patch version is shown for each minor version. 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-python-list--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-python-list--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-python-list--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-python-list--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-python-list--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable.     
Display the concise help for this command     
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-python-list--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable. 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-python-list--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-python-list--no-python-downloads)
    
Disable automatic downloads of Python.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files.     
Only show available Python downloads.
By default, installed distributions and available downloads for the current platform are shown.     
Only show installed Python versions.
By default, installed distributions and available downloads for the current platform are shown. 

[`--output-format`](https://docs.astral.sh/uv/reference/cli/#uv-python-list--output-format) _output-format_ 
    
Select the output format
[default: text]
Possible values:
  * `text`: Plain text (for humans)
  * `json`: JSON (for computers)



[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-python-list--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable. 

[`--python-downloads-json-url`](https://docs.astral.sh/uv/reference/cli/#uv-python-list--python-downloads-json-url) _python-downloads-json-url_ 
    
URL pointing to JSON of custom Python installations     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Show the URLs of available Python downloads.
By default, these display as `<download available>`.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store.     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
### [uv python install](https://docs.astral.sh/uv/reference/cli/#uv-python-install)
Download and install Python versions.
Supports CPython and PyPy. CPython distributions are downloaded from the Astral `python-build-standalone` project. PyPy distributions are downloaded from `python.org`. The available Python versions are bundled with each uv release. To install new Python versions, you may need upgrade uv.
Python versions are installed into the uv Python directory, which can be retrieved with `uv python dir`.
By default, Python executables are added to a directory on the path with a minor version suffix, e.g., `python3.13`. To install `python3` and `python`, use the `--default` flag. Use `uv python dir --bin` to see the target directory.
Multiple Python versions may be requested.
See `uv help python` to view supported request formats.
### Usage

```
uv python install [OPTIONS] [TARGETS]...

```

### Arguments     
The Python version(s) to install.
If not provided, the requested Python version(s) will be read from the `UV_PYTHON` environment variable then `.python-versions` or `.python-version` files. If none of the above are present, uv will check if it has installed any Python versions. If not, it will install the latest stable version of Python.
See [uv python](https://docs.astral.sh/uv/reference/cli/#uv-python) to view supported request formats.
### Options 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-python-install--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-python-install--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-python-install--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--compile-bytecode`](https://docs.astral.sh/uv/reference/cli/#uv-python-install--compile-bytecode), `--compile` 
    
Compile Python's standard library to bytecode after installation.
By default, uv does not compile Python (`.py`) files to bytecode (`__pycache__/*.pyc`); instead, compilation is performed lazily the first time a module is imported. For use-cases in which start time is important, such as CLI applications and Docker containers, this option can be enabled to trade longer installation times and some additional disk space for faster start times.
When enabled, uv will process the Python version's `stdlib` directory. It will ignore any compilation errors.
May also be set with the `UV_COMPILE_BYTECODE` environment variable. 

[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-python-install--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable.     
Use as the default Python version.
By default, only a `python{major}.{minor}` executable is installed, e.g., `python3.10`. When the `--default` flag is used, `python{major}`, e.g., `python3`, and `python` executables are also installed.
Alternative Python variants will still include their tag. For example, installing 3.13+freethreaded with `--default` will include `python3t` and `pythont` instead of `python3` and `python`.
If multiple Python versions are requested, uv will exit with an error. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-python-install--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable.     
Replace existing Python executables during installation.
By default, uv will refuse to replace executables that it does not manage.
Implies `--reinstall`.     
Display the concise help for this command 

[`--install-dir`](https://docs.astral.sh/uv/reference/cli/#uv-python-install--install-dir), `-i` _install-dir_ 
    
The directory to store the Python installation in.
If provided, `UV_PYTHON_INSTALL_DIR` will need to be set for subsequent operations for uv to discover the Python installation.
See `uv python dir` to view the current Python installation directory. Defaults to `~/.local/share/uv/python`.
May also be set with the `UV_PYTHON_INSTALL_DIR` environment variable.     
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions. 

[`--mirror`](https://docs.astral.sh/uv/reference/cli/#uv-python-install--mirror) _mirror_ 
    
Set the URL to use as the source for downloading Python installations.
The provided URL will replace `https://github.com/astral-sh/python-build-standalone/releases/download` in, e.g., `https://github.com/astral-sh/python-build-standalone/releases/download/20240713/cpython-3.12.4%2B20240713-aarch64-apple-darwin-install_only.tar.gz`.
Distributions can be read from a local directory by using the `file://` URL scheme.     
Do not install a Python executable into the `bin` directory.
This can also be set with `UV_PYTHON_INSTALL_BIN=0`. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-python-install--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable. 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-python-install--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-python-install--no-python-downloads)
    
Disable automatic downloads of Python.     
Do not register the Python installation in the Windows registry.
This can also be set with `UV_PYTHON_INSTALL_REGISTRY=0`.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-python-install--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable. 

[`--pypy-mirror`](https://docs.astral.sh/uv/reference/cli/#uv-python-install--pypy-mirror) _pypy-mirror_ 
    
Set the URL to use as the source for downloading PyPy installations.
The provided URL will replace `https://downloads.python.org/pypy` in, e.g., `https://downloads.python.org/pypy/pypy3.8-v7.3.7-osx64.tar.bz2`.
Distributions can be read from a local directory by using the `file://` URL scheme. 

[`--python-downloads-json-url`](https://docs.astral.sh/uv/reference/cli/#uv-python-install--python-downloads-json-url) _python-downloads-json-url_ 
    
URL pointing to JSON of custom Python installations     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Reinstall the requested Python version, if it's already installed.
If a minor version is requested, all matching installed patch versions are reinstalled.
By default, uv will exit successfully if the version is already installed.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store.     
Upgrade existing Python installations to the latest patch version.
By default, uv will not upgrade already-installed Python versions to newer patch releases. With `--upgrade`, uv will upgrade to the latest available patch version for the specified minor version(s).
If the requested versions are not yet installed, uv will install them.
This option is only supported for minor version requests, e.g., `3.12`; uv will exit with an error if a patch version, e.g., `3.12.2`, is requested.     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
### [uv python upgrade](https://docs.astral.sh/uv/reference/cli/#uv-python-upgrade)
Upgrade installed Python versions.
Upgrades versions to the latest supported patch release.
A target Python minor version to upgrade may be provided, e.g., `3.13`. Multiple versions may be provided to perform more than one upgrade.
If no target version is provided, then uv will upgrade all managed CPython versions.
During an upgrade, uv will not uninstall outdated patch versions.
When an upgrade is performed, virtual environments created by uv will automatically use the new version. However, if the virtual environment was created before the upgrade functionality was added, it will continue to use the old Python version; to enable upgrades, the environment must be recreated.
Upgrades are not yet supported for alternative implementations, like PyPy.
### Usage

```
uv python upgrade [OPTIONS] [TARGETS]...

```

### Arguments     
The Python minor version(s) to upgrade.
If no target version is provided, then uv will upgrade all managed CPython versions.
### Options 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-python-upgrade--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-python-upgrade--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-python-upgrade--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--compile-bytecode`](https://docs.astral.sh/uv/reference/cli/#uv-python-upgrade--compile-bytecode), `--compile` 
    
Compile Python's standard library to bytecode after installation.
By default, uv does not compile Python (`.py`) files to bytecode (`__pycache__/*.pyc`); instead, compilation is performed lazily the first time a module is imported. For use-cases in which start time is important, such as CLI applications and Docker containers, this option can be enabled to trade longer installation times and some additional disk space for faster start times.
When enabled, uv will process the Python version's `stdlib` directory. It will ignore any compilation errors.
May also be set with the `UV_COMPILE_BYTECODE` environment variable. 

[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-python-upgrade--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-python-upgrade--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable.     
Display the concise help for this command 

[`--install-dir`](https://docs.astral.sh/uv/reference/cli/#uv-python-upgrade--install-dir), `-i` _install-dir_ 
    
The directory Python installations are stored in.
If provided, `UV_PYTHON_INSTALL_DIR` will need to be set for subsequent operations for uv to discover the Python installation.
See `uv python dir` to view the current Python installation directory. Defaults to `~/.local/share/uv/python`.
May also be set with the `UV_PYTHON_INSTALL_DIR` environment variable.     
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions. 

[`--mirror`](https://docs.astral.sh/uv/reference/cli/#uv-python-upgrade--mirror) _mirror_ 
    
Set the URL to use as the source for downloading Python installations.
The provided URL will replace `https://github.com/astral-sh/python-build-standalone/releases/download` in, e.g., `https://github.com/astral-sh/python-build-standalone/releases/download/20240713/cpython-3.12.4%2B20240713-aarch64-apple-darwin-install_only.tar.gz`.
Distributions can be read from a local directory by using the `file://` URL scheme. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-python-upgrade--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable. 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-python-upgrade--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-python-upgrade--no-python-downloads)
    
Disable automatic downloads of Python.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-python-upgrade--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable. 

[`--pypy-mirror`](https://docs.astral.sh/uv/reference/cli/#uv-python-upgrade--pypy-mirror) _pypy-mirror_ 
    
Set the URL to use as the source for downloading PyPy installations.
The provided URL will replace `https://downloads.python.org/pypy` in, e.g., `https://downloads.python.org/pypy/pypy3.8-v7.3.7-osx64.tar.bz2`.
Distributions can be read from a local directory by using the `file://` URL scheme. 

[`--python-downloads-json-url`](https://docs.astral.sh/uv/reference/cli/#uv-python-upgrade--python-downloads-json-url) _python-downloads-json-url_ 
    
URL pointing to JSON of custom Python installations     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Reinstall the latest Python patch, if it's already installed.
By default, uv will exit successfully if the latest patch is already installed.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store.     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
### [uv python find](https://docs.astral.sh/uv/reference/cli/#uv-python-find)
Search for a Python installation.
Displays the path to the Python executable.
See `uv help python` to view supported request formats and details on discovery behavior.
### Usage

```
uv python find [OPTIONS] [REQUEST]

```

### Arguments     
The Python request.
See [uv python](https://docs.astral.sh/uv/reference/cli/#uv-python) to view supported request formats.
### Options 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-python-find--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-python-find--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-python-find--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-python-find--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-python-find--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable.     
Display the concise help for this command     
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-python-find--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable. 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-python-find--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-project`](https://docs.astral.sh/uv/reference/cli/#uv-python-find--no-project), `--no_workspace` 
    
Avoid discovering a project or workspace.
Otherwise, when no request is provided, the Python requirement of a project in the current directory or parent directories will be used.
May also be set with the `UV_NO_PROJECT` environment variable. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-python-find--no-python-downloads)
    
Disable automatic downloads of Python.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-python-find--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable. 

[`--python-downloads-json-url`](https://docs.astral.sh/uv/reference/cli/#uv-python-find--python-downloads-json-url) _python-downloads-json-url_ 
    
URL pointing to JSON of custom Python installations     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Resolve symlinks in the output path.
When enabled, the output path will be canonicalized, resolving any symlinks. 

[`--script`](https://docs.astral.sh/uv/reference/cli/#uv-python-find--script) _script_ 
    
Find the environment for a Python script, rather than the current project     
Show the Python version that would be used instead of the path to the interpreter     
Only find system Python interpreters.
By default, uv will report the first Python interpreter it would use, including those in an active virtual environment or a virtual environment in the current working directory or any parent directory.
The `--system` option instructs uv to skip virtual environment Python interpreters and restrict its search to the system path.
May also be set with the `UV_SYSTEM_PYTHON` environment variable.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store.     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
### [uv python pin](https://docs.astral.sh/uv/reference/cli/#uv-python-pin)
Pin to a specific Python version.
Writes the pinned Python version to a `.python-version` file, which is used by other uv commands to determine the required Python version.
If no version is provided, uv will look for an existing `.python-version` file and display the currently pinned version. If no `.python-version` file is found, uv will exit with an error.
See `uv help python` to view supported request formats.
### Usage

```
uv python pin [OPTIONS] [REQUEST]

```

### Arguments     
The Python version request.
uv supports more formats than other tools that read `.python-version` files, i.e., `pyenv`. If compatibility with those tools is needed, only use version numbers instead of complex requests such as .
If no request is provided, the currently pinned version will be shown.
See [uv python](https://docs.astral.sh/uv/reference/cli/#uv-python) to view supported request formats.
### Options 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-python-pin--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-python-pin--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-python-pin--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-python-pin--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-python-pin--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable.     
Update the global Python version pin.
Writes the pinned Python version to a `.python-version` file in the uv user configuration directory: `XDG_CONFIG_HOME/uv` on Linux/macOS and `%APPDATA%/uv` on Windows.
When a local Python version pin is not found in the working directory or an ancestor directory, this version will be used instead.     
Display the concise help for this command     
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-python-pin--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable. 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-python-pin--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-project`](https://docs.astral.sh/uv/reference/cli/#uv-python-pin--no-project), `--no-workspace` 
    
Avoid validating the Python pin is compatible with the project or workspace.
By default, a project or workspace is discovered in the current directory or any parent directory. If a workspace is found, the Python pin is validated against the workspace's `requires-python` constraint.
May also be set with the `UV_NO_PROJECT` environment variable. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-python-pin--no-python-downloads)
    
Disable automatic downloads of Python.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-python-pin--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable. 

[`--python-downloads-json-url`](https://docs.astral.sh/uv/reference/cli/#uv-python-pin--python-downloads-json-url) _python-downloads-json-url_ 
    
URL pointing to JSON of custom Python installations     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Write the resolved Python interpreter path instead of the request.
Ensures that the exact same interpreter is used.
This option is usually not safe to use when committing the `.python-version` file to version control.     
Remove the Python version pin     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store.     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
### [uv python dir](https://docs.astral.sh/uv/reference/cli/#uv-python-dir)
Show the uv Python installation directory.
By default, Python installations are stored in the uv data directory at `$XDG_DATA_HOME/uv/python` or `$HOME/.local/share/uv/python` on Unix and `%APPDATA%\uv\data\python` on Windows.
The Python installation directory may be overridden with `$UV_PYTHON_INSTALL_DIR`.
To view the directory where uv installs Python executables instead, use the `--bin` flag. The Python executable directory may be overridden with `$UV_PYTHON_BIN_DIR`.
### Usage

```
uv python dir [OPTIONS]

```

### Options 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-python-dir--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable.     
Show the directory into which `uv python` will install Python executables.
The Python executable directory is determined according to the XDG standard and is derived from the following environment variables, in order of preference:
  * `$UV_PYTHON_BIN_DIR`
  * `$XDG_BIN_HOME`
  * `$XDG_DATA_HOME/../bin`
  * `$HOME/.local/bin`



[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-python-dir--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-python-dir--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-python-dir--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-python-dir--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable.     
Display the concise help for this command     
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-python-dir--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable. 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-python-dir--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-python-dir--no-python-downloads)
    
Disable automatic downloads of Python.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-python-dir--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store.     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
### [uv python uninstall](https://docs.astral.sh/uv/reference/cli/#uv-python-uninstall)
Uninstall Python versions
### Usage

```
uv python uninstall [OPTIONS] <TARGETS>...

```

### Arguments     
The Python version(s) to uninstall.
See [uv python](https://docs.astral.sh/uv/reference/cli/#uv-python) to view supported request formats.
### Options     
Uninstall all managed Python versions 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-python-uninstall--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-python-uninstall--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-python-uninstall--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-python-uninstall--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-python-uninstall--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable.     
Display the concise help for this command 

[`--install-dir`](https://docs.astral.sh/uv/reference/cli/#uv-python-uninstall--install-dir), `-i` _install-dir_ 
    
The directory where the Python was installed
May also be set with the `UV_PYTHON_INSTALL_DIR` environment variable.     
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-python-uninstall--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable. 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-python-uninstall--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-python-uninstall--no-python-downloads)
    
Disable automatic downloads of Python.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-python-uninstall--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store.     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
### [uv python update-shell](https://docs.astral.sh/uv/reference/cli/#uv-python-update-shell)
Ensure that the Python executable directory is on the `PATH`.
If the Python executable directory is not present on the `PATH`, uv will attempt to add it to the relevant shell configuration files.
If the shell configuration files already include a blurb to add the executable directory to the path, but the directory is not present on the `PATH`, uv will exit with an error.
The Python executable directory is determined according to the XDG standard and can be retrieved with `uv python dir --bin`.
### Usage

```
uv python update-shell [OPTIONS]

```

### Options 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-python-update-shell--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-python-update-shell--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-python-update-shell--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-python-update-shell--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-python-update-shell--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable.     
Display the concise help for this command     
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-python-update-shell--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable. 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-python-update-shell--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-python-update-shell--no-python-downloads)
    
Disable automatic downloads of Python.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-python-update-shell--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store.     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
Manage Python packages with a pip-compatible interface
### Usage

```
uv pip [OPTIONS] <COMMAND>

```

### Commands     
Compile a `requirements.in` file to a `requirements.txt` or `pylock.toml` file     
Sync an environment with a `requirements.txt` or `pylock.toml` file     
Install packages into an environment 

[`uv pip uninstall`](https://docs.astral.sh/uv/reference/cli/#uv-pip-uninstall)
    
Uninstall packages from an environment     
List, in requirements format, packages installed in an environment     
List, in tabular format, packages installed in an environment     
Show information about one or more installed packages     
Display the dependency tree for an environment     
Verify installed packages have compatible dependencies
### [uv pip compile](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile)
Compile a `requirements.in` file to a `requirements.txt` or `pylock.toml` file
### Usage

```
uv pip compile [OPTIONS] <SRC_FILE|--group <GROUP>>

```

### Arguments     
Include the packages listed in the given files.
The following formats are supported: `requirements.txt`, `.py` files with inline metadata, `pylock.toml`, `pyproject.toml`, `setup.py`, and `setup.cfg`.
If a `pyproject.toml`, `setup.py`, or `setup.cfg` file is provided, uv will extract the requirements for the relevant project.
If `-` is provided, then requirements will be read from stdin.
The order of the requirements files and the requirements in them is used to determine priority during resolution.
### Options     
Include all optional dependencies.
Only applies to `pyproject.toml`, `setup.py`, and `setup.cfg` sources. 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--annotation-style`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--annotation-style) _annotation-style_ 
    
The style of the annotation comments included in the output file, used to indicate the source of each package.
Defaults to `split`.
Possible values:
  * `line`: Render the annotations on a single, comma-separated line
  * `split`: Render each annotation on its own line



[`--build-constraints`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--build-constraints), `--build-constraint`, `-b` _build-constraints_ 
    
Constrain build dependencies using the given requirements files when building source distributions.
Constraints files are `requirements.txt`-like files that only control the _version_ of a requirement that's installed. However, including a package in a constraints file will _not_ trigger the installation of that package.
May also be set with the `UV_BUILD_CONSTRAINT` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable.     
Path to a PEM-encoded CA certificate bundle.
If provided, this overrides the default certificate source. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--config-setting`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--config-setting), `--config-settings`, `-C` _config-setting_ 
    
Settings to pass to the PEP 517 build backend, specified as `KEY=VALUE` pairs 

[`--config-settings-package`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--config-settings-package), `--config-settings-package` _config-settings-package_ 
    
Settings to pass to the PEP 517 build backend for a specific package, specified as `PACKAGE:KEY=VALUE` pairs 

[`--constraints`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--constraints), `--constraint`, `-c` _constraints_ 
    
Constrain versions using the given requirements files.
Constraints files are `requirements.txt`-like files that only control the _version_ of a requirement that's installed. However, including a package in a constraints file will _not_ trigger the installation of that package.
This is equivalent to pip's `--constraint` option.
May also be set with the `UV_CONSTRAINT` environment variable. 

[`--custom-compile-command`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--custom-compile-command) _custom-compile-command_ 
    
The header comment to include at the top of the output file generated by `uv pip compile`.
Used to reflect custom build scripts and commands that wrap `uv pip compile`.
May also be set with the `UV_CUSTOM_COMPILE_COMMAND` environment variable. 

[`--default-index`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--default-index) _default-index_ 
    
The default package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--index` flag.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
May also be set with the `UV_DEFAULT_INDEX` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable. 

[`--emit-build-options`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--emit-build-options)
    
Include `--no-binary` and `--only-binary` entries in the generated output file     
Include `--find-links` entries in the generated output file 

[`--emit-index-annotation`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--emit-index-annotation)
    
Include comment annotations indicating the index used to resolve each package (e.g., `# from https://pypi.org/simple`)     
Include `--index-url` and `--extra-index-url` entries in the generated output file 

[`--exclude-newer`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--exclude-newer) _exclude-newer_ 
    
Limit candidate packages to those that were uploaded prior to the given date.
The date is compared against the upload time of each individual distribution artifact (i.e., when each file was uploaded to the package index), not the release date of the package version.
Accepts RFC 3339 timestamps (e.g., `2006-12-02T02:07:43Z`), local dates in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Use `false` to disable `exclude-newer`.
May also be set with the `UV_EXCLUDE_NEWER` environment variable. 

[`--exclude-newer-package`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--exclude-newer-package) _exclude-newer-package_ 
    
Limit candidate packages for specific packages to those that were uploaded prior to the given date.
Accepts package-date pairs in the format `PACKAGE=DATE`, where `DATE` is an RFC 3339 timestamp (e.g., `2006-12-02T02:07:43Z`), a local date in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Can be provided multiple times for different packages. 

[`--excludes`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--excludes), `--exclude` _excludes_ 
    
Exclude packages from resolution using the given requirements files.
Excludes files are `requirements.txt`-like files that specify packages to exclude from the resolution. When a package is excluded, it will be omitted from the dependency list entirely and its own dependencies will be ignored during the resolution phase. Excludes are unconditional in that requirement specifiers and markers are ignored; any package listed in the provided file will be omitted from all resolved environments.
May also be set with the `UV_EXCLUDE` environment variable. 

[`--extra`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--extra) _extra_ 
    
Include optional dependencies from the specified extra name; may be provided more than once.
Only applies to `pyproject.toml`, `setup.py`, and `setup.cfg` sources. 

[`--extra-index-url`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--extra-index-url) _extra-index-url_ 
    
(Deprecated: use `--index` instead) Extra URLs of package indexes to use, in addition to `--index-url`.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--index-url` (which defaults to PyPI). When multiple `--extra-index-url` flags are provided, earlier values take priority.
May also be set with the `UV_EXTRA_INDEX_URL` environment variable. 

[`--find-links`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--find-links), `-f` _find-links_ 
    
Locations to search for candidate distributions, in addition to those found in the registry indexes.
If a path, the target must be a directory that contains packages as wheel files (`.whl`) or source distributions (e.g., `.tar.gz` or `.zip`) at the top level.
If a URL, the page must contain a flat list of links to package files adhering to the formats described above.
May also be set with the `UV_FIND_LINKS` environment variable. 

[`--fork-strategy`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--fork-strategy) _fork-strategy_ 
    
The strategy to use when selecting multiple versions of a given package across Python versions and platforms.
By default, uv will optimize for selecting the latest version of each package for each supported Python version (`requires-python`), while minimizing the number of selected versions across platforms.
Under `fewest`, uv will minimize the number of selected versions for each package, preferring older versions that are compatible with a wider range of supported Python versions or platforms.
May also be set with the `UV_FORK_STRATEGY` environment variable.
Possible values:
  * `fewest`: Optimize for selecting the fewest number of versions for each package. Older versions may be preferred if they are compatible with a wider range of supported Python versions or platforms
  * `requires-python`: Optimize for selecting latest supported version of each package, for each supported Python version



[`--format`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--format) _format_ 
    
The format in which the resolution should be output.
Supports both `requirements.txt` and `pylock.toml` (PEP 751) output formats.
uv will infer the output format from the file extension of the output file, if provided. Otherwise, defaults to `requirements.txt`.
Possible values:
  * `requirements.txt`: Export in `requirements.txt` format
  * `pylock.toml`: Export in `pylock.toml` format

    
Include distribution hashes in the output file 

[`--group`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--group) _group_ 
    
Install the specified dependency group from a `pyproject.toml`.
If no path is provided, the `pyproject.toml` in the working directory is used.
May be provided multiple times.     
Display the concise help for this command 

[`--index`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--index) _index_ 
    
The indexes to use when resolving dependencies, in addition to the default index.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--default-index` (which defaults to PyPI). When multiple `--index` flags are provided, earlier values take priority.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
Relative paths can be disambiguated from index names with `./` or `../` on Unix or `.\\`, `..\\`, `./` or `../` on Windows.
May also be set with the `UV_INDEX` environment variable. 

[`--index-strategy`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--index-strategy) _index-strategy_ 
    
The strategy to use when resolving against multiple index URLs.
By default, uv will stop at the first index on which a given package is available, and limit resolutions to those present on that first index (`first-index`). This prevents "dependency confusion" attacks, whereby an attacker can upload a malicious package under the same name to an alternate index.
May also be set with the `UV_INDEX_STRATEGY` environment variable.
Possible values:
  * `first-index`: Only use results from the first index that returns a match for a given package name
  * `unsafe-first-match`: Search for every package name across all indexes, exhausting the versions from the first index before moving on to the next
  * `unsafe-best-match`: Search for every package name across all indexes, preferring the "best" version found. If a package version is in multiple indexes, only look at the entry for the first index



[`--index-url`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--index-url), `-i` _index-url_ 
    
(Deprecated: use `--default-index` instead) The URL of the Python package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--extra-index-url` flag.
May also be set with the `UV_INDEX_URL` environment variable. 

[`--keyring-provider`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--keyring-provider) _keyring-provider_ 
    
Attempt to use `keyring` for authentication for index URLs.
At present, only `--keyring-provider subprocess` is supported, which configures uv to use the `keyring` CLI to handle authentication.
Defaults to `disabled`.
May also be set with the `UV_KEYRING_PROVIDER` environment variable.
Possible values:
  * `disabled`: Do not use keyring for credential lookup
  * `subprocess`: Use the `keyring` command for credential lookup



[`--link-mode`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--link-mode) _link-mode_ 
    
The method to use when installing packages from the global cache.
This option is only used when building source distributions.
Defaults to `clone` (also known as Copy-on-Write) on macOS and Linux, and `hardlink` on Windows.
WARNING: The use of symlink link mode is discouraged, as they create tight coupling between the cache and the target environment. For example, clearing the cache (`uv cache clean`) will break all installed packages by way of removing the underlying source files. Use symlinks with caution.
May also be set with the `UV_LINK_MODE` environment variable.
Possible values:
  * `clone`: Clone (i.e., copy-on-write) packages from the source into the destination
  * `copy`: Copy packages from the source into the destination
  * `hardlink`: Hard link packages from the source into the destination
  * `symlink`: Symbolically link packages from the source into the destination

    
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions.     
Exclude comment annotations indicating the source of each package 

[`--no-binary`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--no-binary) _no-binary_ 
    
Don't install pre-built wheels.
The given packages will be built and installed from source. The resolver will still use pre-built wheels to extract package metadata, if available.
Multiple packages may be provided. Disable binaries for all packages with `:all:`. Clear previously specified packages with `:none:`.     
Don't build source distributions.
When enabled, uv will reuse cached wheels from previously built source distributions, but operations that require building a source distribution will exit with an error. uv may still build editable requirements, and their build backends may run arbitrary Python code.
Alias for `--only-binary :all:`. 

[`--no-build-isolation`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--no-build-isolation)
    
Disable isolation when building source distributions.
Assumes that build dependencies specified by PEP 518 are already installed.
May also be set with the `UV_NO_BUILD_ISOLATION` environment variable. 

[`--no-build-isolation-package`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--no-build-isolation-package) _no-build-isolation-package_ 
    
Disable isolation when building source distributions for a specific package.
Assumes that the packages' build dependencies specified by PEP 518 are already installed. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Ignore package dependencies, instead only add those packages explicitly listed on the command line to the resulting requirements file 

[`--no-emit-package`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--no-emit-package), `--unsafe-package` _no-emit-package_ 
    
Specify a package to omit from the output resolution. Its dependencies will still be included in the resolution. Equivalent to pip-compile's `--unsafe-package` option     
Exclude the comment header at the top of the generated output file     
Ignore the registry index (e.g., PyPI), instead relying on direct URL dependencies and those provided via `--find-links` 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--no-python-downloads)
    
Disable automatic downloads of Python.     
Ignore the `tool.uv.sources` table when resolving dependencies. Used to lock against the standards-compliant, publishable package metadata, as opposed to using any workspace, Git, URL, or local path sources
May also be set with the `UV_NO_SOURCES` environment variable. 

[`--no-sources-package`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--no-sources-package) _no-sources-package_ 
    
Don't use sources from the `tool.uv.sources` table for the specified packages [env: `UV_NO_SOURCES_PACKAGE`=]     
Include extras in the output file.
By default, uv strips extras, as any packages pulled in by the extras are already included as dependencies in the output file directly. Further, output files generated with `--no-strip-extras` cannot be used as constraints files in `install` and `sync` invocations. 

[`--no-strip-markers`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--no-strip-markers)
    
Include environment markers in the output file.
By default, uv strips environment markers, as the resolution generated by `compile` is only guaranteed to be correct for the target environment.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--only-binary`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--only-binary) _only-binary_ 
    
Only use pre-built wheels; don't build source distributions.
When enabled, uv will reuse cached wheels from previously built source distributions, but operations that require building a source distribution for the given packages will exit with an error. uv may still build editable requirements, and their build backends may run arbitrary Python code.
Multiple packages may be provided. Disable binaries for all packages with `:all:`. Clear previously specified packages with `:none:`. 

[`--output-file`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--output-file), `-o` _output-file_ 
    
Write the compiled requirements to the given `requirements.txt` or `pylock.toml` file.
If the file already exists, the existing versions will be preferred when resolving dependencies, unless `--upgrade` is also specified. 

[`--overrides`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--overrides), `--override` _overrides_ 
    
Override versions using the given requirements files.
Overrides files are `requirements.txt`-like files that force a specific version of a requirement to be installed, regardless of the requirements declared by any constituent package, and regardless of whether this would be considered an invalid resolution.
While constraints are _additive_ , in that they're combined with the requirements of the constituent packages, overrides are _absolute_ , in that they completely replace the requirements of the constituent packages.
May also be set with the `UV_OVERRIDE` environment variable. 

[`--prerelease`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--prerelease) _prerelease_ 
    
The strategy to use when considering pre-release versions.
By default, uv will prefer stable candidates, falling back to pre-releases only after every stable candidate that satisfies the active constraints is rejected (`if-necessary`).
May also be set with the `UV_PRERELEASE` environment variable.
Possible values:
  * `disallow`: Disallow all pre-release versions
  * `allow`: Allow all pre-release versions
  * `if-necessary`: Prefer stable versions, falling back to pre-release versions when necessary
  * `explicit`: Prefer stable versions for first-party packages with explicit pre-release specifiers, falling back to pre-release versions when necessary. Disallow pre-release versions for all other packages
  * `if-necessary-or-explicit`: Deprecated alias for `if-necessary`



[`--prerelease-package`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--prerelease-package) _prerelease-package_ 
    
The strategy to use when considering pre-release versions for a specific package.
Accepts package-mode pairs in the format `PACKAGE=MODE`, where `MODE` is any value accepted by `--prerelease`.
May be provided multiple times for different packages. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable. 

[`--python`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--python), `-p` _python_ 
    
The Python interpreter to use during resolution.
A Python interpreter is required for building source distributions to determine package metadata when there are not wheels.
The interpreter is also used to determine the default minimum Python version, unless `--python-version` is provided.
This option respects `UV_PYTHON`, but when set via environment variable, it is overridden by `--python-version`.
See [uv python](https://docs.astral.sh/uv/reference/cli/#uv-python) for details on Python discovery and supported request formats. 

[`--python-platform`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--python-platform) _python-platform_ 
    
The platform for which requirements should be resolved.
Represented as a "target triple", a string that describes the target platform in terms of its CPU, vendor, and operating system name, like `x86_64-unknown-linux-gnu` or `aarch64-apple-darwin`.
When targeting macOS (Darwin), the default minimum version is `13.0`. Use `MACOSX_DEPLOYMENT_TARGET` to specify a different minimum version, e.g., `14.0`.
When targeting iOS, the default minimum version is `13.0`. Use `IPHONEOS_DEPLOYMENT_TARGET` to specify a different minimum version, e.g., `14.0`.
When targeting Android, the default minimum Android API level is `24`. Use `ANDROID_API_LEVEL` to specify a different minimum version, e.g., `26`.
Possible values:
  * `windows`: An alias for `x86_64-pc-windows-msvc`, the default target for Windows
  * `linux`: An alias for `x86_64-unknown-linux-gnu`, the default target for Linux
  * `macos`: An alias for `aarch64-apple-darwin`, the default target for macOS
  * `x86_64-pc-windows-msvc`: A 64-bit x86 Windows target
  * `aarch64-pc-windows-msvc`: An ARM64 Windows target
  * `i686-pc-windows-msvc`: A 32-bit x86 Windows target
  * `x86_64-unknown-linux-gnu`: An x86 Linux target. Equivalent to `x86_64-manylinux_2_28`
  * `aarch64-apple-darwin`: An ARM-based macOS target, as seen on Apple Silicon devices
  * `x86_64-apple-darwin`: An x86 macOS target
  * `aarch64-unknown-linux-gnu`: An ARM64 Linux target. Equivalent to `aarch64-manylinux_2_28`
  * `aarch64-unknown-linux-musl`: An ARM64 Linux target
  * `x86_64-unknown-linux-musl`: An `x86_64` Linux target
  * `riscv64-unknown-linux`: A RISCV64 Linux target
  * `x86_64-manylinux2014`: An `x86_64` target for the `manylinux2014` platform. Equivalent to `x86_64-manylinux_2_17`
  * `x86_64-manylinux_2_17`: An `x86_64` target for the `manylinux_2_17` platform
  * `x86_64-manylinux_2_28`: An `x86_64` target for the `manylinux_2_28` platform
  * `x86_64-manylinux_2_31`: An `x86_64` target for the `manylinux_2_31` platform
  * `x86_64-manylinux_2_32`: An `x86_64` target for the `manylinux_2_32` platform
  * `x86_64-manylinux_2_33`: An `x86_64` target for the `manylinux_2_33` platform
  * `x86_64-manylinux_2_34`: An `x86_64` target for the `manylinux_2_34` platform
  * `x86_64-manylinux_2_35`: An `x86_64` target for the `manylinux_2_35` platform
  * `x86_64-manylinux_2_36`: An `x86_64` target for the `manylinux_2_36` platform
  * `x86_64-manylinux_2_37`: An `x86_64` target for the `manylinux_2_37` platform
  * `x86_64-manylinux_2_38`: An `x86_64` target for the `manylinux_2_38` platform
  * `x86_64-manylinux_2_39`: An `x86_64` target for the `manylinux_2_39` platform
  * `x86_64-manylinux_2_40`: An `x86_64` target for the `manylinux_2_40` platform
  * `aarch64-manylinux2014`: An ARM64 target for the `manylinux2014` platform. Equivalent to `aarch64-manylinux_2_17`
  * `aarch64-manylinux_2_17`: An ARM64 target for the `manylinux_2_17` platform
  * `aarch64-manylinux_2_28`: An ARM64 target for the `manylinux_2_28` platform
  * `aarch64-manylinux_2_31`: An ARM64 target for the `manylinux_2_31` platform
  * `aarch64-manylinux_2_32`: An ARM64 target for the `manylinux_2_32` platform
  * `aarch64-manylinux_2_33`: An ARM64 target for the `manylinux_2_33` platform
  * `aarch64-manylinux_2_34`: An ARM64 target for the `manylinux_2_34` platform
  * `aarch64-manylinux_2_35`: An ARM64 target for the `manylinux_2_35` platform
  * `aarch64-manylinux_2_36`: An ARM64 target for the `manylinux_2_36` platform
  * `aarch64-manylinux_2_37`: An ARM64 target for the `manylinux_2_37` platform
  * `aarch64-manylinux_2_38`: An ARM64 target for the `manylinux_2_38` platform
  * `aarch64-manylinux_2_39`: An ARM64 target for the `manylinux_2_39` platform
  * `aarch64-manylinux_2_40`: An ARM64 target for the `manylinux_2_40` platform
  * `aarch64-linux-android`: An ARM64 Android target
  * `x86_64-linux-android`: An `x86_64` Android target
  * `wasm32-pyodide2024`: A wasm32 target using the Pyodide 2024 platform. Meant for use with Python 3.12. See <https://pyodide.org/en/stable/development/abi/312.html>
  * `wasm32-pyodide2025`: A wasm32 target using the Pyodide 2025 platform. Meant for use with Python 3.13. See <https://pyodide.org/en/stable/development/abi/313.html>
  * `arm64-apple-ios`: An ARM64 target for iOS device
  * `arm64-apple-ios-simulator`: An ARM64 target for iOS simulator
  * `x86_64-apple-ios-simulator`: An `x86_64` target for iOS simulator



[`--python-version`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--python-version) _python-version_ 
    
The Python version to use for resolution.
For example, `3.8` or `3.8.17`.
Defaults to the version of the Python interpreter used for resolution.
Defines the minimum Python version that must be supported by the resolved requirements.
If a patch version is omitted, the minimum patch version is assumed. For example, `3.8` is mapped to `3.8.0`.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Refresh all cached data 

[`--refresh-package`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--refresh-package) _refresh-package_ 
    
Refresh cached data for a specific package 

[`--resolution`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--resolution) _resolution_ 
    
The strategy to use when selecting between the different compatible versions for a given package requirement.
By default, uv will use the latest compatible version of each package (`highest`).
May also be set with the `UV_RESOLUTION` environment variable.
Possible values:
  * `highest`: Resolve the highest compatible version of each package
  * `lowest`: Resolve the lowest compatible version of each package
  * `lowest-direct`: Resolve the lowest compatible version of any direct dependencies, and the highest compatible version of any transitive dependencies

    
Install packages into the system Python environment.
By default, uv uses the virtual environment in the current working directory or any parent directory, falling back to searching for a Python executable in `PATH`. The `--system` option instructs uv to avoid using a virtual environment Python and restrict its search to the system path.
May also be set with the `UV_SYSTEM_PYTHON` environment variable.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store. 

[`--torch-backend`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--torch-backend) _torch-backend_ 
    
The backend to use when fetching packages in the PyTorch ecosystem (e.g., `cpu`, `cu126`, or `auto`).
When set, uv will ignore the configured index URLs for packages in the PyTorch ecosystem, and will instead use the defined backend.
For example, when set to `cpu`, uv will use the CPU-only PyTorch index; when set to `cu126`, uv will use the PyTorch index for CUDA 12.6.
The `auto` mode will attempt to detect the appropriate PyTorch index based on the currently installed CUDA drivers.
This option is in preview and may change in any future release.
May also be set with the `UV_TORCH_BACKEND` environment variable.
Possible values:
  * `auto`: Select the appropriate PyTorch index based on the operating system and CUDA driver version
  * `cpu`: Use the CPU-only PyTorch index
  * `cu132`: Use the PyTorch index for CUDA 13.2
  * `cu130`: Use the PyTorch index for CUDA 13.0
  * `cu129`: Use the PyTorch index for CUDA 12.9
  * `cu128`: Use the PyTorch index for CUDA 12.8
  * `cu126`: Use the PyTorch index for CUDA 12.6
  * `cu125`: Use the PyTorch index for CUDA 12.5
  * `cu124`: Use the PyTorch index for CUDA 12.4
  * `cu123`: Use the PyTorch index for CUDA 12.3
  * `cu122`: Use the PyTorch index for CUDA 12.2
  * `cu121`: Use the PyTorch index for CUDA 12.1
  * `cu120`: Use the PyTorch index for CUDA 12.0
  * `cu118`: Use the PyTorch index for CUDA 11.8
  * `cu117`: Use the PyTorch index for CUDA 11.7
  * `cu116`: Use the PyTorch index for CUDA 11.6
  * `cu115`: Use the PyTorch index for CUDA 11.5
  * `cu114`: Use the PyTorch index for CUDA 11.4
  * `cu113`: Use the PyTorch index for CUDA 11.3
  * `cu112`: Use the PyTorch index for CUDA 11.2
  * `cu111`: Use the PyTorch index for CUDA 11.1
  * `cu110`: Use the PyTorch index for CUDA 11.0
  * `cu102`: Use the PyTorch index for CUDA 10.2
  * `cu101`: Use the PyTorch index for CUDA 10.1
  * `cu100`: Use the PyTorch index for CUDA 10.0
  * `cu92`: Use the PyTorch index for CUDA 9.2
  * `cu91`: Use the PyTorch index for CUDA 9.1
  * `cu90`: Use the PyTorch index for CUDA 9.0
  * `cu80`: Use the PyTorch index for CUDA 8.0
  * `rocm7.2`: Use the PyTorch index for ROCm 7.2
  * `rocm7.1`: Use the PyTorch index for ROCm 7.1
  * `rocm7.0`: Use the PyTorch index for ROCm 7.0
  * `rocm6.4`: Use the PyTorch index for ROCm 6.4
  * `rocm6.3`: Use the PyTorch index for ROCm 6.3
  * `rocm6.2.4`: Use the PyTorch index for ROCm 6.2.4
  * `rocm6.2`: Use the PyTorch index for ROCm 6.2
  * `rocm6.1`: Use the PyTorch index for ROCm 6.1
  * `rocm6.0`: Use the PyTorch index for ROCm 6.0
  * `rocm5.7`: Use the PyTorch index for ROCm 5.7
  * `rocm5.6`: Use the PyTorch index for ROCm 5.6
  * `rocm5.5`: Use the PyTorch index for ROCm 5.5
  * `rocm5.4.2`: Use the PyTorch index for ROCm 5.4.2
  * `rocm5.4`: Use the PyTorch index for ROCm 5.4
  * `rocm5.3`: Use the PyTorch index for ROCm 5.3
  * `rocm5.2`: Use the PyTorch index for ROCm 5.2
  * `rocm5.1.1`: Use the PyTorch index for ROCm 5.1.1
  * `rocm4.2`: Use the PyTorch index for ROCm 4.2
  * `rocm4.1`: Use the PyTorch index for ROCm 4.1
  * `rocm4.0.1`: Use the PyTorch index for ROCm 4.0.1
  * `xpu`: Use the PyTorch index for Intel XPU

    
Perform a universal resolution, attempting to generate a single `requirements.txt` output file that is compatible with all operating systems, architectures, and Python implementations.
In universal mode, the current Python version (or user-provided `--python-version`) will be treated as a lower bound. For example, `--universal --python-version 3.7` would produce a universal resolution for Python 3.7 and later.
Implies `--no-strip-markers`.     
Allow package upgrades, ignoring pinned versions in any existing output file. Implies `--refresh` 

[`--upgrade-group`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--upgrade-group) _upgrade-group_ 
    
Allow upgrades for all packages in a dependency group, ignoring pinned versions in any existing output file 

[`--upgrade-package`](https://docs.astral.sh/uv/reference/cli/#uv-pip-compile--upgrade-package), `-P` _upgrade-package_ 
    
Allow upgrades for a specific package, ignoring pinned versions in any existing output file. Implies `--refresh-package`     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
### [uv pip sync](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync)
Sync an environment with a `requirements.txt` or `pylock.toml` file.
When syncing an environment, any packages not listed in the `requirements.txt` or `pylock.toml` file will be removed. To retain extraneous packages, use `uv pip install` instead.
The input file is presumed to be the output of a `pip compile` or `uv export` operation, in which it will include all transitive dependencies. If transitive dependencies are not present in the file, they will not be installed. Use `--strict` to warn if any transitive dependencies are missing.
### Usage

```
uv pip sync [OPTIONS] <SRC_FILE>...

```

### Arguments     
Include the packages listed in the given files.
The following formats are supported: `requirements.txt`, `.py` files with inline metadata, `pylock.toml`, `pyproject.toml`, `setup.py`, and `setup.cfg`.
If a `pyproject.toml`, `setup.py`, or `setup.cfg` file is provided, uv will extract the requirements for the relevant project.
If `-` is provided, then requirements will be read from stdin.
### Options     
Include all optional dependencies.
Only applies to `pylock.toml`, `pyproject.toml`, `setup.py`, and `setup.cfg` sources. 

[`--allow-empty-requirements`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--allow-empty-requirements)
    
Allow sync of empty requirements, which will clear the environment of all packages 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--break-system-packages`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--break-system-packages)
    
Allow uv to modify an `EXTERNALLY-MANAGED` Python installation.
WARNING: `--break-system-packages` is intended for use in continuous integration (CI) environments, when installing into Python installations that are managed by an external package manager, like `apt`. It should be used with caution, as such Python installations explicitly recommend against modifications by other package managers (like uv or `pip`).
May also be set with the `UV_BREAK_SYSTEM_PACKAGES` environment variable. 

[`--build-constraints`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--build-constraints), `--build-constraint`, `-b` _build-constraints_ 
    
Constrain build dependencies using the given requirements files when building source distributions.
Constraints files are `requirements.txt`-like files that only control the _version_ of a requirement that's installed. However, including a package in a constraints file will _not_ trigger the installation of that package.
May also be set with the `UV_BUILD_CONSTRAINT` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--cert`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--cert) _file_ 
    
Path to a PEM-encoded CA certificate bundle.
If provided, this overrides the default certificate source. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--compile-bytecode`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--compile-bytecode), `--compile` 
    
Compile Python files to bytecode after installation.
By default, uv does not compile Python (`.py`) files to bytecode (`__pycache__/*.pyc`); instead, compilation is performed lazily the first time a module is imported. For use-cases in which start time is critical, such as CLI applications and Docker containers, this option can be enabled to trade longer installation times for faster start times.
When enabled, install operations (e.g., `uv pip install`) will compile installed or reinstalled Python files. Commands that perform a sync operation (e.g., `uv sync` or `uv run`) will process the entire site-packages directory including packages that are not being modified.
May also be set with the `UV_COMPILE_BYTECODE` environment variable. 

[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--config-setting`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--config-setting), `--config-settings`, `-C` _config-setting_ 
    
Settings to pass to the PEP 517 build backend, specified as `KEY=VALUE` pairs 

[`--config-settings-package`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--config-settings-package), `--config-settings-package` _config-settings-package_ 
    
Settings to pass to the PEP 517 build backend for a specific package, specified as `PACKAGE:KEY=VALUE` pairs 

[`--constraints`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--constraints), `--constraint`, `-c` _constraints_ 
    
Constrain versions using the given requirements files.
Constraints files are `requirements.txt`-like files that only control the _version_ of a requirement that's installed. However, including a package in a constraints file will _not_ trigger the installation of that package.
This is equivalent to pip's `--constraint` option.
May also be set with the `UV_CONSTRAINT` environment variable. 

[`--default-index`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--default-index) _default-index_ 
    
The default package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--index` flag.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
May also be set with the `UV_DEFAULT_INDEX` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable.     
Perform a dry run, i.e., don't actually install anything but resolve the dependencies and print the resulting plan 

[`--exclude-newer`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--exclude-newer) _exclude-newer_ 
    
Limit candidate packages to those that were uploaded prior to the given date.
The date is compared against the upload time of each individual distribution artifact (i.e., when each file was uploaded to the package index), not the release date of the package version.
Accepts RFC 3339 timestamps (e.g., `2006-12-02T02:07:43Z`), local dates in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Use `false` to disable `exclude-newer`.
May also be set with the `UV_EXCLUDE_NEWER` environment variable. 

[`--exclude-newer-package`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--exclude-newer-package) _exclude-newer-package_ 
    
Limit candidate packages for specific packages to those that were uploaded prior to the given date.
Accepts package-date pairs in the format `PACKAGE=DATE`, where `DATE` is an RFC 3339 timestamp (e.g., `2006-12-02T02:07:43Z`), a local date in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Can be provided multiple times for different packages. 

[`--extra`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--extra) _extra_ 
    
Include optional dependencies from the specified extra name; may be provided more than once.
Only applies to `pylock.toml`, `pyproject.toml`, `setup.py`, and `setup.cfg` sources. 

[`--extra-index-url`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--extra-index-url) _extra-index-url_ 
    
(Deprecated: use `--index` instead) Extra URLs of package indexes to use, in addition to `--index-url`.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--index-url` (which defaults to PyPI). When multiple `--extra-index-url` flags are provided, earlier values take priority.
May also be set with the `UV_EXTRA_INDEX_URL` environment variable. 

[`--find-links`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--find-links), `-f` _find-links_ 
    
Locations to search for candidate distributions, in addition to those found in the registry indexes.
If a path, the target must be a directory that contains packages as wheel files (`.whl`) or source distributions (e.g., `.tar.gz` or `.zip`) at the top level.
If a URL, the page must contain a flat list of links to package files adhering to the formats described above.
May also be set with the `UV_FIND_LINKS` environment variable. 

[`--group`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--group) _group_ 
    
Install the specified dependency group from a `pylock.toml` or `pyproject.toml`.
If no path is provided, the `pylock.toml` or `pyproject.toml` in the working directory is used.
May be provided multiple times.     
Display the concise help for this command 

[`--index`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--index) _index_ 
    
The indexes to use when resolving dependencies, in addition to the default index.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--default-index` (which defaults to PyPI). When multiple `--index` flags are provided, earlier values take priority.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
Relative paths can be disambiguated from index names with `./` or `../` on Unix or `.\\`, `..\\`, `./` or `../` on Windows.
May also be set with the `UV_INDEX` environment variable. 

[`--index-strategy`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--index-strategy) _index-strategy_ 
    
The strategy to use when resolving against multiple index URLs.
By default, uv will stop at the first index on which a given package is available, and limit resolutions to those present on that first index (`first-index`). This prevents "dependency confusion" attacks, whereby an attacker can upload a malicious package under the same name to an alternate index.
May also be set with the `UV_INDEX_STRATEGY` environment variable.
Possible values:
  * `first-index`: Only use results from the first index that returns a match for a given package name
  * `unsafe-first-match`: Search for every package name across all indexes, exhausting the versions from the first index before moving on to the next
  * `unsafe-best-match`: Search for every package name across all indexes, preferring the "best" version found. If a package version is in multiple indexes, only look at the entry for the first index



[`--index-url`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--index-url), `-i` _index-url_ 
    
(Deprecated: use `--default-index` instead) The URL of the Python package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--extra-index-url` flag.
May also be set with the `UV_INDEX_URL` environment variable. 

[`--keyring-provider`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--keyring-provider) _keyring-provider_ 
    
Attempt to use `keyring` for authentication for index URLs.
At present, only `--keyring-provider subprocess` is supported, which configures uv to use the `keyring` CLI to handle authentication.
Defaults to `disabled`.
May also be set with the `UV_KEYRING_PROVIDER` environment variable.
Possible values:
  * `disabled`: Do not use keyring for credential lookup
  * `subprocess`: Use the `keyring` command for credential lookup



[`--link-mode`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--link-mode) _link-mode_ 
    
The method to use when installing packages from the global cache.
Defaults to `clone` (also known as Copy-on-Write) on macOS and Linux, and `hardlink` on Windows.
WARNING: The use of symlink link mode is discouraged, as they create tight coupling between the cache and the target environment. For example, clearing the cache (`uv cache clean`) will break all installed packages by way of removing the underlying source files. Use symlinks with caution.
May also be set with the `UV_LINK_MODE` environment variable.
Possible values:
  * `clone`: Clone (i.e., copy-on-write) packages from the source into the destination
  * `copy`: Copy packages from the source into the destination
  * `hardlink`: Hard link packages from the source into the destination
  * `symlink`: Symbolically link packages from the source into the destination

    
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions. 

[`--no-allow-empty-requirements`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--no-allow-empty-requirements)


[`--no-binary`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--no-binary) _no-binary_ 
    
Don't install pre-built wheels.
The given packages will be built and installed from source. The resolver will still use pre-built wheels to extract package metadata, if available.
Multiple packages may be provided. Disable binaries for all packages with `:all:`. Clear previously specified packages with `:none:`. 

[`--no-break-system-packages`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--no-break-system-packages)
    
Don't build source distributions.
When enabled, uv will reuse cached wheels from previously built source distributions, but operations that require building a source distribution will exit with an error. uv may still build editable requirements, and their build backends may run arbitrary Python code.
Alias for `--only-binary :all:`. 

[`--no-build-isolation`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--no-build-isolation)
    
Disable isolation when building source distributions.
Assumes that build dependencies specified by PEP 518 are already installed.
May also be set with the `UV_NO_BUILD_ISOLATION` environment variable. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Ignore the registry index (e.g., PyPI), instead relying on direct URL dependencies and those provided via `--find-links` 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--no-python-downloads)
    
Disable automatic downloads of Python.     
Ignore the `tool.uv.sources` table when resolving dependencies. Used to lock against the standards-compliant, publishable package metadata, as opposed to using any workspace, Git, URL, or local path sources
May also be set with the `UV_NO_SOURCES` environment variable. 

[`--no-sources-package`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--no-sources-package) _no-sources-package_ 
    
Don't use sources from the `tool.uv.sources` table for the specified packages [env: `UV_NO_SOURCES_PACKAGE`=] 

[`--no-verify-hashes`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--no-verify-hashes)
    
Disable validation of hashes in the requirements file.
By default, uv will verify any available hashes in the requirements file, but will not require that all requirements have an associated hash. To enforce hash validation, use `--require-hashes`.
May also be set with the `UV_NO_VERIFY_HASHES` environment variable.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--only-binary`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--only-binary) _only-binary_ 
    
Only use pre-built wheels; don't build source distributions.
When enabled, uv will reuse cached wheels from previously built source distributions, but operations that require building a source distribution for the given packages will exit with an error. uv may still build editable requirements, and their build backends may run arbitrary Python code.
Multiple packages may be provided. Disable binaries for all packages with `:all:`. Clear previously specified packages with `:none:`. 

[`--prefix`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--prefix) _prefix_ 
    
Install packages into `lib`, `bin`, and other top-level folders under the specified directory, as if a virtual environment were present at that location.
In general, prefer the use of `--python` to install into an alternate environment, as scripts and other artifacts installed via `--prefix` will reference the installing interpreter, rather than any interpreter added to the `--prefix` directory, rendering them non-portable.
Unlike other install operations, this command does not require discovery of an existing Python environment and only searches for a Python interpreter to use for package resolution. If a suitable Python interpreter cannot be found, uv will install one. To disable this, add `--no-python-downloads`. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable. 

[`--python`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--python), `-p` _python_ 
    
The Python interpreter into which packages should be installed.
By default, syncing requires a virtual environment. A path to an alternative Python can be provided, but it is only recommended in continuous integration (CI) environments and should be used with caution, as it can modify the system Python installation.
See [uv python](https://docs.astral.sh/uv/reference/cli/#uv-python) for details on Python discovery and supported request formats.
May also be set with the `UV_PYTHON` environment variable. 

[`--python-platform`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--python-platform) _python-platform_ 
    
The platform for which requirements should be installed.
Represented as a "target triple", a string that describes the target platform in terms of its CPU, vendor, and operating system name, like `x86_64-unknown-linux-gnu` or `aarch64-apple-darwin`.
When targeting macOS (Darwin), the default minimum version is `13.0`. Use `MACOSX_DEPLOYMENT_TARGET` to specify a different minimum version, e.g., `14.0`.
When targeting iOS, the default minimum version is `13.0`. Use `IPHONEOS_DEPLOYMENT_TARGET` to specify a different minimum version, e.g., `14.0`.
When targeting Android, the default minimum Android API level is `24`. Use `ANDROID_API_LEVEL` to specify a different minimum version, e.g., `26`.
WARNING: When specified, uv will select wheels that are compatible with the _target_ platform; as a result, the installed distributions may not be compatible with the _current_ platform. Conversely, any distributions that are built from source may be incompatible with the _target_ platform, as they will be built for the _current_ platform. The `--python-platform` option is intended for advanced use cases.
Possible values:
  * `windows`: An alias for `x86_64-pc-windows-msvc`, the default target for Windows
  * `linux`: An alias for `x86_64-unknown-linux-gnu`, the default target for Linux
  * `macos`: An alias for `aarch64-apple-darwin`, the default target for macOS
  * `x86_64-pc-windows-msvc`: A 64-bit x86 Windows target
  * `aarch64-pc-windows-msvc`: An ARM64 Windows target
  * `i686-pc-windows-msvc`: A 32-bit x86 Windows target
  * `x86_64-unknown-linux-gnu`: An x86 Linux target. Equivalent to `x86_64-manylinux_2_28`
  * `aarch64-apple-darwin`: An ARM-based macOS target, as seen on Apple Silicon devices
  * `x86_64-apple-darwin`: An x86 macOS target
  * `aarch64-unknown-linux-gnu`: An ARM64 Linux target. Equivalent to `aarch64-manylinux_2_28`
  * `aarch64-unknown-linux-musl`: An ARM64 Linux target
  * `x86_64-unknown-linux-musl`: An `x86_64` Linux target
  * `riscv64-unknown-linux`: A RISCV64 Linux target
  * `x86_64-manylinux2014`: An `x86_64` target for the `manylinux2014` platform. Equivalent to `x86_64-manylinux_2_17`
  * `x86_64-manylinux_2_17`: An `x86_64` target for the `manylinux_2_17` platform
  * `x86_64-manylinux_2_28`: An `x86_64` target for the `manylinux_2_28` platform
  * `x86_64-manylinux_2_31`: An `x86_64` target for the `manylinux_2_31` platform
  * `x86_64-manylinux_2_32`: An `x86_64` target for the `manylinux_2_32` platform
  * `x86_64-manylinux_2_33`: An `x86_64` target for the `manylinux_2_33` platform
  * `x86_64-manylinux_2_34`: An `x86_64` target for the `manylinux_2_34` platform
  * `x86_64-manylinux_2_35`: An `x86_64` target for the `manylinux_2_35` platform
  * `x86_64-manylinux_2_36`: An `x86_64` target for the `manylinux_2_36` platform
  * `x86_64-manylinux_2_37`: An `x86_64` target for the `manylinux_2_37` platform
  * `x86_64-manylinux_2_38`: An `x86_64` target for the `manylinux_2_38` platform
  * `x86_64-manylinux_2_39`: An `x86_64` target for the `manylinux_2_39` platform
  * `x86_64-manylinux_2_40`: An `x86_64` target for the `manylinux_2_40` platform
  * `aarch64-manylinux2014`: An ARM64 target for the `manylinux2014` platform. Equivalent to `aarch64-manylinux_2_17`
  * `aarch64-manylinux_2_17`: An ARM64 target for the `manylinux_2_17` platform
  * `aarch64-manylinux_2_28`: An ARM64 target for the `manylinux_2_28` platform
  * `aarch64-manylinux_2_31`: An ARM64 target for the `manylinux_2_31` platform
  * `aarch64-manylinux_2_32`: An ARM64 target for the `manylinux_2_32` platform
  * `aarch64-manylinux_2_33`: An ARM64 target for the `manylinux_2_33` platform
  * `aarch64-manylinux_2_34`: An ARM64 target for the `manylinux_2_34` platform
  * `aarch64-manylinux_2_35`: An ARM64 target for the `manylinux_2_35` platform
  * `aarch64-manylinux_2_36`: An ARM64 target for the `manylinux_2_36` platform
  * `aarch64-manylinux_2_37`: An ARM64 target for the `manylinux_2_37` platform
  * `aarch64-manylinux_2_38`: An ARM64 target for the `manylinux_2_38` platform
  * `aarch64-manylinux_2_39`: An ARM64 target for the `manylinux_2_39` platform
  * `aarch64-manylinux_2_40`: An ARM64 target for the `manylinux_2_40` platform
  * `aarch64-linux-android`: An ARM64 Android target
  * `x86_64-linux-android`: An `x86_64` Android target
  * `wasm32-pyodide2024`: A wasm32 target using the Pyodide 2024 platform. Meant for use with Python 3.12. See <https://pyodide.org/en/stable/development/abi/312.html>
  * `wasm32-pyodide2025`: A wasm32 target using the Pyodide 2025 platform. Meant for use with Python 3.13. See <https://pyodide.org/en/stable/development/abi/313.html>
  * `arm64-apple-ios`: An ARM64 target for iOS device
  * `arm64-apple-ios-simulator`: An ARM64 target for iOS simulator
  * `x86_64-apple-ios-simulator`: An `x86_64` target for iOS simulator



[`--python-version`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--python-version) _python-version_ 
    
The minimum Python version that should be supported by the requirements (e.g., `3.7` or `3.7.9`).
If a patch version is omitted, the minimum patch version is assumed. For example, `3.7` is mapped to `3.7.0`.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Refresh all cached data 

[`--refresh-package`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--refresh-package) _refresh-package_ 
    
Refresh cached data for a specific package 

[`--reinstall`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--reinstall), `--force-reinstall` 
    
Reinstall all packages, regardless of whether they're already installed. Implies `--refresh` 

[`--reinstall-package`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--reinstall-package) _reinstall-package_ 
    
Reinstall a specific package, regardless of whether it's already installed. Implies `--refresh-package`     
Require a matching hash for each requirement.
By default, uv will verify any available hashes in the requirements file, but will not require that all requirements have an associated hash.
When `--require-hashes` is enabled, _all_ requirements must include a hash or set of hashes, and _all_ requirements must either be pinned to exact versions (e.g., `==1.0.0`), or be specified via direct URL.
Hash-checking mode introduces a number of additional constraints:
  * Git dependencies are not supported. - Editable installations are not supported. - Local dependencies are not supported, unless they point to a specific wheel (`.whl`) or source archive (`.zip`, `.tar.gz`), as opposed to a directory.


May also be set with the `UV_REQUIRE_HASHES` environment variable.     
Validate the Python environment after completing the installation, to detect packages with missing dependencies or other issues     
Install packages into the system Python environment.
By default, uv installs into the virtual environment in the current working directory or any parent directory. The `--system` option instructs uv to instead use the first Python found in the system `PATH`.
WARNING: `--system` is intended for use in continuous integration (CI) environments and should be used with caution, as it can modify the system Python installation.
May also be set with the `UV_SYSTEM_PYTHON` environment variable.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store. 

[`--target`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--target), `-t` _target_ 
    
Install packages into the specified directory, rather than into the virtual or system Python environment. The packages will be installed at the top-level of the directory.
Unlike other install operations, this command does not require discovery of an existing Python environment and only searches for a Python interpreter to use for package resolution. If a suitable Python interpreter cannot be found, uv will install one. To disable this, add `--no-python-downloads`. 

[`--torch-backend`](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--torch-backend) _torch-backend_ 
    
The backend to use when fetching packages in the PyTorch ecosystem (e.g., `cpu`, `cu126`, or `auto`).
When set, uv will ignore the configured index URLs for packages in the PyTorch ecosystem, and will instead use the defined backend.
For example, when set to `cpu`, uv will use the CPU-only PyTorch index; when set to `cu126`, uv will use the PyTorch index for CUDA 12.6.
The `auto` mode will attempt to detect the appropriate PyTorch index based on the currently installed CUDA drivers.
This option is in preview and may change in any future release.
May also be set with the `UV_TORCH_BACKEND` environment variable.
Possible values:
  * `auto`: Select the appropriate PyTorch index based on the operating system and CUDA driver version
  * `cpu`: Use the CPU-only PyTorch index
  * `cu132`: Use the PyTorch index for CUDA 13.2
  * `cu130`: Use the PyTorch index for CUDA 13.0
  * `cu129`: Use the PyTorch index for CUDA 12.9
  * `cu128`: Use the PyTorch index for CUDA 12.8
  * `cu126`: Use the PyTorch index for CUDA 12.6
  * `cu125`: Use the PyTorch index for CUDA 12.5
  * `cu124`: Use the PyTorch index for CUDA 12.4
  * `cu123`: Use the PyTorch index for CUDA 12.3
  * `cu122`: Use the PyTorch index for CUDA 12.2
  * `cu121`: Use the PyTorch index for CUDA 12.1
  * `cu120`: Use the PyTorch index for CUDA 12.0
  * `cu118`: Use the PyTorch index for CUDA 11.8
  * `cu117`: Use the PyTorch index for CUDA 11.7
  * `cu116`: Use the PyTorch index for CUDA 11.6
  * `cu115`: Use the PyTorch index for CUDA 11.5
  * `cu114`: Use the PyTorch index for CUDA 11.4
  * `cu113`: Use the PyTorch index for CUDA 11.3
  * `cu112`: Use the PyTorch index for CUDA 11.2
  * `cu111`: Use the PyTorch index for CUDA 11.1
  * `cu110`: Use the PyTorch index for CUDA 11.0
  * `cu102`: Use the PyTorch index for CUDA 10.2
  * `cu101`: Use the PyTorch index for CUDA 10.1
  * `cu100`: Use the PyTorch index for CUDA 10.0
  * `cu92`: Use the PyTorch index for CUDA 9.2
  * `cu91`: Use the PyTorch index for CUDA 9.1
  * `cu90`: Use the PyTorch index for CUDA 9.0
  * `cu80`: Use the PyTorch index for CUDA 8.0
  * `rocm7.2`: Use the PyTorch index for ROCm 7.2
  * `rocm7.1`: Use the PyTorch index for ROCm 7.1
  * `rocm7.0`: Use the PyTorch index for ROCm 7.0
  * `rocm6.4`: Use the PyTorch index for ROCm 6.4
  * `rocm6.3`: Use the PyTorch index for ROCm 6.3
  * `rocm6.2.4`: Use the PyTorch index for ROCm 6.2.4
  * `rocm6.2`: Use the PyTorch index for ROCm 6.2
  * `rocm6.1`: Use the PyTorch index for ROCm 6.1
  * `rocm6.0`: Use the PyTorch index for ROCm 6.0
  * `rocm5.7`: Use the PyTorch index for ROCm 5.7
  * `rocm5.6`: Use the PyTorch index for ROCm 5.6
  * `rocm5.5`: Use the PyTorch index for ROCm 5.5
  * `rocm5.4.2`: Use the PyTorch index for ROCm 5.4.2
  * `rocm5.4`: Use the PyTorch index for ROCm 5.4
  * `rocm5.3`: Use the PyTorch index for ROCm 5.3
  * `rocm5.2`: Use the PyTorch index for ROCm 5.2
  * `rocm5.1.1`: Use the PyTorch index for ROCm 5.1.1
  * `rocm4.2`: Use the PyTorch index for ROCm 4.2
  * `rocm4.1`: Use the PyTorch index for ROCm 4.1
  * `rocm4.0.1`: Use the PyTorch index for ROCm 4.0.1
  * `xpu`: Use the PyTorch index for Intel XPU

    
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
### [uv pip install](https://docs.astral.sh/uv/reference/cli/#uv-pip-install)
Install packages into an environment
### Usage

```
uv pip install [OPTIONS] <PACKAGE|--requirements <REQUIREMENTS>|--editable <EDITABLE>|--group <GROUP>>

```

### Arguments     
Install all listed packages.
The order of the packages is used to determine priority during resolution.
### Options     
Include all optional dependencies.
Only applies to `pylock.toml`, `pyproject.toml`, `setup.py`, and `setup.cfg` sources. 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--break-system-packages`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--break-system-packages)
    
Allow uv to modify an `EXTERNALLY-MANAGED` Python installation.
WARNING: `--break-system-packages` is intended for use in continuous integration (CI) environments, when installing into Python installations that are managed by an external package manager, like `apt`. It should be used with caution, as such Python installations explicitly recommend against modifications by other package managers (like uv or `pip`).
May also be set with the `UV_BREAK_SYSTEM_PACKAGES` environment variable. 

[`--build-constraints`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--build-constraints), `--build-constraint`, `-b` _build-constraints_ 
    
Constrain build dependencies using the given requirements files when building source distributions.
Constraints files are `requirements.txt`-like files that only control the _version_ of a requirement that's installed. However, including a package in a constraints file will _not_ trigger the installation of that package.
May also be set with the `UV_BUILD_CONSTRAINT` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable.     
Path to a PEM-encoded CA certificate bundle.
If provided, this overrides the default certificate source. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--compile-bytecode`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--compile-bytecode), `--compile` 
    
Compile Python files to bytecode after installation.
By default, uv does not compile Python (`.py`) files to bytecode (`__pycache__/*.pyc`); instead, compilation is performed lazily the first time a module is imported. For use-cases in which start time is critical, such as CLI applications and Docker containers, this option can be enabled to trade longer installation times for faster start times.
When enabled, install operations (e.g., `uv pip install`) will compile installed or reinstalled Python files. Commands that perform a sync operation (e.g., `uv sync` or `uv run`) will process the entire site-packages directory including packages that are not being modified.
May also be set with the `UV_COMPILE_BYTECODE` environment variable. 

[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--config-setting`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--config-setting), `--config-settings`, `-C` _config-setting_ 
    
Settings to pass to the PEP 517 build backend, specified as `KEY=VALUE` pairs 

[`--config-settings-package`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--config-settings-package), `--config-settings-package` _config-settings-package_ 
    
Settings to pass to the PEP 517 build backend for a specific package, specified as `PACKAGE:KEY=VALUE` pairs 

[`--constraints`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--constraints), `--constraint`, `-c` _constraints_ 
    
Constrain versions using the given requirements files.
Constraints files are `requirements.txt`-like files that only control the _version_ of a requirement that's installed. However, including a package in a constraints file will _not_ trigger the installation of that package.
This is equivalent to pip's `--constraint` option.
May also be set with the `UV_CONSTRAINT` environment variable. 

[`--default-index`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--default-index) _default-index_ 
    
The default package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--index` flag.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
May also be set with the `UV_DEFAULT_INDEX` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable.     
Perform a dry run, i.e., don't actually install anything but resolve the dependencies and print the resulting plan 

[`--editable`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--editable), `-e` _editable_ 
    
Install the editable package based on the provided local file path     
Perform an exact sync, removing extraneous packages.
By default, installing will make the minimum necessary changes to satisfy the requirements. When enabled, uv will update the environment to exactly match the requirements, removing packages that are not included in the requirements. 

[`--exclude-newer`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--exclude-newer) _exclude-newer_ 
    
Limit candidate packages to those that were uploaded prior to the given date.
The date is compared against the upload time of each individual distribution artifact (i.e., when each file was uploaded to the package index), not the release date of the package version.
Accepts RFC 3339 timestamps (e.g., `2006-12-02T02:07:43Z`), local dates in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Use `false` to disable `exclude-newer`.
May also be set with the `UV_EXCLUDE_NEWER` environment variable. 

[`--exclude-newer-package`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--exclude-newer-package) _exclude-newer-package_ 
    
Limit candidate packages for specific packages to those that were uploaded prior to the given date.
Accepts package-date pairs in the format `PACKAGE=DATE`, where `DATE` is an RFC 3339 timestamp (e.g., `2006-12-02T02:07:43Z`), a local date in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Can be provided multiple times for different packages. 

[`--excludes`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--excludes), `--exclude` _excludes_ 
    
Exclude packages from resolution using the given requirements files.
Excludes files are `requirements.txt`-like files that specify packages to exclude from the resolution. When a package is excluded, it will be omitted from the dependency list entirely and its own dependencies will be ignored during the resolution phase. Excludes are unconditional in that requirement specifiers and markers are ignored; any package listed in the provided file will be omitted from all resolved environments.
May also be set with the `UV_EXCLUDE` environment variable. 

[`--extra`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--extra) _extra_ 
    
Include optional dependencies from the specified extra name; may be provided more than once.
Only applies to `pylock.toml`, `pyproject.toml`, `setup.py`, and `setup.cfg` sources. 

[`--extra-index-url`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--extra-index-url) _extra-index-url_ 
    
(Deprecated: use `--index` instead) Extra URLs of package indexes to use, in addition to `--index-url`.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--index-url` (which defaults to PyPI). When multiple `--extra-index-url` flags are provided, earlier values take priority.
May also be set with the `UV_EXTRA_INDEX_URL` environment variable. 

[`--find-links`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--find-links), `-f` _find-links_ 
    
Locations to search for candidate distributions, in addition to those found in the registry indexes.
If a path, the target must be a directory that contains packages as wheel files (`.whl`) or source distributions (e.g., `.tar.gz` or `.zip`) at the top level.
If a URL, the page must contain a flat list of links to package files adhering to the formats described above.
May also be set with the `UV_FIND_LINKS` environment variable. 

[`--fork-strategy`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--fork-strategy) _fork-strategy_ 
    
The strategy to use when selecting multiple versions of a given package across Python versions and platforms.
By default, uv will optimize for selecting the latest version of each package for each supported Python version (`requires-python`), while minimizing the number of selected versions across platforms.
Under `fewest`, uv will minimize the number of selected versions for each package, preferring older versions that are compatible with a wider range of supported Python versions or platforms.
May also be set with the `UV_FORK_STRATEGY` environment variable.
Possible values:
  * `fewest`: Optimize for selecting the fewest number of versions for each package. Older versions may be preferred if they are compatible with a wider range of supported Python versions or platforms
  * `requires-python`: Optimize for selecting latest supported version of each package, for each supported Python version



[`--group`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--group) _group_ 
    
Install the specified dependency group from a `pylock.toml` or `pyproject.toml`.
If no path is provided, the `pylock.toml` or `pyproject.toml` in the working directory is used.
May be provided multiple times.     
Display the concise help for this command 

[`--index`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--index) _index_ 
    
The indexes to use when resolving dependencies, in addition to the default index.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--default-index` (which defaults to PyPI). When multiple `--index` flags are provided, earlier values take priority.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
Relative paths can be disambiguated from index names with `./` or `../` on Unix or `.\\`, `..\\`, `./` or `../` on Windows.
May also be set with the `UV_INDEX` environment variable. 

[`--index-strategy`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--index-strategy) _index-strategy_ 
    
The strategy to use when resolving against multiple index URLs.
By default, uv will stop at the first index on which a given package is available, and limit resolutions to those present on that first index (`first-index`). This prevents "dependency confusion" attacks, whereby an attacker can upload a malicious package under the same name to an alternate index.
May also be set with the `UV_INDEX_STRATEGY` environment variable.
Possible values:
  * `first-index`: Only use results from the first index that returns a match for a given package name
  * `unsafe-first-match`: Search for every package name across all indexes, exhausting the versions from the first index before moving on to the next
  * `unsafe-best-match`: Search for every package name across all indexes, preferring the "best" version found. If a package version is in multiple indexes, only look at the entry for the first index



[`--index-url`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--index-url), `-i` _index-url_ 
    
(Deprecated: use `--default-index` instead) The URL of the Python package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--extra-index-url` flag.
May also be set with the `UV_INDEX_URL` environment variable. 

[`--keyring-provider`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--keyring-provider) _keyring-provider_ 
    
Attempt to use `keyring` for authentication for index URLs.
At present, only `--keyring-provider subprocess` is supported, which configures uv to use the `keyring` CLI to handle authentication.
Defaults to `disabled`.
May also be set with the `UV_KEYRING_PROVIDER` environment variable.
Possible values:
  * `disabled`: Do not use keyring for credential lookup
  * `subprocess`: Use the `keyring` command for credential lookup



[`--link-mode`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--link-mode) _link-mode_ 
    
The method to use when installing packages from the global cache.
Defaults to `clone` (also known as Copy-on-Write) on macOS and Linux, and `hardlink` on Windows.
WARNING: The use of symlink link mode is discouraged, as they create tight coupling between the cache and the target environment. For example, clearing the cache (`uv cache clean`) will break all installed packages by way of removing the underlying source files. Use symlinks with caution.
May also be set with the `UV_LINK_MODE` environment variable.
Possible values:
  * `clone`: Clone (i.e., copy-on-write) packages from the source into the destination
  * `copy`: Copy packages from the source into the destination
  * `hardlink`: Hard link packages from the source into the destination
  * `symlink`: Symbolically link packages from the source into the destination

    
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions. 

[`--no-binary`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--no-binary) _no-binary_ 
    
Don't install pre-built wheels.
The given packages will be built and installed from source. The resolver will still use pre-built wheels to extract package metadata, if available.
Multiple packages may be provided. Disable binaries for all packages with `:all:`. Clear previously specified packages with `:none:`. 

[`--no-break-system-packages`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--no-break-system-packages)
    
Don't build source distributions.
When enabled, uv will reuse cached wheels from previously built source distributions, but operations that require building a source distribution will exit with an error. uv may still build editable requirements, and their build backends may run arbitrary Python code.
Alias for `--only-binary :all:`. 

[`--no-build-isolation`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--no-build-isolation)
    
Disable isolation when building source distributions.
Assumes that build dependencies specified by PEP 518 are already installed.
May also be set with the `UV_NO_BUILD_ISOLATION` environment variable. 

[`--no-build-isolation-package`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--no-build-isolation-package) _no-build-isolation-package_ 
    
Disable isolation when building source distributions for a specific package.
Assumes that the packages' build dependencies specified by PEP 518 are already installed. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable.     
Ignore package dependencies, instead only installing those packages explicitly listed on the command line or in the requirements files     
Install any editable dependencies as non-editable [env: UV_NO_EDITABLE=] 

[`--no-editable-package`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--no-editable-package) _no-editable-package_ 
    
Install the specified editable packages as non-editable     
Ignore the registry index (e.g., PyPI), instead relying on direct URL dependencies and those provided via `--find-links` 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--no-python-downloads)
    
Disable automatic downloads of Python.     
Ignore the `tool.uv.sources` table when resolving dependencies. Used to lock against the standards-compliant, publishable package metadata, as opposed to using any workspace, Git, URL, or local path sources
May also be set with the `UV_NO_SOURCES` environment variable. 

[`--no-sources-package`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--no-sources-package) _no-sources-package_ 
    
Don't use sources from the `tool.uv.sources` table for the specified packages [env: `UV_NO_SOURCES_PACKAGE`=] 

[`--no-verify-hashes`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--no-verify-hashes)
    
Disable validation of hashes in the requirements file.
By default, uv will verify any available hashes in the requirements file, but will not require that all requirements have an associated hash. To enforce hash validation, use `--require-hashes`.
May also be set with the `UV_NO_VERIFY_HASHES` environment variable.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--only-binary`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--only-binary) _only-binary_ 
    
Only use pre-built wheels; don't build source distributions.
When enabled, uv will reuse cached wheels from previously built source distributions, but operations that require building a source distribution for the given packages will exit with an error. uv may still build editable requirements, and their build backends may run arbitrary Python code.
Multiple packages may be provided. Disable binaries for all packages with `:all:`. Clear previously specified packages with `:none:`. 

[`--overrides`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--overrides), `--override` _overrides_ 
    
Override versions using the given requirements files.
Overrides files are `requirements.txt`-like files that force a specific version of a requirement to be installed, regardless of the requirements declared by any constituent package, and regardless of whether this would be considered an invalid resolution.
While constraints are _additive_ , in that they're combined with the requirements of the constituent packages, overrides are _absolute_ , in that they completely replace the requirements of the constituent packages.
May also be set with the `UV_OVERRIDE` environment variable. 

[`--prefix`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--prefix) _prefix_ 
    
Install packages into `lib`, `bin`, and other top-level folders under the specified directory, as if a virtual environment were present at that location.
In general, prefer the use of `--python` to install into an alternate environment, as scripts and other artifacts installed via `--prefix` will reference the installing interpreter, rather than any interpreter added to the `--prefix` directory, rendering them non-portable.
Unlike other install operations, this command does not require discovery of an existing Python environment and only searches for a Python interpreter to use for package resolution. If a suitable Python interpreter cannot be found, uv will install one. To disable this, add `--no-python-downloads`. 

[`--prerelease`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--prerelease) _prerelease_ 
    
The strategy to use when considering pre-release versions.
By default, uv will prefer stable candidates, falling back to pre-releases only after every stable candidate that satisfies the active constraints is rejected (`if-necessary`).
May also be set with the `UV_PRERELEASE` environment variable.
Possible values:
  * `disallow`: Disallow all pre-release versions
  * `allow`: Allow all pre-release versions
  * `if-necessary`: Prefer stable versions, falling back to pre-release versions when necessary
  * `explicit`: Prefer stable versions for first-party packages with explicit pre-release specifiers, falling back to pre-release versions when necessary. Disallow pre-release versions for all other packages
  * `if-necessary-or-explicit`: Deprecated alias for `if-necessary`



[`--prerelease-package`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--prerelease-package) _prerelease-package_ 
    
The strategy to use when considering pre-release versions for a specific package.
Accepts package-mode pairs in the format `PACKAGE=MODE`, where `MODE` is any value accepted by `--prerelease`.
May be provided multiple times for different packages. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable. 

[`--python`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--python), `-p` _python_ 
    
The Python interpreter into which packages should be installed.
By default, installation requires a virtual environment. A path to an alternative Python can be provided, but it is only recommended in continuous integration (CI) environments and should be used with caution, as it can modify the system Python installation.
See [uv python](https://docs.astral.sh/uv/reference/cli/#uv-python) for details on Python discovery and supported request formats.
May also be set with the `UV_PYTHON` environment variable. 

[`--python-platform`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--python-platform) _python-platform_ 
    
The platform for which requirements should be installed.
Represented as a "target triple", a string that describes the target platform in terms of its CPU, vendor, and operating system name, like `x86_64-unknown-linux-gnu` or `aarch64-apple-darwin`.
When targeting macOS (Darwin), the default minimum version is `13.0`. Use `MACOSX_DEPLOYMENT_TARGET` to specify a different minimum version, e.g., `14.0`.
When targeting iOS, the default minimum version is `13.0`. Use `IPHONEOS_DEPLOYMENT_TARGET` to specify a different minimum version, e.g., `14.0`.
When targeting Android, the default minimum Android API level is `24`. Use `ANDROID_API_LEVEL` to specify a different minimum version, e.g., `26`.
WARNING: When specified, uv will select wheels that are compatible with the _target_ platform; as a result, the installed distributions may not be compatible with the _current_ platform. Conversely, any distributions that are built from source may be incompatible with the _target_ platform, as they will be built for the _current_ platform. The `--python-platform` option is intended for advanced use cases.
Possible values:
  * `windows`: An alias for `x86_64-pc-windows-msvc`, the default target for Windows
  * `linux`: An alias for `x86_64-unknown-linux-gnu`, the default target for Linux
  * `macos`: An alias for `aarch64-apple-darwin`, the default target for macOS
  * `x86_64-pc-windows-msvc`: A 64-bit x86 Windows target
  * `aarch64-pc-windows-msvc`: An ARM64 Windows target
  * `i686-pc-windows-msvc`: A 32-bit x86 Windows target
  * `x86_64-unknown-linux-gnu`: An x86 Linux target. Equivalent to `x86_64-manylinux_2_28`
  * `aarch64-apple-darwin`: An ARM-based macOS target, as seen on Apple Silicon devices
  * `x86_64-apple-darwin`: An x86 macOS target
  * `aarch64-unknown-linux-gnu`: An ARM64 Linux target. Equivalent to `aarch64-manylinux_2_28`
  * `aarch64-unknown-linux-musl`: An ARM64 Linux target
  * `x86_64-unknown-linux-musl`: An `x86_64` Linux target
  * `riscv64-unknown-linux`: A RISCV64 Linux target
  * `x86_64-manylinux2014`: An `x86_64` target for the `manylinux2014` platform. Equivalent to `x86_64-manylinux_2_17`
  * `x86_64-manylinux_2_17`: An `x86_64` target for the `manylinux_2_17` platform
  * `x86_64-manylinux_2_28`: An `x86_64` target for the `manylinux_2_28` platform
  * `x86_64-manylinux_2_31`: An `x86_64` target for the `manylinux_2_31` platform
  * `x86_64-manylinux_2_32`: An `x86_64` target for the `manylinux_2_32` platform
  * `x86_64-manylinux_2_33`: An `x86_64` target for the `manylinux_2_33` platform
  * `x86_64-manylinux_2_34`: An `x86_64` target for the `manylinux_2_34` platform
  * `x86_64-manylinux_2_35`: An `x86_64` target for the `manylinux_2_35` platform
  * `x86_64-manylinux_2_36`: An `x86_64` target for the `manylinux_2_36` platform
  * `x86_64-manylinux_2_37`: An `x86_64` target for the `manylinux_2_37` platform
  * `x86_64-manylinux_2_38`: An `x86_64` target for the `manylinux_2_38` platform
  * `x86_64-manylinux_2_39`: An `x86_64` target for the `manylinux_2_39` platform
  * `x86_64-manylinux_2_40`: An `x86_64` target for the `manylinux_2_40` platform
  * `aarch64-manylinux2014`: An ARM64 target for the `manylinux2014` platform. Equivalent to `aarch64-manylinux_2_17`
  * `aarch64-manylinux_2_17`: An ARM64 target for the `manylinux_2_17` platform
  * `aarch64-manylinux_2_28`: An ARM64 target for the `manylinux_2_28` platform
  * `aarch64-manylinux_2_31`: An ARM64 target for the `manylinux_2_31` platform
  * `aarch64-manylinux_2_32`: An ARM64 target for the `manylinux_2_32` platform
  * `aarch64-manylinux_2_33`: An ARM64 target for the `manylinux_2_33` platform
  * `aarch64-manylinux_2_34`: An ARM64 target for the `manylinux_2_34` platform
  * `aarch64-manylinux_2_35`: An ARM64 target for the `manylinux_2_35` platform
  * `aarch64-manylinux_2_36`: An ARM64 target for the `manylinux_2_36` platform
  * `aarch64-manylinux_2_37`: An ARM64 target for the `manylinux_2_37` platform
  * `aarch64-manylinux_2_38`: An ARM64 target for the `manylinux_2_38` platform
  * `aarch64-manylinux_2_39`: An ARM64 target for the `manylinux_2_39` platform
  * `aarch64-manylinux_2_40`: An ARM64 target for the `manylinux_2_40` platform
  * `aarch64-linux-android`: An ARM64 Android target
  * `x86_64-linux-android`: An `x86_64` Android target
  * `wasm32-pyodide2024`: A wasm32 target using the Pyodide 2024 platform. Meant for use with Python 3.12. See <https://pyodide.org/en/stable/development/abi/312.html>
  * `wasm32-pyodide2025`: A wasm32 target using the Pyodide 2025 platform. Meant for use with Python 3.13. See <https://pyodide.org/en/stable/development/abi/313.html>
  * `arm64-apple-ios`: An ARM64 target for iOS device
  * `arm64-apple-ios-simulator`: An ARM64 target for iOS simulator
  * `x86_64-apple-ios-simulator`: An `x86_64` target for iOS simulator



[`--python-version`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--python-version) _python-version_ 
    
The minimum Python version that should be supported by the requirements (e.g., `3.7` or `3.7.9`).
If a patch version is omitted, the minimum patch version is assumed. For example, `3.7` is mapped to `3.7.0`.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Refresh all cached data 

[`--refresh-package`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--refresh-package) _refresh-package_ 
    
Refresh cached data for a specific package 

[`--reinstall`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--reinstall), `--force-reinstall` 
    
Reinstall all packages, regardless of whether they're already installed. Implies `--refresh` 

[`--reinstall-package`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--reinstall-package) _reinstall-package_ 
    
Reinstall a specific package, regardless of whether it's already installed. Implies `--refresh-package`     
Require a matching hash for each requirement.
By default, uv will verify any available hashes in the requirements file, but will not require that all requirements have an associated hash.
When `--require-hashes` is enabled, _all_ requirements must include a hash or set of hashes, and _all_ requirements must either be pinned to exact versions (e.g., `==1.0.0`), or be specified via direct URL.
Hash-checking mode introduces a number of additional constraints:
  * Git dependencies are not supported. - Editable installations are not supported. - Local dependencies are not supported, unless they point to a specific wheel (`.whl`) or source archive (`.zip`, `.tar.gz`), as opposed to a directory.


May also be set with the `UV_REQUIRE_HASHES` environment variable. 

[`--requirements`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--requirements), `--requirement`, `-r` _requirements_ 
    
Install the packages listed in the given files.
The following formats are supported: `requirements.txt`, `.py` files with inline metadata, `pylock.toml`, `pyproject.toml`, `setup.py`, and `setup.cfg`.
If a `pyproject.toml`, `setup.py`, or `setup.cfg` file is provided, uv will extract the requirements for the relevant project.
If `-` is provided, then requirements will be read from stdin. 

[`--resolution`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--resolution) _resolution_ 
    
The strategy to use when selecting between the different compatible versions for a given package requirement.
By default, uv will use the latest compatible version of each package (`highest`).
May also be set with the `UV_RESOLUTION` environment variable.
Possible values:
  * `highest`: Resolve the highest compatible version of each package
  * `lowest`: Resolve the lowest compatible version of each package
  * `lowest-direct`: Resolve the lowest compatible version of any direct dependencies, and the highest compatible version of any transitive dependencies

    
Validate the Python environment after completing the installation, to detect packages with missing dependencies or other issues     
Install packages into the system Python environment.
By default, uv installs into the virtual environment in the current working directory or any parent directory. The `--system` option instructs uv to instead use the first Python found in the system `PATH`.
WARNING: `--system` is intended for use in continuous integration (CI) environments and should be used with caution, as it can modify the system Python installation.
May also be set with the `UV_SYSTEM_PYTHON` environment variable.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store. 

[`--target`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--target), `-t` _target_ 
    
Install packages into the specified directory, rather than into the virtual or system Python environment. The packages will be installed at the top-level of the directory.
Unlike other install operations, this command does not require discovery of an existing Python environment and only searches for a Python interpreter to use for package resolution. If a suitable Python interpreter cannot be found, uv will install one. To disable this, add `--no-python-downloads`. 

[`--torch-backend`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--torch-backend) _torch-backend_ 
    
The backend to use when fetching packages in the PyTorch ecosystem (e.g., `cpu`, `cu126`, or `auto`)
When set, uv will ignore the configured index URLs for packages in the PyTorch ecosystem, and will instead use the defined backend.
For example, when set to `cpu`, uv will use the CPU-only PyTorch index; when set to `cu126`, uv will use the PyTorch index for CUDA 12.6.
The `auto` mode will attempt to detect the appropriate PyTorch index based on the currently installed CUDA drivers.
This option is in preview and may change in any future release.
May also be set with the `UV_TORCH_BACKEND` environment variable.
Possible values:
  * `auto`: Select the appropriate PyTorch index based on the operating system and CUDA driver version
  * `cpu`: Use the CPU-only PyTorch index
  * `cu132`: Use the PyTorch index for CUDA 13.2
  * `cu130`: Use the PyTorch index for CUDA 13.0
  * `cu129`: Use the PyTorch index for CUDA 12.9
  * `cu128`: Use the PyTorch index for CUDA 12.8
  * `cu126`: Use the PyTorch index for CUDA 12.6
  * `cu125`: Use the PyTorch index for CUDA 12.5
  * `cu124`: Use the PyTorch index for CUDA 12.4
  * `cu123`: Use the PyTorch index for CUDA 12.3
  * `cu122`: Use the PyTorch index for CUDA 12.2
  * `cu121`: Use the PyTorch index for CUDA 12.1
  * `cu120`: Use the PyTorch index for CUDA 12.0
  * `cu118`: Use the PyTorch index for CUDA 11.8
  * `cu117`: Use the PyTorch index for CUDA 11.7
  * `cu116`: Use the PyTorch index for CUDA 11.6
  * `cu115`: Use the PyTorch index for CUDA 11.5
  * `cu114`: Use the PyTorch index for CUDA 11.4
  * `cu113`: Use the PyTorch index for CUDA 11.3
  * `cu112`: Use the PyTorch index for CUDA 11.2
  * `cu111`: Use the PyTorch index for CUDA 11.1
  * `cu110`: Use the PyTorch index for CUDA 11.0
  * `cu102`: Use the PyTorch index for CUDA 10.2
  * `cu101`: Use the PyTorch index for CUDA 10.1
  * `cu100`: Use the PyTorch index for CUDA 10.0
  * `cu92`: Use the PyTorch index for CUDA 9.2
  * `cu91`: Use the PyTorch index for CUDA 9.1
  * `cu90`: Use the PyTorch index for CUDA 9.0
  * `cu80`: Use the PyTorch index for CUDA 8.0
  * `rocm7.2`: Use the PyTorch index for ROCm 7.2
  * `rocm7.1`: Use the PyTorch index for ROCm 7.1
  * `rocm7.0`: Use the PyTorch index for ROCm 7.0
  * `rocm6.4`: Use the PyTorch index for ROCm 6.4
  * `rocm6.3`: Use the PyTorch index for ROCm 6.3
  * `rocm6.2.4`: Use the PyTorch index for ROCm 6.2.4
  * `rocm6.2`: Use the PyTorch index for ROCm 6.2
  * `rocm6.1`: Use the PyTorch index for ROCm 6.1
  * `rocm6.0`: Use the PyTorch index for ROCm 6.0
  * `rocm5.7`: Use the PyTorch index for ROCm 5.7
  * `rocm5.6`: Use the PyTorch index for ROCm 5.6
  * `rocm5.5`: Use the PyTorch index for ROCm 5.5
  * `rocm5.4.2`: Use the PyTorch index for ROCm 5.4.2
  * `rocm5.4`: Use the PyTorch index for ROCm 5.4
  * `rocm5.3`: Use the PyTorch index for ROCm 5.3
  * `rocm5.2`: Use the PyTorch index for ROCm 5.2
  * `rocm5.1.1`: Use the PyTorch index for ROCm 5.1.1
  * `rocm4.2`: Use the PyTorch index for ROCm 4.2
  * `rocm4.1`: Use the PyTorch index for ROCm 4.1
  * `rocm4.0.1`: Use the PyTorch index for ROCm 4.0.1
  * `xpu`: Use the PyTorch index for Intel XPU

    
Allow package upgrades, ignoring pinned versions in any existing output file. Implies `--refresh` 

[`--upgrade-group`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--upgrade-group) _upgrade-group_ 
    
Allow upgrades for all packages in a dependency group, ignoring pinned versions in any existing output file 

[`--upgrade-package`](https://docs.astral.sh/uv/reference/cli/#uv-pip-install--upgrade-package), `-P` _upgrade-package_ 
    
Allow upgrades for a specific package, ignoring pinned versions in any existing output file. Implies `--refresh-package`     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
### [uv pip uninstall](https://docs.astral.sh/uv/reference/cli/#uv-pip-uninstall)
Uninstall packages from an environment
### Usage

```
uv pip uninstall [OPTIONS] <PACKAGE|--requirements <REQUIREMENTS>>

```

### Arguments     
Uninstall all listed packages
### Options 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-pip-uninstall--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--break-system-packages`](https://docs.astral.sh/uv/reference/cli/#uv-pip-uninstall--break-system-packages)
    
Allow uv to modify an `EXTERNALLY-MANAGED` Python installation.
WARNING: `--break-system-packages` is intended for use in continuous integration (CI) environments, when installing into Python installations that are managed by an external package manager, like `apt`. It should be used with caution, as such Python installations explicitly recommend against modifications by other package managers (like uv or `pip`).
May also be set with the `UV_BREAK_SYSTEM_PACKAGES` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-pip-uninstall--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable.     
Path to a PEM-encoded CA certificate bundle.
If provided, this overrides the default certificate source. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-pip-uninstall--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-pip-uninstall--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-pip-uninstall--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable.     
Perform a dry run, i.e., don't actually uninstall anything but print the resulting plan     
Display the concise help for this command 

[`--keyring-provider`](https://docs.astral.sh/uv/reference/cli/#uv-pip-uninstall--keyring-provider) _keyring-provider_ 
    
Attempt to use `keyring` for authentication for remote requirements files.
At present, only `--keyring-provider subprocess` is supported, which configures uv to use the `keyring` CLI to handle authentication.
Defaults to `disabled`.
May also be set with the `UV_KEYRING_PROVIDER` environment variable.
Possible values:
  * `disabled`: Do not use keyring for credential lookup
  * `subprocess`: Use the `keyring` command for credential lookup

    
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions. 

[`--no-break-system-packages`](https://docs.astral.sh/uv/reference/cli/#uv-pip-uninstall--no-break-system-packages)


[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-pip-uninstall--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable. 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-pip-uninstall--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-pip-uninstall--no-python-downloads)
    
Disable automatic downloads of Python.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--prefix`](https://docs.astral.sh/uv/reference/cli/#uv-pip-uninstall--prefix) _prefix_ 
    
Uninstall packages from the specified `--prefix` directory 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-pip-uninstall--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable. 

[`--python`](https://docs.astral.sh/uv/reference/cli/#uv-pip-uninstall--python), `-p` _python_ 
    
The Python interpreter from which packages should be uninstalled.
By default, uninstallation requires a virtual environment. A path to an alternative Python can be provided, but it is only recommended in continuous integration (CI) environments and should be used with caution, as it can modify the system Python installation.
See [uv python](https://docs.astral.sh/uv/reference/cli/#uv-python) for details on Python discovery and supported request formats.
May also be set with the `UV_PYTHON` environment variable.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout. 

[`--requirements`](https://docs.astral.sh/uv/reference/cli/#uv-pip-uninstall--requirements), `--requirement`, `-r` _requirements_ 
    
Uninstall the packages listed in the given files.
The following formats are supported: `requirements.txt`, `.py` files with inline metadata, `pylock.toml`, `pyproject.toml`, `setup.py`, and `setup.cfg`.     
Use the system Python to uninstall packages.
By default, uv uninstalls from the virtual environment in the current working directory or any parent directory. The `--system` option instructs uv to instead use the first Python found in the system `PATH`.
WARNING: `--system` is intended for use in continuous integration (CI) environments and should be used with caution, as it can modify the system Python installation.
May also be set with the `UV_SYSTEM_PYTHON` environment variable.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store. 

[`--target`](https://docs.astral.sh/uv/reference/cli/#uv-pip-uninstall--target), `-t` _target_ 
    
Uninstall packages from the specified `--target` directory     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
### [uv pip freeze](https://docs.astral.sh/uv/reference/cli/#uv-pip-freeze)
List, in requirements format, packages installed in an environment
### Usage

```
uv pip freeze [OPTIONS]

```

### Options 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-pip-freeze--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-pip-freeze--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable.     
Path to a PEM-encoded CA certificate bundle.
If provided, this overrides the default certificate source. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-pip-freeze--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-pip-freeze--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-pip-freeze--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable. 

[`--exclude`](https://docs.astral.sh/uv/reference/cli/#uv-pip-freeze--exclude) _exclude_ 
    
Exclude the specified package(s) from the output 

[`--exclude-editable`](https://docs.astral.sh/uv/reference/cli/#uv-pip-freeze--exclude-editable)
    
Exclude any editable packages from output     
Display the concise help for this command     
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-pip-freeze--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable. 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-pip-freeze--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-pip-freeze--no-python-downloads)
    
Disable automatic downloads of Python.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--path`](https://docs.astral.sh/uv/reference/cli/#uv-pip-freeze--path) _paths_ 
    
Restrict to the specified installation path for listing packages (can be used multiple times) 

[`--prefix`](https://docs.astral.sh/uv/reference/cli/#uv-pip-freeze--prefix) _prefix_ 
    
List packages from the specified `--prefix` directory 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-pip-freeze--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable. 

[`--python`](https://docs.astral.sh/uv/reference/cli/#uv-pip-freeze--python), `-p` _python_ 
    
The Python interpreter for which packages should be listed.
By default, uv lists packages in a virtual environment but will show packages in a system Python environment if no virtual environment is found.
See [uv python](https://docs.astral.sh/uv/reference/cli/#uv-python) for details on Python discovery and supported request formats.
May also be set with the `UV_PYTHON` environment variable.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Validate the Python environment, to detect packages with missing dependencies and other issues     
List packages in the system Python environment.
Disables discovery of virtual environments.
See [uv python](https://docs.astral.sh/uv/reference/cli/#uv-python) for details on Python discovery.
May also be set with the `UV_SYSTEM_PYTHON` environment variable.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store. 

[`--target`](https://docs.astral.sh/uv/reference/cli/#uv-pip-freeze--target), `-t` _target_ 
    
List packages from the specified `--target` directory     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
### [uv pip list](https://docs.astral.sh/uv/reference/cli/#uv-pip-list)
List, in tabular format, packages installed in an environment
### Usage

```
uv pip list [OPTIONS]

```

### Options 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-pip-list--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-pip-list--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--cert`](https://docs.astral.sh/uv/reference/cli/#uv-pip-list--cert) _file_ 
    
Path to a PEM-encoded CA certificate bundle.
If provided, this overrides the default certificate source. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-pip-list--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-pip-list--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--default-index`](https://docs.astral.sh/uv/reference/cli/#uv-pip-list--default-index) _default-index_ 
    
The default package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--index` flag.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
May also be set with the `UV_DEFAULT_INDEX` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-pip-list--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable.     
Only include editable projects 

[`--exclude`](https://docs.astral.sh/uv/reference/cli/#uv-pip-list--exclude) _exclude_ 
    
Exclude the specified package(s) from the output 

[`--exclude-editable`](https://docs.astral.sh/uv/reference/cli/#uv-pip-list--exclude-editable)
    
Exclude any editable packages from output 

[`--exclude-newer`](https://docs.astral.sh/uv/reference/cli/#uv-pip-list--exclude-newer) _exclude-newer_ 
    
Limit candidate packages to those that were uploaded prior to the given date.
The date is compared against the upload time of each individual distribution artifact (i.e., when each file was uploaded to the package index), not the release date of the package version.
Accepts RFC 3339 timestamps (e.g., `2006-12-02T02:07:43Z`), local dates in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Use `false` to disable `exclude-newer`.
May also be set with the `UV_EXCLUDE_NEWER` environment variable. 

[`--exclude-newer-package`](https://docs.astral.sh/uv/reference/cli/#uv-pip-list--exclude-newer-package) _exclude-newer-package_ 
    
Limit candidate packages for specific packages to those that were uploaded prior to the given date.
Accepts package-date pairs in the format `PACKAGE=DATE`, where `DATE` is an RFC 3339 timestamp (e.g., `2006-12-02T02:07:43Z`), a local date in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Can be provided multiple times for different packages. 

[`--extra-index-url`](https://docs.astral.sh/uv/reference/cli/#uv-pip-list--extra-index-url) _extra-index-url_ 
    
(Deprecated: use `--index` instead) Extra URLs of package indexes to use, in addition to `--index-url`.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--index-url` (which defaults to PyPI). When multiple `--extra-index-url` flags are provided, earlier values take priority.
May also be set with the `UV_EXTRA_INDEX_URL` environment variable. 

[`--find-links`](https://docs.astral.sh/uv/reference/cli/#uv-pip-list--find-links), `-f` _find-links_ 
    
Locations to search for candidate distributions, in addition to those found in the registry indexes.
If a path, the target must be a directory that contains packages as wheel files (`.whl`) or source distributions (e.g., `.tar.gz` or `.zip`) at the top level.
If a URL, the page must contain a flat list of links to package files adhering to the formats described above.
May also be set with the `UV_FIND_LINKS` environment variable. 

[`--format`](https://docs.astral.sh/uv/reference/cli/#uv-pip-list--format) _format_ 
    
Select the output format
[default: columns]
Possible values:
  * `columns`: Display the list of packages in a human-readable table
  * `freeze`: Display the list of packages in a `pip freeze`-like format, with one package per line alongside its version
  * `json`: Display the list of packages in a machine-readable JSON format

    
Display the concise help for this command 

[`--index`](https://docs.astral.sh/uv/reference/cli/#uv-pip-list--index) _index_ 
    
The indexes to use when resolving dependencies, in addition to the default index.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--default-index` (which defaults to PyPI). When multiple `--index` flags are provided, earlier values take priority.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
Relative paths can be disambiguated from index names with `./` or `../` on Unix or `.\\`, `..\\`, `./` or `../` on Windows.
May also be set with the `UV_INDEX` environment variable. 

[`--index-strategy`](https://docs.astral.sh/uv/reference/cli/#uv-pip-list--index-strategy) _index-strategy_ 
    
The strategy to use when resolving against multiple index URLs.
By default, uv will stop at the first index on which a given package is available, and limit resolutions to those present on that first index (`first-index`). This prevents "dependency confusion" attacks, whereby an attacker can upload a malicious package under the same name to an alternate index.
May also be set with the `UV_INDEX_STRATEGY` environment variable.
Possible values:
  * `first-index`: Only use results from the first index that returns a match for a given package name
  * `unsafe-first-match`: Search for every package name across all indexes, exhausting the versions from the first index before moving on to the next
  * `unsafe-best-match`: Search for every package name across all indexes, preferring the "best" version found. If a package version is in multiple indexes, only look at the entry for the first index



[`--index-url`](https://docs.astral.sh/uv/reference/cli/#uv-pip-list--index-url), `-i` _index-url_ 
    
(Deprecated: use `--default-index` instead) The URL of the Python package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--extra-index-url` flag.
May also be set with the `UV_INDEX_URL` environment variable. 

[`--keyring-provider`](https://docs.astral.sh/uv/reference/cli/#uv-pip-list--keyring-provider) _keyring-provider_ 
    
Attempt to use `keyring` for authentication for index URLs.
At present, only `--keyring-provider subprocess` is supported, which configures uv to use the `keyring` CLI to handle authentication.
Defaults to `disabled`.
May also be set with the `UV_KEYRING_PROVIDER` environment variable.
Possible values:
  * `disabled`: Do not use keyring for credential lookup
  * `subprocess`: Use the `keyring` command for credential lookup

    
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-pip-list--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable.     
Ignore the registry index (e.g., PyPI), instead relying on direct URL dependencies and those provided via `--find-links` 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-pip-list--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-pip-list--no-python-downloads)
    
Disable automatic downloads of Python.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files.     
List outdated packages.
The latest version of each package will be shown alongside the installed version. Up-to-date packages will be omitted from the output. 

[`--prefix`](https://docs.astral.sh/uv/reference/cli/#uv-pip-list--prefix) _prefix_ 
    
List packages from the specified `--prefix` directory 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-pip-list--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable. 

[`--python`](https://docs.astral.sh/uv/reference/cli/#uv-pip-list--python), `-p` _python_ 
    
The Python interpreter for which packages should be listed.
By default, uv lists packages in a virtual environment but will show packages in a system Python environment if no virtual environment is found.
See [uv python](https://docs.astral.sh/uv/reference/cli/#uv-python) for details on Python discovery and supported request formats.
May also be set with the `UV_PYTHON` environment variable.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Validate the Python environment, to detect packages with missing dependencies and other issues     
List packages in the system Python environment.
Disables discovery of virtual environments.
See [uv python](https://docs.astral.sh/uv/reference/cli/#uv-python) for details on Python discovery.
May also be set with the `UV_SYSTEM_PYTHON` environment variable.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store. 

[`--target`](https://docs.astral.sh/uv/reference/cli/#uv-pip-list--target), `-t` _target_ 
    
List packages from the specified `--target` directory     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
### [uv pip show](https://docs.astral.sh/uv/reference/cli/#uv-pip-show)
Show information about one or more installed packages
### Usage

```
uv pip show [OPTIONS] [PACKAGE]...

```

### Arguments     
The package(s) to display
### Options 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-pip-show--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-pip-show--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--cert`](https://docs.astral.sh/uv/reference/cli/#uv-pip-show--cert) _file_ 
    
Path to a PEM-encoded CA certificate bundle.
If provided, this overrides the default certificate source. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-pip-show--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-pip-show--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-pip-show--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable.     
Show the full list of installed files for each package     
Display the concise help for this command     
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-pip-show--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable. 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-pip-show--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-pip-show--no-python-downloads)
    
Disable automatic downloads of Python.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--prefix`](https://docs.astral.sh/uv/reference/cli/#uv-pip-show--prefix) _prefix_ 
    
Show a package from the specified `--prefix` directory 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-pip-show--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable. 

[`--python`](https://docs.astral.sh/uv/reference/cli/#uv-pip-show--python), `-p` _python_ 
    
The Python interpreter to find the package in.
By default, uv looks for packages in a virtual environment but will look for packages in a system Python environment if no virtual environment is found.
See [uv python](https://docs.astral.sh/uv/reference/cli/#uv-python) for details on Python discovery and supported request formats.
May also be set with the `UV_PYTHON` environment variable.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Validate the Python environment, to detect packages with missing dependencies and other issues     
Show a package in the system Python environment.
Disables discovery of virtual environments.
See [uv python](https://docs.astral.sh/uv/reference/cli/#uv-python) for details on Python discovery.
May also be set with the `UV_SYSTEM_PYTHON` environment variable.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store. 

[`--target`](https://docs.astral.sh/uv/reference/cli/#uv-pip-show--target), `-t` _target_ 
    
Show a package from the specified `--target` directory     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
### [uv pip tree](https://docs.astral.sh/uv/reference/cli/#uv-pip-tree)
Display the dependency tree for an environment
### Usage

```
uv pip tree [OPTIONS]

```

### Options 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-pip-tree--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-pip-tree--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--cert`](https://docs.astral.sh/uv/reference/cli/#uv-pip-tree--cert) _file_ 
    
Path to a PEM-encoded CA certificate bundle.
If provided, this overrides the default certificate source. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-pip-tree--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-pip-tree--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--default-index`](https://docs.astral.sh/uv/reference/cli/#uv-pip-tree--default-index) _default-index_ 
    
The default package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--index` flag.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
May also be set with the `UV_DEFAULT_INDEX` environment variable. 

[`--depth`](https://docs.astral.sh/uv/reference/cli/#uv-pip-tree--depth), `-d` _depth_ 
    
Maximum display depth of the dependency tree
[default: 255] 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-pip-tree--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable. 

[`--exclude-newer`](https://docs.astral.sh/uv/reference/cli/#uv-pip-tree--exclude-newer) _exclude-newer_ 
    
Limit candidate packages to those that were uploaded prior to the given date.
The date is compared against the upload time of each individual distribution artifact (i.e., when each file was uploaded to the package index), not the release date of the package version.
Accepts RFC 3339 timestamps (e.g., `2006-12-02T02:07:43Z`), local dates in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Use `false` to disable `exclude-newer`.
May also be set with the `UV_EXCLUDE_NEWER` environment variable. 

[`--exclude-newer-package`](https://docs.astral.sh/uv/reference/cli/#uv-pip-tree--exclude-newer-package) _exclude-newer-package_ 
    
Limit candidate packages for specific packages to those that were uploaded prior to the given date.
Accepts package-date pairs in the format `PACKAGE=DATE`, where `DATE` is an RFC 3339 timestamp (e.g., `2006-12-02T02:07:43Z`), a local date in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Can be provided multiple times for different packages. 

[`--extra-index-url`](https://docs.astral.sh/uv/reference/cli/#uv-pip-tree--extra-index-url) _extra-index-url_ 
    
(Deprecated: use `--index` instead) Extra URLs of package indexes to use, in addition to `--index-url`.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--index-url` (which defaults to PyPI). When multiple `--extra-index-url` flags are provided, earlier values take priority.
May also be set with the `UV_EXTRA_INDEX_URL` environment variable. 

[`--find-links`](https://docs.astral.sh/uv/reference/cli/#uv-pip-tree--find-links), `-f` _find-links_ 
    
Locations to search for candidate distributions, in addition to those found in the registry indexes.
If a path, the target must be a directory that contains packages as wheel files (`.whl`) or source distributions (e.g., `.tar.gz` or `.zip`) at the top level.
If a URL, the page must contain a flat list of links to package files adhering to the formats described above.
May also be set with the `UV_FIND_LINKS` environment variable.     
Display the concise help for this command 

[`--index`](https://docs.astral.sh/uv/reference/cli/#uv-pip-tree--index) _index_ 
    
The indexes to use when resolving dependencies, in addition to the default index.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--default-index` (which defaults to PyPI). When multiple `--index` flags are provided, earlier values take priority.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
Relative paths can be disambiguated from index names with `./` or `../` on Unix or `.\\`, `..\\`, `./` or `../` on Windows.
May also be set with the `UV_INDEX` environment variable. 

[`--index-strategy`](https://docs.astral.sh/uv/reference/cli/#uv-pip-tree--index-strategy) _index-strategy_ 
    
The strategy to use when resolving against multiple index URLs.
By default, uv will stop at the first index on which a given package is available, and limit resolutions to those present on that first index (`first-index`). This prevents "dependency confusion" attacks, whereby an attacker can upload a malicious package under the same name to an alternate index.
May also be set with the `UV_INDEX_STRATEGY` environment variable.
Possible values:
  * `first-index`: Only use results from the first index that returns a match for a given package name
  * `unsafe-first-match`: Search for every package name across all indexes, exhausting the versions from the first index before moving on to the next
  * `unsafe-best-match`: Search for every package name across all indexes, preferring the "best" version found. If a package version is in multiple indexes, only look at the entry for the first index



[`--index-url`](https://docs.astral.sh/uv/reference/cli/#uv-pip-tree--index-url), `-i` _index-url_ 
    
(Deprecated: use `--default-index` instead) The URL of the Python package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--extra-index-url` flag.
May also be set with the `UV_INDEX_URL` environment variable. 

[`--invert`](https://docs.astral.sh/uv/reference/cli/#uv-pip-tree--invert), `--reverse` 
    
Show the reverse dependencies for the given package. This flag will invert the tree and display the packages that depend on the given package 

[`--keyring-provider`](https://docs.astral.sh/uv/reference/cli/#uv-pip-tree--keyring-provider) _keyring-provider_ 
    
Attempt to use `keyring` for authentication for index URLs.
At present, only `--keyring-provider subprocess` is supported, which configures uv to use the `keyring` CLI to handle authentication.
Defaults to `disabled`.
May also be set with the `UV_KEYRING_PROVIDER` environment variable.
Possible values:
  * `disabled`: Do not use keyring for credential lookup
  * `subprocess`: Use the `keyring` command for credential lookup

    
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-pip-tree--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable.     
Do not de-duplicate repeated dependencies. Usually, when a package has already displayed its dependencies, further occurrences will not re-display its dependencies, and will include a (*) to indicate it has already been shown. This flag will cause those duplicates to be repeated     
Ignore the registry index (e.g., PyPI), instead relying on direct URL dependencies and those provided via `--find-links` 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-pip-tree--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-pip-tree--no-python-downloads)
    
Disable automatic downloads of Python.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files.     
Show the latest available version of each package in the tree 

[`--package`](https://docs.astral.sh/uv/reference/cli/#uv-pip-tree--package) _package_ 
    
Display only the specified packages 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-pip-tree--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable. 

[`--prune`](https://docs.astral.sh/uv/reference/cli/#uv-pip-tree--prune) _prune_ 
    
Prune the given package from the display of the dependency tree 

[`--python`](https://docs.astral.sh/uv/reference/cli/#uv-pip-tree--python), `-p` _python_ 
    
The Python interpreter for which packages should be listed.
By default, uv lists packages in a virtual environment but will show packages in a system Python environment if no virtual environment is found.
See [uv python](https://docs.astral.sh/uv/reference/cli/#uv-python) for details on Python discovery and supported request formats.
May also be set with the `UV_PYTHON` environment variable.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Show compressed wheel sizes for packages in the tree 

[`--show-version-specifiers`](https://docs.astral.sh/uv/reference/cli/#uv-pip-tree--show-version-specifiers)
    
Show the version constraint(s) imposed on each package     
Validate the Python environment, to detect packages with missing dependencies and other issues     
List packages in the system Python environment.
Disables discovery of virtual environments.
See [uv python](https://docs.astral.sh/uv/reference/cli/#uv-python) for details on Python discovery.
May also be set with the `UV_SYSTEM_PYTHON` environment variable.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store.     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
### [uv pip check](https://docs.astral.sh/uv/reference/cli/#uv-pip-check)
Verify installed packages have compatible dependencies
### Usage

```
uv pip check [OPTIONS]

```

### Options 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-pip-check--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-pip-check--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable.     
Path to a PEM-encoded CA certificate bundle.
If provided, this overrides the default certificate source. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-pip-check--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-pip-check--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-pip-check--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable.     
Display the concise help for this command     
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-pip-check--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable. 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-pip-check--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-pip-check--no-python-downloads)
    
Disable automatic downloads of Python.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-pip-check--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable. 

[`--python`](https://docs.astral.sh/uv/reference/cli/#uv-pip-check--python), `-p` _python_ 
    
The Python interpreter for which packages should be checked.
By default, uv checks packages in a virtual environment but will check packages in a system Python environment if no virtual environment is found.
See [uv python](https://docs.astral.sh/uv/reference/cli/#uv-python) for details on Python discovery and supported request formats.
May also be set with the `UV_PYTHON` environment variable. 

[`--python-platform`](https://docs.astral.sh/uv/reference/cli/#uv-pip-check--python-platform) _python-platform_ 
    
The platform for which packages should be checked.
By default, the installed packages are checked against the platform of the current interpreter.
Represented as a "target triple", a string that describes the target platform in terms of its CPU, vendor, and operating system name, like `x86_64-unknown-linux-gnu` or `aarch64-apple-darwin`.
When targeting macOS (Darwin), the default minimum version is `13.0`. Use `MACOSX_DEPLOYMENT_TARGET` to specify a different minimum version, e.g., `14.0`.
When targeting iOS, the default minimum version is `13.0`. Use `IPHONEOS_DEPLOYMENT_TARGET` to specify a different minimum version, e.g., `14.0`.
When targeting Android, the default minimum Android API level is `24`. Use `ANDROID_API_LEVEL` to specify a different minimum version, e.g., `26`.
Possible values:
  * `windows`: An alias for `x86_64-pc-windows-msvc`, the default target for Windows
  * `linux`: An alias for `x86_64-unknown-linux-gnu`, the default target for Linux
  * `macos`: An alias for `aarch64-apple-darwin`, the default target for macOS
  * `x86_64-pc-windows-msvc`: A 64-bit x86 Windows target
  * `aarch64-pc-windows-msvc`: An ARM64 Windows target
  * `i686-pc-windows-msvc`: A 32-bit x86 Windows target
  * `x86_64-unknown-linux-gnu`: An x86 Linux target. Equivalent to `x86_64-manylinux_2_28`
  * `aarch64-apple-darwin`: An ARM-based macOS target, as seen on Apple Silicon devices
  * `x86_64-apple-darwin`: An x86 macOS target
  * `aarch64-unknown-linux-gnu`: An ARM64 Linux target. Equivalent to `aarch64-manylinux_2_28`
  * `aarch64-unknown-linux-musl`: An ARM64 Linux target
  * `x86_64-unknown-linux-musl`: An `x86_64` Linux target
  * `riscv64-unknown-linux`: A RISCV64 Linux target
  * `x86_64-manylinux2014`: An `x86_64` target for the `manylinux2014` platform. Equivalent to `x86_64-manylinux_2_17`
  * `x86_64-manylinux_2_17`: An `x86_64` target for the `manylinux_2_17` platform
  * `x86_64-manylinux_2_28`: An `x86_64` target for the `manylinux_2_28` platform
  * `x86_64-manylinux_2_31`: An `x86_64` target for the `manylinux_2_31` platform
  * `x86_64-manylinux_2_32`: An `x86_64` target for the `manylinux_2_32` platform
  * `x86_64-manylinux_2_33`: An `x86_64` target for the `manylinux_2_33` platform
  * `x86_64-manylinux_2_34`: An `x86_64` target for the `manylinux_2_34` platform
  * `x86_64-manylinux_2_35`: An `x86_64` target for the `manylinux_2_35` platform
  * `x86_64-manylinux_2_36`: An `x86_64` target for the `manylinux_2_36` platform
  * `x86_64-manylinux_2_37`: An `x86_64` target for the `manylinux_2_37` platform
  * `x86_64-manylinux_2_38`: An `x86_64` target for the `manylinux_2_38` platform
  * `x86_64-manylinux_2_39`: An `x86_64` target for the `manylinux_2_39` platform
  * `x86_64-manylinux_2_40`: An `x86_64` target for the `manylinux_2_40` platform
  * `aarch64-manylinux2014`: An ARM64 target for the `manylinux2014` platform. Equivalent to `aarch64-manylinux_2_17`
  * `aarch64-manylinux_2_17`: An ARM64 target for the `manylinux_2_17` platform
  * `aarch64-manylinux_2_28`: An ARM64 target for the `manylinux_2_28` platform
  * `aarch64-manylinux_2_31`: An ARM64 target for the `manylinux_2_31` platform
  * `aarch64-manylinux_2_32`: An ARM64 target for the `manylinux_2_32` platform
  * `aarch64-manylinux_2_33`: An ARM64 target for the `manylinux_2_33` platform
  * `aarch64-manylinux_2_34`: An ARM64 target for the `manylinux_2_34` platform
  * `aarch64-manylinux_2_35`: An ARM64 target for the `manylinux_2_35` platform
  * `aarch64-manylinux_2_36`: An ARM64 target for the `manylinux_2_36` platform
  * `aarch64-manylinux_2_37`: An ARM64 target for the `manylinux_2_37` platform
  * `aarch64-manylinux_2_38`: An ARM64 target for the `manylinux_2_38` platform
  * `aarch64-manylinux_2_39`: An ARM64 target for the `manylinux_2_39` platform
  * `aarch64-manylinux_2_40`: An ARM64 target for the `manylinux_2_40` platform
  * `aarch64-linux-android`: An ARM64 Android target
  * `x86_64-linux-android`: An `x86_64` Android target
  * `wasm32-pyodide2024`: A wasm32 target using the Pyodide 2024 platform. Meant for use with Python 3.12. See <https://pyodide.org/en/stable/development/abi/312.html>
  * `wasm32-pyodide2025`: A wasm32 target using the Pyodide 2025 platform. Meant for use with Python 3.13. See <https://pyodide.org/en/stable/development/abi/313.html>
  * `arm64-apple-ios`: An ARM64 target for iOS device
  * `arm64-apple-ios-simulator`: An ARM64 target for iOS simulator
  * `x86_64-apple-ios-simulator`: An `x86_64` target for iOS simulator



[`--python-version`](https://docs.astral.sh/uv/reference/cli/#uv-pip-check--python-version) _python-version_ 
    
The Python version against which packages should be checked.
By default, the installed packages are checked against the version of the current interpreter.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Check packages in the system Python environment.
Disables discovery of virtual environments.
See [uv python](https://docs.astral.sh/uv/reference/cli/#uv-python) for details on Python discovery.
May also be set with the `UV_SYSTEM_PYTHON` environment variable.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store.     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
## [uv venv](https://docs.astral.sh/uv/reference/cli/#uv-venv)
Create a virtual environment.
By default, creates a virtual environment named `.venv` in the working directory. An alternative path may be provided positionally.
If in a project, the default environment name can be changed with the `UV_PROJECT_ENVIRONMENT` environment variable; this only applies when run from the project root directory.
If a virtual environment exists at the target path, it will be removed and a new, empty virtual environment will be created.
When using uv, the virtual environment does not need to be activated. uv will find a virtual environment (named `.venv`) in the working directory or any parent directories.
### Usage

```
uv venv [OPTIONS] [PATH]

```

### Arguments     
The path to the virtual environment to create.
Default to `.venv` in the working directory.
Relative paths are resolved relative to the working directory.
### Options     
Preserve any existing files or directories at the target path.
By default, `uv venv` will exit with an error if the given path is non-empty. The `--allow-existing` option will instead write to the given path, regardless of its contents, and without clearing it beforehand.
WARNING: This option can lead to unexpected behavior if the existing virtual environment and the newly-created virtual environment are linked to different Python interpreters. 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-venv--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-venv--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable.     
Remove any existing files or directories at the target path [env: UV_VENV_CLEAR=]
By default, `uv venv` will exit with an error if the given path is non-empty. The `--clear` option will instead clear a non-empty path before creating a new virtual environment. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-venv--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-venv--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--default-index`](https://docs.astral.sh/uv/reference/cli/#uv-venv--default-index) _default-index_ 
    
The default package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--index` flag.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
May also be set with the `UV_DEFAULT_INDEX` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-venv--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable. 

[`--exclude-newer`](https://docs.astral.sh/uv/reference/cli/#uv-venv--exclude-newer) _exclude-newer_ 
    
Limit candidate packages to those that were uploaded prior to the given date.
The date is compared against the upload time of each individual distribution artifact (i.e., when each file was uploaded to the package index), not the release date of the package version.
Accepts RFC 3339 timestamps (e.g., `2006-12-02T02:07:43Z`), local dates in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Use `false` to disable `exclude-newer`.
May also be set with the `UV_EXCLUDE_NEWER` environment variable. 

[`--exclude-newer-package`](https://docs.astral.sh/uv/reference/cli/#uv-venv--exclude-newer-package) _exclude-newer-package_ 
    
Limit candidate packages for specific packages to those that were uploaded prior to the given date.
Accepts package-date pairs in the format `PACKAGE=DATE`, where `DATE` is an RFC 3339 timestamp (e.g., `2006-12-02T02:07:43Z`), a local date in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Can be provided multiple times for different packages. 

[`--extra-index-url`](https://docs.astral.sh/uv/reference/cli/#uv-venv--extra-index-url) _extra-index-url_ 
    
(Deprecated: use `--index` instead) Extra URLs of package indexes to use, in addition to `--index-url`.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--index-url` (which defaults to PyPI). When multiple `--extra-index-url` flags are provided, earlier values take priority.
May also be set with the `UV_EXTRA_INDEX_URL` environment variable. 

[`--find-links`](https://docs.astral.sh/uv/reference/cli/#uv-venv--find-links), `-f` _find-links_ 
    
Locations to search for candidate distributions, in addition to those found in the registry indexes.
If a path, the target must be a directory that contains packages as wheel files (`.whl`) or source distributions (e.g., `.tar.gz` or `.zip`) at the top level.
If a URL, the page must contain a flat list of links to package files adhering to the formats described above.
May also be set with the `UV_FIND_LINKS` environment variable.     
Allow `--clear` to remove a non-virtual environment directory.
This will remove all files and directories at the target path.     
Display the concise help for this command 

[`--index`](https://docs.astral.sh/uv/reference/cli/#uv-venv--index) _index_ 
    
The indexes to use when resolving dependencies, in addition to the default index.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--default-index` (which defaults to PyPI). When multiple `--index` flags are provided, earlier values take priority.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
Relative paths can be disambiguated from index names with `./` or `../` on Unix or `.\\`, `..\\`, `./` or `../` on Windows.
May also be set with the `UV_INDEX` environment variable. 

[`--index-strategy`](https://docs.astral.sh/uv/reference/cli/#uv-venv--index-strategy) _index-strategy_ 
    
The strategy to use when resolving against multiple index URLs.
By default, uv will stop at the first index on which a given package is available, and limit resolutions to those present on that first index (`first-index`). This prevents "dependency confusion" attacks, whereby an attacker can upload a malicious package under the same name to an alternate index.
May also be set with the `UV_INDEX_STRATEGY` environment variable.
Possible values:
  * `first-index`: Only use results from the first index that returns a match for a given package name
  * `unsafe-first-match`: Search for every package name across all indexes, exhausting the versions from the first index before moving on to the next
  * `unsafe-best-match`: Search for every package name across all indexes, preferring the "best" version found. If a package version is in multiple indexes, only look at the entry for the first index



[`--index-url`](https://docs.astral.sh/uv/reference/cli/#uv-venv--index-url), `-i` _index-url_ 
    
(Deprecated: use `--default-index` instead) The URL of the Python package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--extra-index-url` flag.
May also be set with the `UV_INDEX_URL` environment variable. 

[`--keyring-provider`](https://docs.astral.sh/uv/reference/cli/#uv-venv--keyring-provider) _keyring-provider_ 
    
Attempt to use `keyring` for authentication for index URLs.
At present, only `--keyring-provider subprocess` is supported, which configures uv to use the `keyring` CLI to handle authentication.
Defaults to `disabled`.
May also be set with the `UV_KEYRING_PROVIDER` environment variable.
Possible values:
  * `disabled`: Do not use keyring for credential lookup
  * `subprocess`: Use the `keyring` command for credential lookup



[`--link-mode`](https://docs.astral.sh/uv/reference/cli/#uv-venv--link-mode) _link-mode_ 
    
The method to use when installing packages from the global cache.
This option is only used for installing seed packages.
Defaults to `clone` (also known as Copy-on-Write) on macOS and Linux, and `hardlink` on Windows.
WARNING: The use of symlink link mode is discouraged, as they create tight coupling between the cache and the target environment. For example, clearing the cache (`uv cache clean`) will break all installed packages by way of removing the underlying source files. Use symlinks with caution.
May also be set with the `UV_LINK_MODE` environment variable.
Possible values:
  * `clone`: Clone (i.e., copy-on-write) packages from the source into the destination
  * `copy`: Copy packages from the source into the destination
  * `hardlink`: Hard link packages from the source into the destination
  * `symlink`: Symbolically link packages from the source into the destination

    
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-venv--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable.     
Ignore the registry index (e.g., PyPI), instead relying on direct URL dependencies and those provided via `--find-links` 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-venv--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-project`](https://docs.astral.sh/uv/reference/cli/#uv-venv--no-project), `--no-workspace` 
    
Avoid discovering a project or workspace.
By default, uv searches for projects in the current directory or any parent directory to determine the default path of the virtual environment and check for Python version constraints, if any.
May also be set with the `UV_NO_PROJECT` environment variable. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-venv--no-python-downloads)
    
Disable automatic downloads of Python.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-venv--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable. 

[`--prompt`](https://docs.astral.sh/uv/reference/cli/#uv-venv--prompt) _prompt_ 
    
Provide an alternative prompt prefix for the virtual environment.
By default, the prompt is dependent on whether a path was provided to `uv venv`. If provided (e.g, `uv venv project`), the prompt is set to the directory name. If not provided (`uv venv`), the prompt is set to the current directory's name.
If "." is provided, the current directory name will be used regardless of whether a path was provided to `uv venv`. 

[`--python`](https://docs.astral.sh/uv/reference/cli/#uv-venv--python), `-p` _python_ 
    
The Python interpreter to use for the virtual environment.
During virtual environment creation, uv will not look for Python interpreters in virtual environments.
See [uv python](https://docs.astral.sh/uv/reference/cli/#uv-python) for details on Python discovery and supported request formats.
May also be set with the `UV_PYTHON` environment variable.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Refresh all cached data 

[`--refresh-package`](https://docs.astral.sh/uv/reference/cli/#uv-venv--refresh-package) _refresh-package_ 
    
Refresh cached data for a specific package     
Make the virtual environment relocatable [env: UV_VENV_RELOCATABLE=]
A relocatable virtual environment can be moved around and redistributed without invalidating its associated entrypoint and activation scripts.
Note that this can only be guaranteed for standard `console_scripts` and `gui_scripts`. Other scripts may be adjusted if they ship with a generic `#!python[w]` shebang, and binaries are left as-is.
As a result of making the environment relocatable (by way of writing relative, rather than absolute paths), the entrypoints and scripts themselves will _not_ be relocatable. In other words, copying those entrypoints and scripts to a location outside the environment will not work, as they reference paths relative to the environment itself.     
Install seed packages (one or more of: `pip`, `setuptools`, and `wheel`) into the virtual environment [env: UV_VENV_SEED=]
Note that `setuptools` and `wheel` are not included in Python 3.12+ environments.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store. 

[`--system-site-packages`](https://docs.astral.sh/uv/reference/cli/#uv-venv--system-site-packages)
    
Give the virtual environment access to the system site packages directory.
Unlike `pip`, when a virtual environment is created with `--system-site-packages`, uv will _not_ take system site packages into account when running commands like `uv pip list` or `uv pip install`. The `--system-site-packages` flag will provide the virtual environment with access to the system site packages directory at runtime, but will not affect the behavior of uv commands.     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
## [uv build](https://docs.astral.sh/uv/reference/cli/#uv-build)
Build Python packages into source distributions and wheels.
`uv build` accepts a path to a directory or source distribution, which defaults to the current working directory.
By default, if passed a directory, `uv build` will build a source distribution ("sdist") from the source directory, and a binary distribution ("wheel") from the source distribution.
`uv build --sdist` can be used to build only the source distribution, `uv build --wheel` can be used to build only the binary distribution, and `uv build --sdist --wheel` can be used to build both distributions from source.
If passed a source distribution, `uv build --wheel` will build a wheel from the source distribution.
### Usage

```
uv build [OPTIONS] [SRC]

```

### Arguments     
The directory from which distributions should be built, or a source distribution archive to build into a wheel.
Defaults to the current working directory.
### Options 

[`--all-packages`](https://docs.astral.sh/uv/reference/cli/#uv-build--all-packages), `--all` 
    
Builds all packages in the workspace.
The workspace will be discovered from the provided source directory, or the current directory if no source directory is provided.
If the workspace member does not exist, uv will exit with an error. 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-build--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--build-constraints`](https://docs.astral.sh/uv/reference/cli/#uv-build--build-constraints), `--build-constraint`, `-b` _build-constraints_ 
    
Constrain build dependencies using the given requirements files when building distributions.
Constraints files are `requirements.txt`-like files that only control the _version_ of a build dependency that's installed. However, including a package in a constraints file will _not_ trigger the inclusion of that package on its own.
May also be set with the `UV_BUILD_CONSTRAINT` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-build--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable.     
Clear the output directory before the build, removing stale artifacts 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-build--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-build--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--config-setting`](https://docs.astral.sh/uv/reference/cli/#uv-build--config-setting), `--config-settings`, `-C` _config-setting_ 
    
Settings to pass to the PEP 517 build backend, specified as `KEY=VALUE` pairs 

[`--config-settings-package`](https://docs.astral.sh/uv/reference/cli/#uv-build--config-settings-package), `--config-settings-package` _config-settings-package_ 
    
Settings to pass to the PEP 517 build backend for a specific package, specified as `PACKAGE:KEY=VALUE` pairs 

[`--default-index`](https://docs.astral.sh/uv/reference/cli/#uv-build--default-index) _default-index_ 
    
The default package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--index` flag.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
May also be set with the `UV_DEFAULT_INDEX` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-build--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable. 

[`--exclude-newer`](https://docs.astral.sh/uv/reference/cli/#uv-build--exclude-newer) _exclude-newer_ 
    
Limit candidate packages to those that were uploaded prior to the given date.
The date is compared against the upload time of each individual distribution artifact (i.e., when each file was uploaded to the package index), not the release date of the package version.
Accepts RFC 3339 timestamps (e.g., `2006-12-02T02:07:43Z`), local dates in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Use `false` to disable `exclude-newer`.
May also be set with the `UV_EXCLUDE_NEWER` environment variable. 

[`--exclude-newer-package`](https://docs.astral.sh/uv/reference/cli/#uv-build--exclude-newer-package) _exclude-newer-package_ 
    
Limit candidate packages for specific packages to those that were uploaded prior to the given date.
Accepts package-date pairs in the format `PACKAGE=DATE`, where `DATE` is an RFC 3339 timestamp (e.g., `2006-12-02T02:07:43Z`), a local date in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Can be provided multiple times for different packages. 

[`--extra-index-url`](https://docs.astral.sh/uv/reference/cli/#uv-build--extra-index-url) _extra-index-url_ 
    
(Deprecated: use `--index` instead) Extra URLs of package indexes to use, in addition to `--index-url`.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--index-url` (which defaults to PyPI). When multiple `--extra-index-url` flags are provided, earlier values take priority.
May also be set with the `UV_EXTRA_INDEX_URL` environment variable. 

[`--find-links`](https://docs.astral.sh/uv/reference/cli/#uv-build--find-links), `-f` _find-links_ 
    
Locations to search for candidate distributions, in addition to those found in the registry indexes.
If a path, the target must be a directory that contains packages as wheel files (`.whl`) or source distributions (e.g., `.tar.gz` or `.zip`) at the top level.
If a URL, the page must contain a flat list of links to package files adhering to the formats described above.
May also be set with the `UV_FIND_LINKS` environment variable.     
Always build through PEP 517, don't use the fast path for the uv build backend.
By default, uv won't create a PEP 517 build environment for packages using the uv build backend, but use a fast path that calls into the build backend directly. This option forces always using PEP 517. 

[`--fork-strategy`](https://docs.astral.sh/uv/reference/cli/#uv-build--fork-strategy) _fork-strategy_ 
    
The strategy to use when selecting multiple versions of a given package across Python versions and platforms.
By default, uv will optimize for selecting the latest version of each package for each supported Python version (`requires-python`), while minimizing the number of selected versions across platforms.
Under `fewest`, uv will minimize the number of selected versions for each package, preferring older versions that are compatible with a wider range of supported Python versions or platforms.
May also be set with the `UV_FORK_STRATEGY` environment variable.
Possible values:
  * `fewest`: Optimize for selecting the fewest number of versions for each package. Older versions may be preferred if they are compatible with a wider range of supported Python versions or platforms
  * `requires-python`: Optimize for selecting latest supported version of each package, for each supported Python version

    
Display the concise help for this command 

[`--index`](https://docs.astral.sh/uv/reference/cli/#uv-build--index) _index_ 
    
The indexes to use when resolving dependencies, in addition to the default index.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--default-index` (which defaults to PyPI). When multiple `--index` flags are provided, earlier values take priority.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
Relative paths can be disambiguated from index names with `./` or `../` on Unix or `.\\`, `..\\`, `./` or `../` on Windows.
May also be set with the `UV_INDEX` environment variable. 

[`--index-strategy`](https://docs.astral.sh/uv/reference/cli/#uv-build--index-strategy) _index-strategy_ 
    
The strategy to use when resolving against multiple index URLs.
By default, uv will stop at the first index on which a given package is available, and limit resolutions to those present on that first index (`first-index`). This prevents "dependency confusion" attacks, whereby an attacker can upload a malicious package under the same name to an alternate index.
May also be set with the `UV_INDEX_STRATEGY` environment variable.
Possible values:
  * `first-index`: Only use results from the first index that returns a match for a given package name
  * `unsafe-first-match`: Search for every package name across all indexes, exhausting the versions from the first index before moving on to the next
  * `unsafe-best-match`: Search for every package name across all indexes, preferring the "best" version found. If a package version is in multiple indexes, only look at the entry for the first index



[`--index-url`](https://docs.astral.sh/uv/reference/cli/#uv-build--index-url), `-i` _index-url_ 
    
(Deprecated: use `--default-index` instead) The URL of the Python package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--extra-index-url` flag.
May also be set with the `UV_INDEX_URL` environment variable. 

[`--keyring-provider`](https://docs.astral.sh/uv/reference/cli/#uv-build--keyring-provider) _keyring-provider_ 
    
Attempt to use `keyring` for authentication for index URLs.
At present, only `--keyring-provider subprocess` is supported, which configures uv to use the `keyring` CLI to handle authentication.
Defaults to `disabled`.
May also be set with the `UV_KEYRING_PROVIDER` environment variable.
Possible values:
  * `disabled`: Do not use keyring for credential lookup
  * `subprocess`: Use the `keyring` command for credential lookup



[`--link-mode`](https://docs.astral.sh/uv/reference/cli/#uv-build--link-mode) _link-mode_ 
    
The method to use when installing packages from the global cache.
This option is only used when building source distributions.
Defaults to `clone` (also known as Copy-on-Write) on macOS and Linux, and `hardlink` on Windows.
WARNING: The use of symlink link mode is discouraged, as they create tight coupling between the cache and the target environment. For example, clearing the cache (`uv cache clean`) will break all installed packages by way of removing the underlying source files. Use symlinks with caution.
May also be set with the `UV_LINK_MODE` environment variable.
Possible values:
  * `clone`: Clone (i.e., copy-on-write) packages from the source into the destination
  * `copy`: Copy packages from the source into the destination
  * `hardlink`: Hard link packages from the source into the destination
  * `symlink`: Symbolically link packages from the source into the destination

    
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions.     
Don't install pre-built wheels.
The given packages will be built and installed from source. The resolver will still use pre-built wheels to extract package metadata, if available.
May also be set with the `UV_NO_BINARY` environment variable. 

[`--no-binary-package`](https://docs.astral.sh/uv/reference/cli/#uv-build--no-binary-package) _no-binary-package_ 
    
Don't install pre-built wheels for a specific package [env: `UV_NO_BINARY_PACKAGE`=]     
Don't build source distributions.
When enabled, uv will reuse cached wheels from previously built source distributions, but operations that require building a source distribution will exit with an error. First-party packages, such as projects in the workspace, will still be built. uv will also still build editable requirements, and their build backends may run arbitrary Python code.
May also be set with the `UV_NO_BUILD` environment variable. 

[`--no-build-isolation`](https://docs.astral.sh/uv/reference/cli/#uv-build--no-build-isolation)
    
Disable isolation when building source distributions.
Assumes that build dependencies specified by PEP 518 are already installed.
May also be set with the `UV_NO_BUILD_ISOLATION` environment variable. 

[`--no-build-isolation-package`](https://docs.astral.sh/uv/reference/cli/#uv-build--no-build-isolation-package) _no-build-isolation-package_ 
    
Disable isolation when building source distributions for a specific package.
Assumes that the packages' build dependencies specified by PEP 518 are already installed.     
Hide logs from the build backend 

[`--no-build-package`](https://docs.astral.sh/uv/reference/cli/#uv-build--no-build-package) _no-build-package_ 
    
Don't build source distributions for a specific package [env: `UV_NO_BUILD_PACKAGE`=]
First-party packages, such as projects in the workspace, will still be built. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-build--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable. 

[`--no-create-gitignore`](https://docs.astral.sh/uv/reference/cli/#uv-build--no-create-gitignore)
    
Do not create a `.gitignore` file in the output directory.
By default, uv creates a `.gitignore` file in the output directory to exclude build artifacts from version control. When this flag is used, the file will be omitted.     
Ignore the registry index (e.g., PyPI), instead relying on direct URL dependencies and those provided via `--find-links` 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-build--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-build--no-python-downloads)
    
Disable automatic downloads of Python.     
Ignore the `tool.uv.sources` table when resolving dependencies. Used to lock against the standards-compliant, publishable package metadata, as opposed to using any workspace, Git, URL, or local path sources
May also be set with the `UV_NO_SOURCES` environment variable. 

[`--no-sources-package`](https://docs.astral.sh/uv/reference/cli/#uv-build--no-sources-package) _no-sources-package_ 
    
Don't use sources from the `tool.uv.sources` table for the specified packages [env: `UV_NO_SOURCES_PACKAGE`=] 

[`--no-verify-hashes`](https://docs.astral.sh/uv/reference/cli/#uv-build--no-verify-hashes)
    
Disable validation of hashes in the requirements file.
By default, uv will verify any available hashes in the requirements file, but will not require that all requirements have an associated hash. To enforce hash validation, use `--require-hashes`.
May also be set with the `UV_NO_VERIFY_HASHES` environment variable.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--out-dir`](https://docs.astral.sh/uv/reference/cli/#uv-build--out-dir), `-o` _out-dir_ 
    
The output directory to which distributions should be written.
Defaults to the `dist` subdirectory within the source directory, or the directory containing the source distribution archive. 

[`--package`](https://docs.astral.sh/uv/reference/cli/#uv-build--package) _package_ 
    
Build a specific package in the workspace.
The workspace will be discovered from the provided source directory, or the current directory if no source directory is provided.
If the workspace member does not exist, uv will exit with an error. 

[`--prerelease`](https://docs.astral.sh/uv/reference/cli/#uv-build--prerelease) _prerelease_ 
    
The strategy to use when considering pre-release versions.
By default, uv will prefer stable candidates, falling back to pre-releases only after every stable candidate that satisfies the active constraints is rejected (`if-necessary`).
May also be set with the `UV_PRERELEASE` environment variable.
Possible values:
  * `disallow`: Disallow all pre-release versions
  * `allow`: Allow all pre-release versions
  * `if-necessary`: Prefer stable versions, falling back to pre-release versions when necessary
  * `explicit`: Prefer stable versions for first-party packages with explicit pre-release specifiers, falling back to pre-release versions when necessary. Disallow pre-release versions for all other packages
  * `if-necessary-or-explicit`: Deprecated alias for `if-necessary`



[`--prerelease-package`](https://docs.astral.sh/uv/reference/cli/#uv-build--prerelease-package) _prerelease-package_ 
    
The strategy to use when considering pre-release versions for a specific package.
Accepts package-mode pairs in the format `PACKAGE=MODE`, where `MODE` is any value accepted by `--prerelease`.
May be provided multiple times for different packages. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-build--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable. 

[`--python`](https://docs.astral.sh/uv/reference/cli/#uv-build--python), `-p` _python_ 
    
The Python interpreter to use for the build environment.
By default, builds are executed in isolated virtual environments. The discovered interpreter will be used to create those environments, and will be symlinked or copied in depending on the platform.
See [uv python](https://docs.astral.sh/uv/reference/cli/#uv-python) to view supported request formats.
May also be set with the `UV_PYTHON` environment variable.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Refresh all cached data 

[`--refresh-package`](https://docs.astral.sh/uv/reference/cli/#uv-build--refresh-package) _refresh-package_ 
    
Refresh cached data for a specific package     
Require a matching hash for each requirement.
By default, uv will verify any available hashes in the requirements file, but will not require that all requirements have an associated hash.
When `--require-hashes` is enabled, _all_ requirements must include a hash or set of hashes, and _all_ requirements must either be pinned to exact versions (e.g., `==1.0.0`), or be specified via direct URL.
Hash-checking mode introduces a number of additional constraints:
  * Git dependencies are not supported. - Editable installations are not supported. - Local dependencies are not supported, unless they point to a specific wheel (`.whl`) or source archive (`.zip`, `.tar.gz`), as opposed to a directory.


May also be set with the `UV_REQUIRE_HASHES` environment variable. 

[`--resolution`](https://docs.astral.sh/uv/reference/cli/#uv-build--resolution) _resolution_ 
    
The strategy to use when selecting between the different compatible versions for a given package requirement.
By default, uv will use the latest compatible version of each package (`highest`).
May also be set with the `UV_RESOLUTION` environment variable.
Possible values:
  * `highest`: Resolve the highest compatible version of each package
  * `lowest`: Resolve the lowest compatible version of each package
  * `lowest-direct`: Resolve the lowest compatible version of any direct dependencies, and the highest compatible version of any transitive dependencies

    
Build a source distribution ("sdist") from the given directory     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store.     
Allow package upgrades, ignoring pinned versions in any existing output file. Implies `--refresh` 

[`--upgrade-group`](https://docs.astral.sh/uv/reference/cli/#uv-build--upgrade-group) _upgrade-group_ 
    
Allow upgrades for all packages in a dependency group, ignoring pinned versions in any existing output file 

[`--upgrade-package`](https://docs.astral.sh/uv/reference/cli/#uv-build--upgrade-package), `-P` _upgrade-package_ 
    
Allow upgrades for a specific package, ignoring pinned versions in any existing output file. Implies `--refresh-package`     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)     
Build a binary distribution ("wheel") from the given directory
## [uv publish](https://docs.astral.sh/uv/reference/cli/#uv-publish)
Upload distributions to an index
### Usage

```
uv publish [OPTIONS] [FILES]...

```

### Arguments     
Paths to the files to upload. Accepts glob expressions.
Defaults to the `dist` directory. Selects only wheels and source distributions and their attestations, while ignoring other files.
### Options 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-publish--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-publish--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--check-url`](https://docs.astral.sh/uv/reference/cli/#uv-publish--check-url) _check-url_ 
    
Check an index URL for existing files to skip duplicate uploads.
This option allows retrying publishing that failed after only some, but not all files have been uploaded, and handles errors due to parallel uploads of the same file.
Before uploading, the index is checked. If the exact same file already exists in the index, the file will not be uploaded. If an error occurred during the upload, the index is checked again, to handle cases where the identical file was uploaded twice in parallel.
The exact behavior will vary based on the index. When uploading to PyPI, uploading the same file succeeds even without `--check-url`, while most other indexes error.
The index must provide one of the supported hashes (SHA-256, SHA-384, or SHA-512).
May also be set with the `UV_PUBLISH_CHECK_URL` environment variable. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-publish--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-publish--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-publish--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable.     
Perform a dry run without uploading files.
The command checks the distribution metadata locally, and checks for existing files if `--check-url` or `--index` is provided, but will not upload any files.     
Display the concise help for this command 

[`--index`](https://docs.astral.sh/uv/reference/cli/#uv-publish--index) _index_ 
    
The name of an index in the configuration to use for publishing.
The index must have a `publish-url` setting, for example:

```
[[tool.uv.index]]
name = "pypi"
url = "https://pypi.org/simple"
publish-url = "https://upload.pypi.org/legacy/"

```

The index `url` will be used to check for existing files to skip duplicate uploads.
With these settings, the following two calls are equivalent:

```
uv publish --index pypi
uv publish --publish-url https://upload.pypi.org/legacy/ --check-url https://pypi.org/simple

```

May also be set with the `UV_PUBLISH_INDEX` environment variable. 

[`--keyring-provider`](https://docs.astral.sh/uv/reference/cli/#uv-publish--keyring-provider) _keyring-provider_ 
    
Attempt to use `keyring` for authentication for remote requirements files.
At present, only `--keyring-provider subprocess` is supported, which configures uv to use the `keyring` CLI to handle authentication.
Defaults to `disabled`.
May also be set with the `UV_KEYRING_PROVIDER` environment variable.
Possible values:
  * `disabled`: Do not use keyring for credential lookup
  * `subprocess`: Use the `keyring` command for credential lookup

    
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions. 

[`--no-attestations`](https://docs.astral.sh/uv/reference/cli/#uv-publish--no-attestations)
    
Do not upload attestations for the published files.
By default, uv attempts to upload matching PEP 740 attestations with each distribution that is published.
May also be set with the `UV_PUBLISH_NO_ATTESTATIONS` environment variable. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-publish--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable. 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-publish--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-publish--no-python-downloads)
    
Disable automatic downloads of Python.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--password`](https://docs.astral.sh/uv/reference/cli/#uv-publish--password), `-p` _password_ 
    
The password for the upload
May also be set with the `UV_PUBLISH_PASSWORD` environment variable. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-publish--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable. 

[`--publish-url`](https://docs.astral.sh/uv/reference/cli/#uv-publish--publish-url) _publish-url_ 
    
The URL of the upload endpoint (not the index URL).
Note that there are typically different URLs for index access (e.g., `https:://.../simple`) and index upload.
Defaults to PyPI's publish URL (<https://upload.pypi.org/legacy/>).
May also be set with the `UV_PUBLISH_URL` environment variable.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store. 

[`--token`](https://docs.astral.sh/uv/reference/cli/#uv-publish--token), `-t` _token_ 
    
The token for the upload.
Using a token is equivalent to passing `__token__` as `--username` and the token as `--password` password.
May also be set with the `UV_PUBLISH_TOKEN` environment variable. 

[`--trusted-publishing`](https://docs.astral.sh/uv/reference/cli/#uv-publish--trusted-publishing) _trusted-publishing_ 
    
Configure trusted publishing.
By default, uv checks for trusted publishing when running in a supported environment, but ignores it if it isn't configured.
uv's supported environments for trusted publishing include GitHub Actions and GitLab CI/CD.
Possible values:
  * `automatic`: Attempt trusted publishing when we're in a supported environment, continue if that fails
  * `always`
  * `never`



[`--username`](https://docs.astral.sh/uv/reference/cli/#uv-publish--username), `-u` _username_ 
    
The username for the upload
May also be set with the `UV_PUBLISH_USERNAME` environment variable.     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
## [uv workspace](https://docs.astral.sh/uv/reference/cli/#uv-workspace)
Inspect uv workspaces
### Usage

```
uv workspace [OPTIONS] <COMMAND>

```

### Commands 

[`uv workspace metadata`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-metadata)
    
View metadata about the current workspace 

[`uv workspace dir`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-dir)
    
Display the path of a workspace member 

[`uv workspace list`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-list)
    
List the members of a workspace
### [uv workspace metadata](https://docs.astral.sh/uv/reference/cli/#uv-workspace-metadata)
View metadata about the current workspace.
The output of this command is not yet stable.
### Usage

```
uv workspace metadata [OPTIONS]

```

### Options     
Sync dependencies to the active virtual environment.
Instead of creating or updating the virtual environment for the project or script, the active virtual environment will be preferred, if the `VIRTUAL_ENV` environment variable is set. 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-metadata--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-metadata--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-metadata--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-metadata--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--config-setting`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-metadata--config-setting), `--config-settings`, `-C` _config-setting_ 
    
Settings to pass to the PEP 517 build backend, specified as `KEY=VALUE` pairs 

[`--config-settings-package`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-metadata--config-settings-package), `--config-settings-package` _config-settings-package_ 
    
Settings to pass to the PEP 517 build backend for a specific package, specified as `PACKAGE:KEY=VALUE` pairs 

[`--default-index`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-metadata--default-index) _default-index_ 
    
The default package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--index` flag.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
May also be set with the `UV_DEFAULT_INDEX` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-metadata--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable.     
Perform a dry run, without writing the lockfile.
In dry-run mode, uv will resolve the project's dependencies and report on the resulting changes, but will not write the lockfile to disk.     
Perform an exact sync, removing extraneous packages.
By default, synchronization preserves packages that are not part of the selected resolution. When enabled, uv removes those packages from the environment. 

[`--exclude-newer`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-metadata--exclude-newer) _exclude-newer_ 
    
Limit candidate packages to those that were uploaded prior to the given date.
The date is compared against the upload time of each individual distribution artifact (i.e., when each file was uploaded to the package index), not the release date of the package version.
Accepts RFC 3339 timestamps (e.g., `2006-12-02T02:07:43Z`), local dates in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Use `false` to disable `exclude-newer`.
May also be set with the `UV_EXCLUDE_NEWER` environment variable. 

[`--exclude-newer-package`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-metadata--exclude-newer-package) _exclude-newer-package_ 
    
Limit candidate packages for specific packages to those that were uploaded prior to the given date.
Accepts package-date pairs in the format `PACKAGE=DATE`, where `DATE` is an RFC 3339 timestamp (e.g., `2006-12-02T02:07:43Z`), a local date in the same format (e.g., `2006-12-02`) resolved based on your system's configured time zone, a "friendly" duration (e.g., `24 hours`, `1 week`, `30 days`), or an ISO 8601 duration (e.g., `PT24H`, `P7D`, `P30D`).
Durations do not respect semantics of the local time zone and are always resolved to a fixed number of seconds assuming that a day is 24 hours (e.g., DST transitions are ignored). Calendar units such as months and years are not allowed.
Can be provided multiple times for different packages. 

[`--extra-index-url`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-metadata--extra-index-url) _extra-index-url_ 
    
(Deprecated: use `--index` instead) Extra URLs of package indexes to use, in addition to `--index-url`.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--index-url` (which defaults to PyPI). When multiple `--extra-index-url` flags are provided, earlier values take priority.
May also be set with the `UV_EXTRA_INDEX_URL` environment variable. 

[`--find-links`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-metadata--find-links), `-f` _find-links_ 
    
Locations to search for candidate distributions, in addition to those found in the registry indexes.
If a path, the target must be a directory that contains packages as wheel files (`.whl`) or source distributions (e.g., `.tar.gz` or `.zip`) at the top level.
If a URL, the page must contain a flat list of links to package files adhering to the formats described above.
May also be set with the `UV_FIND_LINKS` environment variable. 

[`--fork-strategy`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-metadata--fork-strategy) _fork-strategy_ 
    
The strategy to use when selecting multiple versions of a given package across Python versions and platforms.
By default, uv will optimize for selecting the latest version of each package for each supported Python version (`requires-python`), while minimizing the number of selected versions across platforms.
Under `fewest`, uv will minimize the number of selected versions for each package, preferring older versions that are compatible with a wider range of supported Python versions or platforms.
May also be set with the `UV_FORK_STRATEGY` environment variable.
Possible values:
  * `fewest`: Optimize for selecting the fewest number of versions for each package. Older versions may be preferred if they are compatible with a wider range of supported Python versions or platforms
  * `requires-python`: Optimize for selecting latest supported version of each package, for each supported Python version

    
Assert that a `uv.lock` exists without checking if it is up-to-date [env: UV_FROZEN=]     
Display the concise help for this command 

[`--index`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-metadata--index) _index_ 
    
The indexes to use when resolving dependencies, in addition to the default index.
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
All indexes provided via this flag take priority over the index specified by `--default-index` (which defaults to PyPI). When multiple `--index` flags are provided, earlier values take priority.
Indexes configured in `uv.toml` or `pyproject.toml` may be selected by name. Enable the `index-by-name` preview feature to prefer index names over relative paths.
Relative paths can be disambiguated from index names with `./` or `../` on Unix or `.\\`, `..\\`, `./` or `../` on Windows.
May also be set with the `UV_INDEX` environment variable. 

[`--index-strategy`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-metadata--index-strategy) _index-strategy_ 
    
The strategy to use when resolving against multiple index URLs.
By default, uv will stop at the first index on which a given package is available, and limit resolutions to those present on that first index (`first-index`). This prevents "dependency confusion" attacks, whereby an attacker can upload a malicious package under the same name to an alternate index.
May also be set with the `UV_INDEX_STRATEGY` environment variable.
Possible values:
  * `first-index`: Only use results from the first index that returns a match for a given package name
  * `unsafe-first-match`: Search for every package name across all indexes, exhausting the versions from the first index before moving on to the next
  * `unsafe-best-match`: Search for every package name across all indexes, preferring the "best" version found. If a package version is in multiple indexes, only look at the entry for the first index



[`--index-url`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-metadata--index-url), `-i` _index-url_ 
    
(Deprecated: use `--default-index` instead) The URL of the Python package index (by default: <https://pypi.org/simple>).
Accepts either a repository compliant with PEP 503 (the simple repository API), or a local directory laid out in the same format.
The index given by this flag is given lower priority than all other indexes specified via the `--extra-index-url` flag.
May also be set with the `UV_INDEX_URL` environment variable. 

[`--keyring-provider`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-metadata--keyring-provider) _keyring-provider_ 
    
Attempt to use `keyring` for authentication for index URLs.
At present, only `--keyring-provider subprocess` is supported, which configures uv to use the `keyring` CLI to handle authentication.
Defaults to `disabled`.
May also be set with the `UV_KEYRING_PROVIDER` environment variable.
Possible values:
  * `disabled`: Do not use keyring for credential lookup
  * `subprocess`: Use the `keyring` command for credential lookup



[`--link-mode`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-metadata--link-mode) _link-mode_ 
    
The method to use when installing packages from the global cache.
This option is only used when building source distributions.
Defaults to `clone` (also known as Copy-on-Write) on macOS and Linux, and `hardlink` on Windows.
WARNING: The use of symlink link mode is discouraged, as they create tight coupling between the cache and the target environment. For example, clearing the cache (`uv cache clean`) will break all installed packages by way of removing the underlying source files. Use symlinks with caution.
May also be set with the `UV_LINK_MODE` environment variable.
Possible values:
  * `clone`: Clone (i.e., copy-on-write) packages from the source into the destination
  * `copy`: Copy packages from the source into the destination
  * `hardlink`: Hard link packages from the source into the destination
  * `symlink`: Symbolically link packages from the source into the destination

    
Check if the lockfile is up-to-date [env: UV_LOCKED=]
Asserts that the `uv.lock` would remain unchanged after a resolution. If the lockfile is missing or needs to be updated, uv will exit with an error.     
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions.     
Don't install pre-built wheels.
The given packages will be built and installed from source. The resolver will still use pre-built wheels to extract package metadata, if available.
May also be set with the `UV_NO_BINARY` environment variable. 

[`--no-binary-package`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-metadata--no-binary-package) _no-binary-package_ 
    
Don't install pre-built wheels for a specific package [env: `UV_NO_BINARY_PACKAGE`=]     
Don't build source distributions.
When enabled, uv will reuse cached wheels from previously built source distributions, but operations that require building a source distribution will exit with an error. First-party packages, such as projects in the workspace, will still be built. uv will also still build editable requirements, and their build backends may run arbitrary Python code.
May also be set with the `UV_NO_BUILD` environment variable. 

[`--no-build-isolation`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-metadata--no-build-isolation)
    
Disable isolation when building source distributions.
Assumes that build dependencies specified by PEP 518 are already installed.
May also be set with the `UV_NO_BUILD_ISOLATION` environment variable. 

[`--no-build-isolation-package`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-metadata--no-build-isolation-package) _no-build-isolation-package_ 
    
Disable isolation when building source distributions for a specific package.
Assumes that the packages' build dependencies specified by PEP 518 are already installed. 

[`--no-build-package`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-metadata--no-build-package) _no-build-package_ 
    
Don't build source distributions for a specific package [env: `UV_NO_BUILD_PACKAGE`=]
First-party packages, such as projects in the workspace, will still be built. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-metadata--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable.     
Ignore the registry index (e.g., PyPI), instead relying on direct URL dependencies and those provided via `--find-links` 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-metadata--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-metadata--no-python-downloads)
    
Disable automatic downloads of Python.     
Ignore the `tool.uv.sources` table when resolving dependencies. Used to lock against the standards-compliant, publishable package metadata, as opposed to using any workspace, Git, URL, or local path sources
May also be set with the `UV_NO_SOURCES` environment variable. 

[`--no-sources-package`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-metadata--no-sources-package) _no-sources-package_ 
    
Don't use sources from the `tool.uv.sources` table for the specified packages [env: `UV_NO_SOURCES_PACKAGE`=]     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--prerelease`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-metadata--prerelease) _prerelease_ 
    
The strategy to use when considering pre-release versions.
By default, uv will prefer stable candidates, falling back to pre-releases only after every stable candidate that satisfies the active constraints is rejected (`if-necessary`).
May also be set with the `UV_PRERELEASE` environment variable.
Possible values:
  * `disallow`: Disallow all pre-release versions
  * `allow`: Allow all pre-release versions
  * `if-necessary`: Prefer stable versions, falling back to pre-release versions when necessary
  * `explicit`: Prefer stable versions for first-party packages with explicit pre-release specifiers, falling back to pre-release versions when necessary. Disallow pre-release versions for all other packages
  * `if-necessary-or-explicit`: Deprecated alias for `if-necessary`



[`--prerelease-package`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-metadata--prerelease-package) _prerelease-package_ 
    
The strategy to use when considering pre-release versions for a specific package.
Accepts package-mode pairs in the format `PACKAGE=MODE`, where `MODE` is any value accepted by `--prerelease`.
May be provided multiple times for different packages. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-metadata--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable. 

[`--python`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-metadata--python), `-p` _python_ 
    
The Python interpreter to use during resolution.
A Python interpreter is required for building source distributions to determine package metadata when there are not wheels.
The interpreter is also used as the fallback value for the minimum Python version if `requires-python` is not set.
See [uv python](https://docs.astral.sh/uv/reference/cli/#uv-python) for details on Python discovery and supported request formats.
May also be set with the `UV_PYTHON` environment variable.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Refresh all cached data 

[`--refresh-package`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-metadata--refresh-package) _refresh-package_ 
    
Refresh cached data for a specific package 

[`--resolution`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-metadata--resolution) _resolution_ 
    
The strategy to use when selecting between the different compatible versions for a given package requirement.
By default, uv will use the latest compatible version of each package (`highest`).
May also be set with the `UV_RESOLUTION` environment variable.
Possible values:
  * `highest`: Resolve the highest compatible version of each package
  * `lowest`: Resolve the lowest compatible version of each package
  * `lowest-direct`: Resolve the lowest compatible version of any direct dependencies, and the highest compatible version of any transitive dependencies



[`--script`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-metadata--script) _script_ 
    
View metadata for the specified PEP 723 Python script, rather than the current workspace.
If provided, uv will resolve the dependencies based on the script's inline metadata table, in adherence with PEP 723.     
Sync the environment to include module ownership metadata in the output.
This adds a mapping from importable module names to references to the package nodes that provide them. By default, the environment is synced in inexact mode.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store.     
Allow package upgrades, ignoring pinned versions in any existing output file. Implies `--refresh` 

[`--upgrade-group`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-metadata--upgrade-group) _upgrade-group_ 
    
Allow upgrades for all packages in a dependency group, ignoring pinned versions in any existing output file 

[`--upgrade-package`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-metadata--upgrade-package), `-P` _upgrade-package_ 
    
Allow upgrades for a specific package, ignoring pinned versions in any existing output file. Implies `--refresh-package`     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
### [uv workspace dir](https://docs.astral.sh/uv/reference/cli/#uv-workspace-dir)
Display the path of a workspace member.
By default, the path to the workspace root directory is displayed. The `--package` option can be used to display the path to a workspace member instead.
If used outside of a workspace, i.e., if a `pyproject.toml` cannot be found, uv will exit with an error.
### Usage

```
uv workspace dir [OPTIONS]

```

### Options 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-dir--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-dir--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-dir--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-dir--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-dir--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable.     
Display the concise help for this command     
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-dir--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable. 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-dir--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-dir--no-python-downloads)
    
Disable automatic downloads of Python.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--package`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-dir--package) _package_ 
    
Display the path to a specific package in the workspace 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-dir--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store.     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
### [uv workspace list](https://docs.astral.sh/uv/reference/cli/#uv-workspace-list)
List the members of a workspace.
Displays newline separated names of workspace members.
### Usage

```
uv workspace list [OPTIONS]

```

### Options 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-list--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-list--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-list--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-list--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-list--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable.     
Display the concise help for this command     
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-list--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable. 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-list--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-list--no-python-downloads)
    
Disable automatic downloads of Python.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files.     
Show paths instead of names 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-workspace-list--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
List all standalone scripts with inline metadata in the workspace     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store.     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
## [uv cache](https://docs.astral.sh/uv/reference/cli/#uv-cache)
Manage uv's cache
### Usage

```
uv cache [OPTIONS] <COMMAND>

```

### Commands     
Clear the cache, removing all entries or those linked to specific packages     
Prune dangling cache entries and cached environments     
Show the cache directory     
Show the cache size
### [uv cache clean](https://docs.astral.sh/uv/reference/cli/#uv-cache-clean)
Clear the cache, removing all entries or those linked to specific packages
### Usage

```
uv cache clean [OPTIONS] [PACKAGE]...

```

### Arguments     
The packages to remove from the cache
### Options 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-cache-clean--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-cache-clean--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-cache-clean--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-cache-clean--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-cache-clean--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable.     
Force removal of the cache, ignoring in-use checks.
By default, `uv cache clean` will block until no process is reading the cache. When `--force` is used, `uv cache clean` will proceed without taking a lock.     
Display the concise help for this command     
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-cache-clean--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable. 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-cache-clean--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-cache-clean--no-python-downloads)
    
Disable automatic downloads of Python.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-cache-clean--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store.     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
### [uv cache prune](https://docs.astral.sh/uv/reference/cli/#uv-cache-prune)
Prune dangling cache entries and cached environments
### Usage

```
uv cache prune [OPTIONS]

```

### Options 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-cache-prune--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-cache-prune--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable.     
Optimize the cache for persistence in a continuous integration environment, like GitHub Actions.
By default, uv caches both the wheels that it builds from source and the pre-built wheels that it downloads directly, to enable high-performance package installation. In some scenarios, though, persisting pre-built wheels may be undesirable. For example, in GitHub Actions, it's faster to omit pre-built wheels from the cache and instead have re-download them on each run. However, it typically _is_ faster to cache wheels that are built from source, since the wheel building process can be expensive, especially for extension modules.
In `--ci` mode, uv will prune any pre-built wheels from the cache, but retain any wheels that were built from source. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-cache-prune--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-cache-prune--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-cache-prune--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable.     
Force removal of the cache, ignoring in-use checks.
By default, `uv cache prune` will block until no process is reading the cache. When `--force` is used, `uv cache prune` will proceed without taking a lock.     
Display the concise help for this command     
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-cache-prune--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable. 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-cache-prune--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-cache-prune--no-python-downloads)
    
Disable automatic downloads of Python.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-cache-prune--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store.     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
### [uv cache dir](https://docs.astral.sh/uv/reference/cli/#uv-cache-dir)
Show the cache directory.
By default, the cache is stored in `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on Unix and `%LOCALAPPDATA%\uv\cache` on Windows.
When `--no-cache` is used, the cache is stored in a temporary directory and discarded when the process exits.
An alternative cache directory may be specified via the `cache-dir` setting, the `--cache-dir` option, or the `$UV_CACHE_DIR` environment variable.
Note that it is important for performance for the cache directory to be located on the same file system as the Python environment uv is operating on.
### Usage

```
uv cache dir [OPTIONS]

```

### Options 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-cache-dir--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-cache-dir--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-cache-dir--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-cache-dir--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-cache-dir--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable.     
Display the concise help for this command     
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-cache-dir--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable. 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-cache-dir--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-cache-dir--no-python-downloads)
    
Disable automatic downloads of Python.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-cache-dir--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store.     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
### [uv cache size](https://docs.astral.sh/uv/reference/cli/#uv-cache-size)
Show the cache size.
Displays the total size of the cache directory. This includes all downloaded and built wheels, source distributions, and other cached data. By default, displays a human-readable size when the output is a terminal and raw bytes otherwise.
### Usage

```
uv cache size [OPTIONS]

```

### Options 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-cache-size--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-cache-size--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-cache-size--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-cache-size--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-cache-size--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable.     
Display the concise help for this command 

[`--human`](https://docs.astral.sh/uv/reference/cli/#uv-cache-size--human), `--human-readable`, `-H` 
    
Display the cache size in human-readable format (e.g., `1.2GiB` instead of raw bytes)     
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-cache-size--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable. 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-cache-size--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-cache-size--no-python-downloads)
    
Disable automatic downloads of Python.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--output-format`](https://docs.astral.sh/uv/reference/cli/#uv-cache-size--output-format) _output-format_ 
    
Select the output format
[default: auto]
Possible values:
  * `auto`: Display a human-readable size in terminals and raw bytes otherwise
  * `human`: Display the cache size in a human-readable format
  * `machine`: Display the cache size in raw bytes



[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-cache-size--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store.     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
## [uv self](https://docs.astral.sh/uv/reference/cli/#uv-self)
Manage the uv executable
### Usage

```
uv self [OPTIONS] <COMMAND>

```

### Commands     
Update uv     
Display uv's version
### [uv self update](https://docs.astral.sh/uv/reference/cli/#uv-self-update)
Update uv
### Usage

```
uv self update [OPTIONS] [TARGET_VERSION]

```

### Arguments     
Update to the specified version. If not provided, uv will update to the latest version
### Options 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-self-update--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-self-update--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-self-update--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-self-update--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-self-update--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable.     
Run without performing the update     
Display the concise help for this command     
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-self-update--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable. 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-self-update--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-self-update--no-python-downloads)
    
Disable automatic downloads of Python.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-self-update--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store. 

[`--token`](https://docs.astral.sh/uv/reference/cli/#uv-self-update--token) _token_ 
    
A GitHub token for authentication. A token is not required but can be used to reduce the chance of encountering rate limits
May also be set with the `UV_GITHUB_TOKEN` environment variable.     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
### [uv self version](https://docs.astral.sh/uv/reference/cli/#uv-self-version)
Display uv's version
### Usage

```
uv self version [OPTIONS]

```

### Options 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-self-version--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-self-version--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-self-version--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-self-version--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-self-version--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable.     
Display the concise help for this command     
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-self-version--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable. 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-self-version--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-self-version--no-python-downloads)
    
Disable automatic downloads of Python.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--output-format`](https://docs.astral.sh/uv/reference/cli/#uv-self-version--output-format) _output-format_ 


[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-self-version--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Only print the version     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store.     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
## [uv generate-shell-completion](https://docs.astral.sh/uv/reference/cli/#uv-generate-shell-completion)
Generate shell completion
### Usage

```
uv generate-shell-completion [OPTIONS] <SHELL>

```

### Arguments     
The shell to generate the completion script for
### Options 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-generate-shell-completion--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-generate-shell-completion--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable.     
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions.     
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-generate-shell-completion--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store.
## [uv help](https://docs.astral.sh/uv/reference/cli/#uv-help)
Display documentation for a command
### Usage

```
uv help [OPTIONS] [COMMAND]...

```

### Arguments
### Options 

[`--allow-insecure-host`](https://docs.astral.sh/uv/reference/cli/#uv-help--allow-insecure-host), `--trusted-host` _allow-insecure-host_ 
    
Allow insecure connections to a host.
Can be provided multiple times.
Expects to receive either a hostname (e.g., `localhost`), a host-port pair (e.g., `localhost:8080`), or a URL (e.g., `https://localhost`).
WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use `--allow-insecure-host` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
May also be set with the `UV_INSECURE_HOST` environment variable. 

[`--cache-dir`](https://docs.astral.sh/uv/reference/cli/#uv-help--cache-dir) _cache-dir_ 
    
Path to the cache directory.
Defaults to `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on macOS and Linux, and `%LOCALAPPDATA%\uv\cache` on Windows.
To view the location of the cache directory, run `uv cache dir`.
May also be set with the `UV_CACHE_DIR` environment variable. 

[`--color`](https://docs.astral.sh/uv/reference/cli/#uv-help--color) _color-choice_ 
    
Control the use of color in output.
By default, uv will automatically detect support for colors when writing to a terminal.
Possible values:
  * `auto`: Enables colored output only when the output is going to a terminal or TTY with support
  * `always`: Enables colored output regardless of the detected environment
  * `never`: Disables colored output



[`--config-file`](https://docs.astral.sh/uv/reference/cli/#uv-help--config-file) _config-file_ 
    
The path to a `uv.toml` file to use for configuration.
While uv configuration can be included in a `pyproject.toml` file, it is not allowed in this context.
May also be set with the `UV_CONFIG_FILE` environment variable. 

[`--directory`](https://docs.astral.sh/uv/reference/cli/#uv-help--directory) _directory_ 
    
Change to the given directory prior to running the command.
Relative paths are resolved with the given directory as the base.
See `--project` to only change the project root directory.
May also be set with the `UV_WORKING_DIR` environment variable.     
Display the concise help for this command     
Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
By default, uv prefers using Python versions it manages. However, it will use system Python versions if a uv-managed Python is not installed. This option disables use of system Python versions. 

[`--no-cache`](https://docs.astral.sh/uv/reference/cli/#uv-help--no-cache), `--no-cache-dir`, `-n` 
    
Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation
May also be set with the `UV_NO_CACHE` environment variable.     
Avoid discovering configuration files (`pyproject.toml`, `uv.toml`).
Normally, configuration files are discovered in the current directory, parent directories, or user configuration directories.
May also be set with the `UV_NO_CONFIG` environment variable. 

[`--no-managed-python`](https://docs.astral.sh/uv/reference/cli/#uv-help--no-managed-python)
    
Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
Instead, uv will search for a suitable Python version on the system.     
Disable pager when printing help     
Hide all progress outputs [env: UV_NO_PROGRESS=]
For example, spinners or progress bars. 

[`--no-python-downloads`](https://docs.astral.sh/uv/reference/cli/#uv-help--no-python-downloads)
    
Disable automatic downloads of Python.     
Disable network access [env: UV_OFFLINE=]
When disabled, uv will only use locally cached data and locally available files. 

[`--project`](https://docs.astral.sh/uv/reference/cli/#uv-help--project) _project_ 
    
Discover a project in the given directory.
All `pyproject.toml`, `uv.toml`, and `.python-version` files will be discovered by walking up the directory tree from the project root, as will the project's virtual environment (`.venv`).
Other command-line arguments (such as relative paths) will be resolved relative to the current working directory.
See `--directory` to change the working directory entirely.
This setting has no effect when used in the `uv pip` interface.
May also be set with the `UV_PROJECT` environment variable.     
Use quiet output.
Repeating this option, e.g., `-qq`, will enable a silent mode in which uv will write no output to stdout.     
Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
By default, uv uses bundled Mozilla root certificates, which improves portability and performance (especially on macOS).
However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store.     
Use verbose output.
You can configure fine-grained logging using the `RUST_LOG` environment variable. (<https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives>)
Back to top 
