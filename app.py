from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel
from main import Game

app = FastAPI()
game = Game()


@app.get("/")
async def get_ui():
    return FileResponse("index.html")


@app.get("/styles.css")
async def get_styles():
    return FileResponse("styles.css")


@app.get("/script.js")
async def get_script():
    return FileResponse("script.js")


@app.get("/start")
async def start():
    return game.start()


@app.get("/switch")
async def switch():
    return game.switch()


@app.post("/place")
async def place(x: int, y: int):
    return game.place(x, y)


@app.post("/move")
async def move(x: int, y: int, nx: int, ny: int):
    return game.move(x, y, nx, ny)


@app.post("/undo")
async def undo():
    return game.undo()


@app.get("/get_winner")
async def get_winner():
    return game.get_winner()


@app.get("/is_placement_phase")
async def is_placement_phase():
    return game.is_placement_phase()


@app.get("/is_move_phase")
async def is_move_phase():
    return game.is_move_phase()


@app.get("/evaluate_board")
async def evaluate_board():
    return game.evaluate_board()


@app.get("/get_possible_moves")
async def get_possible_moves():
    return game.get_possible_moves()


@app.get("/minimax")
async def minimax(depth: int):
    return game.minimax(depth)


@app.get("/get_computer_move")
async def get_computer_move(depth: int):
    return game.get_computer_move(depth)
