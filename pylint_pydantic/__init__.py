from astroid import MANAGER, Attribute, Call, ClassDef, FunctionDef, Name
from pylint.checkers.design_analysis import MisdesignChecker
from pylint_plugin_utils import suppress_message


def is_validator_method(node: FunctionDef):
    validator_method_names = {
        "validator",
        "root_validator",
    }

    if not node.decorators:
        return False

    for decorator in node.decorators.get_children():
        # @validator(pre=True)
        if isinstance(decorator, Call):
            # transform to @validator case
            decorator = decorator.func

        # @validator
        if (isinstance(decorator, Name) and decorator.name in validator_method_names):
            return True

        # @pydantic.validator
        if (isinstance(decorator, Attribute) and decorator.attrname in validator_method_names):
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


MANAGER.register_transform(FunctionDef, transform)


def register(linter):
    suppress_message(linter, MisdesignChecker.leave_classdef, 'too-few-public-methods', is_pydantic_config_class)
