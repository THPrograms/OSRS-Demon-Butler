import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import sqlite3
from datetime import date, datetime
import time
from PIL import Image, ImageDraw, ImageFont
from PIL import ImageFilter
import random
import math
import asyncio
import schedule
from discord.ui import Button, View

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True



def dbconnection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

conn = dbconnection(r"C:\Users\tommy\Documents\GitHub\RuneBot\RuneBot\RuneBotDB.db")
cur = conn.cursor()

cur.execute("Select * from Users where LOWER(UserName) = ?", ("litheriam",))

rows = cur.fetchall()
for row in rows:
    print(row)