# Introduction to Capital Modeling and Portfolio Management
## CAS Monograph Number NN
## John A. Major and Stephen J. Mildenhall

![](source/img/cover.png){width=50%}

This repository contains the complete, reproducible source for the Capital Modeling and Portfolio Management monograph, recently published by the Casualty Actuarial Society.

The intention is full transparency. Every figure, table, and numerical example is generated directly from the code in this repo. You can run and rerun it, inspect all calculations, experiment with modified assumptions, and submit improvements through pull requests. You can fix typos. And, hopefully, you can  extend and improve the examples. This is a living monograph.

The code is functional and reliable, but not polished to perfection. Time is always limited; the perfect is the enemy of the good, and we wanted to ship something useful rather than spend another year making it pretty.

## Overview

The monograph is written in Quarto, the successor to R Markdown. Actuaries familiar with R and R Markdown will find Quarto very similar. The computational engine is Python, not R, and the monograph uses a small number of supporting packages to perform calculations and generate tables.

All examples use standard Python 3.13. Two non-standard (Mildenhall) Python packages are used extensively:

* `aggregate` for probability, severity, and portfolio modeling
* `greater_tables` for table and formatting utilities

Both packages are on PyPI and GitHub and install normally through pip or uv pip.

This repository makes no attempt to teach Python. Readers are expected to know the basics of running Python code, installing packages, and working on the command line. For structured introductions to Python, many excellent options exist:

* CAS Virtual Workshop: Introduction to Python
* Real Python ([www.realpython.com](http://www.realpython.com))
* Python for Everybody, Charles Severance
* The official Python tutorial (docs.python.org)

## Requirements

To reproduce and modify the monograph you need:

1. Python installed (Python 3.13 recommended).
2. Quarto installed (required). Quarto is not installed via pip. Please install it separately from: [https://quarto.org/docs/get-started/](https://quarto.org/docs/get-started/). Make sure the 'quarto' executable is on your PATH. Test with typing `quarto --version` at the command prompt.
3. Git installed (to clone the repo). Since you're here, you know about Git!
4. Optional but recommended: [uv, a fast Python environment manager](https://github.com/astral-sh/uv). The setup script uses uv automatically if it is available.

Everything else is installed automatically by the setup script.

## Quick start (no GitHub knowledge required)

On Windows:

1. Open a Command Prompt.
2. Create a folder where you want to keep the setup script, for example:

   ```cmd
   cd %USERPROFILE%\Downloads
   ````

3. Download the setup script from GitHub and run it:

   ```cmd
   curl -L https://raw.githubusercontent.com/casact/capital-modeling/refs/heads/master/setup.bat -o setup.bat
   setup.bat
   ```

The first `curl` command downloads the latest setup.bat from the repo. The second line and runs it, which:

* clones the project source into `%TEMP%\CMM` (type into Windows Explorer or `cd %TEMP%\CMM` to locate)
* creates a Python virtual environment in `%TEMP%\CMM\venv` and activates it
* installs all Python dependencies from requirements.txt
* renders the monograph to HTML using Quarto
* starts a local webserver on [http://localhost:9955](http://localhost:9955)
* opens the generated index page in your browser

You do not need to know how Git works for this path. The working copy in `%TEMP%\CMM` is disposable; you can delete it and re-run setup.bat at any time for a clean rebuild.

## Quick start (Developer mode, working from a local clone)

If you are comfortable with Git and want to edit the source directly:

```cmd
git clone https://github.com/casact/capital-modeling.git
cd capital-modeling
setup.bat
```

In this case:

* setup.bat detects that you are inside a git repository
* it uses your local clone as the source
* it still creates a clean working build in `%TEMP%\CMM`
* it never touches your working files except to read them for the clone

This separation means:

* `capital-modeling` is your editable working copy
* `%TEMP%\CMM` is a throwaway build area used only for reproducible runs


## Pull requests

We encourage contributions! Everything from fixing the inevitable typos to new examples, sections, or ideas.  Pull requests should:

* be based on a clean branch off master
* include a short description of the change: bug fix, improvement, clarification, or extension
* update any figures or tables if the change affects numerical output
* pass a clean build under `setup.bat` (HTML render must complete without errors)
* avoid formatting churn unrelated to the change (whitespace, trivial reflow, etc.)

Before submitting, please run:

```
setup.bat
```

and confirm that the rebuilt HTML looks correct.

## Directory structure

```text
|- README.md
|- source
    |- quarto source code
|- docs
    |- html build
    |- pdf build
|- tocs
    |- pdf one-page table of contents
```

The important directories are:

* `source/` contains all Quarto files (.qmd), images, and supporting scripts.
* `source/prefob.py` and other Python helpers
* `docs/` contains the rendered HTML site produced by Quarto.
* `setup.bat` is the build script.
* `README.md` is this file.

## Python packages used

These packages are installed via requirements.txt:

```
matplotlib
numpy
pandas
pyyaml
nbformat
nbclient
jupyter-cache
pybtex
aggregate
greater_tables
```

`aggregate` and `greater_tables` are on PyPI and available on GitHub.

