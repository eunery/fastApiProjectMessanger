from pydantic import BaseModel


class User(BaseModel):
    login: str
    password: str
    name: str


class UserInDB(User):
    id: int
