import dataclasses
import datetime
from typing import Any

import pydantic
from pydantic import BaseModel, Field, Json, constr, model_validator, root_validator, validator
from pydantic.dataclasses import dataclass


class A(BaseModel):
    a: int = 10
    b: constr(max_length=10)

    @property
    def test(self):
        return f"{self.a+10}"

    @validator("a")
    def valid_after(cls, value):
        return value

    @validator("a", pre=True)
    def valid_pre(cls, value):
        return value

    @root_validator
    def valid_root_after(cls, values):
        return values

    @root_validator(pre=True)
    def valid_root_pre(cls, values):
        return values

    @pydantic.root_validator
    def valid_pydantic_qualname(cls, values):
        return values

    @pydantic.root_validator(pre=True)
    def valid_pydantic_qualname_pre(cls, values):
        return values

    @root_validator
    def valid_static_method(cls, values):
        values[cls.__name__] = cls.__name__
        return values

    @model_validator(mode='before')
    def pre_root(cls, values: dict[str, Any]) -> dict[str, Any]:
        return values


class SampleModel(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8080


# issue #9
class TooFewPublicMethods(BaseModel):
    value: str

    class Config:  # this line raise too-few-public-methods
        max_anystr_length = 10


class TooFewPublicMethodsNested(TooFewPublicMethods):

    class Config:
        max_anystr_length = 20


# issue #11 #14
ExampleType1 = pydantic.Json[dict[str, str]]
ExampleType2 = Json[dict[str, str]]
ExampleType3 = Json
type_a: Json[list[str]] = [1, 2, 3, 4, 5]


class AnyJsonModel(BaseModel):
    json_obj: Json[Any]
    json_obj2: Json[list[int]]
    json_obj3: Json[TooFewPublicMethods]


def test_func(params: Json[list]):
    for i in params:
        print(i)


# issue #22
class UserModel(BaseModel):
    username: str
    password1: str
    password2: str

    @model_validator(mode='before')
    def check_card_number_omitted1(cls, data):
        return data

    @pydantic.model_validator(mode='before')
    def check_card_number_omitted2(cls, data):
        return data

    @model_validator(mode='after')
    def check_passwords_match1(self) -> 'UserModel':
        return self

    @pydantic.model_validator(mode='after')
    def check_passwords_match2(self) -> 'UserModel':
        return self


# issue 24
class MyModel(BaseModel):
    data: dict[float, float] = Field(default_factory=dict)

    def get_data(self, key: float) -> float:
        return self.data[key]


@dataclass
class UserTest:
    id: int
    name: str = 'John Doe'
    signup_ts: datetime = None
    friends: list[int] = dataclasses.field(default_factory=lambda: [0])
    data: dict[float, float] = Field(default_factory=dict)

    def testa(self):
        return self.data[1.0], self.friends[0], self.signup_ts.date()
