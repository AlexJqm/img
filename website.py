from flask import Flask, render_template
from threading import Thread
import astronaute

t = Thread(target=bot.run)
t.start()

app = Flask(__name__, static_folder='public', template_folder='views', static_url_path='')
@app.route('/')
def homepage():
    return render_template('index.html')
