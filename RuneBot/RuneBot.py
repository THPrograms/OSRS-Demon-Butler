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


lvlup = [['pLaYEr', 'sTrenGth ', 1, 5], ['pLaYEr', 'sTrenGth ', 1, 5], ['pLaYEr', 'sTrenGth ', 1, 5],
         ['pLaYEr', 'sTrenGth ', 1, 5], ['pLaYEr', 'sTrenGth ', 1, 5], ['pLaYEr', 'sTrenGth ', 1, 5],
         ['pLaYEr', 'sTrenGth ', 1, 5], ['pLaYEr', 'sTrenGth ', 1, 5], ['pLaYEr', 'sTrenGth ', 1, 5],
         ['pLaYEr', 'sTrenGth ', 1, 5], ['pLaYEr', 'sTrenGth ', 1, 5], ['pLaYEr', 'sTrenGth ', 1, 5],
         ['pLaYEr', 'sTrenGth ', 1, 5], ['pLaYEr', 'sTrenGth ', 1, 5], ['pLaYEr', 'sTrenGth ', 1, 5],
         ['pLaYEr', 'sTrenGth ', 1, 5], ['pLaYEr', 'sTrenGth ', 1, 5], ['pLaYEr', 'sTrenGth ', 1, 5],
         ['pLaYEr', 'sTrenGth ', 1, 5], ['pLaYEr', 'sTrenGth ', 1, 5], ]
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


"""Functions below still need refactoring

hslist = ['Overall', 'Attack', 'Defence', 'Strength', 'Hitpoints', 'Ranged', 'Prayer',
          'Magic', 'Cooking', 'Woodcutting', 'Fletching', 'Fishing', 'Firemaking', 'Crafting', 'Smithing', 'Mining',
          'Herblore', 'Agility', 'Thieving', 'Slayer', 'Farming', 'Runecraft', 'Hunter', 'Construction',
          'Bounty Hunter - Hunter', 'Bounty Hunter - Rogue', 'Clue Scrolls (all)', 'Clue Scrolls (beginner)',
          'Clue Scrolls (easy)', 'Clue Scrolls (medium)', 'Clue Scrolls (hard)', 'Clue Scrolls (elite)',
          'Clue Scrolls (master)', 'LMS - Rank', 'Soul Wars Zeal', 'Abyssal Sire', 'Alchemical Hydra',
          'Barrows Chests', 'Bryophyta', 'Callisto', 'Cerberus', 'Chambers of Xeric',
          'Chambers of Xeric: Challenge Mode', 'Chaos Elemental', 'Chaos Fanatic', 'Commander Zilyana',
          'Corporeal Beast', 'Crazy Archaeologist', 'Dagannoth Prime', 'Dagannoth Rex', 'Dagannoth Supreme',
          'Deranged Archaeologist', 'General Graardor', 'Giant Mole', 'Grotesque Guardians',
          'Hespori', 'Kalphite Queen', 'King Black Dragon', 'Kraken', "Kree'Arra", "K'ril Tsutsaroth", 'Mimic',
          'Nightmare', "Phosani's Nightmare", 'Obor', 'Sarachnis', 'Scorpia', 'Skotizo', 'Tempoross', 'The Gauntlet',
          'The Corrupted Gauntlet', 'Theatre of Blood', 'Theatre of Blood: Hard Mode', 'Thermonuclear Smoke Devil',
          'TzKal-Zuk', 'TzTok-Jad', 'Venenatis', "Vet'ion", 'Vorkath', 'Wintertodt', 'Zalcano', 'Zulrah', 'N/A']


@bot.command()
async def rank(ctx: commands.Context):
    ctx.content = ctx.content.lower()
    gnamelookup = ctx.content.split()
    glength = len(gnamelookup)
    gnamelast = ctx.content.split()[glength - 1:]
    gnameinput = ctx.content.split()[1:]

    def listtostring(gnameinput):
        str1 = " "
        return (str1.join(gnameinput)).replace(" ", "+")

    def listtostring2(gnamelast):
        str1 = " "
        return (str1.join(gnamelast)).replace(" ", "+")

    import requests
    # designating the web url to pull from
    url = 'https://secure.runescape.com/m=hiscore_oldschool_ironman/group-ironman/?groupName=' + (
        listtostring(gnameinput).title())

    r = requests.get(url)

    from bs4 import BeautifulSoup

    soup = BeautifulSoup(r.content, 'html.parser')

    rows = soup.select('tbody tr')
    # grabbing all data in the table body on the osrs highscores
    n = soup.find_all('td')
    Gdata = n
    # write the entire table body data into a text file for review
    file1 = open(r"C:\Users\tommy\Documents\GitHub\RuneBot\GroupIronStats", "w+")

    file1.write(str(Gdata))
    file1.close()

    string1 = (listtostring2(gnamelast)) + '</a>'

    file1 = open(r"C:\Users\tommy\Documents\GitHub\RuneBot\GroupIronStats", "r")

    flag = 0
    index = 0
    # Grabbing Line That Silk Cart group data is on
    for line in file1:
        index += 1

        if string1 in line:
            flag = 1
            break

    if flag == 0:
        print('String', string1, 'Not Found')
    else:
        print('String', string1, 'Found In Line', index)
        file1.close()

        file1 = open(r"C:\Users\tommy\Documents\GitHub\RuneBot\GroupIronStats", "r")

        silkstats = file1.readlines()
        # combining the variables
        silkstats1 = (silkstats[index])
        silkstats2 = (silkstats[index - 1])
        silkstats3 = (silkstats[index - 2])
        silkstats4 = silkstats2 + silkstats1 + silkstats3

        file1.close()
        # pulling the data from specific spots in the code
        gname = str(silkstats4)[133:144]
        grank = str(silkstats4)[526:531]
        gtotlvl = str(silkstats4)[190:195]
        gtotexp = str(silkstats4)[236:246]
        print(silkstats4)
        # outputting the results into discord message
        await ctx.channel.send(
            '```Group Name: ' + gname.title() + '\nRank: ' + grank + '\nTotal Level: ' + gtotlvl + '\nTotal XP: ' + gtotexp + '```'.format(
                ctx.author))


@bot.command()
async def skill(ctx: commands.Context):
    ctx.content = (ctx.content).title()
    SkillLookup = ctx.content.split()[1]
    pnameinput = ctx.content.split()[2:]

    def listtostring(pnameinput):
        str1 = " "
        return (str1.join(pnameinput)).replace(" ", "%A0")

    def listtostring2(pnameinput):
        str1 = " "
        return (str1.join(pnameinput))

    print(listtostring(pnameinput))
    print(SkillLookup)

    import requests
    import lxml.html as lh

    url = 'https://secure.runescape.com/m=hiscore_oldschool/hiscorepersonal?user1=' + (listtostring(pnameinput))
    # Create a handle, page, to handle the contents of the website
    page = requests.get(url)
    # Store the contents of the website under doc
    doc = lh.fromstring(page.content)
    # Parse data that are stored between <tr>..</tr> of HTML
    tr_elements = doc.xpath('//tr')
    # Create empty list
    col = []
    i = 0
    # For each row, store each first element (header) and an empty list
    pstats = ""
    for t in tr_elements[0]:
        i += 1
        name = t.text_content()
        pstats = pstats + ('%d:"%s"' % (i, name))

    file1 = open(r"C:\Users\tommy\Documents\GitHub\RuneBot\Pstats", "w+")

    file1.write(str(pstats))
    file1.close()

    file1 = open(r"C:\Users\tommy\Documents\GitHub\RuneBot\Pstats", "r")

    flag = 0
    index = 0
    # Grabbing Line That Silk Cart group data is on
    for line in file1:
        index += 1

        if SkillLookup in line:
            flag = 1
            break

    if flag == 0:
        await ctx.channel.send(
            '```' + SkillLookup + ' Does Not Exist Or Does Not Meet Highscore Requirements```'.format(ctx.author))
    else:
        file1.close()

        file1 = open(r"C:\Users\tommy\Documents\GitHub\RuneBot\Pstats", "r")

        personalstats = file1.readlines()
        # combining the variables
        skill = (personalstats[index - 1]).strip()
        prank = (personalstats[index + 1]).strip()
        plevel = (personalstats[index + 2]).strip()
        pxp = (personalstats[index + 3]).strip()
        await ctx.channel.send('```Name: ' + listtostring2(
            pnameinput) + '\nSkill: ' + skill + '\nRank: ' + prank + '\nLevel: ' + plevel + '\nXP: ' + pxp + '```'.format(
            ctx.author))


@bot.command()
async def kc(ctx: commands.Context):
    ctx.content = (ctx.content).title()
    BossLookup = (ctx.content).split()[1]
    pnameinput = (ctx.content).split()[2:]

    def listtostring(pnameinput):
        str1 = " "
        return (str1.join(pnameinput)).replace(" ", "%A0")

    def listtostring2(pnameinput):
        str1 = " "
        return (str1.join(pnameinput))

    print(listtostring(pnameinput))
    print(BossLookup)

    import requests
    import lxml.html as lh

    url = 'https://secure.runescape.com/m=hiscore_oldschool/hiscorepersonal?user1=' + (listtostring(pnameinput))
    # Create a handle, page, to handle the contents of the website
    page = requests.get(url)
    # Store the contents of the website under doc
    doc = lh.fromstring(page.content)
    # Parse data that are stored between <tr>..</tr> of HTML
    tr_elements = doc.xpath('//tr')
    # Create empty list
    col = []
    i = 0
    # For each row, store each first element (header) and an empty list
    pstats = ""
    for t in tr_elements[0]:
        i += 1
        name = t.text_content()
        pstats = pstats + ('%d:"%s"' % (i, name))

    file1 = open(r"C:\Users\tommy\Documents\GitHub\RuneBot\Pstats", "w+")

    file1.write(str(pstats))
    file1.close()

    file1 = open(r"C:\Users\tommy\Documents\GitHub\RuneBot\Pstats", "r")

    flag = 0
    index = 0
    # Grabbing Line That Silk Cart group data is on
    for line in file1:
        index += 1

        if BossLookup in line:
            flag = 1
            break

    if flag == 0:
        await ctx.channel.send(
            '```' + BossLookup + ' Does Not Exist Or Does Not Meet Highscore Requirements```'.format(ctx.author))
    else:
        file1.close()

        file1 = open(r"C:\Users\tommy\Documents\GitHub\RuneBot\Pstats", "r")

        personalstats = file1.readlines()
        # combining the variables
        skillboss = (personalstats[index - 1]).strip()
        prank = (personalstats[index]).strip()
        pscore = (personalstats[index + 1]).strip()
        await ctx.channel.send('```Name: ' + listtostring2(
            pnameinput) + '\nBoss: ' + skillboss + '\nRank: ' + prank + '\nScore: ' + pscore + '```'.format(ctx.author))
        # embedVar = discord.Embed(title="OSRS High Scores",description="This bot is a work in progress, thank you for giving it a try.",color=0x00fff0, timestamp=datetime.utcnow())
        # embedVar.set_thumbnail(url="https://i.imgur.com/ZIsEXmZ.png")
        # embedVar.add_field(name="Commands:",value="!rank [group name] - Pulls Group Iron group ranking from OSRS High Scores\n\n!skill [skill] [playername] - Pulls the current stats for the provided player's skill\n\n!kc [boss/minigame](Use First Or Last Name Ex: Rex For Daganoth Rex) [playername] - Pulls The Current Stats For The Provided Player And Boss/Minigame",inline=False)
        # embedVar.add_field(name="Creator:", value="Thomikaze#4519", inline=False)
        # embedVar.add_field(name="Contact:", value="TommyF.Herndon@gmail.com", inline=False)
        # embedVar.set_footer(text="Version 1.0")
        # await message.channel.send(embed=embedVar)


@bot.command()
async def help(ctx: commands.Context):
    embedVar = discord.Embed(title="OSRS High Scores",
                             description="This bot is a work in progress, thank you for giving it a try.",
                             color=0x00fff0, timestamp=datetime.utcnow())
    embedVar.set_thumbnail(url="https://i.imgur.com/ZIsEXmZ.png")
    embedVar.add_field(name="Commands:",
                       value="!rank [group name] - Pulls Group Iron group ranking from OSRS High Scores\n\n!skill [skill] [playername] - Pulls the current stats for the provided player's skill\n\n!kc [boss/minigame](Use First Or Last Name Ex: Rex For Daganoth Rex) [playername] - Pulls The Current Stats For The Provided Player And Boss/Minigame",
                       inline=False)
    embedVar.add_field(name="Creator:", value="Thomikaze#4519", inline=False)
    embedVar.add_field(name="Contact:", value="TommyF.Herndon@gmail.com", inline=False)
    embedVar.set_footer(text="Version 1.0")
    await ctx.channel.send(embed=embedVar)


@bot.command()
async def player(ctx: commands.Context):
    ctx.content = (ctx.content).title()
    pnameinput = ctx.content.split()[1:]

    def listtostring(pnameinput):
        str1 = " "
        return (str1.join(pnameinput)).replace(" ", "%A0")

    def listtostring2(pnameinput):
        str1 = " "
        return (str1.join(pnameinput))

    print(listtostring(pnameinput))

    import requests
    import lxml.html as lh

    url = 'https://secure.runescape.com/m=hiscore_oldschool/hiscorepersonal?user1=' + (listtostring(pnameinput))
    print(url)
    # Create a handle, page, to handle the contents of the website
    page = requests.get(url)
    print(page)
    # Store the contents of the website under doc
    doc = lh.fromstring(page.content)
    print(doc)
    # Parse data that are stored between <tr>..</tr> of HTML
    tr_elements = doc.xpath('//tr')
    print(tr_elements)
    # Create empty list
    col = []
    i = 0
    # For each row, store each first element (header) and an empty list
    pstats = ""
    for t in tr_elements[0]:
        i += 1
        name = t.text_content()
        pstats = pstats + ('%d:"%s"' % (i, name))

    file1 = open(r"C:\Users\tommy\Documents\GitHub\RuneBot\Pstats", "w+")

    file1.write(str(pstats))
    file1.write("\nN/A" + "\nN/A" + "\nN/A" + "\nN/A" + "\nN/A")
    file1.close()

    with open(r"C:\Users\tommy\Documents\GitHub\RuneBot\Pstats", "r") as file1:
        data = file1.readlines()
    file1.close()

    data[9] = "Blank\n"

    with open(r"C:\Users\tommy\Documents\GitHub\RuneBot\Pstats", "w") as file1:
        file1.writelines(data)
    file1.close()

    file1 = open(r"C:\Users\tommy\Documents\GitHub\RuneBot\Pstats", "r")
    slist = []
    plist = []
    index = 0

    for line in file1:
        index += 1
        for I in hslist:
            if I in line:
                slist.append(I)
                plist.append(index)
                continue
            continue
        continue

    file1.close()

    file2 = open(r"C:\Users\tommy\Documents\GitHub\RuneBot\Fstats", "w")

    index = 0
    lp = 0
    flist = []
    for I in hslist:
        index += 1
        if I in slist:
            flist.append(plist[lp])
            lp = lp + 1

        else:
            flist.append(plist[-5])
    for I in flist:
        file2.write((str(I)) + "\n")

    print(flist)
    file2.close()

    # for I in hslist:
    # print(I)

    print(plist)
    print(slist)
    plist = []
    button1 = Button(label="Main")
    button2 = Button(label="Char Stats")
    button3 = Button(label="B - C")
    button4 = Button(label="D - S")
    button5 = Button(label="T - Z")
    view1 = View()
    view2 = View()
    view3 = View()
    view4 = View()
    view5 = View()
    view1.add_item(button2)
    view1.add_item(button3)
    view1.add_item(button4)
    view1.add_item(button5)
    view2.add_item(button1)
    view2.add_item(button3)
    view2.add_item(button4)
    view2.add_item(button5)
    view3.add_item(button1)
    view3.add_item(button2)
    view3.add_item(button4)
    view3.add_item(button5)
    view4.add_item(button1)
    view4.add_item(button2)
    view4.add_item(button3)
    view4.add_item(button5)
    view5.add_item(button1)
    view5.add_item(button2)
    view5.add_item(button3)
    view5.add_item(button4)

    file1 = open(r"C:\Users\tommy\Documents\GitHub\RuneBot\Pstats", "r")
    file2 = open(r"C:\Users\tommy\Documents\GitHub\RuneBot\Fstats", "r")
    personalstats = file1.readlines()
    psline = file2.readlines()

    Overall = (personalstats[int(psline[0].strip()) + 2]).strip()
    Attack = (personalstats[int(psline[1].strip()) + 2]).strip()
    Defence = (personalstats[int(psline[2].strip()) + 2]).strip()
    Strength = (personalstats[int(psline[3].strip()) + 2]).strip()
    Hitpoints = (personalstats[int(psline[4].strip()) + 2]).strip()
    Ranged = (personalstats[int(psline[5].strip()) + 2]).strip()
    Prayer = (personalstats[int(psline[6].strip()) + 2]).strip()
    Magic = (personalstats[int(psline[7].strip()) + 2]).strip()
    Cooking = (personalstats[int(psline[8].strip()) + 2]).strip()
    Woodcutting = (personalstats[int(psline[9].strip()) + 2]).strip()
    Fletching = (personalstats[int(psline[10].strip()) + 2]).strip()
    Fishing = (personalstats[int(psline[11].strip()) + 2]).strip()
    Firemaking = (personalstats[int(psline[12].strip()) + 2]).strip()
    Crafting = (personalstats[int(psline[13].strip()) + 2]).strip()
    Smithing = (personalstats[int(psline[14].strip()) + 2]).strip()
    Mining = (personalstats[int(psline[15].strip()) + 2]).strip()
    Herblore = (personalstats[int(psline[16].strip()) + 2]).strip()
    Agility = (personalstats[int(psline[17].strip()) + 2]).strip()
    Thieving = (personalstats[int(psline[18].strip()) + 2]).strip()
    Slayer = (personalstats[int(psline[19].strip()) + 2]).strip()
    Farming = (personalstats[int(psline[20].strip()) + 2]).strip()
    Runecraft = (personalstats[int(psline[21].strip()) + 2]).strip()
    Hunter = (personalstats[int(psline[22].strip()) + 2]).strip()
    Construction = (personalstats[int(psline[23].strip()) + 2]).strip()
    BountyHunterHunter = (personalstats[int(psline[24].strip()) + 1]).strip()
    BountyHunterRogue = (personalstats[int(psline[25].strip()) + 1]).strip()
    ClueScrollsall = (personalstats[int(psline[26].strip()) + 1]).strip()
    ClueScrollsbeginner = (personalstats[int(psline[27].strip()) + 1]).strip()
    ClueScrollseasy = (personalstats[int(psline[28].strip()) + 1]).strip()
    ClueScrollsmedium = (personalstats[int(psline[29].strip()) + 1]).strip()
    ClueScrollshard = (personalstats[int(psline[30].strip()) + 1]).strip()
    ClueScrollselite = (personalstats[int(psline[31].strip()) + 1]).strip()
    ClueScrollsmaster = (personalstats[int(psline[32].strip()) + 1]).strip()
    LMSRank = (personalstats[int(psline[33].strip()) + 1]).strip()
    SoulWarsZeal = (personalstats[int(psline[34].strip()) + 1]).strip()
    AbyssalSire = (personalstats[int(psline[35].strip()) + 1]).strip()
    AlchemicalHydra = (personalstats[int(psline[36].strip()) + 1]).strip()
    BarrowsChests = (personalstats[int(psline[37].strip()) + 1]).strip()
    Bryophyta = (personalstats[int(psline[38].strip()) + 1]).strip()
    Callisto = (personalstats[int(psline[39].strip()) + 1]).strip()
    Cerberus = (personalstats[int(psline[40].strip()) + 1]).strip()
    ChambersofXeric = (personalstats[int(psline[41].strip()) + 1]).strip()
    ChambersofXericChallengeMode = (personalstats[int(psline[42].strip()) + 1]).strip()
    ChaosElemental = (personalstats[int(psline[43].strip()) + 1]).strip()
    ChaosFanatic = (personalstats[int(psline[44].strip()) + 1]).strip()
    CommanderZilyana = (personalstats[int(psline[45].strip()) + 1]).strip()
    CorporealBeast = (personalstats[int(psline[46].strip()) + 1]).strip()
    CrazyArchaeologist = (personalstats[int(psline[47].strip()) + 1]).strip()
    DagannothPrime = (personalstats[int(psline[48].strip()) + 1]).strip()
    DagannothRex = (personalstats[int(psline[49].strip()) + 1]).strip()
    DagannothSupreme = (personalstats[int(psline[50].strip()) + 1]).strip()
    DerangedArchaeologist = (personalstats[int(psline[51].strip()) + 1]).strip()
    GeneralGraardor = (personalstats[int(psline[52].strip()) + 1]).strip()
    GiantMole = (personalstats[int(psline[53].strip()) + 1]).strip()
    GrotesqueGuardians = (personalstats[int(psline[54].strip()) + 1]).strip()
    Hespori = (personalstats[int(psline[55].strip()) + 1]).strip()
    KalphiteQueen = (personalstats[int(psline[56].strip()) + 1]).strip()
    KingBlackDragon = (personalstats[int(psline[57].strip()) + 1]).strip()
    Kraken = (personalstats[int(psline[58].strip()) + 1]).strip()
    KreeArra = (personalstats[int(psline[59].strip()) + 1]).strip()
    KrilTsutsaroth = (personalstats[int(psline[60].strip()) + 1]).strip()
    Mimic = (personalstats[int(psline[61].strip()) + 1]).strip()
    Nightmare = (personalstats[int(psline[62].strip()) + 1]).strip()
    PhosanisNightmare = (personalstats[int(psline[63].strip()) + 1]).strip()
    Obor = (personalstats[int(psline[64].strip()) + 1]).strip()
    Sarachnis = (personalstats[int(psline[65].strip()) + 1]).strip()
    Scorpia = (personalstats[int(psline[66].strip()) + 1]).strip()
    Skotizo = (personalstats[int(psline[67].strip()) + 1]).strip()
    Tempoross = (personalstats[int(psline[68].strip()) + 1]).strip()
    TheGauntlet = (personalstats[int(psline[69].strip()) + 1]).strip()
    TheCorruptedGauntlet = (personalstats[int(psline[70].strip()) + 1]).strip()
    TheatreofBlood = (personalstats[int(psline[71].strip()) + 1]).strip()
    TheatreofBloodHardMode = (personalstats[int(psline[72].strip()) + 1]).strip()
    ThermonuclearSmokeDevil = (personalstats[int(psline[73].strip()) + 1]).strip()
    TzKaZuk = (personalstats[int(psline[74].strip()) + 1]).strip()
    TzTokJad = (personalstats[int(psline[75].strip()) + 1]).strip()
    Venenatis = (personalstats[int(psline[76].strip()) + 1]).strip()
    Vetion = (personalstats[int(psline[77].strip()) + 1]).strip()
    Vorkath = (personalstats[int(psline[78].strip()) + 1]).strip()
    Wintertodt = (personalstats[int(psline[79].strip()) + 1]).strip()
    Zalcano = (personalstats[int(psline[80].strip()) + 1]).strip()
    Zulrah = (personalstats[int(psline[81].strip()) + 1]).strip()

    embedVar = discord.Embed(title=listtostring2(pnameinput) + " - High Scores",
                             description="This bot is a work in progress, thank you for giving it a try.",
                             color=0x00fff0, timestamp=datetime.datetime.now())
    embedVar.set_thumbnail(url="https://i.imgur.com/itFUcLj.jpg")
    embedVar.add_field(name="Overall", value=Overall, inline=False)

    embedVar1 = discord.Embed(title=listtostring2(pnameinput) + " - High Scores",
                              description="Displaying Character Stats For " + listtostring2(
                                  pnameinput) + "\n===============================", color=0x00fff0,
                              timestamp=datetime.utcnow())
    embedVar1.set_thumbnail(url="https://i.imgur.com/itFUcLj.jpg")
    embedVar1.add_field(name="Attack", value=Attack, inline=True)
    embedVar1.add_field(name="Defence", value=Defence, inline=True)
    embedVar1.add_field(name="Strength", value=Strength, inline=True)
    embedVar1.add_field(name="Hitpoints", value=Hitpoints, inline=True)
    embedVar1.add_field(name="Ranged", value=Ranged, inline=True)
    embedVar1.add_field(name="Prayer", value=Prayer, inline=True)
    embedVar1.add_field(name="Magic", value=Magic, inline=True)
    embedVar1.add_field(name="Cooking", value=Cooking, inline=True)
    embedVar1.add_field(name="Woodcutting", value=Woodcutting, inline=True)
    embedVar1.add_field(name="Fletching", value=Fletching, inline=True)
    embedVar1.add_field(name="Fishing", value=Fishing, inline=True)
    embedVar1.add_field(name="Firemaking", value=Firemaking, inline=True)
    embedVar1.add_field(name="Crafting", value=Crafting, inline=True)
    embedVar1.add_field(name="Smithing", value=Smithing, inline=True)
    embedVar1.add_field(name="Mining", value=Mining, inline=True)
    embedVar1.add_field(name="Herblore", value=Herblore, inline=True)
    embedVar1.add_field(name="Agility", value=Agility, inline=True)
    embedVar1.add_field(name="Thieving", value=Thieving, inline=True)
    embedVar1.add_field(name="Slayer", value=Slayer, inline=True)
    embedVar1.add_field(name="Farming", value=Farming, inline=True)
    embedVar1.add_field(name="Runecraft", value=Runecraft, inline=True)
    embedVar1.add_field(name="Hunter", value=Hunter, inline=True)
    embedVar1.add_field(name="Construction", value=Construction, inline=True)

    embedVar2 = discord.Embed(title=listtostring2(pnameinput) + " - High Scores",
                              description="Displaying Counts For Bosses/MiniGames B-C For " + listtostring2(
                                  pnameinput) + "\n===========================================", color=0x00fff0,
                              timestamp=datetime.utcnow())
    embedVar2.set_thumbnail(url="https://i.imgur.com/itFUcLj.jpg")
    embedVar2.add_field(name="Bounty Hunter \nHunter", value=BountyHunterHunter, inline=True)
    embedVar2.add_field(name="Bounty Hunter \nRogue", value=BountyHunterRogue, inline=True)
    embedVar2.add_field(name="Clue Scrolls \n(all)", value=ClueScrollsall, inline=True)
    embedVar2.add_field(name="Clue Scrolls \n(beginner)", value=ClueScrollsbeginner, inline=True)
    embedVar2.add_field(name="Clue Scrolls \n(easy)", value=ClueScrollseasy, inline=True)
    embedVar2.add_field(name="Clue Scrolls \n(medium)", value=ClueScrollsmedium, inline=True)
    embedVar2.add_field(name="Clue Scrolls \n(hard)", value=ClueScrollshard, inline=True)
    embedVar2.add_field(name="Clue Scrolls \n(elite)", value=ClueScrollselite, inline=True)
    embedVar2.add_field(name="Clue Scrolls \n(master)", value=ClueScrollsmaster, inline=True)
    embedVar2.add_field(name="LMS - Rank", value=LMSRank, inline=True)
    embedVar2.add_field(name="Soul Wars \nZeal", value=SoulWarsZeal, inline=True)
    embedVar2.add_field(name="Abyssal Sire", value=AbyssalSire, inline=True)
    embedVar2.add_field(name="Alchemical \nHydra", value=AlchemicalHydra, inline=True)
    embedVar2.add_field(name="Barrows \nChests", value=BarrowsChests, inline=True)
    embedVar2.add_field(name="Bryophyta", value=Bryophyta, inline=True)
    embedVar2.add_field(name="Callisto", value=Callisto, inline=True)
    embedVar2.add_field(name="Cerberus", value=Cerberus, inline=True)
    embedVar2.add_field(name="Chambers of Xeric", value=ChambersofXeric, inline=True)
    embedVar2.add_field(name="Chambers of Xeric: \nChallenge Mode", value=ChambersofXericChallengeMode, inline=True)
    embedVar2.add_field(name="Chaos \nElemental", value=ChaosElemental, inline=True)
    embedVar2.add_field(name="Chaos \nFanatic", value=ChaosFanatic, inline=True)
    embedVar2.add_field(name="Commander \nZilyana", value=CommanderZilyana, inline=True)
    embedVar2.add_field(name="Corporeal \nBeast", value=CorporealBeast, inline=True)
    embedVar2.add_field(name="Crazy \nArchaeologist", value=CrazyArchaeologist, inline=True)

    embedVar3 = discord.Embed(title=listtostring2(pnameinput) + " - High Scores",
                              description="Displaying Counts For Bosses/MiniGames D-S For " + listtostring2(
                                  pnameinput) + "\n===========================================", color=0x00fff0,
                              timestamp=datetime.utcnow())
    embedVar3.set_thumbnail(url="https://i.imgur.com/itFUcLj.jpg")
    embedVar3.add_field(name="Dagannoth \nPrime", value=DagannothPrime, inline=True)
    embedVar3.add_field(name="Dagannoth \nRex", value=DagannothRex, inline=True)
    embedVar3.add_field(name="Dagannoth \nSupreme", value=DagannothSupreme, inline=True)
    embedVar3.add_field(name="Deranged \nArchaeologist", value=DerangedArchaeologist, inline=True)
    embedVar3.add_field(name="General \nGraardor", value=GeneralGraardor, inline=True)
    embedVar3.add_field(name="Giant \nMole", value=GiantMole, inline=True)
    embedVar3.add_field(name="Grotesque \nGuardians", value=GrotesqueGuardians, inline=True)
    embedVar3.add_field(name="Hespori", value=Hespori, inline=True)
    embedVar3.add_field(name="Kalphite \nQueen", value=KalphiteQueen, inline=True)
    embedVar3.add_field(name="King Black \nDragon", value=KingBlackDragon, inline=True)
    embedVar3.add_field(name="Kraken", value=Kraken, inline=True)
    embedVar3.add_field(name="Kree'Arra", value=KreeArra, inline=True)
    embedVar3.add_field(name="K'ril \nTsutsaroth", value=KrilTsutsaroth, inline=True)
    embedVar3.add_field(name="Mimic", value=Mimic, inline=True)
    embedVar3.add_field(name="Nightmare", value=Nightmare, inline=True)
    embedVar3.add_field(name="Phosani's \nNightmare", value=PhosanisNightmare, inline=True)
    embedVar3.add_field(name="Obor", value=Obor, inline=True)
    embedVar3.add_field(name="Sarachnis", value=Sarachnis, inline=True)
    embedVar3.add_field(name="Scorpia", value=Scorpia, inline=True)
    embedVar3.add_field(name="Skotizo", value=Skotizo, inline=True)

    embedVar4 = discord.Embed(title=listtostring2(pnameinput) + " - High Scores",
                              description="Displaying Counts For Bosses/MiniGames T-Z For " + listtostring2(
                                  pnameinput) + "\n===========================================", color=0x00fff0,
                              timestamp=datetime.utcnow())
    embedVar4.set_thumbnail(url="https://i.imgur.com/itFUcLj.jpg")
    embedVar4.add_field(name="Tempoross", value=Tempoross, inline=True)
    embedVar4.add_field(name="The Gauntlet", value=TheGauntlet, inline=True)
    embedVar4.add_field(name="The Corrupted \nGauntlet", value=TheCorruptedGauntlet, inline=True)
    embedVar4.add_field(name="Theatre of Blood", value=TheatreofBlood, inline=True)
    embedVar4.add_field(name="Theatre of Blood: \nHard Mode", value=TheatreofBloodHardMode, inline=True)
    embedVar4.add_field(name="Thermonuclear \nSmoke Devil", value=ThermonuclearSmokeDevil, inline=True)
    embedVar4.add_field(name="TzKal-Zuk", value=TzKaZuk, inline=True)
    embedVar4.add_field(name="TzTok-Jad", value=TzTokJad, inline=True)
    embedVar4.add_field(name="Venenatis", value=Venenatis, inline=True)
    embedVar4.add_field(name="Vet'ion", value=Vetion, inline=True)
    embedVar4.add_field(name="Vorkath", value=Vorkath, inline=True)
    embedVar4.add_field(name="Wintertodt", value=Wintertodt, inline=True)
    embedVar4.add_field(name="Zalcano", value=Zalcano, inline=True)
    embedVar4.add_field(name="Zulrah", value=Zulrah, inline=True)
    embedVar4.set_footer(text="Version 1.0")

    await ctx.channel.send(embed=embedVar, view=view1)

    async def button_callback1(interaction):
        await interaction.message.edit(embed=embedVar, view=view1)

    async def button_callback2(interaction):
        await interaction.message.edit(embed=embedVar1, view=view2)

    async def button_callback3(interaction):
        await interaction.message.edit(embed=embedVar2, view=view3)

    async def button_callback4(interaction):
        await interaction.message.edit(embed=embedVar3, view=view4)

    async def button_callback5(interaction):
        await interaction.message.edit(embed=embedVar4, view=view5)

    button1.callback = button_callback1
    button2.callback = button_callback2
    button3.callback = button_callback3
    button4.callback = button_callback4
    button5.callback = button_callback5

    file1.close()
    file2.close()"""


bot.run(os.getenv(str('TOKEN')))
