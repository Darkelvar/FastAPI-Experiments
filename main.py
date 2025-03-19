from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated
from contextlib import asynccontextmanager
from security import (
    authenticate_user,
    fake_users_db,
    create_access_token,
)
from models import SteamGames, Token, SteamGameCreate, SteamGameUpdate
from sqlalchemy import select
from sqlmodel import Session
from db import create_tables, get_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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


@app.get("/games", response_model=list[SteamGames])
async def list_all_games(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Session = Depends(get_session),
    limit: int = 20,
    name: str | None = None,
):
    if name:
        return (
            session.exec(select(SteamGames).limit(limit).where(SteamGames.name == name))
            .scalars()
            .all()
        )
    else:
        return session.exec(select(SteamGames).limit(limit)).scalars().all()


@app.get("/games/{id}", response_model=SteamGames)
async def find_game_by_id(
    token: Annotated[str, Depends(oauth2_scheme)],
    id: int,
    session: Session = Depends(get_session),
):
    found_game = session.get(SteamGames, id)
    if not found_game:
        raise HTTPException(status_code=404, detail="Game not found in the database.")
    else:
        return found_game


@app.get("/games/discount/{id}")
async def get_discounted_price(
    token: Annotated[str, Depends(oauth2_scheme)],
    id: int,
    session: Session = Depends(get_session),
) -> float:
    found_game = session.get(SteamGames, id)
    if not found_game:
        raise HTTPException(status_code=404, detail="Game not found in the database.")
    else:
        discount_multiplier = (100 - found_game.discount) / 100
        return round(found_game.base_price * discount_multiplier, 2)


@app.put("/games/", response_model=SteamGames)
async def add_game(
    token: Annotated[str, Depends(oauth2_scheme)],
    game: SteamGameCreate,
    session: Session = Depends(get_session),
):
    game = SteamGames(**game.model_dump())
    session.add(game)
    session.commit()
    session.refresh(game)
    return game


@app.patch("/games/{id}", response_model=SteamGames)
def update_hero(
    id: int, game_update: SteamGameUpdate, session: Session = Depends(get_session)
):
    game = session.get(SteamGames, id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    update_data = game_update.model_dump(exclude_unset=True)
    game.sqlmodel_update(update_data)
    session.add(game)
    session.commit()
    session.refresh(game)
    return game


@app.delete("/games/{id}")
async def delete_game(
    token: Annotated[str, Depends(oauth2_scheme)],
    id: int,
    session: Session = Depends(get_session),
):
    game = session.get(SteamGames, id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found in the database.")
    session.delete(game)
    session.commit()
    return {"ok": True}
