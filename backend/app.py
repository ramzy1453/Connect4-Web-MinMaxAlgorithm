from game import *
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on("play_event")
def play(data):
    req = data

    if not req:
        socketio.emit("response", {"error": "No data provided"})
        return

    board = req.get("board")
    turn = req.get("turn")
    mode = req.get("mode")

    play_col = req.get("play_col")

    if board is None or turn is None or mode is None or play_col is None:
        socketio.emit("response", {"error": "Invalid data format"})
        return

    state = ConnectFourBoard(board)
    err = 0
    game_state = 0
    if mode == 1:
        if turn == 1:
            play_row, err = Play.humanTurn(state, play_col)
        elif turn == -1:
            play_row, play_col = Play.computerTurn(state, algorithm=1)
    else:
        if turn == 1:
            play_row, play_col = Play.computerTurn(state, algorithm=1)
        elif turn == -1:
            play_row, play_col = Play.computerTurn(state, algorithm=2)

    state.makeMove(play_row, play_col, turn)
    game_state = get_game_state(state, turn)
    print(state.board)

    socketio.emit(
        "response", {"board": state.board, "game_state": game_state, "Err": err}
    )


@socketio.on("timeout_event")
def timeout(data):
    req = data

    if not req:
        socketio.emit("response", {"error": "No data provided"})
        return

    board = req.get("board")
    turn = req.get("turn")

    if board is None or turn is None:
        socketio.emit("response", {"error": "Invalid data format"})
        return

    state = ConnectFourBoard(board)
    game_state = 0
    play_row, play_col = Play.playrandom(state)

    state.makeMove(play_row, play_col, turn)
    game_state = get_game_state(state, turn)

    socketio.emit(
        "response", {"board": state.board, "game_state": game_state, "Err": 0}
    )


def get_game_state(state, turn):
    if state.gameOver(turn):
        if state.win(turn):
            return turn
        else:
            return 2


@socketio.on("disconnect")
def disconnected():
    """event listener when client disconnects to the server"""
    print("user disconnected")
    socketio.emit("disconnect", f"user {request.sid} disconnected", broadcast=True)


if __name__ == "__main__":
    socketio.run(app, debug=True, port=5000)
