from flask import Flask, render_template

app = Flask(__name__, static_folder='public', template_folder='views', static_url_path='')