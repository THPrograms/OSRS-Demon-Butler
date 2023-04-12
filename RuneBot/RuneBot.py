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
from discord.ui import Button, View

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True

"""Need to add the ability for this to work with multiple servers"""

load_dotenv()

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)


@bot.event
async def on_ready():
    client = discord.Client()
    client.loop.create_task(schedule_function())
    print("We alive yo")


@bot.command()
async def register(ctx: commands.Context):
    try:
        print (ctx.message.content)
        author = ctx.message.author.id
        channel = ctx.message.channel.id
        guild = ctx.message.guild.id
        url = userurl(ctx.message.content)[0]
        UserName = userurl(ctx.message.content)[1]
        print (url)
        print (UserName)
        dbformat = (UserName, url, author, channel, guild)
        await ctx.send(verifyuser(dbformat))
    except Exception as e:
        print(f"Error: {e}")


@bot.command()
async def unregister(ctx: commands.Context):
    guild = ctx.message.guild.id
    UserName = userurl(ctx.message.content)[1]
    conn = dbconnection(r"C:\Users\tommy\Documents\GitHub\RuneBot\RuneBot\RuneBotDB.db")
    cur = conn.cursor()
    cur.execute("Select * FROM Users WHERE UserName = ? AND GUILDID= ?", (UserName, guild))
    if cur.fetchone() is None:
        await ctx.send("User Not Registered To Receive HiScore Alerts On This Server")
    else:
        cur.execute("DELETE FROM Users WHERE UserName = ? AND GUILDID= ?", (UserName, guild))
        conn.commit()
        await ctx.send("User Has Been Unregistered From Receiving HiScore Alerts On This Server")


@bot.command()
async def registered(ctx: commands.Context):
    guild = ctx.message.guild.id
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
    print(ctx)
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Unknown command.")


async def send_message(guild_id, channel_id, image):
    channel = await bot.fetch_channel(channel_id)
    print(channel)
    print('made it here')
    with open(image, 'rb') as f:
        picture = discord.File(f)

    await channel.send(file=picture)


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


def hiscoresoup(UserData):
    try:
        data = []
        soup = soupy(UserData[1])
        tableparent = soup.find('div', id='contentHiscores')
        table = tableparent.find('table')
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
        del data[0:3]
        return data
    except Exception as e:
        conn = dbconnection(r"C:\Users\tommy\Documents\GitHub\RuneBot\RuneBot\RuneBotDB.db")
        cur = conn.cursor()
        dt = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        einput = ''.join(("\"", str(e), "\""))
        cur.execute("INSERT INTO ErrorLog VALUES (?, ?)", (dt, einput))
        conn.commit()
        return 'error'


def statsupdate(data, UserData):
    conn = dbconnection(r"C:\Users\tommy\Documents\GitHub\RuneBot\RuneBot\RuneBotDB.db")
    cur = conn.cursor()
    dt = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    headers = ['Username', 'Date']
    stats = [UserData[0], dt]
    for i in data:
        if len(i) == 3:
            headers.append(i[0])
            headers.append(i[0] + " Rank")
            headers.append(i[0] + " Score")
            for i in i[0:]:
                stats.append(i)
        elif len(i) == 4:
            headers.append(i[0])
            headers.append(i[0] + " Rank")
            headers.append(i[0] + " Level")
            headers.append(i[0] + " XP")
            for i in i[0:]:
                stats.append(i)
    headerstring = ', '.join(("\"" + str(header) + "\"" for header in headers))
    statstring = ', '.join(("\"" + str(stat) + "\"" for stat in stats))
    print(headerstring)
    print(statstring)
    cur.execute("INSERT INTO PlayerStats (" + headerstring + ") VALUES (" + statstring + ")")
    conn.commit()


def getusers():
    Users = []
    conn = dbconnection(r"C:\Users\tommy\Documents\GitHub\RuneBot\RuneBot\RuneBotDB.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Users")
    rows = cur.fetchall()
    for i in rows:
        Users.append(list(i))
    return Users


def statcompare(UserData):
    print(UserData[0])
    compstats = []
    finalstats = []
    conn = dbconnection(r"C:\Users\tommy\Documents\GitHub\RuneBot\RuneBot\RuneBotDB.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM PlayerStats WHERE Username = ? ORDER BY Date DESC LIMIT 2", (UserData[0],))
    rows = cur.fetchall()
    NewRow = list(rows[0])
    OldRow = list(rows[1])
    rowdata = [NewRow, OldRow]
    cur.execute("SELECT * FROM Categories")
    rows = cur.fetchall()
    for row in rowdata:
        tempstats = []
        for category in rows:
            if category[0] in row:
                index = row.index(category[0])
                if category[1] == "Skill":
                    tempstats.append([row[index], row[index + 2]])
                elif category[1] == "KC":
                    tempstats.append([row[index], row[index + 2]])
        compstats.append(tempstats)
    oldstatcategories = []
    for i in compstats[1]:
        oldstatcategories.append(i[0])

    for i in compstats[0]:
        compindex = compstats[0].index(i)
        if i[0] not in oldstatcategories:
            finalstats.append([UserData[0], i[0], 'None', i[1]])
            del compstats[0][compindex]

    compstats[0].sort()
    compstats[1].sort()

    for i in compstats[0]:
        compindex = compstats[0].index(i)
        if i not in compstats[1]:
            finalstats.append([UserData[0], i[0], compstats[1][compindex][1], i[1]])
    return finalstats


def dbconnection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn


def updatecategories(categorylist):
    conn = dbconnection(r"C:\Users\tommy\Documents\GitHub\RuneBot\RuneBot\RuneBotDB.db")
    cur = conn.cursor()
    for i in categorylist:
        cur.execute("SELECT * FROM Categories where Category = ?", (i,))
        if cur.fetchone() is None:
            cur.execute("INSERT INTO Categories (Category) VALUES (?)", (i,))
            conn.commit()
    updatestatcols()
    print("Categories Up To Date")
    pass


def updatestatcols():
    tinfo = []
    conn = dbconnection(r"C:\Users\tommy\Documents\GitHub\RuneBot\RuneBot\RuneBotDB.db")
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(PlayerStats)")
    for i in cur.fetchall():
        tinfo.append(i[1])
    cur.execute("SELECT * FROM Categories")
    for i in cur.fetchall():
        if i[0] not in tinfo:
            if i[1] == 'Skill':
                istring = str(i[0])
                irank = istring + " Rank"
                ilevel = istring + " Level"
                ixp = istring + " XP"
                iescape = ''.join(("\"", istring, "\""))
                irankescape = ''.join(("\"", irank, "\""))
                ilevelescape = ''.join(("\"", ilevel, "\""))
                ixpescape = ''.join(("\"", ixp, "\""))
                cur.execute("ALTER TABLE PlayerStats ADD COLUMN " + iescape + " TEXT DEFAULT 'None'")
                conn.commit()
                cur.execute("ALTER TABLE PlayerStats ADD COLUMN " + irankescape + " TEXT DEFAULT 'None'")
                conn.commit()
                cur.execute("ALTER TABLE PlayerStats ADD COLUMN " + ilevelescape + " TEXT DEFAULT 'None'")
                conn.commit()
                cur.execute("ALTER TABLE PlayerStats ADD COLUMN " + ixpescape + " TEXT DEFAULT 'None'")
                conn.commit()
                pass
            elif i[1] == 'KC':
                istring = str(i[0])
                irank = str(istring + " Rank")
                ilevel = str(istring + " Score")
                iescape = ''.join(("\"", istring, "\""))
                irankescape = ''.join(("\"", irank, "\""))
                ilevelescape = ''.join(("\"", ilevel, "\""))
                cur.execute("ALTER TABLE PlayerStats ADD COLUMN " + iescape + " TEXT DEFAULT 'None'")
                conn.commit()
                cur.execute("ALTER TABLE PlayerStats ADD COLUMN " + irankescape + " TEXT DEFAULT 'None'")
                conn.commit()
                cur.execute("ALTER TABLE PlayerStats ADD COLUMN " + ilevelescape + " TEXT DEFAULT 'None'")
                conn.commit()
                pass
            else:
                pass
    print("Column Up To Date")
    pass


def userurl(msgcontent):
    msgcontent = msgcontent.split()
    if len(msgcontent) == 3:
        url = 'https://secure.runescape.com/m=hiscore_oldschool/hiscorepersonal?user1=' + msgcontent[1] + '%A0' + \
              msgcontent[2]
        username = msgcontent[1] + ' ' + msgcontent[2]
        return url, username
    if len(msgcontent) == 2:
        url = 'https://secure.runescape.com/m=hiscore_oldschool/hiscorepersonal?user1=' + msgcontent[1]
        username = msgcontent[1]
        return url, username


def verifyuser(dbformat):
    conn = dbconnection(r"C:\Users\tommy\Documents\GitHub\RuneBot\RuneBot\RuneBotDB.db")
    cur = conn.cursor()
    print(str(dbformat[0].lower()))
    cur.execute("SELECT * FROM Users WHERE LOWER(UserName) = ? AND LOWER(URl) = ? AND CHANNELID= ? AND GUILDID = ?",
                (str(dbformat[0].lower()), str(dbformat[1].lower()), dbformat[3], dbformat[4]))
    if cur.fetchone() is None:
        soup = soupy(dbformat[1])
        header = soup.find('div', id='contentHiscores')
        headercheck = header.text.strip()
        headercheck = headercheck.replace('Ý', ' ')
        if headercheck == f'No player "{dbformat[0]}" found':
            print ("User Not Found")
            return "User does not exist on Old School hiscores"
        else:
            print("User Found")
            print(dbformat[0])
            cur.execute("INSERT INTO Users (UserName, URL, UserID, ChannelID, GuildID) VALUES (?,?,?,?,?)",
                        (dbformat[0], dbformat[1], dbformat[2], dbformat[3], dbformat[4]))
            conn.commit()
            conn = dbconnection(r"C:\Users\tommy\Documents\GitHub\RuneBot\RuneBot\RuneBotDB.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM Users Where UserName = ?", (dbformat[0],))
            row = cur.fetchall()
            UserData = list(row[0])
            print(UserData)
            Data = hiscoresoup(UserData)
            statsupdate(Data, UserData)
            statsupdate(Data, UserData)
            return "User registered to receive HiScore alerts in this channel/server"
    else:
        print("User Already Exists")
        return "User already registered for current channel/server"


async def statmonitor():
    UserData = getusers()
    output = []
    for iud in UserData:
        Data = hiscoresoup(iud)
        if Data == "error":
            print("An error has occurred at " + str(datetime.now()))
            continue
        else: pass
        statsupdate(Data, iud)
        FinalStats = statcompare(iud)
        for stats in FinalStats:
            if stats:
                output.append(stats)
    if not output:
        print("No stats to report")
    else:
        print("Stats to report")
        extendinterface(output)
        await send_message((str(UserData[0][4])), (str(UserData[0][3])),
                           r"C:\Users\tommy\Documents\GitHub\RuneBot\OSRSInterface\Final_Interface.png")
    print(output)
    print("Ran at: " + str(datetime.now()))

mssgbar = 'Tbot:'


def gaussian_blur(newimage):
    width, height = newimage.size
    top_left = (10, 10)
    top_right = (width - 24, 10)
    bottom_left = (10, height - 45.5)
    bottom_right = (width - 24, height - 45.5)
    print(top_left, top_right, bottom_left, bottom_right)
    imagecrop = newimage.crop((top_left[0], top_left[1], bottom_right[0], bottom_right[1]))
    blurred_image = imagecrop.filter(ImageFilter.GaussianBlur(radius=3))
    final_image = newimage.copy()
    final_image.paste(blurred_image, (11, 11))
    final_image.save(r"C:\Users\tommy\Documents\GitHub\RuneBot\OSRSInterface\Final_Interface.png")
    return final_image


def extendinterface(lvlup):
    default_image = Image.open(r"C:\Users\tommy\Documents\GitHub\RuneBot\OSRSInterface\Chat_Interface.png")
    default_image.save(r"C:\Users\tommy\Documents\GitHub\RuneBot\OSRSInterface\Stacked_Interface.png")
    chunkdirectory = r"C:\Users\tommy\Documents\GitHub\RuneBot\OSRSInterface\OSRSInterfaceChunks\\"
    if len(lvlup) > 7:
        for i in lvlup[7:]:
            # Load the image
            image = Image.open(r"C:\Users\tommy\Documents\GitHub\RuneBot\OSRSInterface\Stacked_Interface.png")
            chunknumber = random.choice(range(0, 5))

            # Get the original dimensions
            width, height = image.size

            # Calculate the split point
            split_point = height // 2

            # Split the image in half
            top_half = image.crop((0, 0, width, split_point))
            bottom_half = image.crop((0, split_point, width, height))
            randommiddlefile = os.listdir(chunkdirectory)[chunknumber]
            print(randommiddlefile)
            middle_half = Image.open(r"" + chunkdirectory + randommiddlefile)

            # Get the dimensions of the images
            width1, height1 = top_half.size
            width2, height2 = middle_half.size
            width3, height3 = bottom_half.size

            # Calculate the dimensions for the new image
            new_width = max(width1, width2, width3)
            new_height = height1 + height2 + height3

            # Create a new image with the calculated dimensions
            new_image = Image.new("RGB", (new_width, new_height))

            # Paste the images onto the new image

            new_image.paste(top_half, (0, 0))
            new_image.paste(middle_half, (0, height1))
            new_image.paste(bottom_half, (0, height1 + height2))
            new_image.save(r"C:\Users\tommy\Documents\GitHub\RuneBot\OSRSInterface\Stacked_Interface.png")

        addtext(lvlup, gaussian_blur(new_image))
        return
    else:
        addtext(lvlup, default_image)


def addtext(lvlup, useimage):
    image = useimage
    width, height = image.size
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(r"C:\Users\tommy\Documents\GitHub\RuneBot\OSRSInterface\runescape_uf\runescape_uf.ttf",
                              15)
    textheight = 43
    draw.text((11, height - 43), mssgbar, (0, 0, 0), font=font)
    for i in lvlup:
        textheight = textheight + 16
        draw.text((11, height - textheight),
                  (str(i[0]) + " has grown stronger! " + str(i[1]) + ": " + str(i[2]) + " -> " + str(i[3])), (0, 0, 0),
                  font=font)
    image.save(r"C:\Users\tommy\Documents\GitHub\RuneBot\OSRSInterface\Final_Interface.png")
    print('Image created')


"""print (extendinterface())"""

sched = True

parsecategories()


async def schedule_function():
    while True:
        await asyncio.sleep(300)
        await statmonitor()

bot.run(os.getenv(str('TOKEN')))
