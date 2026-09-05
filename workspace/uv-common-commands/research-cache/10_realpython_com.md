---
url: "https://realpython.com/python-uv/"
title: "Managing Python Projects With uv: An All-in-One Solution – Real Python"
scraped_at: 2026-09-05T09:31:26+00:00
---

# Managing Python Projects With uv: An All-in-One Solution
by [Leodanis Pozo Ramos](https://realpython.com/python-uv/#author) Updated Apr 28, 2025 Reading time estimate 28m 
Mark as Completed Share
Table of Contents
  * [Getting to Know uv for Python](https://realpython.com/python-uv/#getting-to-know-uv-for-python)
  * [Installing uv to Manage Python Projects](https://realpython.com/python-uv/#installing-uv-to-manage-python-projects)
    * [Using the Standalone Installer](https://realpython.com/python-uv/#using-the-standalone-installer)
    * [Installing From PyPI](https://realpython.com/python-uv/#installing-from-pypi)
    * [Upgrading to the Latest uv Version](https://realpython.com/python-uv/#upgrading-to-the-latest-uv-version)
  * [Handling Python Projects With uv](https://realpython.com/python-uv/#handling-python-projects-with-uv)
    * [Creating a Python Project](https://realpython.com/python-uv/#creating-a-python-project)
    * [Running the Project’s Entry-Point Script](https://realpython.com/python-uv/#running-the-projects-entry-point-script)
  * [Using uv for Dependency Management](https://realpython.com/python-uv/#using-uv-for-dependency-management)
    * [Adding and Installing Dependencies](https://realpython.com/python-uv/#adding-and-installing-dependencies)
    * [Upgrading and Removing Dependencies](https://realpython.com/python-uv/#upgrading-and-removing-dependencies)
    * [Managing Development Dependencies](https://realpython.com/python-uv/#managing-development-dependencies)
    * [Locking and Syncing the Environment](https://realpython.com/python-uv/#locking-and-syncing-the-environment)
  * [Building and Publishing Packages](https://realpython.com/python-uv/#building-and-publishing-packages)
    * [Configuring the Project](https://realpython.com/python-uv/#configuring-the-project)
    * [Building a Distribution](https://realpython.com/python-uv/#building-a-distribution)
    * [Publishing a Distribution](https://realpython.com/python-uv/#publishing-a-distribution)
  * [Frequently Asked Questions](https://realpython.com/python-uv/#frequently-asked-questions)


Recommended Course
[Python Project Management With uv](https://realpython.com/courses/python-project-management-with-uv/) (1h 12m)
The uv tool is a high-speed package and project manager for Python. It’s written in Rust and designed to streamline your workflow. It offers fast dependency installation and integrates various functionalities into a single tool.
With uv, you can install and manage multiple Python versions, create virtual environments, efficiently handle project dependencies, reproduce working environments, and even build and publish a project. These capabilities make uv an all-in-one tool for Python project management.
**By the end of this tutorial, you’ll understand that:**
  * **uv is a Python package and project manager** that integrates multiple functionalities into one tool, offering a comprehensive solution for managing Python projects.
  * **uv is used for fast dependency installation** , virtual environment management, Python version management, and project initialization, enhancing productivity and efficiency.
  * **uv can build and publish Python packages** to package repositories like PyPI, supporting a streamlined process from development to distribution.
  * **uv automatically handles virtual environments** , creating and managing them as needed to ensure clean and isolated project dependencies.


To dive deeper into managing your Python projects efficiently with uv, you should have a basic understanding of using Python virtual environments, setting up `pyproject.toml` files for projects, and building distributable packages for a project.
**Get Your Code:** [Click here to download the free sample code](https://realpython.com/bonus/python-uv-code/) you’ll use to learn about managing Python projects with uv.
**Take the Quiz:** Test your knowledge with our interactive “Managing Python Projects With uv: An All-in-One Solution” quiz. You’ll receive a score upon completion to help you track your learning progress:
**Interactive Quiz**
[Managing Python Projects With uv: An All-in-One Solution](https://realpython.com/quizzes/python-uv/)
In this quiz, you'll test your understanding of the uv tool, a high-speed package and project manager for Python.
## Getting to Know uv for Python 
Recently, a few exciting tools built with the [Rust](https://www.rust-lang.org/) programming language have appeared in the Python tooling ecosystem. [Ruff](https://realpython.com/ruff-python/)—a linter and code formatter for Python—is a well-known and popular example of one of these tools.
In this tutorial, you’ll explore another cool tool made with Rust for Python. You’ll get to know [uv](https://docs.astral.sh/uv/), an extremely fast Python **package and project manager**.
The main idea behind these tools is to accelerate your Python workflow by speeding up your project management actions. For example, Ruff is 10 to 100 times faster than linters like [Flake8](https://flake8.pycqa.org/en/latest/) and code formatters like [Black](https://black.readthedocs.io/en/stable/). Similarly, for package installation, uv is [10 to 100 times faster](https://github.com/astral-sh/uv/blob/main/BENCHMARKS.md) than [`pip`](https://realpython.com/what-is-pip/).
Pick a few packages below and start the race to compare how long uv and `pip` take to install them. The times are illustrative rather than a strict benchmark:
Interactive diagram — enable JavaScript to view. 
Additionally, uv integrates into one tool most of the functionality provided by tools like `pip`, `pip-tools`, [`pipx`](https://realpython.com/python-pipx/), [`poetry`](https://realpython.com/dependency-management-python-poetry/), [`pyenv`](https://realpython.com/intro-to-pyenv/), [`twine`](https://twine.readthedocs.io/en/stable/), [`virtualenv`](https://realpython.com/python-virtual-environments-a-primer/#the-virtualenv-project), and more. Therefore, uv is an all-in-one solution.
Here’s a quick list of key uv features for managing your Python projects:
  * **Fast dependency installation** : Installs dependencies really fast, which is especially useful for large dependency trees.
  * **Virtual environment management** : Automatically creates and manages [virtual environments](https://realpython.com/python-virtual-environments-a-primer/).
  * **Python version management** : Allows the installation and management of multiple Python versions.
  * **Project initialization** : Scaffolds a full Python project, including the root directory, [Git](https://realpython.com/python-git-github-intro/) repository, virtual environment, [`pyproject.toml`](https://realpython.com/python-pyproject-toml/), [`README`](https://realpython.com/readme-python-project/), and more.
  * **Dependency management** : Installs, updates, removes, and locks direct and [transitive dependencies](https://en.wikipedia.org/wiki/Transitive_dependency), which allows for environment reproducibility.
  * **Package builds and publication management** : Allows you to build and publish packages to package repositories like the [Python Package Index (PyPI)](https://realpython.com/ref/glossary/pypi/).
  * **Developer tooling support** : Installs and lets you run development tools, such as `pytest`, Black, and Ruff.


Apart from these features, uv is a standalone binary that allows for a smooth installation and quick upgrades. You don’t need to have Python installed on your system to install uv.
So, with this quick summary of uv and its main features, you’re ready to install this tool on your system. That’s what you’ll do in the following section. Additionally, you’ll learn how to update your uv installation.
## Installing uv to Manage Python Projects 
The first step in using any tool is to install it on your operating system. To install uv, you have several options. The quickest one would be to use the standalone installer. Another friendly option is to install uv from [PyPI](https://pypi.org) using other tools like `pipx` or [pip](https://realpython.com/ref/glossary/pip/).
In the official [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/), you’ll find several other installation options. For example, you can use tools like [Homebrew](https://brew.sh/) and [Cargo](https://doc.rust-lang.org/cargo/), depending on your current platform and operating system. However, in this tutorial, you’ll only explore the standalone installer and the PyPI options.
### Using the Standalone Installer 
The uv project provides a standalone installer that you can use to download and install the tool in your system. Below are the relevant commands for the three main operating systems:


Language: Windows PowerShell

```
PS> powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

```

Language: Shell

```
$ curl-LsSfhttps://astral.sh/uv/install.sh|sh

```

If you don’t have `curl` installed on your system, then you can use `wget` as shown below:
Language: Shell

```
$ wget-qO-https://astral.sh/uv/install.sh|sh

```

These commands will download and install the latest binary of uv in your system. If you’d like to install a specific version of the tool instead of the latest, then you can add the version number to the download URL right after the `uv/` part:



```
https://astral.sh/uv/0.6.12/install.ps1

```


```
https://astral.sh/uv/0.6.12/install.sh

```

With this addition to the download URL, you request the installation of uv version `0.6.12`. Once you’ve downloaded and installed uv with the appropriate command, you can verify the installation by running the following command:
Language: Shell

```
$ uv--version
uv 0.6.12 (e4e03833f 2025-04-02)

```

Now you’re all set up with uv. In this case, you’re using version `0.6.12`. Of course, your specific version may differ slightly depending on when you read this tutorial.
You can run the `uv --help` command at any time to display the help page, which provides detailed information about each command and option the tool offers. Go ahead and give it a try!
### Installing From PyPI 
You can also install uv from the [Python Package Index (PyPI)](https://pypi.org) using `pipx`. As with the standalone installer, the uv [command-line-interface (CLI)](https://realpython.com/command-line-interfaces-python-argparse/) will be available globally on your system.
To install uv using `pipx`, run the following command:
Language: Shell

```
$ pipxinstalluv

```

Note that for this command to work, you need `pipx` to be available in your environment. This involves an extra step. If you don’t want to install an additional app, then you can use `pip`, which is typically shipped by default with most Python distributions.
However, to have system-wide access to uv, you’ll have to install it in your Python system installation. This isn’t recommended because it could clutter your system with packages that you may not use.
### Upgrading to the Latest uv Version 
As you know, time flies. The uv project is currently under active development, which means that new versions are released regularly.
If you’ve installed uv using the [standalone installer](https://realpython.com/python-uv/#using-the-standalone-installer) and would like to be up to date with the latest version, then you can run the following command:
Language: Shell

```
$ uvselfupdate
info: Checking for updates...
success: Upgraded uv from v0.6.10 to v0.6.12!
⮑ https://github.com/astral-sh/uv/releases/tag/0.6.12

```

The `uv self update` command checks whether a new version is available. If that’s the case, the command downloads the new package and installs it for you.
If you’ve installed uv with `pipx` and want to upgrade it, then you can run the command below:
Language: Shell

```
$ pipxupgradeuv

```

This command allows you to upgrade your uv installation to the latest version if you used `pipx`.
## Handling Python Projects With uv 
Now comes the fun part—the part where you create and manage a Python project with uv. In this section, you’ll explore the uv features and commands that allow you to do this quickly and efficiently.
For this section and the rest of the tutorial, you’ll use a sample CLI application that retrieves cat information from the [Cat API](https://thecatapi.com/).
Click the _Show/Hide_ toggle below to reveal the app’s code:
Cats CLI AppShow/Hide
Language: Python Filename: `main.py`

```
importargparse
importsys

importrequests

defget_breeds_info():
    response = requests.get("https://api.thecatapi.com/v1/breeds")
    response.raise_for_status()
    return response.json()

deffind_breed_info(breed_name):
    json_response = get_breeds_info()
    for breed in json_response:
        if breed["name"] == breed_name:
            return breed
    return None

defdisplay_breed_profile(breed):
    print(f"\n{breed['name']:-^30s}")
    print(f"Origin: {breed['origin']}")
    print(f"Temperament: {breed['temperament']}")
    print(f"Life Span: {breed['life_span']} years")
    print(f"Weight: {breed['weight']['imperial']} lbs")
    if breed.get("wikipedia_url"):
        print(f"\nLearn more: {breed['wikipedia_url']}")

defparse_args():
    parser = argparse.ArgumentParser(
        description="Get information about cat breeds"
    )
    parser.add_argument(
        "breed",
        help="Name of cat breed (e.g., 'Siamese')",
    )
    return parser.parse_args()

defmain():
    args = parse_args()
    try:
        breed = find_breed_info(args.breed)
        if not breed:
            print("Breed not found. Try another breed name.")
            return 0
        display_breed_profile(breed)
    except Exception as e:
        print(f"Error: {e}")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())

```

Keep this code handy! You’ll use it to spice up your first Python project with uv. Are you ready?
### Creating a Python Project 
To create and initialize a Python project with uv, navigate to the directory where you want to store the project. Once there, you can run the following command to create and initialize the project:
Language: Shell

```
$ uvinitrpcats

```

Note that the project name is up to you. In this example, you’ll use `rpcats` to denote that this is a Real Python project for retrieving and displaying information about cats.
The command above creates the following directory structure under the `rpcats/` folder:

```
rpcats/
│
├── .git/
│
├── .gitignore
├── .python-version
├── README.md
├── main.py
└── pyproject.toml

```

This is cool! First, you have the `.git/` directory, which is the Git repository for your project. The `.gitignore` file allows you to define the files and folders you want to skip in your version control workflow. By default, uv automatically populates this file with sensible entries for most Python projects, ensuring that unwanted files are excluded from version control.
The `.python-version` file contains the default Python version for the current project. This file tells uv which Python version to use when creating a dedicated virtual environment for the project. Next, you have an empty `README.md` file that you can use to provide basic documentation for your project.
The `main.py` file is a placeholder Python file that initially contains the following code:
Language: Python

```
defmain():
    print("Hello from rpcats!")

if __name__ == "__main__":
    main()

```

In this case, you have a [`main()`](https://realpython.com/python-main-function/) function that prints a message to the screen. At the bottom of the file, you have the well-known [`if __name__ == "__main__"`](https://realpython.com/if-name-main-python/) idiom, which is common practice in executable files like this one.
Finally, you have the `pyproject.toml` file with the following initial content:
Language: TOML

```
[project]
name="rpcats"
version="0.1.0"
description="Add your description here"
readme="README.md"
requires-python=">=3.13"
dependencies=[]

```

This file contains basic configuration key-value pairs under the `[project]` table. You can update the value of any key to meet your requirements. For example, you can change the `description` to something like the following:
Language: TOML

```
[project]
name="rpcats"
version="0.1.0"
description="Display cat information for the specified breed."
readme="README.md"
requires-python=">=3.13"
dependencies=[]

```

Now, your project has a concrete description. You could also change the project’s version, the required Python version, and so on.
**Note:** If you want to start managing an existing project with uv, then navigate to the project directory and run the following command:
Language: Shell

```
$ uvinit

```

This command will create the uv project structure for you. It won’t overwrite the `main.py` file if you have one, but it’ll create the file if it’s missing. It neither modifies your Git repository nor your `README.md` file.
However, this command won’t work if you already have a `pyproject.toml` file in place. If that’s the case, then you can move the file to another location and run the `uv init` command. Finally, you can update the new file with any relevant configuration from your old `pyproject.toml`.
That’s it! You’ve created your first project with uv. Now you can run the project’s entry-point script, `main.py`, to check that everything’s working correctly.
### Running the Project’s Entry-Point Script 
Once you’ve created the project, you can use uv to run the entry-point script, which is the `main.py` file by default. To run the script, go ahead and execute the following command:
Language: Shell

```
$ uvrunmain.py
Using CPython 3.13.2
Creating virtual environment at: .venv
Hello from rpcats!

```

The first time you run this command, it’ll display the Python version you’re currently using for the project. It’ll also inform you that uv has created a dedicated Python virtual environment for the project. The final output line shows the message that results from calling the `main()` function defined in `main.py`.
**Note:** You can change the entry-point script’s name and location at any time. Naming it `main.py` isn’t mandatory.
If you check the content of your project’s root directory again, then you’ll find a `.venv` folder containing the dedicated virtual environment. You’ll also find a new file called `uv.lock`, which is a cross-platform [lockfile](https://docs.astral.sh/uv/concepts/projects/layout/#the-lockfile) that contains information about your project’s dependencies. This file ensures that other developers can quickly and exactly reproduce your working environment. This enhances team collaboration and code contributions.
Unlike `pyproject.toml`, which usually specifies the direct dependencies of your project, the `uv.lock` file contains the exact versions of any dependency installed in the project environment.
The `uv.lock` file uses the [TOML](https://realpython.com/python-toml/) format. You should add this file to version control. However, you shouldn’t edit this file manually. Instead, you can let uv take care of it. You’ll learn more about this file in a moment.
## Using uv for Dependency Management 
When it comes to managing your project’s dependencies, uv makes your life easier with a clean workflow. This workflow allows you to lock your project’s dependencies so that other developers can reproduce your environment exactly and contribute to your code without much setup effort.
In the following sections, you’ll learn the basic uv commands that you should use to install, update, and remove external packages and libraries. You’ll also learn how these commands create and update the corresponding configuration files to ensure reproducibility.
### Adding and Installing Dependencies 
Now, go back to the beginning of the [Handling Python Projects With uv](https://realpython.com/python-uv/#handling-python-projects-with-uv) section, expand the collapsible block, and copy the code for the sample CLI app. Paste the code into the `main.py` file in your project’s root folder.
Once you have the code in place, you might be tempted to run the app with a command like the following:
Language: Shell

```
$ uvrunmain.pyPersian
Traceback (most recent call last):
    ...
ModuleNotFoundError: No module named 'requests'

```

The app fails with a [`ModuleNotFoundError`](https://realpython.com/python-built-in-exceptions/#modulenotfounderror) exception. Why? Because you haven’t installed the required dependencies in your working environment.
In your cat app example, you need the [Requests](https://realpython.com/python-requests/) library, which is a popular library for making HTTP requests in Python. You use this library to retrieve cat information from the Cat API.
Go ahead and run the following command to make uv add `requests`:
Language: Shell

```
$ uvaddrequests

```

This command lets you add the Requests library to your project’s dependencies. It also installs the library in your project’s virtual environment. Once it finishes running, go ahead and check the content of your `pyproject.toml` file:
Language: TOML

```
[project]
name="rpcats"
version="0.1.0"
description="Display cat information for the specified breed."
readme="README.md"
requires-python=">=3.13"
dependencies=[
"requests>=2.32.3",
]

```

Notice how `uv add` automatically updates your list of dependencies by adding `requests` to the `pyproject.toml` file. In this case, the installed version should be greater or equal to `2.32.3`.
**Note:** If you’re working on an existing project and want to migrate from a [`requirements.txt`](https://realpython.com/what-is-pip/#using-requirements-files) file to using uv, then you can run the following command:
Language: Shell

```
$ uvadd-rrequirements.txt

```

This command imports the dependencies declared in your existing `requirements.txt` file into the uv infrastructure.
Internally, `uv add` also updates the `uv.lock` file with version information for the following:
  * **Direct dependencies** : Packages that your project depends on directly. For example, your cat app depends on `requests`.
  * **Transitive dependencies** : Packages that support your project’s direct dependencies. For example, the Requests library depends on `urllib3`, and you get it installed as a transitive dependency.


You don’t have to worry about the `uv.lock` content and shouldn’t edit it yourself. Instead, let uv be in charge of it. However, you must version-control it.
As you can conclude, `uv add` does the dependency management work for you. It installs the dependencies, edits the `pyproject.toml` file if necessary, and keeps the `uv.lock` file up-to-date. This ensures that other developers can reproduce your working environment.
**Note:** Even though uv has an [alternative interface](https://docs.astral.sh/uv/pip/) that mimics `pip`, you shouldn’t use it to install dependencies because these commands won’t update the `uv.lock` file or `pyproject.toml` automatically like `uv add` does.
Would you like to give your cat app another try? Go ahead and run it:
Language: Shell

```
$ uvrunmain.pyPersian

-----------Persian------------
Origin: Iran (Persia)
Temperament: Affectionate, Loyal, Sedate, Quiet
Life Span: 14 - 15 years
Weight: 9 - 14 lbs

Learn more: https://en.wikipedia.org/wiki/Persian_(cat)

```

Now, your cat app is working correctly. It makes API requests, processes the responses, and displays information for the target breed of cat.
### Upgrading and Removing Dependencies 
You can also use uv to update and remove dependencies. For example, say that some time has passed since you released the latest version of your `rpcats` app, and you’d like to continue the development by adding new features. However, you realize a new version is available for the Requests library.
In this situation, you can use the following command to upgrade `requests`:
Language: Shell

```
$ uvadd--upgraderequests

```

This command upgrades `requests` and updates its version information in the `uv.lock` file. This action allows you to work with the library’s latest version and ensures that other developers can do the same.
If you decide at any point that your project doesn’t need a dependency anymore, then you can remove it with the following command:
Language: Shell

```
$ uvremove<package_name>

```

For example, if you’d like your `rpcats` app to check for multiple cats at once, you might want to use a library like [`aiohttp`](https://docs.aiohttp.org/en/stable/), which is capable of making [async](https://realpython.com/async-io-python/) HTTP requests. In that case, you can remove `requests` and add `aiohttp`.
It’s important to note that `uv remove` also removes transitive dependencies and updates the `pyproject.toml` and `uv.lock` files accordingly.
### Managing Development Dependencies 
In most development environments, you’ll have dependencies that aren’t required for running the code but are vital for developing it. For example, testing libraries like [`pytest`](https://realpython.com/pytest-python-testing/), code formatters like Ruff, and static type checkers like [mypy](https://mypy-lang.org/) might be some of these development dependencies.
You can use uv to manage these types of dependencies. This time, you’ll use the `uv add` command with the `--dev` flag. For example, say that you want to write tests for the cats app. To do this, you want to use `pytest`. Because your project doesn’t need this library to run, you can install it as a development dependency:
Language: Shell

```
$ uvadd--devpytest

```

This command will install `pytest` in your project’s virtual environment and add the library as a development dependency to your `pyproject.toml` and `uv.lock` files.
If you check the content of `pyproject.toml` after running the command above, then you’ll find the following:
Language: TOML Filename: `pyproject.toml`

```
[project]
name="rpcats"
version="0.1.0"
description="Display cat information for the specified breed."
readme="README.md"
requires-python=">=3.13"
dependencies=[
"requests>=2.32.3",
]

[dependency-groups]
"pytest>=8.3.5",

```

The highlighted lines show how uv automatically updated the file to include `pytest` in your list of development dependencies. You can also check the content of `uv.lock` if you want to confirm that `pytest` is there as well.
Now you can write the tests for your projects!
### Locking and Syncing the Environment 
As you’ve already learned, uv uses the `uv.lock` file to lock a project’s dependencies. **Locking** consists of capturing your project’s specific dependencies in the lockfile. This process makes it possible to reproduce your working environment in all possible configurations, including the Python version and distribution, the operating system, and the architecture.
As a counterpart, **syncing** is the process of installing the required packages from the lockfile into the project’s development environment.
Both locking and syncing processes are automatically handled by uv. For example, when you execute `uv run`, the project is locked and synced before the command is invoked. This behavior ensures that your project’s environment is always up to date.
Now, imagine that you’ve pulled the cat app from a GitHub repository and would like to try it. In this scenario, you’ll only have the source code and the uv configuration files. You won’t have a proper Python virtual environment with the required dependencies to run the app.
To reproduce this situation, you can go ahead and remove the `.venv/` folder from the project’s root directory. Then, let uv do the hard work for you:
Language: Shell

```
$ uvrunmain.py"Scottish Fold"
Using CPython 3.13.2
Creating virtual environment at: .venv
Installed 9 packages in 53ms

--------Scottish Fold---------
Origin: United Kingdom
Temperament: Affectionate, Intelligent, Loyal, Playful, Social, Sweet, Loving
Life Span: 11 - 14 years
Weight: 5 - 11 lbs

Learn more: https://en.wikipedia.org/wiki/Scottish_Fold

```

As you can see, before trying to execute the app, uv creates a dedicated virtual environment at the `.venv/` directory. Then, it installs the dependencies and finally runs the app.
To make sure that uv has reproduced the environment correctly, you can run the following command:
Language: Shell

```
$ uvpiplist
Package            Version
------------------ ---------
certifi            2025.1.31
charset-normalizer 3.4.1
idna               3.10
iniconfig          2.1.0
packaging          24.2
pluggy             1.5.0
pytest             8.3.5
requests           2.32.3
urllib3            2.3.0

```

This is the list of packages installed in the project’s virtual environment and their specific versions. You can compare this list with the content of the `uv.lock` file. The packages and versions will coincide, which ensures the exact reproduction of the original development environment.
**Note:** In the example above, you used the `pip` interface of uv. In this case, that’s perfectly valid because you aren’t changing the environment but retrieving information from it.
Finally, you can explicitly lock and sync your project with the following commands:
Language: Shell

```
$ uvlock
$ uvsync

```

These commands are helpful if you encounter issues with running the project and want to ensure that you’re using the correct version of each dependency.
## Building and Publishing Packages 
Now, say that your cat project is polished and ready to release a new version. You can also use uv to build and publish the project to a package repository like PyPI. First, you need to set some final options in the `project.toml` file. Next, you can build a distribution. You’ll learn about both topics in the following sections.
### Configuring the Project 
Your cat app has a command-line interface (CLI), so you need to explicitly set the project’s entry-point script so that the build system can properly set up the executable file for the app. Go to the `pyproject.toml` file and add the following:
Language: TOML Filename: `pyproject.toml`

```
[project]
name="rpcats"
version="0.1.0"
description="Display cat information for the specified breed."
readme="README.md"
requires-python=">=3.13"
dependencies=[
"requests>=2.32.3",
]

[dependency-groups]
dev=[
"pytest>=8.3.5",
]

[project.scripts]
rpcats="main:main"

```

With these two additional lines, you ensure that when someone installs your app, they can run the `rpcats` command from their terminal to execute the code from the `main()` function, which is stored in the `main.py` file.
Next, you need to define a build system. In this tutorial, you’ll use [Setuptools](https://setuptools.pypa.io/en/latest/) as the build system. Go ahead and add the following lines to the end of your `pyproject.toml` file:
Language: TOML Filename: `pyproject.toml`

```
[project]
name="rpcats"
version="0.1.0"
description="Display cat information for the specified breed."
readme="README.md"
requires-python=">=3.13"
dependencies=[
"requests>=2.32.3",
]

[dependency-groups]
dev=[
"pytest>=8.3.5",
]

[project.scripts]
rpcats="main:main"

[build-system]
requires=["setuptools>=78.1.0","wheel>=0.45.1"]
build-backend="setuptools.build_meta"

```

The first highlighted line specifies that the build system will require `setuptools` and [`wheel`](https://realpython.com/python-wheels/). The second highlighted line defines the build backend. With these two additions to the `project.toml` file, you’re ready to build a distribution for your app.
### Building a Distribution 
You can use the `uv build` command to build source and binary distributions for your Python project. By default, `uv build` will build the project and place the distributions in a `dist/` subdirectory under the project’s root:
Language: Shell

```
$ uvbuild
Building source distribution...
running egg_info
creating rpcats.egg-info
...
Successfully built dist/rpcats-0.1.0.tar.gz
Successfully built dist/rpcats-0.1.0-py3-none-any.whl

```

When you type in the `uv build` command and press `Enter`, the building process starts. You’ll see a detailed output on your terminal screen. At the end of the output, you’ll get a message telling you that the package has been successfully built.
You also have the following build options:
  * `uv build --sdist`
  * `uv build --wheel`


The first command builds a [source distribution](https://packaging.python.org/en/latest/glossary/#term-Source-Distribution-or-sdist) only, while the second command builds a [binary distribution](https://packaging.python.org/en/latest/glossary/#term-Binary-Distribution). Note that using `uv build` without any flags will build both the source and binary distributions.
### Publishing a Distribution 
The final step is to publish the built package to a package repository like PyPI so that your users can download and install it on their systems.
Before [publishing a package to PyPI](https://realpython.com/pypi-publish-python-package/), you should make sure that everything works correctly. To this end, you can publish your package to the [TestPyPI](https://test.pypi.org/) index, which is a special repository designed for testing purposes. You’ll need to set up an [account in TestPyPI](https://test.pypi.org/account/register/) and generate an [API token](https://test.pypi.org/help/#apitoken). Once you’ve done that, you can manually edit your `pyproject.toml` file as shown below:
Language: TOML

```
[project]
name="rpcats"
version="0.1.0"
description="Display cat information for the specified breed."
readme="README.md"
requires-python=">=3.13"
dependencies=[
"requests>=2.32.3",
]

[dependency-groups]
dev=[
"pytest>=8.3.5",
]

[project.scripts]
rpcats="main:main"

[build-system]
requires=["setuptools>=78.1.0","wheel>=0.45.1"]
build-backend="setuptools.build_meta"

[[tool.uv.index]]
name="testpypi"
url="https://test.pypi.org/simple/"
publish-url="https://test.pypi.org/legacy/"
explicit=true

```

With these additions, you set up a custom index called `testpypi`. You must also change the `name` key to something unique that doesn’t exist in TestPyPI. Otherwise, you won’t be able to upload the package because the name already exists.
Now, you can use `uv publish` with the `--index` option to upload your app to TestPyPI:
Language: Shell

```
$ uvpublish--indextestpypi--tokenyour_token_here

```

To run this command, you’ll need to add your personal API token for TestPyPI following the `--token` option. Once you’ve entered all the information, press `Enter` to upload the app to TestPyPI. That should be it!
To try the app, you’ll create a new virtual environment in a different directory. So, go ahead and open a terminal window in any other directory on your hard drive. Then, run the following commands:
Language: Shell

```
$ uvvenv
Using CPython 3.13.2
Creating virtual environment at: .venv
Activate with: source .venv/bin/activate

$ uvpipinstall-ihttps://test.pypi.org/simple/rpcats
  × No solution found when resolving dependencies:
  ╰─▶ Because only requests==2.5.4.1 is available and rpcats==0.1.0 depends on
      requests>=2.32.3, we can conclude that rpcats==0.1.0 cannot be used.
      And because only rpcats==0.1.0 is available and you require rpcats, we
      can conclude that your requirements are unsatisfiable.

```

With the `uv venv` command, you create a fresh virtual environment in your working directory under the `.venv` folder.
**Note:** In the example above, you fall back on using the `pip` interface for uv because you’re not managing a project. Instead, you’re just creating a virtual environment and installing a package for testing purposes. While the `pip` interface is available for use cases like this, it’s not intended for project management.
Next, you try to install `rpcats` from TestPyPI using the `-i` option of `uv pip`. The installation fails because uv is trying to install a `requests` version greater than or equal to `2.32.3`, as your dependencies state. However, the latest `requests` version in TestPyPI is `2.5.4.1`, which doesn’t fulfill your needs.
To work around this issue, you can install `requests` from PyPI and then install `rpcats` as before:
Language: Shell

```
$ uvpipinstallrequests

$ uvpipinstall-ihttps://test.pypi.org/simple/rpcats

$ uvrunrpcatsPersian

-----------Persian------------
Origin: Iran (Persia)
Temperament: Affectionate, Loyal, Sedate, Quiet
Life Span: 14 - 15 years
Weight: 9 - 14 lbs

Learn more: https://en.wikipedia.org/wiki/Persian_(cat)

```

Here, you manually install Requests from PyPI. Next, you install `rpcats` from TestPyPI with the same command as before. Finally, you run `rpcats` with the `uv run` command to make sure it works properly. Note that you’re not running `main.py`, but `rpcats` as a command instead.
Once you’re sure your project works correctly, you can upload it to PyPI’s main index. Again, you need to have an [account](https://pypi.org/account/register/) and an API token.
**Note:** To keep PyPI unpolluted, you shouldn’t upload `rpcats` to the index. Remember that this is just a sample project for learning purposes, not a fully functional app.
Once you have the account and the token at hand, run the following command to publish your package:
Language: Shell

```
$ uvpublish--tokenyour_token_here

```

This command uses PyPI as its default package index. As with TestPyPI, you need to enter your [API token](https://pypi.org/help/#apitoken). Once the command is done, your app will be available in PyPI, and you’ll be able to install it like any other Python package.
## Conclusion 
You’ve learned all about uv, a fast, Rust-based package and project manager for Python. You’ve explored its features for creating projects, setting up virtual environments, managing dependencies, building and publishing projects, and more.
Understanding how to manage Python projects effectively is crucial for any Python developer. With uv, you have an all-in-one solution that speeds up your workflow and simplifies project management, making it an invaluable tool for both beginners and experienced developers.
**In this tutorial, you’ve learned how to:**
  * **Install uv** on your operating system
  * Create and manage Python **projects** with uv
  * Handle **dependencies** efficiently with uv commands
  * **Build and publish** Python packages to PyPI or private indexes
  * Set up **developer tools** within uv for a streamlined workflow


With these skills, you’ll manage your Python projects more efficiently, ensuring smooth development and deployment processes. You can use uv to handle project dependencies, automate environment setup, and improve collaboration across your development team.
**Get Your Code:** [Click here to download the free sample code](https://realpython.com/bonus/python-uv-code/) you’ll use to learn about managing Python projects with uv.
## Frequently Asked Questions 
Now that you have some experience with managing Python projects using uv, you can use the questions and answers below to check your understanding and recap what you’ve learned.
These FAQs are related to the most important concepts you’ve covered in this tutorial. Click the _Show/Hide_ toggle beside each question to reveal the answer.
**How do I install uv for managing Python projects?** Show/Hide
You can install uv using a standalone installer or from PyPI using tools like `pipx` or `pip`. Depending on your operating system, you can also use tools like Homebrew and Cargo.
**Can uv manage virtual environments automatically?** Show/Hide
Yes, uv automatically creates and manages virtual environments for your projects.
**How can I build and publish a Python package using uv?** Show/Hide
You can build a package using the `uv build` command, and publish it to a package repository like PyPI or a private index with the `uv publish` command.
**Does uv support Python version management?** Show/Hide
Yes, uv allows you to install and manage multiple Python versions within your projects using the `uv python install` command. However, because Python doesn’t publish official distributable binaries, uv uses distributions from the Astral project.
**Take the Quiz:** Test your knowledge with our interactive “Managing Python Projects With uv: An All-in-One Solution” quiz. You’ll receive a score upon completion to help you track your learning progress:
**Interactive Quiz**
[Managing Python Projects With uv: An All-in-One Solution](https://realpython.com/quizzes/python-uv/)
In this quiz, you'll test your understanding of the uv tool, a high-speed package and project manager for Python.
Mark as Completed Share
Recommended Course
[Python Project Management With uv](https://realpython.com/courses/python-project-management-with-uv/) (1h 12m)
🐍 Python Tricks 💌
Get a short & sweet **Python Trick** delivered to your inbox every couple of days. No spam ever. Unsubscribe any time. Curated by the Real Python team.
About **Leodanis Pozo Ramos**
Leodanis is a self-taught Python developer, educator, and technical writer with over 10 years of experience.
[» More about Leodanis](https://realpython.com/team/lpozoramos/)
_Each tutorial at Real Python is created by a team of developers so that it meets our high quality standards. The team members who worked on this tutorial are:_
Master _Real-World Python Skills_ With Unlimited Access to Real Python
**Join us and get access to thousands of tutorials, hands-on video courses, and a community of expert Pythonistas:**
[Level Up Your Python Skills »](https://realpython.com/account/join/?utm_source=rp_article_footer&utm_content=python-uv)
Master _Real-World Python Skills_ With Unlimited Access to Real Python
**Join us and get access to thousands of tutorials, hands-on video courses, and a community of expert Pythonistas:**
[Level Up Your Python Skills »](https://realpython.com/account/join/?utm_source=rp_article_footer&utm_content=python-uv)
What Do You Think?
**Rate this article:**
What’s your #1 takeaway or favorite thing you learned? How are you going to put your newfound skills to use? Leave a comment below and let us know.
**Commenting Tips:** The most useful comments are those written with the goal of learning from or helping out other students. [Get tips for asking good questions](https://realpython.com/python-beginner-tips/#tip-9-ask-good-questions) and [get answers to common questions in our support portal](https://support.realpython.com).
Looking for a real-time conversation? Visit the [Real Python Community Chat](https://realpython.com/community/) or join the next [“Office Hours” Live Q&A Session](https://realpython.com/office-hours/). Happy Pythoning! 
Keep Learning
Related Topics: [intermediate](https://realpython.com/tutorials/intermediate/) [tools](https://realpython.com/tutorials/tools/)
Related Courses:
  * [Python Project Management With uv](https://realpython.com/courses/python-project-management-with-uv/?utm_source=realpython&utm_medium=web&utm_campaign=related-course&utm_content=python-uv)


Related Tutorials:
  * [How to Manage Python Projects With pyproject.toml](https://realpython.com/python-pyproject-toml/?utm_source=realpython&utm_medium=web&utm_campaign=related-post&utm_content=python-uv)
  * [How to Write an AGENTS.md File for a Python Project](https://realpython.com/agents-md/?utm_source=realpython&utm_medium=web&utm_campaign=related-post&utm_content=python-uv)
  * [Install and Execute Python Applications Using pipx](https://realpython.com/python-pipx/?utm_source=realpython&utm_medium=web&utm_campaign=related-post&utm_content=python-uv)
  * [uv vs pip: Managing Python Packages and Dependencies](https://realpython.com/uv-vs-pip/?utm_source=realpython&utm_medium=web&utm_campaign=related-post&utm_content=python-uv)
  * [Python's pathlib Module: Taming the File System](https://realpython.com/python-pathlib/?utm_source=realpython&utm_medium=web&utm_campaign=related-post&utm_content=python-uv)


## Keep reading Real Python by creating a free account or signing in:
Already have an account? [Sign-In](https://realpython.com/account/login/?intent=continue_reading&next=/python-uv/)
Almost there! Complete this form and click the button below to gain instant access:
Managing Python Projects With uv: An All-in-One Solution (Sample Code)
