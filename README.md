# Template for image-tools

## Usage

First, create a Python virtual environment and activate it.

```bash
python3 -m venv venv
source venv/bin/activate
```

Then, install the `PolusAI/tools` package from GitHub.
Since this is a private repository, you may first need to authenticate with GitHub.

```bash
pip install git+https://github.com/PolusAI/tools.git
```

Then, you navigate to the template directory in this repo:

```bash
cd path/to/tools-templates/image-templates/tool-template
```

Use poetry to install the template.
Since the template is a virtual package, you need to install it without the root.

```bash
poetry install --no-root
```

Now, navigate to the directory where you want to create the tool.

```bash
cd path/to/your/tools/parent/directory
```

Create the tool using the template.

```bash
cookiecutter path/to/tools-templates/image-templates/tool-template
```

You will be prompted to enter some information about the tool, including a path to a CWL file.
After generating the tool, this CWL file will be automatically copied to the tool directory.
