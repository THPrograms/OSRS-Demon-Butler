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
Users = ['OborsBigToe', 'Grewp Eyeron']
#print (getvachievements(Users, 5))
achievlist = ["DSupreme 777 -> 888","Muspah 40 -> 56","Zalcano 120 -> 172", "Woodcutt 67 -> 68", "Winterto 89 -> 90"]
skilladdtext('Construction', 'OborsBigToe', '99', '200000000', '1', '0', achievlist)