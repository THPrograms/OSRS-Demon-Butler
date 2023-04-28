from PIL import Image, ImageDraw, ImageFont
from PIL import ImageFilter
import requests

def addtext(Skill, User, Level, XP, Rank, ExpToLvl, RecAchv):
    image = Image.open(r"C:\Users\tommy\Documents\GitHub\RuneBot\OSRSInterface\Skill Display.png")
    width, height = image.size
    draw = ImageDraw.Draw(image)
    titlefont = ImageFont.truetype(r"C:\Users\tommy\Documents\GitHub\RuneBot\OSRSInterface\runescape_uf\OCRAEXT.ttf",
                            26)
    statfont = ImageFont.truetype(r"C:\Users\tommy\Documents\GitHub\RuneBot\OSRSInterface\runescape_uf\OCRAEXT.ttf",
                            23)
    recntachfont = ImageFont.truetype(r"C:\Users\tommy\Documents\GitHub\RuneBot\OSRSInterface\runescape_uf\OCRAEXT.ttf",
                            12)
    draw.text((22, 18), Skill + ' - ' + User, (127,71,221), font=titlefont)
    draw.text((89, 61), Level, (207,144,21), font=statfont)
    draw.text((67, 93), XP, (207,144,21), font=statfont)
    draw.text((79, 124), Rank, (207,144,21), font=statfont)
    draw.text((151, 155), ExpToLvl, (207,144,21), font=statfont)
    draw.text((342, 95), 'Phantom Mus. 228 -> 397', (207, 144, 21), font=recntachfont)
    image.save(r"C:\Users\tommy\Documents\GitHub\RuneBot\OSRSInterface\Final_SkillDis.png")
    print('Image created')


addtext('Construction', 'OborsBigToe', '99', '200000000', '1', '0', '0')