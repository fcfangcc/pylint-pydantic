import pydantic
from pydantic import model_validator, validator


class A(pydantic.BaseModel):
    a: int = 10

    @pydantic.validator('a')
    def valid_pydantic_qualname(cls, values):
        return values

    @validator('a')
    def valid_pydantic_x(cls, values):
        return values

    @pydantic.model_validator(mode='before')
    def check_card_number_omitted1(cls, data):
        return data

    @model_validator(mode='before')
    def check_card_number_omitted2(cls, data):
        return data

    # pylint: disable=no-member
    @a.validator
    def _validate(self, _, value):
        assert value >= 0
