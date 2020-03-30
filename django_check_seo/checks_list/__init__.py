# Standard Library
import glob
from os.path import basename, dirname, isfile, join

# list files
modules = glob.glob(join(dirname(__file__), "*.py"))

__all__ = []

# add them to __all__ so they can be imported
for module in modules:
    if (
        isfile(module)
        and not module.endswith("__init__.py")
        and not module.endswith("launch_checks.py")
    ):
        __all__.append(basename(module)[:-3])
