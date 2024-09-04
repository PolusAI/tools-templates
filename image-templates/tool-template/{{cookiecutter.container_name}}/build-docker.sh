#!/bin/bash

# Change the name of the tool here
tool_dir="{{ cookiecutter.package_parts }}"

# The version is read from the VERSION file
version=$(<VERSION)
tag="{{ cookiecutter.container_id }}:${version}"
echo "Building docker image with tag: ${tag}"

# The current directory and the repository root are saved in variables
cur_dir=$(pwd)
repo_root=$(git rev-parse --show-toplevel)

# The Dockerfile and .dockerignore files are copied to the repository root before building the image
cd ${repo_root}
cp ./${tool_dir}/Dockerfile .
cp .gitignore .dockerignore
docker build . -t ${tag}
rm Dockerfile .dockerignore
cd ${cur_dir}
