from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Game(BaseModel):
    name: str
    price: float
    genre: str
    discount: int | None = 0

game_database = [Game(name='Death Stranding', price=169, genre='Action RPG'), Game(name='Like a Dragon: Infinite Wealth', price=299, genre='jRPG'), Game(name='Medieval Dynasty', price=109, genre='Simulator', discount=35)]

@app.get('/games')
async def get_games():
    return {'games': game_database}

@app.get('/games/{name}')
async def read_game(name: str):
    return [game for game in game_database if game.name==name][0]

@app.put('/games/')
async def add_game(game: Game):
    game_database.append(game)
    return game
