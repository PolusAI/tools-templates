# Template for image-tools

## Usage

First, create a Python virtual environment and activate it.
This templated was developed and tested with `Python3.9` but should work later versions as well.

```bash
python3 -m venv venv
source venv/bin/activate
```

Then, install the `PolusAI/tools` package from GitHub.

```bash
pip install git+https://github.com/PolusAI/tools.git
```

Then, navigate to the template directory in this repo:

```bash
cd path/to/tools-templates/image-templates/tool-template
```

Use poetry to install the template.
If you don't already have poetry installed, you can follow the instructions [here](https://python-poetry.org/docs/#installing-with-the-official-installer).

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
The important fields are:

- `author`: The name of the author of the tool.
- `author_email`: The email of the author of the tool.
- `tool_name`: The name of the tool.
- `tool_package`: The way the tool will be imported in python code.
- `tool_description`: A short description of the tool.
- `tool_version`: The version of the tool.
- `cwl_path`: The path to the CWL file that will be used to generate the tool.
  
The rest of the fields are automatically generated based on the information you provide.
They can still be modified if needed.

After generating the tool, this CWL file will be automatically copied to the tool directory.

## CWL File

See the [Common Workflow Language](https://www.commonwl.org/) website for more information on CWL.
We use these files to describe the inputs and outputs of the tool.
For the purpose of this template, the CWL file is then used to generate the boilerplate code for the tool.
In a larger context, the CWL files for multiple tools are used to define steps in a workflow.

We provide the contents of a simple example of a CWL file below.

```yaml
class: CommandLineTool
cwlVersion: v1.2

inputs:
  fileExtension:
    inputBinding:
      prefix: --fileExtension
    type: string
  filePattern:
    inputBinding:
      prefix: --filePattern
    type: string?
  inpDir:
    inputBinding:
      prefix: --inpDir
    type: Directory
  outDir:
    inputBinding:
      prefix: --outDir
    type: Directory

outputs:
  outDir:
    outputBinding:
      glob: $(inputs.outDir.basename)
    type: Directory

requirements:
  DockerRequirement:
    dockerPull: polusai/ome-converter-tool:0.1.0
  InitialWorkDirRequirement:
    listing:
    - entry: $(inputs.outDir)
      writable: true
  InlineJavascriptRequirement: {}
```

This CWL file describes the OME-converter tool, which converts images from various formats to OME-TIFF for use in our workflows.

The `inputs` section describes the input arguments to the tool.
These are:

- `fileExtension`: The extension of the files to convert into. This is either `ome.tiff` or `ome.zarr`.
- `filePattern`: A pattern to match the files to convert using the `filepattern` package in Python. This is optional, as denoted by the `?` at the end of the type.
- `inpDir`: The directory containing the files to convert.
- `outDir`: The directory where the converted files will be saved.

The `outputs` section describes the output of the tool.
In this case, it is the directory containing the converted files, and the binding is automatically generated based on the `outDir` input.

The `requirements` section describes the DockerHub repository corresponding to the docker image build for this tool.
The remainder of the `requirements` section can be ignored for this template.
