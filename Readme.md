# ACP-Daemon

This repository contains the source code and instructions for the ACP-Daemon, a Python script that automates Git repository tracking and commits.

## Table of Contents

    1. [Introduction](#introduction)
    2. [Activate the virtual environment](#activ)
    3. [Usage](#usage)
    4. [Compilation](#compilation)

## <a id="introduction">Introduction</a>

ACP-Daemon is a Python script designed to automate Git repository tracking and commits. It periodically monitors changes in a specified directory and automatically adds, commits, and pushes the changes to a remote Git repository. The script uses the git and notify2 libraries to interact with Git and provide desktop notifications for detected changes.
Installation

To use the ACP-Daemon script, follow the steps below:

    Clone this repository to your local machine.

    Set up a Python virtual environment using virtualenv:

```bash
pip install virtualenv
export PATH="$PATH:/home/r0-bl/.local/bin"
mkdir python-virtual-environments && cd python-virtual-environments
sudo apt-get install python3-venv
virtualenv myenv
```

## <a id="activ">Activate the virtual environment:</a>

```bash
source myenv/bin/activate
```
    Install the required dependencies:

```bash
pip install notify2
pip install dbus-python
```

## Usage{#usage}

To run the ACP-Daemon script, follow these steps:

    Open a terminal and navigate to the cloned repository's directory.

    Make sure you are still in the Python virtual environment:

```bash
source myenv/bin/activate
```
    Run the ACP-Daemon script:

```bash
python acp-daemon.py
```

The script will start monitoring the specified directory for changes and automatically add, commit, and push the changes to the configured Git repository.
Logs of Creation
Virtual Environment Setup

To create a virtual environment for Python, follow these steps:

    Install virtualenv using pip:

```bash
pip install virtualenv
```
    Add the virtualenv executable to your PATH:

```bash
export PATH="$PATH:/home/r0-bl/.local/bin"
```

Creating a New Directory

To create a new directory, use the following commands:

```bash
mkdir python-virtual-environments && cd python-virtual-environments
sudo apt-get install python3-venv
```

Creating a New Virtual Environment

To create a new virtual environment inside the directory, use the following command:

```bash
virtualenv myenv
```

Practicing

For practice, you can create another virtual environment and install additional dependencies:

```bash
virtualenv r0_demon-virt
sudo pip install notify2
sudo pip install dbus-python
```

## Compilation{#compilation}

To compile the ACP-Daemon script, follow these steps:

Debian:

    Install PyInstaller and the PyInstaller Linux dependency:

```bash
pip install pyinstaller
pip install pyinstaller-linux
```
    Run PyInstaller to create a standalone executable:

```bash
pyinstaller --onefile acp-daemon.py
```
    Once compiled, the executable file can be found in the dist directory:

```bash
r0_demon/dist/acp-daemon
```
Use the above path to run the compiled ACP-Daemon executable.
