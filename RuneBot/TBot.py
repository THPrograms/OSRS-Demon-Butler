import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import sqlite3
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from PIL import ImageFilter
import random
import asyncio
import traceback
from discord.ui import Button, View
from github import Github




intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True

"""Need to add the ability for this to work with multiple servers"""

load_dotenv()

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)


@bot.event
async def on_ready():
    print("Tbot in da hous!")

def dbconnection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn



bot.run(os.getenv(str('TBOTTOKEN')))