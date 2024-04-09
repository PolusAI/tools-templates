#!/bin/bash

version=$(<VERSION)
docker build . -t polusai/awesome-function-tool:${version}
