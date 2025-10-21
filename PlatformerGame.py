import pygame as scr
import random as rng
import time
import math
import sys
import os

path = os.path.dirname(os.path.abspath(__file__))

def limit(var,base,cap):
    return max(min(var,cap),base)

def write(msg,pos,size,col):
    sFont = scr.font.Font(os.path.join(path,'Fonts','Grand9K Pixel.ttf'),size)
    Ssurf = sFont.render(msg,True,col)
    Srect = Ssurf.get_rect()
    Srect.midtop = pos
    bdr.blit(Ssurf, Srect)

def draw(img,pos,size):
    dImg = img.copy()
    dImg = scr.transform.scale(dImg,size)
    dRct = dImg.get_rect()
    dRct.centre = pos
    bdr.blit(dImg,dRct)

def writelines(msgs,pos,size,col,bCol):
    run = True
    while run:
        clk.tick(60)
        for event in scr.event.get():
            if event.type == scr.QUIT:
                run = False
                scr.quit()
                sys.exit()
            elif event.type == scr.KEYDOWN:
                run = False
        bdr.fill(bCol)
        for msg in range(len(msgs)):
            write(msgs[msg],(pos[0],pos[1]+1.2*size*msg),size,col)
        write('Press Any Key to Return',(pos[0],pos[1]+1.25*size*len(msgs)),size,col)
        scr.display.flip()

def selector(opts,cols,dTxt,dPos,bPos,dSze,tSze,bSze,tCol,bCol):
    sel = 0
    sSpd = 0
    pSpd = 0
    cancel = False
    run = True
    while run:
        clk.tick(60)
        for event in scr.event.get():
            if event.type == scr.QUIT:
                run = False
                scr.quit()
                sys.exit()
            elif event.type == scr.KEYDOWN:
                if event.key == scr.K_ESCAPE:
                    run = False
                    cancel = True
                elif event.key == scr.K_LEFT:
                    sSpd -= 1
                elif event.key == scr.K_RIGHT:
                    sSpd += 1
                elif event.key == scr.K_z:
                    run = False
            elif event.type == scr.KEYUP:
                if event.key == scr.K_LEFT:
                    sSpd += 1
                elif event.key == scr.K_RIGHT:
                    sSpd -= 1
        sSpd = limit(sSpd,-1,1)
        if sSpd != 0 or not (sel/10).is_integer():
            if sSpd != 0:
                pSpd = sSpd
            sel = (sel+pSpd+5)%(len(opts)*10)-5
        bdr.fill(bCol)
        write(dTxt,dPos,dSze,tCol)
        for i in range(len(opts)):
            scale = max(1,2-abs(i-(sel/10)))/2
            r,g,b = cols[i]
            scr.draw.rect(bdr,(max(0,r-25),max(0,g-25),max(0,b-25)),scr.Rect(math.floor(bPos[0]-bSze[0]*(sel/10-i)-bSze[0]*scale/2),math.floor(bPos[1]-bSze[1]*scale/2),math.floor(bSze[0]*scale),math.floor(bSze[1]*scale)),border_radius=math.floor(10*scale))
            scr.draw.rect(bdr,(r,g,b),scr.Rect(math.floor(bPos[0]-bSze[0]*(sel/10-i)-bSze[0]*scale/2),math.floor(bPos[1]-bSze[1]*scale/2),math.floor(bSze[0]*scale),math.floor(bSze[1]*scale)-10),border_radius=math.floor(10*scale))
            write(opts[i],(bPos[0]-bSze[0]*(sel/10-i),bPos[1]-tSze*scale/2),math.floor(tSze*scale),tCol)
        scr.display.flip()
    if cancel:
        return None
    else:
        return opts[sel//10]

def textbox(cLim,tLns,dTxt,tPos,bPos,tSze,bSze,tCol,bCol,aCap=True):
    text = []
    line = 0
    caps = False
    kbrd = [{scr.K_BACKQUOTE:'`',scr.K_1:'1',scr.K_2:'2',scr.K_3:'3',scr.K_4:'4',scr.K_5:'5',scr.K_6:'6',scr.K_7:'7',scr.K_8:'8',scr.K_9:'9',scr.K_0:'0',scr.K_MINUS:'-',scr.K_EQUALS:'=',
            scr.K_q:'q',scr.K_w:'w',scr.K_e:'e',scr.K_r:'r',scr.K_t:'t',scr.K_y:'y',scr.K_u:'u',scr.K_i:'i',scr.K_o:'o',scr.K_p:'p',scr.K_LEFTBRACKET:'[',scr.K_RIGHTBRACKET:']',scr.K_BACKSLASH:'\\',
            scr.K_a:'a',scr.K_s:'s',scr.K_d:'d',scr.K_f:'f',scr.K_g:'g',scr.K_h:'h',scr.K_j:'j',scr.K_k:'k',scr.K_l:'l',scr.K_SEMICOLON:';',scr.K_QUOTE:'\'',
            scr.K_z:'z',scr.K_x:'x',scr.K_c:'c',scr.K_v:'v',scr.K_b:'b',scr.K_n:'n',scr.K_m:'m',scr.K_COMMA:',',scr.K_PERIOD:'.',scr.K_SLASH:'/',scr.K_SPACE:' '},
            {scr.K_BACKQUOTE:'~',scr.K_1:'!',scr.K_2:'@',scr.K_3:'#',scr.K_4:'$',scr.K_5:'%',scr.K_6:'^',scr.K_7:'&',scr.K_8:'*',scr.K_9:'(',scr.K_0:')',scr.K_MINUS:'_',scr.K_EQUALS:'+',
            scr.K_q:'Q',scr.K_w:'W',scr.K_e:'E',scr.K_r:'R',scr.K_t:'T',scr.K_y:'Y',scr.K_u:'U',scr.K_i:'I',scr.K_o:'O',scr.K_p:'P',scr.K_LEFTBRACKET:'{',scr.K_RIGHTBRACKET:'}',scr.K_BACKSLASH:'|',
            scr.K_a:'A',scr.K_s:'S',scr.K_d:'D',scr.K_f:'F',scr.K_g:'G',scr.K_h:'H',scr.K_j:'J',scr.K_k:'K',scr.K_l:'L',scr.K_SEMICOLON:':',scr.K_QUOTE:'"',
            scr.K_z:'Z',scr.K_x:'X',scr.K_c:'C',scr.K_v:'V',scr.K_b:'B',scr.K_n:'N',scr.K_m:'M',scr.K_COMMA:'<',scr.K_PERIOD:'>',scr.K_SLASH:'?',scr.K_SPACE:' '}]
    for i in range(tLns):
        text.append('')
    cancel = False
    run = True
    while run:
        clk.tick(60)
        for event in scr.event.get():
            if event.type == scr.QUIT:
                run = False
                scr.quit()
                sys.exit()
            elif event.type == scr.KEYDOWN:
                if event.key == scr.K_ESCAPE:
                    run = False
                    cancel = True
                if not aCap:
                    if event.key in cKys:
                        text[line] = cKys[event.key]
                        run = False
                else:
                    if event.key in kbrd[caps]:
                        if len(text[line]) == cLim:
                            line = (line+1)%tLns
                        text[line] = text[line]+kbrd[caps][event.key]
                    elif event.key == scr.K_BACKSPACE:
                        if text[line] == '':
                            line = (line-1)%tLns
                        else:
                            text[line] = text[line][0:-1]
                    elif event.key == scr.K_LSHIFT:
                        caps = aCap
                    elif event.key == scr.K_RETURN:
                        if line == tLns-1:
                            run = False
                        else:
                            line = line+1
            elif event.type == scr.KEYUP:
                if event.key == scr.K_LSHIFT:
                    caps = False
        bdr.fill(bCol)
        write(dTxt,tPos,tSze,tCol)
        for i in range(tLns):
            if i == line and time.mktime(time.localtime())%2 == 0:
                write(text[i]+'|',(bPos[0],bSze*i+bPos[1]),bSze,tCol)
            else:
                write(text[i],(bPos[0],bSze*i+bPos[1]),bSze,tCol)
        scr.display.flip()
    if cancel:
        return None
    else:
        fMsg = ''
        for i in range(tLns):
            if i > 0:
                fMsg = fMsg+'\n'
            fMsg = fMsg+text[i]
        return fMsg

def slider(sVal,vMin,vMax,dTxt,dPos,sPos,dSze,tSze,sSze,tCol,oCol,lCol,hCol,bCol):
    val = sVal
    sSpd = 0
    sDel = 0
    cancel = False
    run = True
    while run:
        clk.tick(60)
        for event in scr.event.get():
            if event.type == scr.QUIT:
                run = False
                scr.quit()
                sys.exit()
            elif event.type == scr.KEYDOWN:
                if event.key == scr.K_ESCAPE:
                    run = False
                    cancel = True
                elif event.key == scr.K_LEFT:
                    sSpd -= 1
                elif event.key == scr.K_RIGHT:
                    sSpd += 1
                elif event.key == scr.K_z:
                    run = False
            elif event.type == scr.KEYUP:
                if event.key == scr.K_LEFT:
                    sSpd += 1
                elif event.key == scr.K_RIGHT:
                    sSpd -= 1
        sDel = max(0,sDel-1)
        if sSpd != 0 and sDel <= 0:
            val = limit(val+sSpd,vMin,vMax)
            sDel = 5
        bdr.fill(bCol)
        write(dTxt,dPos,dSze,tCol)
        x = sSze[0]*((val-vMin)/(vMax-vMin))
        scr.draw.rect(bdr,hCol,scr.Rect(sPos[0]-(sSze[0]//2),sPos[1],sSze[0],sSze[1]))
        scr.draw.rect(bdr,lCol,scr.Rect(sPos[0]-(sSze[0]//2),sPos[1],x,sSze[1]))
        scr.draw.rect(bdr,oCol,scr.Rect(sPos[0]-(sSze[0]//2)-5,sPos[1]-5,sSze[0]+10,sSze[1]+10),5,border_radius=5)
        write(str(val),(sPos[0]-(sSze[0]//2)+x,sPos[1]+sSze[1]+10),tSze,tCol)
        scr.display.flip()
    if cancel:
        return sVal
    else:
        return val

scr.init()

scr.display.set_icon(scr.image.load(os.path.join(path,'Sprites','icon.png')))
bdr = scr.display.set_mode((800,600),scr.SCALED|scr.RESIZABLE)
scr.display.set_caption('PlatformerGame')

sSFX = scr.mixer.Sound(os.path.join(path,'SFX','step.mp3'))      # Step Sound Effect
jSFX = scr.mixer.Sound(os.path.join(path,'SFX','jump.mp3'))      # Jump Sound Effect
wSFX = scr.mixer.Sound(os.path.join(path,'SFX','win.mp3'))       # Win Sound Effect
lSFX = scr.mixer.Sound(os.path.join(path,'SFX','destroyed.mp3')) # Lose Sound Effect
aSFX = scr.mixer.Sound(os.path.join(path,'SFX','powerUp.mp3'))   # Acceleration Sound Effect
bSFX = scr.mixer.Sound(os.path.join(path,'SFX','bounce.mp3'))    # Bounce Sound Effect
fSFX = scr.mixer.Sound(os.path.join(path,'SFX','tinyJump.mp3'))  # Sticky Jump Sound Effect
tSFX = scr.mixer.Sound(os.path.join(path,'SFX','warp.mp3'))      # Warp Sound Effect
sCdn = 0 # Step Sound Cooldown
sSFX.set_volume(0.3)
aSFX.set_volume(0.1)
gVol = 100 # Game Volume

cKys = {scr.K_BACKQUOTE:'`',scr.K_1:'1',scr.K_2:'2',scr.K_3:'3',scr.K_4:'4',scr.K_5:'5',scr.K_6:'6',scr.K_7:'7',scr.K_8:'8',scr.K_9:'9',scr.K_0:'0',scr.K_MINUS:'-',scr.K_EQUALS:'=',scr.K_BACKSPACE:'Bksp',scr.K_DELETE:'Del',scr.K_INSERT:'Insert',
        scr.K_TAB:'Tab',scr.K_q:'Q',scr.K_w:'W',scr.K_e:'E',scr.K_r:'R',scr.K_t:'T',scr.K_y:'Y',scr.K_u:'U',scr.K_i:'I',scr.K_o:'O',scr.K_p:'P',scr.K_LEFTBRACKET:'[',scr.K_RIGHTBRACKET:']',scr.K_BACKSLASH:'\\',scr.K_HOME:'Home',scr.K_END:'End',
        scr.K_a:'A',scr.K_s:'S',scr.K_d:'D',scr.K_f:'F',scr.K_g:'G',scr.K_h:'H',scr.K_j:'J',scr.K_k:'K',scr.K_l:'L',scr.K_SEMICOLON:';',scr.K_QUOTE:'\'',scr.K_RETURN:'Enter',scr.K_PAGEUP:'PgUp',scr.K_PAGEDOWN:'PgDown',
        scr.K_LSHIFT:'LShift',scr.K_z:'Z',scr.K_x:'X',scr.K_c:'C',scr.K_v:'V',scr.K_b:'B',scr.K_n:'N',scr.K_m:'M',scr.K_COMMA:',',scr.K_PERIOD:'.',scr.K_SLASH:'/',scr.K_RSHIFT:'RShift',scr.K_UP:'Up',
        scr.K_LCTRL:'LCtrl',scr.K_LALT:'LAlt',scr.K_SPACE:'Space',scr.K_RALT:'RAlt',scr.K_RCTRL:'RCtrl',scr.K_LEFT:'Left',scr.K_DOWN:'Down',scr.K_RIGHT:'Right'}
ctrl = {'left':scr.K_LEFT,'right':scr.K_RIGHT,'jump':scr.K_UP,'select':scr.K_z,'back':scr.K_x,'reset':scr.K_c} # Controls
ctNm = {'left':'Move Left','right':'Move Right','jump':'Jump','select':'Next Level/Warp','back':'Previous Level','reset':'Reset Level'} # Control Names
dTxt = 0         # Info Text Display Time
iTxt = ''        # Info Text To Be Displayed
fscn = False     # Fullscreen Active
aMde = False     # Assist Mode Active
nMde = False     # Exit Into Nightmare Levels Flag
pPos = (400,500) # Player Position (centered)
hAcc = 0         # Horizontal Acceleration (rightPressed-leftPressed)
hVel = 0         # Horizontal Velocity
fDir = 1         # Facing Direction
jHgt = -15       # Jump Height
bHgt = -25       # Bounce Pad Jump Height
sHgt = -5        # Sticky Jump Height
jmps = 0         # Times Jumped Since Ground Touched
mJmp = 1         # Max Jumps Before Touching Ground
cJmp = 1         # Flight Flag (0 is flying, 1 is jumping)
tJmp = False     # Attempt Jump Flag
wJmp = False     # Wall Jump Flag
vVel = 0         # Vertical Velocity (up to down)
pMVl = 3         # Max Horizontal Velocity
aMVl = 10        # Max Horizontal Velocity On Accelerator
sFct = 0.95      # Jump Slowing Factor
gAcc = 0.75      # Acceleration Due To Gravity
tVel = 20        # Terminal Velocity
cTme = 0         # Coyote Time Counter
jPrd = 10        # Jump Period (max coyote time)
wTyp = -1        # Wall Type
fTyp = -1        # Floor Type
wSfc = 0         # Warp Surface
lArr = [[(0,scr.Rect(0,550,800,50),False),(0,scr.Rect(70,480,100,20),False),(0,scr.Rect(150,400,100,20),False),(3,scr.Rect(325,355,100,20),False),    # Platforms In Basic Levels
         (0,scr.Rect(150,310,100,20),False),(0,scr.Rect(-50,300,100,20),False),(0,scr.Rect(750,300,100,20),False),(0,scr.Rect(630,250,100,20),False), # Formatted (surfaceType,boundingBox,assistModeOnly)
         (2,scr.Rect(550,190,100,20),False),(0,scr.Rect(380,170,100,20),False),(1,scr.Rect(350,110,100,20),False),(0,scr.Rect(75,305,50,20),True)],
        [(0,scr.Rect(0,550,800,50),False),(0,scr.Rect(575,475,100,20),False),(0,scr.Rect(440,425,100,20),False),(0,scr.Rect(300,375,100,20),False),
         (0,scr.Rect(145,310,100,20),False),(6,scr.Rect(40,240,100,20),False),(2,scr.Rect(165,125,100,20),False),(2,scr.Rect(320,125,90,20),False),
         (2,scr.Rect(460,125,75,20),False),(2,scr.Rect(585,125,50,20),False),(4,scr.Rect(245,210,450,20),False),(1,scr.Rect(680,125,100,20),False),
         (0,scr.Rect(242,207,456,26),True)],
        [(0,scr.Rect(0,550,800,50),False),(0,scr.Rect(47,332,755,14),False),(0,scr.Rect(17,413,13,14),False),(0,scr.Rect(65,468,15,15),False),
         (0,scr.Rect(119,517,19,19),False),(4,scr.Rect(743,342,50,213),False),(5,scr.Rect(75,330,729,17),False),(2,scr.Rect(523,278,16,12),False),
         (2,scr.Rect(589,231,18,13),False),(2,scr.Rect(665,187,23,12),False),(0,scr.Rect(1,170,224,11),False),(1,scr.Rect(492,42,62,14),False),
         (2,scr.Rect(750,166,20,14),False),(6,scr.Rect(783,249,14,82),True),(5,scr.Rect(449,34,15,129),False),(2,scr.Rect(279,151,20,12),False),
         (2,scr.Rect(360,135,21,13),False)],
        [(0,scr.Rect(0,550,800,50),False),(5,scr.Rect(0,430,20,120),False),(0,scr.Rect(80,430,640,20),False),(5,scr.Rect(780,430,20,120),False),
         (4,scr.Rect(0,0,20,350),False),(4,scr.Rect(780,0,20,350),False),(6,scr.Rect(200,300,20,75),False),(6,scr.Rect(315,260,20,75),False),
         (5,scr.Rect(120,190,20,75),False),(6,scr.Rect(45,130,20,75),False),(5,scr.Rect(225,115,20,75),False),(5,scr.Rect(300,100,75,20),False),
         (6,scr.Rect(475,130,20,75),False),(1,scr.Rect(400,250,50,20),False),(6,scr.Rect(-3,-3,26,356),True),(6,scr.Rect(777,-3,26,356),True),
         (6,scr.Rect(600,365,50,20),True),(6,scr.Rect(540,320,50,20),True),(6,scr.Rect(480,280,50,20),True),(4,scr.Rect(360,160,20,100),False),
         (6,scr.Rect(357,157,26,106),True),(5,scr.Rect(535,80,200,20),False)],
        [(0,scr.Rect(0,550,475,50),False),(0,scr.Rect(550,550,250,50),False),(1,scr.Rect(490,350,45,20),False),(0,scr.Rect(657,480,100,20),False),
         (0,scr.Rect(15,440,100,20),False),(5,scr.Rect(140,120,20,300),False),(0,scr.Rect(185,110,100,20),False),(6,scr.Rect(400,155,20,250),False),
         (6,scr.Rect(605,155,20,250),False),(0,scr.Rect(325,125,100,20),False),(4,scr.Rect(320,450,20,100),False),(0,scr.Rect(317,447,26,106),True),
         (6,scr.Rect(475,600,75,20),True)],
        [(0,scr.Rect(0,550,80,20),False),(0,scr.Rect(120,550,80,20),False),(0,scr.Rect(240,550,80,20),False),(0,scr.Rect(360,550,80,20),False),
         (0,scr.Rect(480,550,80,20),False),(0,scr.Rect(600,550,80,20),False),(0,scr.Rect(720,550,80,20),False),(3,scr.Rect(60,480,80,20),False),
         (3,scr.Rect(180,480,80,20),False),(3,scr.Rect(300,480,80,20),False),(3,scr.Rect(420,480,80,20),False),(3,scr.Rect(540,480,80,20),False),
         (3,scr.Rect(660,480,80,20),False),(2,scr.Rect(120,410,80,20),False),(2,scr.Rect(240,410,80,20),False),(2,scr.Rect(360,410,80,20),False),
         (2,scr.Rect(480,410,80,20),False),(2,scr.Rect(600,410,80,20),False),(0,scr.Rect(180,340,80,20),False),(4,scr.Rect(300,340,80,20),False),
         (4,scr.Rect(420,340,80,20),False),(0,scr.Rect(540,340,80,20),False),(5,scr.Rect(240,270,80,20),False),(5,scr.Rect(360,270,80,20),False),
         (5,scr.Rect(480,270,80,20),False),(6,scr.Rect(300,200,80,20),False),(6,scr.Rect(420,200,80,20),False),(1,scr.Rect(360,70,80,20),False),
         (0,scr.Rect(297,337,86,26),True),(0,scr.Rect(417,337,86,26),True),(6,scr.Rect(0,600,800,20),True)],
        [(0,scr.Rect(0,550,800,50),False),(7,scr.Rect(170,388,20,150),False),(0,scr.Rect(250,435,100,20),False),(7,scr.Rect(401,277,20,125),False),
         (2,scr.Rect(271,320,75,20),False),(7,scr.Rect(204,154,20,150),False),(1,scr.Rect(285,215,65,20),False),(0,scr.Rect(268,317,81,26),True)],
        [(7,scr.Rect(0,550,800,50),False),(5,scr.Rect(195,395,20,155),False),(7,scr.Rect(0,395,195,20),False),(5,scr.Rect(0,275,20,120),False),
         (7,scr.Rect(90,255,160,20),False),(5,scr.Rect(230,155,20,100),False),(7,scr.Rect(250,155,200,20),False),(1,scr.Rect(470,210,75,20),False),
         (7,scr.Rect(0,200,20,75),False),(5,scr.Rect(640,220,20,330),True),(7,scr.Rect(640,145,20,75),True)]]
nArr = [[(0,scr.Rect(0,550,800,50),False),(0,scr.Rect(98,447,95,23),False),(4,scr.Rect(1,334,181,53),False),(2,scr.Rect(254,407,50,32),False),       # Platforms In Nightmare Levels
         (2,scr.Rect(363,377,50,29),False),(6,scr.Rect(501,356,103,33),False),(4,scr.Rect(617,197,17,410),False),(2,scr.Rect(660,215,106,31),False),
         (0,scr.Rect(60,273,61,30),False),(3,scr.Rect(161,239,205,32),False),(4,scr.Rect(289,190,25,70),False),(4,scr.Rect(201,189,20,72),False),
         (0,scr.Rect(389,201,50,30),False),(4,scr.Rect(375,246,77,25),False),(4,scr.Rect(448,174,17,99),False),(0,scr.Rect(447,145,50,29),False),
         (0,scr.Rect(389,65,50,29),False),(1,scr.Rect(269,72,12,11),False),(4,scr.Rect(492,23,21,154),False),(4,scr.Rect(216,81,114,26),False),
         (0,scr.Rect(-3,500,89,27),False)],
        [(4,scr.Rect(0,590,800,11),False),(0,scr.Rect(397,560,9,11),False),(2,scr.Rect(307,532,9,11),False),(2,scr.Rect(215,500,8,9),False),
         (2,scr.Rect(162,422,10,10),False),(2,scr.Rect(44,494,9,11),False),(2,scr.Rect(654,562,127,9),False),(4,scr.Rect(674,498,85,12),False),
         (4,scr.Rect(647,543,9,32),False),(2,scr.Rect(534,534,50,13),False),(4,scr.Rect(527,505,10,40),False),(2,scr.Rect(472,503,56,18),False),
         (4,scr.Rect(456,451,17,73),False),(3,scr.Rect(459,447,17,13),False),(4,scr.Rect(429,450,27,12),False),(3,scr.Rect(531,404,4,12),False),
         (4,scr.Rect(426,402,7,58),False),(3,scr.Rect(622,364,10,14),False),(2,scr.Rect(667,308,148,18),False),(4,scr.Rect(709,282,14,42),False),
         (4,scr.Rect(788,279,15,46),False),(5,scr.Rect(-8,284,261,17),False),(4,scr.Rect(202,252,9,49),False),(2,scr.Rect(244,283,118,20),False),
         (2,scr.Rect(423,244,15,13),False),(3,scr.Rect(484,198,120,17),False),(6,scr.Rect(614,153,80,16),False),(4,scr.Rect(696,14,12,156),False),
         (3,scr.Rect(740,142,32,20),False),(4,scr.Rect(698,153,103,15),False),(5,scr.Rect(28,131,188,17),False),(4,scr.Rect(210,103,10,46),False),
         (0,scr.Rect(214,128,113,20),False),(0,scr.Rect(390,85,15,13),False),(1,scr.Rect(494,40,12,12),False),(4,scr.Rect(527,-12,12,81),False),
         (4,scr.Rect(471,60,60,16),False)],
        [(2,scr.Rect(54,542,373,5),False),(4,scr.Rect(427,445,8,102),False),(4,scr.Rect(-3,414,11,185),False),(5,scr.Rect(-4,584,492,19),False),
         (4,scr.Rect(474,553,14,54),False),(4,scr.Rect(388,445,50,8),False),(4,scr.Rect(330,487,13,58),False),(4,scr.Rect(247,493,14,53),False),
         (4,scr.Rect(127,485,55,13),False),(4,scr.Rect(95,523,12,23),False),(3,scr.Rect(500,568,48,20),False),(2,scr.Rect(618,590,4,20),False),
         (2,scr.Rect(677,531,6,88),False),(2,scr.Rect(737,547,4,34),False),(5,scr.Rect(790,360,21,156),False),(4,scr.Rect(787,502,25,50),False),
         (3,scr.Rect(7,379,51,14),False),(2,scr.Rect(102,335,3,37),False),(2,scr.Rect(168,354,4,16),False),(6,scr.Rect(238,340,7,15),False),
         (3,scr.Rect(283,145,8,16),False),(4,scr.Rect(327,107,11,147),False),(5,scr.Rect(331,109,476,16),False),(3,scr.Rect(261,198,2,3),False),
         (1,scr.Rect(353,220,5,13),False),(4,scr.Rect(467,73,12,48),False),(4,scr.Rect(642,74,14,46),False),(4,scr.Rect(799,88,6,28),False),
         (0,scr.Rect(7,111,61,14),False),(5,scr.Rect(118,180,3,12),False),(5,scr.Rect(50,208,27,14),False),(4,scr.Rect(149,66,7,146),False),
         (4,scr.Rect(36,121,50,8),False),(0,scr.Rect(735,213,90,12),False),(2,scr.Rect(585,263,109,12),False),(4,scr.Rect(611,208,51,15),False),
         (4,scr.Rect(578,247,13,28),False),(3,scr.Rect(502,257,56,13),False),(4,scr.Rect(331,241,84,16),False),(4,scr.Rect(400,197,15,62),False),
         (3,scr.Rect(455,211,9,21),False),(3,scr.Rect(399,191,17,12),False)]]
pCol = [(225,225,125),(175,255,175),(145,200,255),(125,85,35),(225,75,75),(225,175,35),(35,75,35),(145,60,200),(230,150,195)] # Surface Colours
pSfc = [0.85,0.85,0.99,0.6,0.85,1.1,0.2,0.4,0.85] # Surface Friction
 # Surfaces Are: -1 Midair, 0 Basic, 1 Objective, 2 Ice, 3 Mud, 4 Kill, 5 Accelerator, 6 Bounce Pad, 7 Sticky, 8 Warp

clk = scr.time.Clock()

def playGame(pArr,sLvl,cSkp,bCol,aLvl=[True]):
    global tJmp
    global fTyp
    global hVel
    global hAcc
    global wTyp
    global vVel
    global aMde
    global sCdn
    global cJmp
    global cTme
    global ctrl
    global dTxt
    global nMde
    global iTxt
    global gVol
    global fDir
    global wSfc
    global jmps
    wArr = []
    aArr = aLvl
    assd = False
    cLvl = sLvl
    hLvl = sLvl
    pPos = (400,500)
    for i in range(len(pArr)):
        wArr.append([])
        for ptfm in pArr[i]:
            if ptfm[0] == 8:
                wArr[i].append(ptfm)
    run = True
    while run:
        clk.tick(60)
        for event in scr.event.get():
            if event.type == scr.QUIT:
                run = False
            elif event.type == scr.KEYDOWN:
                if event.key == scr.K_ESCAPE:
                    run = False
                elif event.key == scr.K_n:
                    nMde = True
                    iTxt = 'Press Escape To Enter NIGHTMARE MODE'
                    dTxt = 180
                elif event.key == ctrl['left']:
                    hAcc -= 1
                    fDir = -1
                elif event.key == ctrl['right']:
                    hAcc += 1
                    fDir = 1
                elif event.key == ctrl['jump']:
                    tJmp = True
                elif event.key == ctrl['select']:
                    if fTyp == 1 or ((aMde or hLvl > cLvl) and cSkp):
                        if fTyp == 1:
                            try:
                                aArr[cLvl] = assd
                            except Exception as error:
                                if error == IndexError:
                                    aArr.append(assd)
                        assd = aMde
                        cLvl = (cLvl+1)%len(pArr)
                        if hLvl < cLvl:
                            aArr.append(True)
                            hLvl = cLvl
                            wSFX.play()
                        pPos = (400,500)
                        hVel = 0
                        vVel = 0
                    elif fTyp == 8:
                        pPos = (wArr[cLvl][(wSfc+1)%len(wArr[cLvl])][1].midtop[0],
                                wArr[cLvl][(wSfc+1)%len(wArr[cLvl])][1].midtop[1]-30)
                        tSFX.play()
                elif event.key == ctrl['back'] and cSkp:
                    if cLvl > 0:
                        cLvl -= 1
                        pPos =(400,500)
                        hVel = 0
                        vVel = 0
                elif event.key == ctrl['reset']:
                    pPos = (400,500)
                    hVel = 0
                    vVel = 0
            elif event.type == scr.KEYUP:
                if event.key == ctrl['left']:
                    hAcc += 1
                elif event.key == ctrl['right']:
                    hAcc -= 1
                elif event.key == ctrl['jump']:
                    tJmp = False
        if tJmp:
            if jmps < mJmp-1 or (jmps == mJmp-1 and cTme < jPrd) or (jmps == mJmp and wJmp):
                if fTyp == 6:
                    vVel = bHgt
                    bSFX.play()
                elif fTyp == 7:
                    vVel = sHgt
                    fSFX.play()
                else:
                    vVel = jHgt
                    jSFX.play()
                jmps += cJmp
        if fTyp == 5:
            hVel = limit(hVel+fDir,-aMVl,aMVl)
        else:
            hVel = limit(hVel+limit(hAcc,-1,1),-pMVl,pMVl)
        if wTyp == 5:
            vVel = limit(vVel*sFct-1,bHgt,tVel)
            hVel += fDir*aMVl
        elif wTyp == 7:
            vVel = limit(vVel*sFct+gAcc,bHgt,tVel)/3
            wJmp = True
            cTme = 0
        else:
            vVel = limit(vVel*sFct+gAcc,bHgt,tVel)
        x,y = pPos
        for i in range(4):
            hBlk = False
            vBlk = False
            for ptfm in pArr[cLvl]:
                if not ptfm[2] or aMde:
                    if scr.Rect((x+(hVel/4)+10)%820-20,y-10,20,20).colliderect(ptfm[1]):
                        hBlk = True
                        wTyp = ptfm[0]
                    if scr.Rect(x-10,y+(vVel/4)-10,20,20).colliderect(ptfm[1]):
                        vBlk = True
                        fTyp = ptfm[0]
                        if fTyp == 8:
                            wSfc = wArr[cLvl].index(ptfm)
                    if scr.Rect((x+(hVel/4)+10)%820-20,y+((vVel-gAcc)/4)-10,20,20).colliderect(ptfm[1]) and not (scr.Rect((x+(hVel/4)+10)%820-20,y-10,20,20).colliderect(ptfm[1]) or scr.Rect(x-10,y+(vVel/4)-10,20,20).colliderect(ptfm[1])):
                        hBlk = True
                        vBlk = True
            if hBlk:
                if wTyp == 6:
                    hVel *= -1.25
                    vVel -= 5
                    fDir *= -1
                else:
                    hVel = 0
            else:
                if hVel != 0:
                    wTyp = -1
                x = (x+(hVel/4)+10)%820-10
                sCdn += 1
                if sCdn >= 20:
                    if fTyp == 5 and hVel != 0:
                        aSFX.play()
                    elif hAcc != 0:
                        sSFX.play()
                    sCdn = 0
            if vBlk:
                if vVel > 0:
                    jmps = 0
                    cTme = 0
                    wJmp = False
                if fTyp == 6 and (vVel > 1 or vVel < 0):
                    vVel *= -0.95
                else:
                    vVel = 0
                hVel *= pSfc[fTyp]
            else:
                if vVel != 0 and cTme >= jPrd:
                    fTyp = -1
                y = y+(vVel/4)
                if wTyp == 5 and hVel == 0 and sCdn >= 19:
                    aSFX.play()
                if cJmp == 1:
                    cTme += 1
        pPos = (x,y)
        if fTyp == 4 or wTyp == 4 or y > 800:
            pPos = (400,500)
            hVel = 0
            vVel = 0
            wTyp = 0
            fTyp = 0
            lSFX.play()
        bdr.fill(bCol)
        for ptfm in pArr[cLvl]:
            if not ptfm[2]:
                scr.draw.rect(bdr,pCol[ptfm[0]],ptfm[1])
            elif aMde:
                scr.draw.rect(bdr,pCol[ptfm[0]],ptfm[1],3)
        if cLvl == 0 and cSkp:
            write(cKys[ctrl['select']],(400,10),60,(35,35,75))
        scr.draw.rect(bdr,(255,255,225),scr.Rect(pPos[0]-10,pPos[1]-10,20,20))
        if dTxt > 0:
            dTxt -= 1
            write(iTxt,(175,10),15,(225,225,255))
        else:
            iTxt = ''
        scr.display.flip()
    if cSkp:
        return hLvl,aArr
    else:
        return hLvl

def saveGame(bPgs,nPgs,aPgs):
    start = False
    if not start:
        act = selector(['Save to New File','Save to Existing File','Quit Without Saving'],[(35,255,75),(25,175,255),(255,95,125)],'Save before Quitting?',(400,75),(400,350),65,25,(350,250),(255,255,225),(0,0,15))
        if act == 'Save to New File':
            sNme = textbox(24,1,'Name the New File',(400,75),(400,325),65,40,(255,255,225),(0,0,15))
            if sNme != None:
                with open(path+'/SavedFiles/'+sNme+'.sav','w') as f:
                    f.write(sNme+'\n')
                    f.write(str(bPgs)+'\n')
                    f.write(str(nPgs))
                    for l in aPgs:
                        f.write('\n'+str(int(l)))
                start = True
                return sNme
        elif act == 'Save to Existing File':
            sNme = selector(fNms,fCol,'Overwrite which File?',(400,75),(400,350),65,30,(350,250),(255,255,225),(0,0,15))
            if sNme in fNms:
                with open(path+'/SavedFiles/'+sNme+'.sav','w') as f:
                    f.write(sNme+'\n')
                    f.write(str(bPgs)+'\n')
                    f.write(str(nPgs))
                    for l in aPgs:
                        f.write('\n'+str(int(l)))
                start = True
                return sNme
        else:
            start = True
            return None

def editor():
    files = os.listdir(path+'/CustomLevels')
    lNms = []
    lvls = []
    lCol = []
    for file in files:
        lines = []
        with open(path+'/CustomLevels/'+file,'r') as f:
            data = f.readlines()
            for l in data:
                lines.append(l.strip())
        lNms.append(lines[0])
        lines.remove(lines[0])
        level = []
        for i in range(0,len(lines),6):
            level.append((int(lines[i]),scr.Rect(int(lines[i+1]),int(lines[i+2]),int(lines[i+3]),int(lines[i+4])),bool(int(lines[i+5]))))
        lvls.append(level)
        lCol.append((175,175,125))
    start = False
    while not start:
        act = selector(['Play Custom Level','Create New Level','Edit Existing Level','Erase Custom Level','Check Editor Controls','Back'],[(35,255,75),(125,255,255),(25,175,255),(255,95,125),(225,175,255),(255,240,65)],'Level Editor',(400,75),(400,350),65,25,(350,250),(255,255,225),(0,0,15))
        if act == 'Create New Level':
            lNme = textbox(24,1,'Name your new level',(400,75),(400,325),65,40,(255,255,225),(0,0,15))
            if lNme != None:
                scr.display.set_caption(lNme)
                lvl = editLvl(lNme,[(0,scr.Rect(0,550,800,50),False)])
                if lvl != None:
                    lNms.append(lNme)
                    lvls.append(lvl)
                    lCol.append((175,175,125))
        elif act == 'Edit Existing Level':
            lNme = selector(lNms,lCol,'Edit which Level?',(400,75),(400,350),65,30,(350,250),(255,255,225),(0,0,15))
            if lNme in lNms:
                scr.display.set_caption(lNme)
                lvl = editLvl(lNme,lvls[lNms.index(lNme)])
                if lvl != None:
                    lvls[lNms.index(lNme)] = lvl
        elif act == 'Play Custom Level':
            lNme = selector(lNms,lCol,'Play which Level?',(400,75),(400,350),65,30,(350,250),(255,255,225),(0,0,15))
            if lNme in lNms:
                playGame(lvls,lNms.index(lNme),False,(0,25,30))
        elif act == 'Erase Custom Level':
            lNme = selector(lNms,lCol,'Erase which Level?',(400,75),(400,350),65,30,(350,250),(255,255,225),(0,0,15))
            if lNme in lNms:
                if selector(['Don\'t Erase','Erase Permanently'],[(25,175,255),(255,95,125)],'Are you sure? It cannot be recovered.',(400,75),(400,325),40,30,(350,250),(255,255,225),(0,0,15)) == 'Yes':
                    lvls.remove(lvls[lNms.index(lNme)])
                    lNms.remove(lNme)
                    lCol.remove(lCol[0])
                    os.remove(path+'/CustomLevels/'+lNme)
        elif act == 'Check Editor Controls':
            writelines(['Level Editor Controls:','Up - Move Up/Thin','Down - Move Down/Widen','Left - Move Left/Shorten',
                      'Right - Move Right/Lengthen','Z - Create New Platform','X - Delete Platform','C - Save Level','V - Test Level',
                      'Tab - Cycle Selected Platform','Backtick - Switch Move/Scale','Num. 1-9 - Set Platform Type','0 - Set Platform Assist Mode Only',
                      'F11 - Toggle Full Screen'],(400,0),30,(255,255,225),(0,0,15))
        else:
            start = True

def editLvl(lNme,pArr):
    global hVel
    global vVel
    global dTxt
    eArr = pArr
    savd = False
    pSel = 0
    sMde = False
    nLne = {scr.K_1:0,scr.K_2:1,scr.K_3:2,scr.K_4:3,scr.K_5:4,scr.K_6:5,scr.K_7:6,scr.K_8:7,scr.K_9:8}
    run = True
    while run:
        clk.tick(60)
        for event in scr.event.get():
            if event.type == scr.QUIT:
                run = False
            elif event.type == scr.KEYDOWN:
                if event.key == scr.K_ESCAPE:
                    run = False
                elif event.key == scr.K_F11:
                    scr.display.toggle_fullscreen()
                elif event.key == scr.K_LEFT:
                    hVel -= 1
                elif event.key == scr.K_RIGHT:
                    hVel += 1
                elif event.key == scr.K_UP:
                    vVel -= 1
                elif event.key == scr.K_DOWN:
                    vVel += 1
                elif event.key == scr.K_z:
                    eArr.append((0,scr.Rect(375,275,50,50),False))
                    pSel = len(eArr)-1
                elif event.key == scr.K_x:
                    if len(eArr) > 1:
                        eArr.pop(pSel)
                        pSel = (pSel-1)%len(eArr)
                elif event.key == scr.K_c:
                    if selector(['Python List','Level File'],[(25,175,255),(35,255,75)],'Save As?',(400,75),(400,350),65,45,(350,250),(255,255,225),(0,0,15)) == 'Level File':
                        with open(path+'/CustomLevels/'+lNme+'.txt','w') as f:
                            f.write(lNme+'\n')
                            for ptfm in eArr:
                                f.write(str(ptfm[0])+'\n')
                                f.write(str(ptfm[1].left)+'\n')
                                f.write(str(ptfm[1].top)+'\n')
                                f.write(str(ptfm[1].width)+'\n')
                                f.write(str(ptfm[1].height)+'\n')
                                f.write(str(int(ptfm[2]))+'\n')
                        iTxt = f'Level saved at {path}/CustomLevels/{lNme}.txt'
                        dTxt = 180
                        savd = True
                    else:
                        print(str(eArr).replace(' ','').replace('<r','scr.R').replace('>',''))
                elif event.key == scr.K_v:
                    playGame([eArr],0,False,(0,30,45))
                elif event.key == scr.K_TAB:
                    pSel = (pSel+1)%len(eArr)
                elif event.key == scr.K_BACKQUOTE:
                    sMde = not sMde
                    iTxt = ['Move Mode','Scale Mode'][int(sMde)]
                    dTxt = 180
                elif event.key in nLne:
                    eArr[pSel] = (nLne[event.key],eArr[pSel][1],eArr[pSel][2])
                elif event.key == scr.K_0:
                    eArr[pSel] = (eArr[pSel][0],eArr[pSel][1],not eArr[pSel][2])
            elif event.type == scr.KEYUP:
                if event.key == scr.K_LEFT:
                    hVel += 1
                elif event.key == scr.K_RIGHT:
                    hVel -= 1
                elif event.key == scr.K_UP:
                    vVel += 1
                elif event.key == scr.K_DOWN:
                    vVel -= 1
        if sMde:
            eArr[pSel] = (eArr[pSel][0],eArr[pSel][1].inflate(hVel,vVel),eArr[pSel][2])
        else:
            eArr[pSel] = (eArr[pSel][0],eArr[pSel][1].move(hVel,vVel),eArr[pSel][2])
        if hVel != 0 or vVel != 0:
            iTxt = '{0} {1}:{3} {2}:{4}'.format(['Move','Scale'][int(sMde)],['X','W'][int(sMde)],['Y','H'][int(sMde)],
                                                [eArr[pSel][1].left,eArr[pSel][1].width][int(sMde)],[eArr[pSel][1].top,eArr[pSel][1].height][int(sMde)])
            dTxt = 180
        bdr.fill((0,30,0))
        for ptfm in eArr:
            if not ptfm[2]:
                scr.draw.rect(bdr,pCol[ptfm[0]],ptfm[1])
            else:
                scr.draw.rect(bdr,pCol[ptfm[0]],ptfm[1],3)
        scr.draw.rect(bdr,(0,255,255),eArr[pSel][1],2)
        if dTxt > 0:
            dTxt -= 1
            write(iTxt,(400,10),15,(225,225,255))
        else:
            iTxt = ''
        scr.display.flip()
    if selector(['Save Level','Quit Without Saving'],[(35,255,75),(255,95,125)],'Save before Quitting?',(400,75),(400,325),60,30,(350,250),(255,255,225),(0,0,15)) == 'Save Level':
        with open(path+'/CustomLevels/'+lNme+'.txt','w') as f:
            f.write(lNme+'\n')
            for ptfm in eArr:
                f.write(str(ptfm[0])+'\n')
                f.write(str(ptfm[1].left)+'\n')
                f.write(str(ptfm[1].top)+'\n')
                f.write(str(ptfm[1].width)+'\n')
                f.write(str(ptfm[1].height)+'\n')
                f.write(str(int(ptfm[2]))+'\n')
        savd = True
    if savd:
        return eArr
    else:
        return None

def options():
    global gVol
    global fscn
    global aMde
    start = False
    while not start:
        act = selector([['Set Fullscreen','Set Windowed'][fscn],'Volume','Controls',['Assist Mode Off','Assist Mode On'][aMde],'Back'],[[(0,15,220),(140,150,255)][fscn],(130,185,255),(255,130,40),[(255,95,125),(35,255,75)][aMde],(255,240,65)],'Options',(400,75),(400,350),65,30,(350,250),(255,255,225),(0,0,15))
        if act == ['Set Fullscreen','Set Windowed'][fscn]:
            scr.display.toggle_fullscreen()
            fscn = not fscn
        elif act == 'Volume':
            gVol = slider(gVol,0,100,'Set Volume',(400,75),(400,350),65,25,(550,25),(255,255,225),(255,255,225),(130,185,255),(0,25,45),(0,0,15))
            sSFX.set_volume(0.3*gVol/100)
            jSFX.set_volume(gVol/100)
            wSFX.set_volume(gVol/100)
            lSFX.set_volume(gVol/100)
            aSFX.set_volume(0.1*gVol/100)
            bSFX.set_volume(gVol/100)
            fSFX.set_volume(gVol/100)
            tSFX.set_volume(gVol/100)
        elif act == 'Controls':
            ctrls = []
            cols = []
            for n in list(ctNm.keys()):
                ctrls.append(ctNm[n]+' - '+cKys[ctrl[n]])
                cols.append((35,255,75))
            act = selector(ctrls,cols,'Edit Controls',(400,75),(400,350),65,25,(350,250),(255,255,225),(0,0,15))
            if act != None:
                c = act.split(" - ")[0]
                act = textbox(10,1,f'Edit {c}',(400,75),(400,325),65,40,(255,255,225),(0,0,15),False)
                if act != None:
                    ctrl[list(ctNm.keys())[list(ctNm.values()).index(c)]] = list(cKys.keys())[list(cKys.values()).index(act)]
        elif act == ['Assist Mode Off','Assist Mode On'][aMde]:
            aMde = not aMde
        else:
            start = True

# Load Options
with open(os.path.join(path,'options'),'r') as f:
    fscn = bool(int(f.readline().strip()))
    gVol = int(f.readline().strip())
    for c in list(ctrl.keys()):
        ctrl[c] = list(cKys.keys())[list(cKys.values()).index(f.readline().strip())]
    aMde = bool(int(f.readline().strip()))
    nMde = bool(int(f.readline().strip()))
    dMde = bool(int(f.readline().strip()))
if fscn:
    scr.display.toggle_fullscreen()

# Title Screen
start = False
while not start:
    files = os.listdir(path+'/SavedFiles')
    fNms = []
    fPgs = []
    fCol = []
    for file in files:
        lines = []
        with open(path+'/SavedFiles/'+file,'r') as f:
            data = f.readlines()
            for l in data:
                lines.append(l.strip())
        fNms.append(lines[0])
        lines.remove(lines[0])
        lvls = []
        for i in lines[2:len(lines)]:
            lvls.append(bool(int(i)))
        fPgs.append((int(lines[0]),int(lines[1]),lvls))
        fCol.append((175,175,125))
    act = selector(['New File','Load File','Erase File','Level Editor','Options','Quit'],[(35,255,75),(25,175,255),(255,95,125),(225,175,255),(185,185,185),(255,240,65)],'PlatformerGame',(400,75),(400,350),65,45,(350,250),(255,255,225),(0,0,15))
    if act == 'New File':
        bPgs,aPgs = playGame(lArr,0,True,(0,0,15))
        if nMde:
            nPgs = playGame(nArr,0,False,(40,0,0))
        else:
            nPgs = 0
        fNme = saveGame(bPgs,nPgs,aPgs)
        if fNme in fNms:
                fPgs[fNms.index(fNme)] = (bPgs,nPgs,aPgs)
        elif fNme != None:
            fNms.append(fNme)
            fPgs.append((bPgs,nPgs,aPgs))
            fCol.append((175,175,125))
    elif act == 'Load File':
        file = selector(fNms,fCol,'Load which File?',(400,75),(400,350),65,30,(350,250),(255,255,225),(0,0,15))
        if file in fNms:
            bPgs,aPgs = playGame(lArr,fPgs[fNms.index(file)][0],True,(0,0,15))
            if nMde:
                nPgs = playGame(nArr,fPgs[fNms.index(file)][1],False,(40,0,0))
            else:
                nPgs = fPgs[fNms.index(file)][1]
            fNme = saveGame(bPgs,nPgs,aPgs)
            if fNme in fNms:
                fPgs[fNms.index(fNme)] = (bPgs,nPgs,aPgs)
            elif fNme != None:
                fNms.append(fNme)
                fPgs.append((bPgs,nPgs,aPgs))
                fCol.append((175,175,125))
    elif act == 'Erase File':
        file = selector(fNms,fCol,'Erase which File?',(400,75),(400,350),65,30,(350,250),(255,255,225),(0,0,15))
        if file in fNms:
            if selector(['Don\'t Erase','Erase Permanently'],[(25,175,255),(255,95,125)],'Are you sure? It cannot be recovered.',(400,75),(400,325),40,30,(350,250),(255,255,225),(0,0,15)) == 'Yes':
                fPgs.remove(fPgs[fNms.index(file)])
                fNms.remove(file)
                os.remove(path+'/SavedFiles/'+file)
    elif act == 'Level Editor':
        editor()
    elif act == 'Options':
        options()
    else:
        start = True

# Save Options and Quit
with open(os.path.join(path,'options'),'w') as f:
    f.write(str(int(fscn))+'\n')
    f.write(str(gVol)+'\n')
    for c in list(ctrl.values()):
        f.write(str(cKys[c])+'\n')
    f.write(str(int(aMde))+'\n')
    f.write(str(int(nMde))+'\n')
    f.write(str(int(dMde))+'\n')
scr.quit()
