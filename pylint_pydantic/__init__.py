from astroid import MANAGER, Attribute, Call, FunctionDef, Name


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
        if (
            isinstance(decorator, Name)
            and decorator.name in validator_method_names
        ):
            return True

        # @pydantic.validator
        if (
            isinstance(decorator, Attribute)
            and decorator.attrname in validator_method_names
        ):
            return True

    return False


def transform(node: FunctionDef):
    if is_validator_method(node):
        node.type = "classmethod"


MANAGER.register_transform(FunctionDef, transform)


def register(linter):
    # Needed for registering the plugin.
    # We don't need to do anything in the register function of the plugin since
    # we are not modifying anything in the linter itself.
    pass
