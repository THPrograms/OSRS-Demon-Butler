from PIL import Image, ImageDraw, ImageFont
from PIL import ImageFilter
import requests
import sqlite3
from datetime import datetime, date, timedelta
import traceback
def skilladdtext(Skill, User, Level, XP, Rank, ExpToLvl, RecAchv):
    image = Image.open(r"C:\Users\THerndon\Documents\GitHub\RuneBot\OSRSInterface\Skill Display.png")
    width, height = image.size
    draw = ImageDraw.Draw(image)
    font = r"C:\Users\THerndon\Documents\GitHub\RuneBot\OSRSInterface\runescape_uf\OCRAEXT.TTF"
    titlefont = ImageFont.truetype(font, 26)
    statfont = ImageFont.truetype(font, 23)
    recntachfont = ImageFont.truetype(font, 12)
    draw.text((22, 18), Skill + ' - ' + User, (127,71,221), font=titlefont)
    draw.text((89, 61), Level, (207,144,21), font=statfont)
    draw.text((67, 93), XP, (207,144,21), font=statfont)
    draw.text((79, 124), Rank, (207,144,21), font=statfont)
    draw.text((151, 155), ExpToLvl, (207,144,21), font=statfont)
    draw.text((342, 95), 'Phantom Mus. 228 -> 397', (207, 144, 21), font=recntachfont)
    image.save(r"C:\Users\THerndon\Documents\GitHub\RuneBot\OSRSInterface\Final_SkillDis.png")
    print('Image created')


###

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

def getvachievements():
    try:
        Users = []
        conn = dbconnection(r"C:\Users\THerndon\Documents\GitHub\RuneBot\RuneBot\RuneBotDB.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM v_achievements")
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

def endofday():
    users = []
    startendstats = []
    conn = dbconnection(r"C:\Users\THerndon\Documents\GitHub\RuneBot\RuneBot\RuneBotDB.db")
    c = conn.cursor()
    c.execute("SELECT UserName From Users")
    rows = c.fetchall()
    for row in rows:
        users.append(row[0])
    dt = date.today() - timedelta(5)
    fdt = dt.strftime("%m/%d/%Y")
    sfdt = (fdt+"%")
    for user in users:
        c.execute("SELECT * FROM PlayerStats WHERE Date LIKE ? AND Username = ? ORDER BY Date DESC LIMIT 1", (sfdt+"%", user))
        End = c.fetchall()
        print (End[0])
        c.execute("SELECT * FROM PlayerStats WHERE Date LIKE ? AND Username = ? ORDER BY Date ASC LIMIT 1", (fdt+"%", user))
        Start = c.fetchall()
        print (Start[0])
        startendstats.append((Start[0], End[0]))

    conn.close()
    print (startendstats[0])



#endofday()
#skilladdtext('Construction', 'OborsBigToe', '99', '200000000', '1', '0', '0')

print (getvachievements())