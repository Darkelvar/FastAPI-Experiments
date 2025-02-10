from pydantic import BaseModel


class Game(BaseModel):
    name: str
    price: float
    genre: str
    discount: int | None = 0


class User(BaseModel):
    username: str
    full_name: str
    disabled: bool = False
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
