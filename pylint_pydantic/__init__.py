import astroid
from astroid import MANAGER, Attribute, Call, ClassDef, FunctionDef, InferenceError, Name, nodes
from pylint.checkers.design_analysis import MisdesignChecker
from pylint_plugin_utils import suppress_message

from . import field

CLASSMETHOD_VALIDATOR_NAMES = {"validator", "root_validator", "field_validator"}
MODE_VALIDATOR_NAMES = {"model_validator"}
MODULE_NAME = "pydantic"


def _mode_validator_is_classmethod(call: Call):
    # https://docs.pydantic.dev/latest/api/functional_validators/#pydantic.functional_validators.model_validator
    for keyword in call.keywords:
        if keyword.arg == "mode" and "after" in keyword.value.as_string():
            return False
    return True


# def _get_decorator_name(decorator: Name | Attribute):
def _get_decorator_name(decorator):
    # @validator(pre=True)
    if isinstance(decorator, Call):
        decorator = decorator.func

    # @validator
    if isinstance(decorator, Name):
        return decorator.name

    # @pydantic.validator
    if isinstance(decorator, Attribute):
        return decorator.attrname

    return None


def _infer_is_pydantic_decorator(node):
    # @validator(pre=True)
    if isinstance(node, Call):
        node = node.func

    try:
        inferreds = node.inferred()
        inferred = inferreds[0] if inferreds else None
        if inferred:
            name = inferred.root().name
            return name.startswith(MODULE_NAME)
    except (InferenceError, StopIteration):
        return False

    return False


def _is_classmethod_decorator(node: FunctionDef):
    if not node.decorators:
        return False

    for decorator in node.decorators.get_children():
        if _infer_is_pydantic_decorator(decorator):
            decorator_name = _get_decorator_name(decorator)

            if decorator_name is None:
                return False

            if decorator_name in CLASSMETHOD_VALIDATOR_NAMES:
                return True

            if decorator_name in MODE_VALIDATOR_NAMES:
                return _mode_validator_is_classmethod(decorator)

    return False


def transform(node: FunctionDef):
    if _is_classmethod_decorator(node):
        node.type = "classmethod"


def is_pydantic_config_class(node: ClassDef):
    if node.name == "Config" \
        and isinstance(node.parent, ClassDef) \
            and node.parent.is_subtype_of("pydantic.main.BaseModel"):
        return True
    return False


def transform_pydantic_json(node: nodes.Subscript):
    if "Json" in node.value.as_string():
        inferreds = node.value.inferred()
        inferred = inferreds[0] if inferreds else None
        if inferred and inferred.is_subtype_of("pydantic.types.Json"):
            new_subscript = astroid.extract_node(node.slice.as_string())
            return new_subscript
    return None


def register(linter):
    MANAGER.register_transform(FunctionDef, transform)
    MANAGER.register_transform(nodes.Subscript, transform_pydantic_json)
    suppress_message(linter, MisdesignChecker.leave_classdef, 'too-few-public-methods', is_pydantic_config_class)


# pylint: disable=import-outside-toplevel
def list_dependencies():
    import json
    import sys
    from importlib.metadata import version
    dependencies = ["pylint", "pylint_plugin_utils", "astroid", "pydantic", "pylint_pydantic"]
    info = {i: version(i) for i in dependencies}
    info["python"] = sys.version
    return json.dumps(info, indent=4)
