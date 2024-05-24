from vex import *
import random, time, sys

# BEGIN definice konstant

DELKA = 200
PAUZA = 0.3

L_Block = [
    [
    [False,True,False,False],
    [False,True,False,False],
    [False,True,True,False],
    [False,False,False,False]
    ],
    [
    [False,False,True,False],
    [True,True,True,False],
    [False,False,False,False],
    [False,False,False,False]
    ],
    [
    [True,True,False,False],
    [False,True,False,False],
    [False,True,False,False],
    [False,False,False,False]
    ],
    [
    [False,False,False,False],
    [True,True,True,False],
    [True,False,False,False],
    [False,False,False,False]
    ]
]

CUBE_Block = [
    [
    [False,False,False,False],
    [False,True,True,False],
    [False,True,True,False],
    [False,False,False,False]
    ],
    [
    [False,False,False,False],
    [False,True,True,False],
    [False,True,True,False],
    [False,False,False,False]
    ],
    [
    [False,False,False,False],
    [False,True,True,False],
    [False,True,True,False],
    [False,False,False,False]
    ],
    [
    [False,False,False,False],
    [False,True,True,False],
    [False,True,True,False],
    [False,False,False,False]
    ]
]

Z_Block = [
    [
    [False,False,True,False],
    [False,True,True,False],
    [False,True,False,False],
    [False,False,False,False]
    ],
    [
    [False,False,False,False],
    [False,True,True,False],
    [False,False,True,True],
    [False,False,False,False]
    ],
    [
    [False,True,False,False],
    [False,True,True,False],
    [False,False,True,False],
    [False,False,False,False]
    ],
    [
    [False,False,True,False],
    [False,True,True,False],
    [False,True,False,False],
    [False,False,False,False]
    ]
]

T_Block = [
    [
    [False,False,False,False],
    [False,True,False,False],
    [False,True,True,False],
    [False,True,False,False]
    ],
    [
    [False,False,False,False],
    [False,True,False,False],
    [True,True,True,False],
    [False,False,False,False]
    ],
    [
    [False,False,False,False],
    [False,True,False,False],
    [True,True,False,False],
    [False,True,False,False]
    ],
    [
    [False,False,False,False],
    [False,False,False,False],
    [True,True,True,False],
    [False,True,False,False]
    ]
]

I_Block = [
    [
    [False,True,False,False],
    [False,True,False,False],
    [False,True,False,False],
    [False,True,False,False]
    ],
    [
    [False,False,False,False],
    [False,False,False,False],
    [True,True,True,True],
    [False,False,False,False]
    ],
    [
    [False,True,False,False],
    [False,True,False,False],
    [False,True,False,False],
    [False,True,False,False]
    ],
    [
    [False,False,False,False],
    [False,False,False,False],
    [True,True,True,True],
    [False,False,False,False]
    ]
]

BLOCKS = [L_Block, Z_Block, CUBE_Block, T_Block, I_Block]
FULL = [True, True, True, True, True, True, True, True, True, True]
EMPTY = [True, False, False, False, False, False, False, False, False, True]

# END definice konstant

# BEGIN VEX soucastky

brain=Brain()
controller = Controller()

brain_inertial = Inertial()
left_drive_smart = Motor(Ports.PORT1, 1, False)
right_drive_smart = Motor(Ports.PORT6, 1, True)

drivetrain = SmartDrive(left_drive_smart, right_drive_smart, brain_inertial, 200)
touchled_2 = Touchled(Ports.PORT2)
optical_3 = Optical(Ports.PORT3)
distance_7 = Distance(Ports.PORT7)
bumper_8 = Bumper(Ports.PORT8)

# END VEX soucastky



# zajisteni nahodnosti (podle casu)

random.seed(time.time())

# BEGIN definice globalnich promennych

herni_pole = []
i = 0
x = 0
block = 0
rot = 0
score = 0
sleeptorig = 1
sleept = sleeptorig
end = False

# END definice globalnich promennych

# BEGIN nastaveni herniho pole

for i in range(19):
    radek = [True]
    for j in range(8):
        radek.append(False)
    radek.append(True)
    herni_pole.append(radek)

radek = []
for k in range(10):
    radek.append(True)
herni_pole.append(radek)

# END nastaveni herniho pole

velikost_bloku = 8
def vykreslipole():
    """Vykresli staticke bloky (jiz spadle)"""
    global end
    if end: return
    for x in range(20):
        for y in range(10):
            if herni_pole[x][y]:
                brain.screen.draw_rectangle(x*velikost_bloku,
                                            (10-y)*velikost_bloku,
                                            velikost_bloku,
                                            velikost_bloku
                )

def enum(arr):
    """Nahrada za funkci `enumerate()` pro micropython

    Vrati arr (napr. `["a", "b", "c"]`) ve formatu `[(0, "a"), (1, "b"), (2, "c)]`"""
    global end
    if end: return
    enumi = 0
    for item in arr:
        yield (enumi, item)
        enumi += 1

def kolize(blocki, bx, by):
    """Zjisti kolizi blocku `blocki` na souradnicich `bx, by`"""
    global end
    if end: return
    for y, radek in enum(blocki):
        for x, bunka in enum(radek):
            try:
                if herni_pole[by+y][bx+x] and bunka:
                    return True
            except:
                ...
                # TODO
            
    return False

def vykresliblock(x_pos, y_pos, rotace):
    """Vykresli aktualni blok na souradnicich `x_pos, y_pos` s rotaci `rotace`"""
    global end
    if end: return
    global i
    global block
    global score
    blok = BLOCKS[block]
    if blok == None:
        return
    blok = blok[rotace]
    if kolize(blok, x_pos, y_pos+1):
        brain.play_sound(SoundType.FILLUP)
        for y, radek in enum(blok):
            for x, bunka in enum(radek):
                try:
                    herni_pole[y+y_pos][x+x_pos] = herni_pole[y+y_pos][x+x_pos] or bunka
                except:
                    ...
        
        genblock()

        for idx, radek in enum(herni_pole):
            if idx == 19: continue
            if radek == FULL:
                for g in range(idx-2):
                    herni_pole[idx-g] = herni_pole[idx-g-1]
                herni_pole[0] = EMPTY
                score += 1
                print(str(score))
                break

    for x in range(4):
        for y in range(4):
            if blok[y][x]:
                brain.screen.draw_rectangle(
                                            (y+y_pos)*velikost_bloku,
                                            (10-(x+x_pos))*velikost_bloku,
                                            velikost_bloku,
                                            velikost_bloku
                                            )



def genblock():
    """Vygeneruj nahodny blok, pri 100 neuspesnych pokusech ukonci hru"""
    global end
    if end: return
    def generate():
        """Generace nahodneho bloku"""
        global x, i, rot, block
        i = 0
        x = random.randint(0, 6)
        rot = random.randint(0, 3)
        block = random.randint(0, len(BLOCKS)-1)

    global x, i, rot, block, maint, end

    generate()
    counter = 0
    while kolize(BLOCKS[block][rot], x, i): 
        counter += 1
        if counter >= 100:
            end = True
            brain.play_sound(SoundType.TADA)
            brain.screen.clear_screen()
            brain.screen.print("Game over!")
            brain.screen.render()
            maint.stop()
            return
        generate()

def vykresli():
    """Proved vykresleni"""
    global end
    if end: return
    vykreslipole()
    vykresliblock(x,i,rot)
    brain.screen.render()
    brain.screen.clear_screen()

# BEGIN events

def buttonR():
    global x
    if not kolize(BLOCKS[block][rot], x+1, i):
        x += 1
        vykresli()

def buttonL():
    global x
    if not kolize(BLOCKS[block][rot], x-1, i):
        x -= 1
        vykresli()

def buttonRot():
    global rot
    newrot = (rot+1)%4
    if not kolize(BLOCKS[block][newrot], x, i):
        rot = newrot

def buttonSpeed():
    global sleept
    sleept = 1

def buttonSlow():
    global sleept
    sleept = sleeptorig

controller.buttonRUp.pressed(buttonR)
controller.buttonLUp.pressed(buttonL)
controller.buttonLDown.pressed(buttonRot)
controller.buttonRDown.pressed(buttonSpeed)
controller.buttonRDown.released(buttonSlow)

# END events

def playseq(sq: str) -> None:
    for i, char in enum(sq):
        lg = DELKA
        if i % 4 == 3:
            lg *= 1.5
        brain.play_note(5,int(char),int(lg))
    sleep(PAUZA)

def zvuk():
    "Zvuk"
    while True:
        playseq("5430")

        playseq("35403453")

        playseq("534004535430")

        playseq("3540345353400453")

genblock()

def mainloop():
    global i
    while True:
        sleep(sleept)
        i += 1
        vykresli()

zvukt = Thread(zvuk)
maint = Thread(mainloop)