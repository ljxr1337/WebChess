from flask import Flask, render_template

app = Flask(__name__)
@app.route('/')
def root():
    return render_template('index.html', name='ryan')
#   return "welcome to flask!"

app.run()