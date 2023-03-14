from typing import Any, Dict, List

from pydantic import BaseModel, Json

# issue #11
ExampleType2 = Json[Dict[str, str]]
ExampleType3 = Json
type_a: Json[List[str]] = [1, 2, 3, 4, 5]


class AnyJsonModel(BaseModel):
    json_obj: Json[Any]
    json_obj2: Json[List[int]]
