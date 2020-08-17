from flask import Flask
from flask import render_template, redirect, request
# from werkzeug.wrappers import Request
from chess import WebInterface, Board

app = Flask(__name__)
ui = WebInterface()
game = Board(debug=True)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/newgame')
def newgame():
    # Note that in Python, objects and variables
    # in the global space are available to
    # top-level functions
    game.start()
    ui.board = game.display()
    ui.turn = game.turn
    ui.inputlabel = f'{game.turn} player: '
    ui.errmsg = None
    ui.btnlabel = 'Move'
    return redirect('/play')


@app.route('/play')
def play():
    # TODO: get player move from GET request object
    # TODO: if there is no player move, render the page template
    move = request.args.get("move", None)
    if move is None:
        return render_template('chess.html', ui=ui)
    else:
        if game.prompt(move) == False:
            return render_template('chess.html', ui=ui, error="Invalid Move!")
        else:
            start, end = game.prompt(move)
            game.update(start, end)
            game.next_turn()
            ui.turn = game.turn
            ui.board = game.display()
            return render_template('chess.html', ui=ui)

    # TODO: Validate move, redirect player back to /play again if move is invalid
    # If move is valid, check for pawns to promote
    # Redirect to /promote if there are pawns to promote, otherwise 

@app.route('/promote')
def promote():
    pass

app.run()