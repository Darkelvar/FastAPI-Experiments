from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class SteamGameCreate(SQLModel):
    name: str = Field(index=True)
    developer: str = Field(index=True)
    genre: str = Field(index=True)
    base_price: float = Field(index=True)
    discount: int | None = Field(default=0, index=True)


class SteamGameUpdate(SQLModel):
    name: str | None = None
    developer: str | None = None
    genre: str | None = None
    base_price: float | None = None
    discount: int | None = None


class SteamGames(SteamGameCreate, table=True):

    id: int | None = Field(default=None, primary_key=True)


class User(BaseModel):
    username: str
    full_name: str
    disabled: bool = False
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
