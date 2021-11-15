from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return "<h1> Bem Vindo ao FrameWork Flask. Powered by Pyhton.</h1>"

