import datetime
import discord
from discord.ui import Button, View
import time
from discord.ext import commands

#establishing connection with discord
TOKEN = 'OTA3MDc1OTU2ODc3OTU5MTcw.G_wZ61.MqgT-iCMf5e0DU9jr92IcrTnOHnTKAJ_OL86vY'

client = discord.Client()

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
          'TzKal-Zuk', 'TzTok-Jad', 'Venenatis', "Vet'ion", 'Vorkath', 'Wintertodt', 'Zalcano', 'Zulrah','N/A']



@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

#If message starts with !rank, spit out high score ranking from OSRS highscores
    if message.content.startswith('!rank'):
        message.content = message.content.lower()
        gnamelookup = message.content.split()
        glength = len(gnamelookup)
        gnamelast = message.content.split()[glength-1:]
        gnameinput = message.content.split()[1:]

        def listtostring(gnameinput):
            str1 = " "
            return (str1.join(gnameinput)).replace(" ","+")

        def listtostring2(gnamelast):
            str1 = " "
            return (str1.join(gnamelast)).replace(" ","+")

        import requests
#designating the web url to pull from
        url = 'https://secure.runescape.com/m=hiscore_oldschool_ironman/group-ironman/?groupName='+ (listtostring(gnameinput).title())

        r = requests.get(url)

        from bs4 import BeautifulSoup

        soup = BeautifulSoup(r.content, 'html.parser')

        rows = soup.select('tbody tr')
#grabbing all data in the table body on the osrs highscores
        n = soup.find_all('td')
        Gdata = n
#write the entire table body data into a text file for review
        file1 = open("RuneBot/GroupIronStats", "w+")

        file1.write(str(Gdata))
        file1.close()

        string1 = (listtostring2(gnamelast)) + '</a>'

        file1 = open("RuneBot/GroupIronStats", "r")

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

            file1 = open("RuneBot/GroupIronStats", "r")

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
            await message.channel.send('```Group Name: ' + gname.title() + '\nRank: ' + grank + '\nTotal Level: ' + gtotlvl + '\nTotal XP: ' + gtotexp + '```'.format(message.author))


#pulling any players skill stats
    if message.content.startswith('!skill'):
        message.content = (message.content).title()
        SkillLookup = message.content.split()[1]
        pnameinput = message.content.split()[2:]

        def listtostring(pnameinput):
            str1 = " "
            return (str1.join(pnameinput)).replace(" ", "%A0")
        def listtostring2(pnameinput):
            str1 = " "
            return (str1.join(pnameinput))

        print (listtostring(pnameinput))
        print (SkillLookup)

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


        file1 = open("RuneBot/Pstats", "w+")

        file1.write(str(pstats))
        file1.close()

        file1 = open("RuneBot/Pstats", "r")

        flag = 0
        index = 0
        # Grabbing Line That Silk Cart group data is on
        for line in file1:
            index += 1

            if SkillLookup in line:
                flag = 1
                break

        if flag == 0:
            await message.channel.send('```' + SkillLookup + ' Does Not Exist Or Does Not Meet Highscore Requirements```'.format(message.author))
        else:
            file1.close()

            file1 = open("RuneBot/Pstats", "r")

            personalstats = file1.readlines()
            # combining the variables
            skill = (personalstats[index - 1]).strip()
            prank = (personalstats[index + 1]).strip()
            plevel = (personalstats[index + 2]).strip()
            pxp = (personalstats[index + 3]).strip()
            await message.channel.send('```Name: ' + listtostring2(pnameinput) + '\nSkill: ' + skill + '\nRank: ' + prank + '\nLevel: ' + plevel + '\nXP: ' + pxp + '```'.format(message.author))

#pulling any players skill stats
    if message.content.startswith('!kc'):
        message.content = (message.content).title()
        BossLookup = (message.content).split()[1]
        pnameinput = (message.content).split()[2:]

        def listtostring(pnameinput):
            str1 = " "
            return (str1.join(pnameinput)).replace(" ", "%A0")
        def listtostring2(pnameinput):
            str1 = " "
            return (str1.join(pnameinput))

        print (listtostring(pnameinput))
        print (BossLookup)

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


        file1 = open("RuneBot/Pstats", "w+")

        file1.write(str(pstats))
        file1.close()

        file1 = open("RuneBot/Pstats", "r")

        flag = 0
        index = 0
        # Grabbing Line That Silk Cart group data is on
        for line in file1:
            index += 1

            if BossLookup in line:
                flag = 1
                break

        if flag == 0:
            await message.channel.send('```' + BossLookup + ' Does Not Exist Or Does Not Meet Highscore Requirements```'.format(message.author))
        else:
            file1.close()

            file1 = open("RuneBot/Pstats", "r")

            personalstats = file1.readlines()
            # combining the variables
            skillboss = (personalstats[index - 1]).strip()
            prank = (personalstats[index]).strip()
            pscore = (personalstats[index + 1]).strip()
            await message.channel.send('```Name: ' + listtostring2(pnameinput) + '\nBoss: ' + skillboss + '\nRank: ' + prank + '\nScore: ' + pscore + '```'.format(message.author))
            #embedVar = discord.Embed(title="OSRS High Scores",description="This bot is a work in progress, thank you for giving it a try.",color=0x00fff0, timestamp=datetime.datetime.utcnow())
            #embedVar.set_thumbnail(url="https://i.imgur.com/ZIsEXmZ.png")
            #embedVar.add_field(name="Commands:",value="!rank [group name] - Pulls Group Iron group ranking from OSRS High Scores\n\n!skill [skill] [playername] - Pulls the current stats for the provided player's skill\n\n!kc [boss/minigame](Use First Or Last Name Ex: Rex For Daganoth Rex) [playername] - Pulls The Current Stats For The Provided Player And Boss/Minigame",inline=False)
            #embedVar.add_field(name="Creator:", value="Thomikaze#4519", inline=False)
            #embedVar.add_field(name="Contact:", value="TommyF.Herndon@gmail.com", inline=False)
            #embedVar.set_footer(text="Version 1.0")
            #await message.channel.send(embed=embedVar)


    if message.content.startswith('!help'):
        embedVar = discord.Embed(title="OSRS High Scores", description="This bot is a work in progress, thank you for giving it a try.", color=0x00fff0, timestamp=datetime.datetime.utcnow())
        embedVar.set_thumbnail(url="https://i.imgur.com/ZIsEXmZ.png")
        embedVar.add_field(name="Commands:", value="!rank [group name] - Pulls Group Iron group ranking from OSRS High Scores\n\n!skill [skill] [playername] - Pulls the current stats for the provided player's skill\n\n!kc [boss/minigame](Use First Or Last Name Ex: Rex For Daganoth Rex) [playername] - Pulls The Current Stats For The Provided Player And Boss/Minigame", inline=False)
        embedVar.add_field(name="Creator:", value="Thomikaze#4519",inline=False)
        embedVar.add_field(name="Contact:", value="TommyF.Herndon@gmail.com", inline=False)
        embedVar.set_footer(text="Version 1.0")
        await message.channel.send(embed=embedVar)

    if message.content.startswith('!player'):
        message.content = (message.content).title()
        pnameinput = message.content.split()[1:]


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
        print (url)
        # Create a handle, page, to handle the contents of the website
        page = requests.get(url)
        print (page)
        # Store the contents of the website under doc
        doc = lh.fromstring(page.content)
        print (doc)
        # Parse data that are stored between <tr>..</tr> of HTML
        tr_elements = doc.xpath('//tr')
        print (tr_elements)
        # Create empty list
        col = []
        i = 0
        # For each row, store each first element (header) and an empty list
        pstats = ""
        for t in tr_elements[0]:
            i += 1
            name = t.text_content()
            pstats = pstats + ('%d:"%s"' % (i, name))

        file1 = open("RuneBot/Pstats", "w+")

        file1.write(str(pstats))
        file1.write("\nN/A" + "\nN/A" + "\nN/A" + "\nN/A" + "\nN/A")
        file1.close()

        with open("RuneBot/Pstats", "r") as file1:
            data = file1.readlines()
        file1.close()

        data[9] = "Blank\n"

        with open("RuneBot/Pstats", "w") as file1:
            file1.writelines(data)
        file1.close()




        file1 = open("RuneBot/Pstats", "r")
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

        file2 = open("RuneBot/Fstats", "w")

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

        print (flist)
        file2.close()


        #for I in hslist:
           #print(I)

        print (plist)
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

        file1 = open("RuneBot/Pstats", "r")
        file2 = open("RuneBot/Fstats", "r")
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

        embedVar = discord.Embed(title=listtostring2(pnameinput)+" - High Scores",description="This bot is a work in progress, thank you for giving it a try.",color=0x00fff0, timestamp=datetime.datetime.now())
        embedVar.set_thumbnail(url="https://i.imgur.com/itFUcLj.jpg")
        embedVar.add_field(name="Overall", value=Overall, inline=False)

        embedVar1 = discord.Embed(title=listtostring2(pnameinput)+" - High Scores",description="Displaying Character Stats For " + listtostring2(pnameinput) + "\n===============================",color=0x00fff0, timestamp=datetime.datetime.utcnow())
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

        embedVar2 = discord.Embed(title=listtostring2(pnameinput)+" - High Scores",description="Displaying Counts For Bosses/MiniGames B-C For " + listtostring2(pnameinput) + "\n===========================================",color=0x00fff0, timestamp=datetime.datetime.utcnow())
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

        embedVar3 = discord.Embed(title=listtostring2(pnameinput)+" - High Scores",description="Displaying Counts For Bosses/MiniGames D-S For " + listtostring2(pnameinput) + "\n===========================================",color=0x00fff0, timestamp=datetime.datetime.utcnow())
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

        embedVar4 = discord.Embed(title=listtostring2(pnameinput)+" - High Scores",description="Displaying Counts For Bosses/MiniGames T-Z For " + listtostring2(pnameinput) + "\n===========================================",color=0x00fff0, timestamp=datetime.datetime.utcnow())
        embedVar4.set_thumbnail(url="https://i.imgur.com/itFUcLj.jpg")
        embedVar4.add_field(name="Tempoross", value=Tempoross, inline=True)
        embedVar4.add_field(name="The Gauntlet", value=TheGauntlet, inline=True)
        embedVar4.add_field(name="The Corrupted \nGauntlet", value=TheCorruptedGauntlet, inline=True)
        embedVar4.add_field(name="Theatre of Blood", value=TheatreofBlood, inline=True)
        embedVar4.add_field(name="Theatre of Blood: \nHard Mode", value=TheatreofBloodHardMode,inline=True)
        embedVar4.add_field(name="Thermonuclear \nSmoke Devil", value=ThermonuclearSmokeDevil,inline=True)
        embedVar4.add_field(name="TzKal-Zuk", value=TzKaZuk, inline=True)
        embedVar4.add_field(name="TzTok-Jad", value=TzTokJad, inline=True)
        embedVar4.add_field(name="Venenatis", value=Venenatis, inline=True)
        embedVar4.add_field(name="Vet'ion", value=Vetion, inline=True)
        embedVar4.add_field(name="Vorkath", value=Vorkath, inline=True)
        embedVar4.add_field(name="Wintertodt", value=Wintertodt, inline=True)
        embedVar4.add_field(name="Zalcano", value=Zalcano, inline=True)
        embedVar4.add_field(name="Zulrah", value=Zulrah, inline=True)
        embedVar4.set_footer(text="Version 1.0")

        await message.channel.send(embed=embedVar, view=view1)
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
        file2.close()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)