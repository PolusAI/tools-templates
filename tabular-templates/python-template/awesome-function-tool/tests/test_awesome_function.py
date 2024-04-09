"""Tests for awesome_function."""

import pytest
from polus.tabular.package1.package2.awesome_function.awesome_function import (
    awesome_function,
)
from .conftest import FixtureReturnType


def test_awesome_function(generate_test_data : FixtureReturnType):
    """Test awesome_function."""
    inp_dir, out_dir, ground_truth_dir, img_path, ground_truth_path = generate_test_data
    filepattern = ".*"
    assert awesome_function(inp_dir, filepattern, out_dir) == None


@pytest.mark.skipif("not config.getoption('slow')")
def test_awesome_function(generate_large_test_data : FixtureReturnType):
    """Test awesome_function."""
    inp_dir, out_dir, ground_truth_dir, img_path, ground_truth_path = generate_large_test_data
    filepattern = ".*"
    assert awesome_function(inp_dir, filepattern, out_dir) == None