import os
from flask import Flask, render_template
from discord.ext import commands
from threading import Thread

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

def discord_bot():
    bot.run("NzU3MTg3NTQ3NTQ0NjgyNTk3.X2cv2w.f08QQwi-B-dS6IEM6RUGsrcJW10")

def website():
    app.run()
    
if __name__ == "__main__":
    Thread(target = discord_bot).start()
    Thread(target = website).start()