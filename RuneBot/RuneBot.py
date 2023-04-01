import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True

load_dotenv()

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
async def announce(ctx, title, *, message):
    await ctx.send("**{}**\n{}".format(title, message))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Unknown command.")

bot.run(os.getenv(str('TOKEN')))

