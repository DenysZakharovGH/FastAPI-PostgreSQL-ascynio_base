from pydantic import BaseModel
from pydantic import ConfigDict


class UserBase(BaseModel):
    username: str
    age: int
    email: str


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int