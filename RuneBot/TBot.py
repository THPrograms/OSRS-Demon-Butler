from PIL import Image, ImageDraw, ImageFont
from PIL import ImageFilter
import requests
import sqlite3
from datetime import datetime, date, timedelta
import traceback


def test():
    channelgroups = []
    output = []
    UserData = getusers()
    if UserData == "error":
        print("getusers - An error has occurred at " + str(datetime.now()) + " for " + str(UserData[0]))
        return
    channels = list(dict.fromkeys([(guild[4], guild[3]) for guild in UserData]))
    for i in channels:
        group = [user for user in UserData if user[4] == i[0] and user[3] == i[1]]
        channelgroups.append(group)
        print (i)
    print (channelgroups)



async def statmonitor():
    channelgroups = []
    output = []
    UserData = getusers()
    if UserData == "error":
        print("getusers - An error has occurred at " + str(datetime.now()) + " for " + str(UserData[0]))
        return
    channels = list(dict.fromkeys([(guild[4], guild[3]) for guild in UserData]))
    for i in channels:
        group = [user for user in UserData if user[4] == i[0] and user[3] == i[1]]
        channelgroups.append(group)
        print(i)
    print(channelgroups)
    for group in channelgroups:
        for iud in group:
            data = hiscoresoup(iud)
            if data == "error":
                print("hiscoresoup - An error has occurred at " + str(datetime.now()) + " for " + str(iud[0]))
                continue
            else: pass
            sureturn = statsupdate(data, iud)
            if sureturn == "error":
                print("statsupdate - An error has occurred at " + str(datetime.now()) + " for " + str(iud[0]))
                continue
            else: pass
            finalStats = statcompare(iud)
            if finalStats == "error":
                print("statcompare - An error has occurred at " + str(datetime.now()) + " for " + str(iud[0]))
                continue
            else: pass
            for stats in finalStats:
                if stats:
                    output.append(stats)
        if not output:
            print("No stats to report")
        else:
            print("Stats to report")
            ResultsUpdate(output)
            extendinterface(output)
            await send_message((str(group[0][4])), (str(group[0][3])),
                               r"C:\Users\tommy\Documents\GitHub\RuneBot\OSRSInterface\Final_Interface.png")
        print(output)
        print("Ran at: " + str(datetime.now()))



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



def getusers():
    try:
        Users = []
        conn = dbconnection(r"C:\Users\Tommy\Documents\GitHub\RuneBot\RuneBot\RuneBotDB.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM Users")
        rows = cur.fetchall()
        for i in rows:
            Users.append(list(i))
        return Users
    except:
        conn = dbconnection(r"C:\Users\Tommy\Documents\GitHub\RuneBot\RuneBot\RuneBotDB.db")
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

test()

