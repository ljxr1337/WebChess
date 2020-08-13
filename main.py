from flask import Flask, render_template

app = Flask(__name__)
@app.route('/')
def root():
    return render_template('index.html')

@app.route('/newgame')
def newgame():
    return render_template('chess.html', player="white player")
app.run()