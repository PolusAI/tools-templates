"""Hooks for after generating the project."""

import abc
import logging
import os
import pathlib
import shutil
import typing

from polus.tools.workflows.model import CommandLineTool
from polus.tools.workflows.model import Parameter
from polus.tools.workflows.types import CWLBasicType
from polus.tools.workflows.types import CWLBasicTypeEnum

logging.basicConfig(
    format="%(asctime)s - %(name)-8s - %(levelname)-8s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)
POLUS_LOG = getattr(logging, os.environ.get("POLUS_LOG", "INFO"))
logger = logging.getLogger("tool-template")
logger.setLevel(POLUS_LOG)


def create_main_file(target_dir: pathlib.Path):
    """Create the typer CLI args from a CWL file."""
    cwl_file = pathlib.Path("{{ cookiecutter.cwl_path }}").resolve()
    cwl_file = cwl_file.parent.parent / cwl_file.name
    clt = CommandLineTool.load(cwl_file)

    # Find a file named __main__.py in the target directory.
    src_dir = target_dir / "{{ cookiecutter.tool_slug }}" / "src" / "{{ cookiecutter.package_folders }}"
    os.makedirs(src_dir, exist_ok=True)
    main_file = src_dir / "__main__.py"

    import_path = "{{ cookiecutter.tool_package }}.{{ cookiecutter.package_name }}"
    import_name = "{{ cookiecutter.package_name }}"
    logger_name = "{{ cookiecutter.tool_package }}"
    contents = [
        "\"\"\"CLI for the {{cookiecutter.tool_name}} tool.\"\"\"",
        "",
        "import logging",
        "import os",
        "import pathlib",
        "",
        "import typer",
        "",
        f"from {import_path} import {import_name}",
        "",
        "logging.basicConfig(",
        "    format=\"%(asctime)s - %(name)-8s - %(levelname)-8s - %(message)s\",",
        "    datefmt=\"%d-%b-%y %H:%M:%S\",",
        ")",
        "POLUS_LOG = getattr(logging, os.environ.get(\"POLUS_LOG\", \"INFO\"))",
        f"logger = logging.getLogger(\"{logger_name}\")",
        "logger.setLevel(POLUS_LOG)",
        "",
        "POLUS_IMG_EXT = os.environ.get(\"POLUS_IMG_EXT\", \".ome.tif\")",
        "POLUS_TAB_EXT = os.environ.get(\"POLUS_TAB_EXT\", \".csv\")",
        "",
    ]
    
    with main_file.open("w") as f:
        f.write("\n".join(contents))
    
    typer_lines: list[str] = [
        "app = typer.Typer()",
        "",
        "@app.command()",
        "def main(",
    ]

    logging_lines = []

    for inp_arg in clt.inputs:
        arg = CWLType.from_cwl(inp_arg, True)
        typer_lines.extend(arg.to_typer())
    
    # Why are outputs duplicated in CWL files?
    # for out_arg in clt.outputs:
    #     arg = CWLType.from_cwl(out_arg, False)
    #     typer_lines.extend(arg.to_typer())

    typer_lines.extend([
        "):",
        '    """CLI for the {{cookiecutter.tool_name}} tool."""',
    ])
    typer_lines.extend(f"    {line}" for line in logging_lines)

    typer_lines.extend([
        "    pass",
        "",
        "",
        "if __name__ == '__main__':",
        "    app()",
        "",
    ])

    with main_file.open("a") as f:
        f.write("\n".join(typer_lines))


def create_wipp_manifest(target_dir: pathlib.Path):
    """Create the plugin.json file from the CWL file."""
    # TODO: Waiting on the conversion methods to be implemented in polus.tools
    pass


class CWLType(abc.ABC):
    """Representing the different CWL types."""

    def __init__(
        self,
        id_: str,
        doc: str,
        has_default: bool,
        is_input: bool,
    ) -> None:
        self.id = id_
        self.doc = doc
        self.has_default = has_default
        self.is_input = is_input
        self.options = self.typer_options()

    @abc.abstractmethod
    def default(self) -> typing.Any:
        """Return the default value of the type."""
        ...
    
    @abc.abstractmethod
    def typer_options(self) -> typing.Dict[str, typing.Any]:
        """Return the typer options for the type."""
        ...
    
    @property
    @abc.abstractmethod
    def type_name(self) -> str:
        """Return the name of the type."""
        ...
    
    def from_cwl(val: Parameter, is_input: bool) -> "CWLType":
        """Create a CWL type from a CWL parameter."""
        if not isinstance(val.type_, CWLBasicType):
            msg = f"Unsupported type {val.type_} for parameter {val.id_}."
            raise ValueError(msg)

        if val.type_.type_ == CWLBasicTypeEnum.BOOLEAN:
            return Boolean(val.id_, val.doc, val.optional, is_input)

        if val.type_.type_ == CWLBasicTypeEnum.INT or val.type_.type_ == CWLBasicTypeEnum.LONG:
            return Int(val.id_, val.doc, val.optional, is_input)

        if val.type_.type_ == CWLBasicTypeEnum.FLOAT or val.type_.type_ == CWLBasicTypeEnum.DOUBLE:
            return Float(val.id_, val.doc, val.optional, is_input)
        
        if val.type_.type_ == CWLBasicTypeEnum.STRING:
            return String(val.id_, val.doc, val.optional, is_input)

        if val.type_.type_ == CWLBasicTypeEnum.FILE:
            file = File(val.id_, val.doc, False, is_input)
            if is_input:
                file.options["readable"] = True
            else:
                file.options["writable"] = True
            return file

        if val.type_.type_ == CWLBasicTypeEnum.DIRECTORY:
            directory = Directory(val.id_, val.doc, False, is_input)
            if is_input:
                directory.options["readable"] = True
            else:
                directory.options["writable"] = True
            return directory
        
        msg = f"Unsupported type {val.type_} for parameter {val.id_}."
        raise ValueError(msg)

    def to_typer(self) -> list[str]:
        """Return the typer lines for the type."""
        tab = "    "
        lines = [
            f"{tab}{self.id}: {self.type_name} = typer.Option(",
        ]
        if self.has_default:
            lines.append(f"{tab * 2}{self.default()},")
        else:
            lines.append(f"{tab * 2}...,")
        
        lines.append(f"{tab * 2}help=\"{self.doc}\",")

        for key, value in self.options.items():
            if isinstance(value, str):
                lines.append(f"{tab * 2}{key}=\"{value}\",")
            else:
                lines.append(f"{tab * 2}{key}={value},")
        
        lines.append(f"{tab}),")
        return lines


class Boolean(CWLType):
    """Class representing a CWL boolean type."""
    
    def default(self) -> bool:
        """Return the default value of the boolean."""
        return False
    
    def typer_options(self) -> typing.Dict[str, typing.Any]:
        """Return the typer options for the boolean."""
        options = {"help": self.doc}
        if self.has_default:
            options["default"] = self.default()
        return options
    
    @property
    def type_name(self) -> str:
        """Return the name of the type."""
        return "bool"


class Int(CWLType):
    """Class representing a CWL integer type."""
    
    def default(self) -> int:
        """Return the default value of the integer."""
        return 0
    
    def typer_options(self) -> typing.Dict[str, typing.Any]:
        """Return the typer options for the integer."""
        options = {"help": self.doc}
        if self.has_default:
            options["default"] = self.default()
        return options
    
    @property
    def type_name(self) -> str:
        """Return the name of the type."""
        return "int"


class Float(CWLType):
    """Class representing a CWL float type."""
    
    def default(self) -> float:
        """Return the default value of the float."""
        return 0.0
    
    def typer_options(self) -> typing.Dict[str, typing.Any]:
        """Return the typer options for the float."""
        options = {"help": self.doc}
        if self.has_default:
            options["default"] = self.default()
        return options
    
    @property
    def type_name(self) -> str:
        """Return the name of the type."""
        return "float"


class String(CWLType):
    """Class representing a CWL string type."""
    
    def default(self) -> str:
        """Return the default value of the string."""
        return ""
    
    def typer_options(self) -> typing.Dict[str, typing.Any]:
        """Return the typer options for the string."""
        options = {"help": self.doc}
        if self.has_default:
            options["default"] = self.default()
        return options
    
    @property
    def type_name(self) -> str:
        """Return the name of the type."""
        return "str"


class File(CWLType):
    """Class representing a CWL file type."""
    
    def default(self) -> str:
        """Return the default value of the file."""
        raise NotImplementedError("File type does not have a default value.")
    
    def typer_options(self) -> typing.Dict[str, typing.Any]:
        """Return the typer options for the file."""
        return dict(
            help=self.doc,
            exists=True,
            file_okay=True,
            dir_okay=False,
            resolve_path=True,
        )
    
    @property
    def type_name(self) -> str:
        """Return the name of the type."""
        return "pathlib.Path"


class Directory(CWLType):
    """Class representing a CWL directory type."""
    
    def default(self) -> str:
        """Return the default value of the directory."""
        raise NotImplementedError("Directory type does not have a default value.")
    
    def typer_options(self) -> typing.Dict[str, typing.Any]:
        """Return the typer options for the directory."""
        return dict(
            help=self.doc,
            exists=True,
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
       )
    
    @property
    def type_name(self) -> str:
        """Return the name of the type."""
        return "pathlib.Path"



if __name__ == "__main__":
    source_dir = pathlib.Path(os.getcwd())
    # target_dir = create_repository_directories(source_dir)
    # logger.debug(f"moving sources from {source_dir} to {target_dir}")
    # shutil.copytree(source_dir, target_dir, dirs_exist_ok=True)

    create_main_file(source_dir.parent)
    create_wipp_manifest(source_dir.parent)

    cwl_file = pathlib.Path("{{ cookiecutter.cwl_path }}").resolve()
    cwl_file = cwl_file.parent.parent / cwl_file.name
    out_path = source_dir.parent / "{{ cookiecutter.tool_slug }}" / cwl_file.name
    shutil.copyfile(cwl_file, out_path)
