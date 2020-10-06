import os
from flask import Flask, render_template
from discord.ext import commands
import threading

bot = commands.Bot(command_prefix='!')
bot.remove_command('help')

app = Flask(__name__, static_folder='public', template_folder='views', static_url_path='')

for file in os.listdir("events"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"events.{name}")

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")

@app.route('/')
def homepage():
    return render_template('index.html')

print("Serveur ON")

if __name__ == "__main__":
    t1 = threading.Thread(target=bot.run("NzU3MTg3NTQ3NTQ0NjgyNTk3.X2cv2w.f08QQwi-B-dS6IEM6RUGsrcJW10"))
    t2 = threading.Thread(target=app.run)
    t1.start()
    t2.start()