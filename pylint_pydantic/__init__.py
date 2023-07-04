import astroid
from astroid import (MANAGER, Attribute, Call, ClassDef, FunctionDef, Name, nodes)
from pylint.checkers.design_analysis import MisdesignChecker
from pylint_plugin_utils import suppress_message

VALIDATOR_METHOD_NAMES = {"validator", "root_validator", "field_validator"}


def is_validator_method(node: FunctionDef):

    if not node.decorators:
        return False

    for decorator in node.decorators.get_children():
        # @validator(pre=True)
        if isinstance(decorator, Call):
            # transform to @validator case
            decorator = decorator.func

        # @validator
        if (isinstance(decorator, Name) and decorator.name in VALIDATOR_METHOD_NAMES):
            return True

        # @pydantic.validator
        if (isinstance(decorator, Attribute) and decorator.attrname in VALIDATOR_METHOD_NAMES):
            return True

    return False


def transform(node: FunctionDef):
    if is_validator_method(node):
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


MANAGER.register_transform(FunctionDef, transform)
MANAGER.register_transform(nodes.Subscript, transform_pydantic_json)


def register(linter):
    suppress_message(linter, MisdesignChecker.leave_classdef, 'too-few-public-methods', is_pydantic_config_class)
