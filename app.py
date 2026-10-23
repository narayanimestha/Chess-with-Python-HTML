import chess
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
board = chess.Board()


@app.route("/")
def index():
  return render_template("index.html")


@app.route("/get_board")
def get_board():
  return jsonify({"fen": board.fen(), "is_game_over": board.is_game_over()})


@app.route("/make_move", methods=["POST"])
def make_move():
  global board
  data = request.json
  move_uci = data.get("move")
  try:
    move = chess.Move.from_uci(move_uci)
    if move in board.legal_moves:
      board.push(move)
      return jsonify({
          "success": True,
          "fen": board.fen(),
          "is_game_over": board.is_game_over(),
      })
    else:
      return jsonify({"success": False, "error": "Illegal move"}), 400
  except Exception as e:
    return jsonify({"success": False, "error": str(e)}), 400


@app.route("/reset", methods=["POST"])
def reset():
  global board
  board = chess.Board()
  return jsonify({"success": True, "fen": board.fen()})


if __name__ == "__main__":
  app.run(debug=True)
