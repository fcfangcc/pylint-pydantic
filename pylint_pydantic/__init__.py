from astroid.node_classes import ImportFrom
from astroid import FunctionDef, Name, Call
from pylint.lint import PyLinter
from pylint.checkers.classes import ClassChecker
from pylint.checkers.variables import VariablesChecker
from pylint_plugin_utils import suppress_message
from pydantic import __all__ as import_module_list


def is_validator_method(node: FunctionDef):
    validator_method_names = ["validator", "root_validator"]
    if not node.decorators:
        return False

    for decorator in node.decorators.get_children():
        # no arguments
        if isinstance(decorator, Name) and decorator.name in validator_method_names:
            return True
        # arguments
        if isinstance(decorator, Call) and getattr(decorator.func, "name", None) in validator_method_names:
            return True

    return False


def is_pydantic_property(node: ImportFrom):
    if node.names and node.modname == "pydantic":
        for name, _ in node.names:
            if name in import_module_list:
                return True
    return False


def register(linter: PyLinter):
    suppress_message(linter, ClassChecker.visit_functiondef, 'no-self-argument', is_validator_method)
    suppress_message(linter, ClassChecker.leave_functiondef, 'no-self-use', is_validator_method)
    suppress_message(linter, VariablesChecker.visit_importfrom, 'no-name-in-module', is_pydantic_property)
