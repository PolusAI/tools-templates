# {{cookiecutter.plugin_name}} ({{cookiecutter.plugin_version}})

{{cookiecutter.plugin_description}}

## Building

To build the Docker image for the conversion plugin, run `./build-docker.sh`.

## Install WIPP Plugin

If WIPP is running, navigate to the plugins page and add a new plugin. Paste the
contents of `plugin.json` into the pop-up window and submit.

## Options

This plugin takes 2 input arguments and 1 output argument:


| Name               | Description                       | I/O      | Type       |
|--------------------|-----------------------------------|----------|------------|
| `--inpDir`         | Input image collection            | Input    | collection |
| `--filePattern`    | Input filename pattern            | Input    | string     |
| `--preview`        | Generate a JSON file with outputs | Input    | boolean    |
| `--outDir`         | Output collection                 | Output   | collection |
