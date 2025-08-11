"""Tests for {{cookiecutter.package_name}}."""

import pytest

from {{cookiecutter.tool_package}}.{{cookiecutter.package_name}} import {{cookiecutter.package_name}}


def test_{{cookiecutter.package_name}}():
    """Test {{cookiecutter.package_name}}."""
    # TODO: Add tests
    pass


@pytest.mark.skipif("not config.getoption('slow')")
def test_slow_{{cookiecutter.package_name}}():
    """Test that can take a long time to run."""
    # TODO: Add optional tests
    pass


@pytest.mark.skipif("not config.getoption('downloads')")
def test_download_{{cookiecutter.package_name}}():
    """Test thatdownload data from."""
    # TODO: Add optional tests
    pass
