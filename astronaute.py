import os
from discord.ext import commands

bot = commands.Bot(command_prefix='!')
bot.remove_command('help')



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
    app.run()
    bot.run("NzU3MTg3NTQ3NTQ0NjgyNTk3.X2cv2w.f08QQwi-B-dS6IEM6RUGsrcJW10")