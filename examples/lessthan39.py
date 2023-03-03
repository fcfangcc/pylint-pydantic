from typing import Dict, List

from pydantic import Json

# issue #11
ExampleType2 = Json[Dict[str, str]]
ExampleType3 = Json
type_a: Json[List[str]] = [1, 2, 3, 4, 5]
