import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import sqlite3

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True


load_dotenv()

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print("We alive yo")

@bot.command()
async def register(ctx: commands.Context):
    print('hello')
    try:
        print (ctx.message.author.id)
        print (ctx.message.channel.id)
        print (ctx.message.guild.id)
        print (ctx.message.content)
        print (userurl(ctx.message.content))
    except Exception as e:
        print(f"Error: {e}")

    conn = dbconnection(r"C:\Users\tommy\Documents\GitHub\RuneBot\RuneBot\RuneBotDB.db")



@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Unknown command.")


@bot.event
async def on_message_delete(message: discord.Message):
    msg = f"{message.author} has deleted the message: {message.content}"
    await message.channel.send(msg)

categorylist = []
def parsecategories():
    import requests
    # designating the web url to pull from
    url = 'https://secure.runescape.com/m=hiscore_oldschool/overall'
    r = requests.get(url)
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(r.content, 'html.parser')
    contentcategory = soup.find('div', id='contentCategory')
    categorylist = contentcategory.find_all('a')
    for i in range(len(categorylist)):
        categorylist[i] = categorylist[i].text.strip()
    updatecategories(categorylist)
    pass

def dbconnection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    print (conn)
    return conn


def updatecategories(categorylist):
    conn = dbconnection(r"C:\Users\tommy\Documents\GitHub\RuneBot\RuneBot\RuneBotDB.db")
    print(conn)
    cur = conn.cursor()
    for i in categorylist:
        cur.execute("SELECT * FROM Categories where Category = ?", (i,))
        if cur.fetchone() is None:
            cur.execute("INSERT INTO Categories (Category) VALUES (?)", (i,))
            conn.commit()
    updatestatcols()
    print ("Categories Up To Date")
    pass

def updatestatcols():
    tinfo = []
    conn = dbconnection(r"C:\Users\tommy\Documents\GitHub\RuneBot\RuneBot\RuneBotDB.db")
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(PlayerStats)")
    for i in cur.fetchall():
        tinfo.append(i[1])
    print(tinfo)
    cur.execute("SELECT * FROM Categories")
    for i in cur.fetchall():
        if i[0] not in tinfo:
            istring = str(i[0])
            iescape = ''.join(("\"", istring, "\""))
            print(iescape)
            cur.execute("ALTER TABLE PlayerStats ADD COLUMN " + iescape + " TEXT")
            conn.commit()
    print ("Column Up To Date")
    pass

def userurl(msgcontent):
    msgcontent = (msgcontent).title()
    msgcontent = msgcontent.split()
    if len(msgcontent) == 3:
        url = 'https://secure.runescape.com/m=hiscore_oldschool/hiscorepersonal?user1=' + msgcontent[1] + '%A0' + msgcontent[2]
        username = msgcontent[1] + ' ' + msgcontent[2]
        return url, username
    if len(msgcontent) == 2:
        url = 'https://secure.runescape.com/m=hiscore_oldschool/hiscorepersonal?user1=' + msgcontent[1]
        username = msgcontent[1]
        return url, username




parsecategories()

bot.run(os.getenv(str('TOKEN')))

