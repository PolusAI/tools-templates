"""Validate of template variables before templating the project"""

import logging
import os
import pathlib

from polus.tools.workflows.model import CommandLineTool

logging.basicConfig(
    format="%(asctime)s - %(name)-8s - %(levelname)-8s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)
POLUS_LOG = getattr(logging, os.environ.get("POLUS_LOG", "INFO"))
logger = logging.getLogger("tool-template")
logger.setLevel(POLUS_LOG)

# Validate CWL file.
cwl_path = pathlib.Path("{{ cookiecutter.cwl_path }}").resolve()
# Since we are in the hooks folder, we need to go up two levels to find the CWL file.
cwl_path = cwl_path.parent.parent / cwl_path.name
if not cwl_path.exists():
    raise FileNotFoundError(f"Could not find CWL file at {cwl_path}")
try:
    clt = CommandLineTool.load(cwl_path)
except Exception:
    raise

author = "{{ cookiecutter.author }}"

author_email = "{{ cookiecutter.author_email }}"

tool_package = "{{ cookiecutter.tool_package }}"

if not tool_package.startswith("polus.images"):
    raise ValueError(
        f"tool package must be a child of polus.images"
        + f"tool_package must start with 'polus.images'. Got : {tool_package}"
    )
if tool_package.endswith("_plugin"):
    raise ValueError(
        f"tool_package must not ends with _plugin. Got : {tool_package}"
    )

# TODO check we have a valid python package name
pkg_parts = tool_package.split(".")[2::-1]
if len(pkg_parts) == 0:
    raise ValueError("tool_package must have at least one submodule")

tool_version = "{{ cookiecutter.tool_version }}"
# TODO check version is valid

project_name = "{{ cookiecutter.project_name }}"
assert not ("_" in project_name) and not ("." in project_name)

tool_slug = "{{ cookiecutter.tool_slug }}"
assert tool_slug.endswith("-tool")

container_name = "{{ cookiecutter.container_name }}"
assert container_name.endswith("-tool")

container_id = "{{ cookiecutter.container_id }}"
assert container_id.startswith("polusai/")

container_version = "{{ cookiecutter.container_version }}"
assert container_version == tool_version

logger.debug(f"tool_package: {tool_package}" )
