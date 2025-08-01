from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from main import Game

app = FastAPI()

# Add CORS middleware for web UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

game = Game()


# Pydantic models for request bodies
class PlaceRequest(BaseModel):
    x: int
    y: int


class MoveRequest(BaseModel):
    x: int
    y: int
    nx: int
    ny: int


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
    game.start()
    return {"success": True}


@app.get("/undo")
async def undo():
    success = game.undo()
    return {"success": success}


@app.get("/get_winner")
async def get_winner():
    return {"winner": game.get_winner()}


@app.get("/is_placement_phase")
async def is_placement_phase():
    return {"is_placement_phase": game.is_placement_phase()}


@app.get("/is_move_phase")
async def is_move_phase():
    return {"is_move_phase": game.is_move_phase()}


@app.get("/get_board_state")
async def get_board_state():
    """Get complete board state for UI"""
    return {
        "board": game.board,
        "current_player": game.player,
        "white_count": game.white,
        "black_count": game.black,
        "is_placement_phase": game.is_placement_phase(),
        "winner": game.get_winner(),
        "game_active": game.game_active
    }


@app.post("/place")
async def place(request: PlaceRequest):
    success = game.place(request.x, request.y)
    return {"success": success}


@app.post("/move")
async def move(request: MoveRequest):
    success = game.move(request.x, request.y, request.nx, request.ny)
    return {"success": success}


@app.get("/get_computer_move")
async def get_computer_move(depth: int = Query(3, ge=1, le=6)):
    move = game.get_computer_move(depth)
    return {"move": move}


@app.get("/get_valid_moves")
async def get_valid_moves():
    """Get valid moves for current player"""
    moves = game.get_possible_moves()
    return {"moves": moves}


@app.get("/get_adjacent_positions")
async def get_adjacent_positions(x: int, y: int):
    """Get adjacent positions for a given coordinate"""
    if (x, y) in game.adjacent:
        return {"adjacent": game.adjacent[(x, y)]}
    return {"adjacent": []}
