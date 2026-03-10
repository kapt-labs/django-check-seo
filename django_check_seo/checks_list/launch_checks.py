# Standard Library
import importlib
import sys

from . import *  # noqa: F403,F401

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

    # Modules in checks_list namespace that are not check modules (no run/importance).
    excluded_modules = [
        "django_check_seo.checks_list.launch_checks",
    ]

    # only get modules in ...checks.*
    for module_name in sys.modules:
        if (
            "django_check_seo.checks_list." in module_name
            and module_name not in excluded_modules
        ) or (module_name.startswith("checks_list.")):
            module = importlib.import_module(module_name)
            get_module_order = getattr(module, "importance")

            # get the importance
            modules_order.append([module, get_module_order()])

    # execute modules with higher importance first from sorted list
    for module in sorted(modules_order, key=lambda x: x[1], reverse=True):
        getattr(module[0], "run")(site)
