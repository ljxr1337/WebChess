from flask import Flask, render_template, redirect, request
# from werkzeug.wrappers import Request
from chess import *


app = Flask(__name__)
# ui = WebInterface()
# game = Board(debug=False)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/newgame')
def newgame():
    # Note that in Python, objects and variables
    # in the global space are available to
    # top-level functions
    global ui
    ui = WebInterface()
    global game
    game = Board(debug=False)
    game.start()
    ui.board = game.display()
    ui.turn = game.turn
    ui.inputlabel = f'{game.turn} player: '
    ui.errmsg = None
    ui.btnlabel = 'Move'
    ui.info = game.info
    return redirect('/play')


@app.route('/play', methods=['GET', 'POST'])
def play():
    # TODO: get player move from GET request object
    # TODO: if there is no player move, render the page template
    move = request.form.get("move", None)
    ui.empty = game.movehistory.empty()
    if move is None:
        return render_template('chess.html', ui=ui)
    else:
        ui.empty = game.movehistory.empty()
        valid, output = game.prompt(move)
        if not valid:
            ui.errmsg = output
            return render_template('chess.html', ui=ui)
        else:
            ui.errmsg = None
            game.update(output)
            ui.empty = game.movehistory.empty()
            if game.winner is not None:
                return redirect('/winner')
            ui.info = game.info
            ui.board = game.display()
            if game.promotepawns():
                return redirect('/promote')
            else:
                game.next_turn()
                ui.turn = game.turn
                return render_template('chess.html', ui=ui)

    # TODO: Validate move, redirect player back to /play again if move is invalid
    # If move is valid, check for pawns to promote
    # Redirect to /promote if there are pawns to promote, otherwise 

@app.route('/promote')
def promote():
    piece = request.args.get("promote", None)
    if piece is None:
        return render_template("promote.html", ui=ui)
    else:
        if piece == 'Rook':
            PieceClass = Rook
        elif piece == 'Knight':
            PieceClass = Knight
        elif piece == 'Bishop':
            PieceClass = Bishop
        elif piece == 'Queen':
            PieceClass = Queen
        game.promotepawns(PieceClass)
        game.next_turn()
        ui.turn = game.turn
        ui.board = game.display()
        ui.info = game.info
        return redirect("/play")

@app.route('/undo')
def undo():
    move = game.movehistory.pop()
    game.undo(move)
    game.next_turn()
    ui.turn = game.turn
    ui.board = game.display()
    ui.info = f"undo {game.info}"
    return redirect("/play")

@app.route("/winner")
def winner():
    winner = game.winner
    return render_template("winner.html", winner = winner)

app.run()