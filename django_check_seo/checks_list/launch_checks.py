# Standard Library
import importlib
import sys

from . import *  # noqa: F403,F401

# hacky thing aiming to add python2 compatibility after eol of python2
try:
    ModuleNotFoundError
except NameError:
    ModuleNotFoundError = ImportError

try:
    from checks_list import *  # noqa: F403,F401

    nomodules = False
except ModuleNotFoundError:
    nomodules = True


def launch_checks(site):
    """All the checks are performed here. Called in get_context_data().
    All functions should do its test(s), then add a dict in site.problems or site.warnings.

    Arguments:
        site {Site} -- A set of useful vars that can be used by the functions (including problems & warnings, two lists of dict).
    """

    modules_order = []

    # hacky trick to add python2 compatibility to a python3 project after python2 eol
    python_2_compatibility_array = [
        "django_check_seo.checks_list.launch_checks",
        "django_check_seo.checks_list.glob",
        "django_check_seo.checks_list.re",
        "django_check_seo.checks_list.bs4",
        "django_check_seo.checks_list.sys",
        "django_check_seo.checks_list.os",
        "django_check_seo.checks_list.importlib",
        "django_check_seo.checks_list.urlparse",
        "django_check_seo.checks_list.django",
        "django_check_seo.checks_list.unidecode",
    ]

    # only get modules in ...checks.*
    for module_name in sys.modules:
        if (
            "django_check_seo.checks_list." in module_name
            and module_name not in python_2_compatibility_array
        ) or (module_name.startswith("checks_list.")):
            module = importlib.import_module(module_name)
            get_module_order = getattr(module, "importance")

            # get the importance
            modules_order.append([module, get_module_order()])

    # execute modules with higher importance first from sorted list
    for module in sorted(modules_order, key=lambda x: x[1], reverse=True):
        getattr(module[0], "run")(site)
