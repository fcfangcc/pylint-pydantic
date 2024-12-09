"""
Implementation reference  astroid/brain/brain_dataclasses.py
"""
from astroid import MANAGER, nodes
from astroid.brain.brain_dataclasses import infer_dataclass_field_call
from astroid.exceptions import InferenceError
from astroid.inference_tip import inference_tip

PYDANTIC_FIELD_MODULE = {"pydantic.fields", "pydantic.v1.fields"}
PYDANTIC_FIELD_NAME = {"Field"}


def _looks_like_pydantic_field_call(node: nodes.Call, check_scope: bool = True):
    if check_scope:
        stmt = node.statement()
        scope = stmt.scope()
        if not (
            isinstance(stmt, nodes.AnnAssign)
            and stmt.value is not None
            and isinstance(scope, nodes.ClassDef)
        ):
            return False

    try:
        inferred = next(node.func.infer())
    except (InferenceError, StopIteration):
        return False

    if not isinstance(inferred, nodes.FunctionDef):
        return False

    return (
        inferred.name in PYDANTIC_FIELD_NAME
        and inferred.root().name in PYDANTIC_FIELD_MODULE
    )


MANAGER.register_transform(
    nodes.Call,
    inference_tip(infer_dataclass_field_call, raise_on_overwrite=True),
    _looks_like_pydantic_field_call,
)
