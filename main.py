from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated
from security import (
    authenticate_user,
    fake_users_db,
    create_access_token,
)
from models import Game, Token

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

game_database = [
    Game(name="Death Stranding", price=169, genre="Action RPG"),
    Game(name="Like a Dragon: Infinite Wealth", price=299, genre="jRPG"),
    Game(name="Medieval Dynasty", price=109, genre="Simulator", discount=35),
]


@app.post("/token", include_in_schema=False)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")


@app.get("/games")
async def get_games(
    token: Annotated[str, Depends(oauth2_scheme)], limit: int = 20
) -> list[Game]:
    return game_database[:limit]


@app.get("/games/{name}")
async def read_game(token: Annotated[str, Depends(oauth2_scheme)], name: str) -> Game:
    return [game for game in game_database if game.name == name][0]


@app.put("/games/")
async def add_game(token: Annotated[str, Depends(oauth2_scheme)], game: Game) -> Game:
    game_database.append(game)
    return game
