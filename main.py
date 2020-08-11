from flask import Flask, render_template

app = Flask(__name__)
@app.route('/')
def root():
    return render_template('index.html', name='ryan')

@app.route('/newgame')
def newgame():
    return "Starting a new game"
app.run()