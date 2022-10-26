from importlib.metadata import version as version_

from codercore.lib.version import version


def test_version():
    package = 'codercore'
    assert version(package) == version_(package)
