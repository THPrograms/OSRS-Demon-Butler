from PIL import Image, ImageDraw, ImageFont
from PIL import ImageFilter
import requests
import sqlite3
from datetime import datetime, date, timedelta
import traceback
def skilladdtext(Skill, User, Level, XP, Rank, ExpToLvl, RecAchv):
    image = Image.open(r"C:\Users\THerndon\Documents\GitHub\RuneBot\OSRSInterface\Skill Display.png")
    width, height = image.size
    achvcoord = 96
    draw = ImageDraw.Draw(image)
    font = r"C:\Users\THerndon\Documents\GitHub\RuneBot\OSRSInterface\runescape_uf\OCRAEXT.TTF"
    titlefont = ImageFont.truetype(font, 26)
    statfont = ImageFont.truetype(font, 23)
    recachvfont = ImageFont.truetype(font, 12)
    draw.text((22, 18), Skill + ' - ' + User, (127,71,221), font=titlefont)
    draw.text((89, 61), Level, (207,144,21), font=statfont)
    draw.text((67, 93), XP, (207,144,21), font=statfont)
    draw.text((79, 124), Rank, (207,144,21), font=statfont)
    draw.text((151, 155), ExpToLvl, (207,144,21), font=statfont)
    for achv in RecAchv:
        draw.text((355, achvcoord), achv, (207, 144, 21), font=recachvfont)
        achvcoord = achvcoord + 16
    image.save(r"C:\Users\THerndon\Documents\GitHub\RuneBot\OSRSInterface\Final_SkillDis.png")
    print('Image created')

def statsupdate(data, UserData):
    try:
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
    except:
        conn = dbconnection(r"C:\Users\tommy\Documents\GitHub\RuneBot\RuneBot\RuneBotDB.db")
        cur = conn.cursor()
        dt = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        e = str(traceback.format_exc())
        einput = ''.join(("\"", UserData[0] , e, "\""))
        cur.execute("INSERT INTO ErrorLog VALUES (?, ?)", (dt, einput))
        conn.commit()
        return 'error'
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

@bot.command()
async def skill(ctx: commands.Context):
    ctx.content = (ctx.message.content).title()
    Skill = ctx.message.content.split()[1]
    input = ctx.message.content.split()[1:]
    Username = userurl(input)[1]
    Url = userurl(input)[0]
    data = hiscoresoup([Username, Url])
    if data == 'error':
        print("hiscoresoup - An error has occurred at " + str(datetime.now()) + " during skill function")
        await ctx.send("An error has occurred. Please try again later.")
        return
    else: pass
    sureturn = statsupdate(data, [Username])
    if sureturn == 'error':
        print("statsupdate - An error has occurred at " + str(datetime.now()) + " during skill function")
        await ctx.send("An error has occurred. Please try again later.")
        return
    else: pass

def xptolvl(Level, XP):
    pass

def skillfromdb(Username, Skill):
    try:
        conn = dbconnection(r"C:\Users\tommy\Documents\GitHub\RuneBot\RuneBot\RuneBotDB.db")
        cur = conn.cursor()
        fields = [Skill,"\"" + Skill + " Rank\"", "\"" + Skill + " Level\"", "\"" +Skill + " XP\""]
        print (fields[1])
        print (fields)
        print (Username)
        print (Skill)
        query = "SELECT {0}, {1}, {2}, {3} FROM PlayerStats WHERE Username = ? ORDER BY Date DESC LIMIT 1".format(fields[0], fields[1], fields[2], fields[3])
        cur.execute(query, (Username,))
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except:
        conn = dbconnection(r"C:\Users\tommy\Documents\GitHub\RuneBot\RuneBot\RuneBotDB.db")
        cur = conn.cursor()
        dt = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        e = str(traceback.format_exc())
        einput = ''.join(("\"", Username , e, "\""))
        cur.execute("INSERT INTO ErrorLog VALUES (?, ?)", (dt, einput))
        conn.commit()
        return 'error'


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
    except:
        conn = dbconnection(r"C:\Users\tommy\Documents\GitHub\RuneBot\RuneBot\RuneBotDB.db")
        cur = conn.cursor()
        dt = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        e = str(traceback.format_exc())
        einput = ''.join(("\"", UserData[0] , e, "\""))
        cur.execute("INSERT INTO ErrorLog VALUES (?, ?)", (dt, einput))
        conn.commit()
        return 'error'

def dbconnection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn
def getcategories():
    try:
        Categories = []
        conn = dbconnection(r"C:\Users\THerndon\Documents\GitHub\RuneBot\RuneBot\RuneBotDB.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM Categories")
        rows = cur.fetchall()
        for i in rows:
            Categories.append(list(i))
        return Categories
    except:
        conn = dbconnection(r"C:\Users\THerndon\Documents\GitHub\RuneBot\RuneBot\RuneBotDB.db")
        cur = conn.cursor()
        dt = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        e = str(traceback.format_exc())
        einput = ''.join(("\"", 'getcategories', e, "\""))
        cur.execute("INSERT INTO ErrorLog VALUES (?, ?)", (dt, einput))
        conn.commit()
        return 'error'

def getvachievements(Users, Limit=5):
    achvs = []
    try:
        for i in Users:
            conn = dbconnection(r"C:\Users\THerndon\Documents\GitHub\RuneBot\RuneBot\RuneBotDB.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM v_achievements WHERE UserName = ? ORDER BY Date DESC LIMIT ?", (i, Limit))
            rows = cur.fetchall()
            for i in rows:
                achvs.append(list(i))
        return achvs
    except:
        conn = dbconnection(r"C:\Users\THerndon\Documents\GitHub\RuneBot\RuneBot\RuneBotDB.db")
        cur = conn.cursor()
        dt = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        e = str(traceback.format_exc())
        einput = ''.join(("\"", 'getusers', e, "\""))
        cur.execute("INSERT INTO ErrorLog VALUES (?, ?)", (dt, einput))
        conn.commit()
        return 'error'

def getusers():
    try:
        Users = []
        conn = dbconnection(r"C:\Users\THerndon\Documents\GitHub\RuneBot\RuneBot\RuneBotDB.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM Users")
        rows = cur.fetchall()
        for i in rows:
            Users.append(list(i))
        return Users
    except:
        conn = dbconnection(r"C:\Users\THerndon\Documents\GitHub\RuneBot\RuneBot\RuneBotDB.db")
        cur = conn.cursor()
        dt = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        e = str(traceback.format_exc())
        einput = ''.join(("\"", 'getusers', e, "\""))
        cur.execute("INSERT INTO ErrorLog VALUES (?, ?)", (dt, einput))
        conn.commit()
        return 'error'

def endofday(users):
    startendstats = []
    conn = dbconnection(r"C:\Users\THerndon\Documents\GitHub\RuneBot\RuneBot\RuneBotDB.db")
    c = conn.cursor()
    dt = date.today() - timedelta(6)
    fdt = dt.strftime("%m/%d/%Y")
    sfdt = (fdt+"%")
    for user in users:
        c.execute("SELECT * FROM PlayerStats WHERE Date LIKE ? AND Username = ? ORDER BY Date DESC LIMIT 1", (sfdt+"%", user[0]))
        End = c.fetchall()
        print (End[0])
        c.execute("SELECT * FROM PlayerStats WHERE Date LIKE ? AND Username = ? ORDER BY Date ASC LIMIT 1", (fdt+"%", user[0]))
        Start = c.fetchall()
        print (Start[0])
        startendstats.append((Start[0], End[0]))

    conn.close()
    print (startendstats[0])



#endofday()
#skilladdtext('Construction', 'OborsBigToe', '99', '200000000', '1', '0', '0')
#Users = ['OborsBigToe', 'Grewp Eyeron']
#print (getvachievements(Users, 5))
#achievlist = ["DSupreme 777 -> 888","Muspah 40 -> 56","Zalcano 120 -> 172", "Woodcutt 67 -> 68", "Winterto 89 -> 90"]
#skilladdtext('Construction', 'OborsBigToe', '99', '200000000', '1', '0', achievlist)
skillfromdb('Oborsbigtoe', 'Attack')