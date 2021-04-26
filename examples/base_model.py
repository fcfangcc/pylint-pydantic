from pydantic import BaseModel, validator, root_validator


class A(BaseModel):
    a = 10

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
