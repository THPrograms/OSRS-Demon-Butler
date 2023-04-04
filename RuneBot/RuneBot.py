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
    try:
        author = (ctx.message.author.id)
        channel = (ctx.message.channel.id)
        guild = (ctx.message.guild.id)
        url = (userurl(ctx.message.content)[0])
        UserName = (userurl(ctx.message.content)[1])
        print (url)
        print (UserName)
        dbformat = (UserName, url, author, channel, guild)
        await ctx.send(verifyuser(dbformat))
    except Exception as e:
        print(f"Error: {e}")

@bot.command()
async def unregister(ctx: commands.Context):
    guild = (ctx.message.guild.id)
    UserName = (userurl(ctx.message.content)[1])
    conn = dbconnection(r"C:\Users\tommy\Documents\GitHub\RuneBot\RuneBot\RuneBotDB.db")
    cur = conn.cursor()
    cur.execute("Select * FROM Users WHERE UserName = ? AND GUILDID= ?", (UserName,guild))
    if cur.fetchone() is None:
        await ctx.send("User Not Registered To Receive HiScore Alerts On This Server")
    else:
        cur.execute("DELETE FROM Users WHERE UserName = ? AND GUILDID= ?", (UserName,guild))
        conn.commit()
        await ctx.send("User Has Been Unregistered From Receiving HiScore Alerts On This Server")

@bot.command()
async def registered(ctx: commands.Context):
    guild = (ctx.message.guild.id)
    conn = dbconnection(r"C:\Users\tommy\Documents\GitHub\RuneBot\RuneBot\RuneBotDB.db")
    cur = conn.cursor()
    cur.execute("Select UserName FROM Users WHERE GUILDID= ?", (guild,))
    rows = cur.fetchall()
    if not rows:
        await ctx.send("No Users Registered To Receive Hiscore Alerts On This Server")
    else:
        registeredusers = []
        for i in rows:
            registeredusers.append(i[0])
        output = '\n'.join(registeredusers)
        await ctx.send("Registered Users On This Server: \n" + output)


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
    soup = soupy('https://secure.runescape.com/m=hiscore_oldschool/overall')
    contentcategory = soup.find('div', id='contentCategory')
    categorylist = contentcategory.find_all('a')
    for i in range(len(categorylist)):
        categorylist[i] = categorylist[i].text.strip()
    updatecategories(categorylist)
    pass

def soupy(url):
    import requests
    from bs4 import BeautifulSoup
    url = url
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def hiscoresoup():
    data = []
    soup = soupy('https://secure.runescape.com/m=hiscore_oldschool/hiscorepersonal?user1=Oborsbigtoe')
    tableparent = soup.find('div', id='contentHiscores')
    table = tableparent.find('table')
    print (table)

    print (table.find('tbody'))

    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])

    print (data)

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

def verifyuser(dbformat):
    conn = dbconnection(r"C:\Users\tommy\Documents\GitHub\RuneBot\RuneBot\RuneBotDB.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Users WHERE UserName = ? AND URl = ? AND CHANNELID= ? AND GUILDID = ?", (dbformat[0], dbformat[1], dbformat[3], dbformat[4]))
    if cur.fetchone() is None:
        soup = soupy(dbformat[1])
        header = soup.find('div', id='contentHiscores')
        headercheck = header.text.strip()
        headercheck = headercheck.replace('Ý', ' ')
        if headercheck == (f'No player "{dbformat[0]}" found'):
            print("User Not Found")
            return ("User Does Not Exist On Old School Hiscores")
        else:
            print("User Found")
            cur.execute("INSERT INTO Users (UserName, URL, UserID, ChannelID, GuildID) VALUES (?,?,?,?,?)",(dbformat[0], dbformat[1], dbformat[2], dbformat[3], dbformat[4]))
            conn.commit()
            return ("User Registered To Receive HiScore Alerts In This Channel/Server")
    else:
        print("User Already Exists")
        return ("User Already Registered For Current Channel/Server")




hiscoresoup()
parsecategories()

bot.run(os.getenv(str('TOKEN')))

