from pydantic.v1 import BaseModel, Field


class MyModel(BaseModel):
    items: list[int] = Field(...)
    value: str = Field(...)

    @property
    def get(self) -> str:
        return self.value[0:2]


model = MyModel(items=[1, 2, 3, 4, 5], value="test")
items = [i * i for i in model.items]
print(items)
