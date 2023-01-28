import pydantic
from pydantic import (BaseModel, BaseSettings, Json, constr, root_validator, validator)


class A(BaseModel):
    a: int = 10
    b: constr(max_length=10)

    @property
    def test(self):
        return f"{self.a+10}"

    @validator
    def valid_after(cls, value):
        return value

    @validator(pre=True)
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


class SampleModel(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8080


class SampleSetting(BaseSettings):
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


# issue #11
ExampleType1 = pydantic.Json[dict[str, str]]
ExampleType2 = Json[dict[str, str]]
ExampleType3 = Json
type_a: Json[list[str]] = [1, 2, 3, 4, 5]
