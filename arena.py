#!/usr/bin/python3

"""
arena.py

Tkinter app which computes the probability of victory in Fire Emblem arena battles.

Author: Andrew Brockmann
Completion Date: August 8, 2018
Last Modified: August 8, 2018
"""

from fractions import Fraction
from math import ceil
try:
    from tkinter import *
    from tkinter import messagebox
except ImportError:
    # Modules need to be imported a little differently if running on Python 2
    from Tkinter import *
    import tkMessageBox as messagebox


###############################################################################
############################### True Hit Data #################################
###############################################################################

# True hit table for FE 1-5 (1RN, displayed hit is accurate)
# Given displayed hit x, hit probability is _1RN[x]/100
_1RN_games = ["Fire Emblem 1", "Gaiden", "Mystery of the Emblem", "Genealogy of the Holy War", "Thracia 776"]
_1RN = range(101)

# True hit table for FE 6-13 (2RN)
# Given displayed hit x, hit probability is _2RN[x]/10000
_2RN_games = ["Binding Blade", "Blazing Sword", "Sacred Stones", "Path of Radiance", "Radiant Dawn", \
              "Shadow Dragon", "New Mystery of the Emblem", "Awakening"]
_2RN = [0, 3, 10, 21, 36, 55, 78, 105, 136, 171, 210, 253, 300, 351, 406, 465, 528, 595, 666, 741, 820, 903, 990, 1081, 1176, 1275, 1378, 1485, 1596, 1711, 1830, 1953, 2080, 2211, 2346, 2485, 2628, 2775, 2926, 3081, 3240, 3403, 3570, 3741, 3916, 4095, 4278, 4465, 4656, 4851, 5050, 5247, 5440, 5629, 5814, 5995, 6172, 6345, 6514, 6679, 6840, 6997, 7150, 7299, 7444, 7585, 7722, 7855, 7984, 8109, 8230, 8347, 8460, 8569, 8674, 8775, 8872, 8965, 9054, 9139, 9220, 9297, 9370, 9439, 9504, 9565, 9622, 9675, 9724, 9769, 9810, 9847, 9880, 9909, 9934, 9955, 9972, 9985, 9994, 9999, 10000]

# True hit table for FE Fates (1RN / weighted 2RN hybrid)
# Hit rates below 50 seem to be accurate, while 50 and above seem to use a weighted 2RN formula
# Given displayed hit x, hit probability is Fates[x]/10000
Fates = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000, 3100, 3200, 3300, 3400, 3500, 3600, 3700, 3800, 3900, 4000, 4100, 4200, 4300, 4400, 4500, 4600, 4700, 4800, 4900, 5050, 5183, 5317, 5450, 5583, 5717, 5850, 5983, 6117, 6250, 6383, 6517, 6650, 6783, 6917, 7050, 7183, 7317, 7450, 7583, 7717, 7850, 7983, 8117, 8250, 8383, 8512, 8635, 8753, 8866, 8973, 9075, 9172, 9263, 9349, 9430, 9505, 9575, 9640, 9699, 9753, 9802, 9845, 9883, 9916, 9943, 9965, 9982, 9993, 9999, 10000]


###############################################################################
############################### Tooltip Class #################################
###############################################################################

# Copied with negligible changes from:
# https://stackoverflow.com/questions/3221956/how-do-i-display-tooltips-in-tkinter

# Comments from the original file:
""" tk_ToolTip_class101.py
gives a Tkinter widget a tooltip as the mouse is above the widget
tested with Python27 and Python34  by  vegaseat  09sep2014
www.daniweb.com/programming/software-development/code/484591/a-tooltip-class-for-tkinter

Modified to include a delay time by Victor Zaccardo, 25mar16
"""

class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 180   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(self.tw, text=self.text, justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()


###############################################################################
####################### Functions called by the GUI ###########################
###############################################################################

def clearAll():
    """ Function called by the "Clear All" button. """
    pHit.delete(0, END)
    pDmg.delete(0, END)
    pCrit.delete(0, END)
    pHP.delete(0, END)
    eHit.delete(0, END)
    eDmg.delete(0, END)
    eCrit.delete(0, END)
    eHP.delete(0, END)
    numEntry.delete(0, END)
    denEntry.delete(0, END)
    perEntry.delete(0, END)

def isInt(entry):
    """ Given string input, checks whether it represents an integer value. """
    try:
        x = int(entry)
        if str(x) == entry:
            return True
        else:
            return False
    except ValueError:
        return False

def inputCheck():
    """ Checks input values for problems, fills in default values as necessary, and creates error
        messages. Returns True if the program can run with the given input. """
    Hit = [pHit.get(), eHit.get()]
    Dmg = [pDmg.get(), eDmg.get()]
    Crit = [pCrit.get(), eCrit.get()]
    HP = [pHP.get(), eHP.get()]

    # Error for game not selected
    if RNG.get() == "Choose game":
        messagebox.showerror("Selection error", "Select game from the dropdown menu.")
        return False

    # Errors for missing mandatory values
    missing = []
    if Dmg[0] == "": missing += ["Player Dmg"]
    if Dmg[1] == "": missing += ["Enemy Dmg"]
    if HP[0] == "": missing += ["Player HP"]
    if HP[1] == "": missing += ["Enemy HP"]
    if len(missing) > 0:
        errorMessage = "Mandatory field(s) missing:"
        for field in missing:
            errorMessage += "\n-" + field
        messagebox.showerror("Input error", errorMessage)
        return False

    # Errors for non-integer input values
    notInt = []
    if not isInt(Hit[0]) and Hit[0] != "": notInt += ["Player Hit"]
    if not isInt(Hit[1]) and Hit[1] != "": notInt += ["Enemy Hit"]
    if not isInt(Dmg[0]): notInt += ["Player Dmg"]
    if not isInt(Dmg[1]): notInt += ["Enemy Dmg"]
    if not isInt(Crit[0]) and Crit[0] != "": notInt += ["Player Crit"]
    if not isInt(Crit[1]) and Crit[1] != "": notInt += ["Enemy Crit"]
    if not isInt(HP[0]): notInt += ["Player HP"]
    if not isInt(HP[1]): notInt += ["Enemy HP"]
    if len(notInt) > 0:
        errorMessage = "All input fields must have whole number numeric values. The following fields do not:"
        for field in notInt:
            errorMessage += "\n-" + field
        messagebox.showerror("Input error", errorMessage)
        return False

    # Warnings for missing Hit/Crit values
    if Hit[0] == "":
        missing += ["Player Hit"]
        pHit.insert(0, "100")
        Hit[0] = "100"
    if Hit[1] == "":
        missing += ["Enemy Hit"]
        eHit.insert(0, "100")
        Hit[1] = "100"
    if Crit[0] == "":
        missing += ["Player Crit"]
        pCrit.insert(0, "0")
        Crit[0] = "0"
    if Crit[1] == "":
        missing += ["Enemy Crit"]
        eCrit.insert(0, "0")
        Crit[1] = "0"
    if len(missing) > 0:
        warning = "Optional fields are missing and have been filled in with their default values:"
        for field in missing:
            warning += "\n-" + field
        messagebox.showwarning("Warning", warning)

    Hit = [int(Hit[0]), int(Hit[1])]
    Dmg = [int(Dmg[0]), int(Dmg[1])]
    Crit = [int(Crit[0]), int(Crit[1])]
    HP = [int(HP[0]), int(HP[1])]

    # Hit/Crit out of range errors:
    invalid = []
    if Hit[0] < 0 or Hit[0] > 100: invalid += ["Player Hit"]
    if Hit[1] < 0 or Hit[1] > 100: invalid += ["Enemy Hit"]
    if Crit[0] < 0 or Crit[0] > 100: invalid += ["Player Crit"]
    if Crit[1] < 0 or Crit[1] > 100: invalid += ["Enemy Crit"]
    if len(invalid) > 0:
        errorMessage = "Hit and Crit must be values between 0 and 100 (inclusive)."
        errorMessage += " The following values are out of range:"
        for field in invalid:
            errorMessage += "\n-" + field
        messagebox.showerror("Input error", errorMessage)
        return False

    # Dmg/HP out of range errors:
    if Dmg[0] < 0: invalid += ["Player Dmg"]
    if Dmg[1] < 0: invalid += ["Enemy Dmg"]
    if HP[0] < 0: invalid += ["Player HP"]
    if HP[1] < 0: invalid += ["Enemy HP"]
    if len(invalid) > 0:
        errorMessage = "Dmg and HP values must not be negative. The following values are out of range:"
        for field in invalid:
            errorMessage += "\n-" + field
        messagebox.showerror("Input error", errorMessage)
        return False

    # Endless battle error
    if (Hit[0] == 0 or Dmg[0] == 0) and (Hit[1] == 0 or Dmg[1] == 0):
        messagebox.showerror("Error", "This battle will never end.")
        return False

    return True

# This method will be used to access elements from the DP table without worrying about negative indices.
# Based on my research and timing tests, passing a large list to a Python method repeatedly won't slow
# things down - the method won't recreate the list from scratch with each call.
def A(DP, x, y):
    return DP[max(x, 0)][max(y, 0)]

# The following function is a hack introduced to deal with the case where the player attacks twice per turn
def B(x, y):
    if x <= 0 and y > 0:
        return 0
    else:
        return 1

# Function that determines the victory probability when player and enemy each attack once per round.
# All inputs except m and n should be passed as Fraction objects:
#  m: Number of (non-crit) hits needed to defeat the player
#  n: Number of hits needed to defeat the enemy
#  p1: Player true hit rate
#  p2: Enemy true hit
#  c1: Player critical hit rate
#  c2: Enemy crit rate
def DP_1_1(m, n, p1, p2, c1, c2):
    DP = [x[:] for x in [[Fraction(0)] * (n+1)] * (m+1)]
    # The values DP[0][j] for j > 0 are already initialized to 0
    for i in range(m+1):
        DP[i][0] = Fraction(1)
    # Initialization of DP table is now complete

    # Compute other values with the recurrence relation
    for i in range(1, m+1):
        for j in range(1, n+1):
            r = Fraction(0)
            r += p1 * (1 - p2) * ( c1 * A(DP, i, j-3) + (1 - c1) * A(DP, i, j-1) )
            r += (1 - p1) * p2 * ( c2 * A(DP, i-3, j) + (1 - c2) * A(DP, i-1, j) )
            r += p1 * p2 * ( c1 * c2 * A(DP, i-3, j-3) + c1 * (1 - c2) * A(DP, i-1, j-3) \
                           + (1 - c1) * c2 * A(DP, i-3, j-1) + (1 - c1) * (1 - c2) * A(DP, i-1, j-1) )
            DP[i][j] = r / (p1 + p2 - p1 * p2)

    return DP[m][n]

# Function that determines the victory probability when enemy attacks twice per round
def DP_1_2(m, n, p1, p2, c1, c2):
    DP = [x[:] for x in [[Fraction(0)] * (n+1)] * (m+1)]
    # The values DP[0][j] for j > 0 are already initialized to 0
    for i in range(m+1):
        DP[i][0] = Fraction(1)
    # Initialization of DP table is now complete

    # Compute other values with the recurrence relation
    for i in range(1, m+1):
        for j in range(1, n+1):
            r = Fraction(0)
            r += p1 * (1 - p2) ** 2 * ( c1 * A(DP, i, j-3) + (1 - c1) * A(DP, i, j-1) )
            r += 2 * (1 - p1) * p2 * (1 - p2) * ( c2 * A(DP, i-3, j) + (1 - c2) * A(DP, i-1, j) )
            r += 2 * p1 * p2 * (1 - p2) * ( c1 * c2 * A(DP, i-3, j-3) + c1 * (1 - c2) * A(DP, i-1, j-3) \
                                          + (1 - c1) * c2 * A(DP, i-3, j-1) \
                                          + (1 - c1) * (1 - c2) * A(DP, i-1, j-1) )
            r += (1 - p1) * p2 ** 2 * ( c2 ** 2 * A(DP, i-6, j) + 2 * c2 * (1 - c2) * A(DP, i-4, j) \
                                      + (1 - c2) ** 2 * A(DP, i-2, j) )
            r += p1 * p2 ** 2 * ( c1 * c2 ** 2 * A(DP, i-6, j-3) + (1 - c1) * c2 ** 2 * A(DP, i-6, j-1) \
                                + 2 * c1 * c2 * (1 - c2) * A(DP, i-4, j-3) \
                                + 2 * (1 - c1) * c2 * (1 - c2) * A(DP, i-4, j-1) \
                                + c1 * (1 - c2) ** 2 * A(DP, i-2, j-3) \
                                + (1 - c1) * (1 - c2) ** 2 * A(DP, i-2, j-1) )
            DP[i][j] = r / (p1 + 2 * p2 - 2 * p1 * p2 - p2 ** 2 + p1 * p2 ** 2)

    return DP[m][n]

# Function that determines the victory probability when player attacks twice per round
def DP_2_1(m, n, p1, p2, c1, c2):
    DP = [x[:] for x in [[Fraction(0)] * (n+1)] * (m+1)]
    # The values DP[0][j] for j > 0 are already initialized to 0
    for i in range(m+1):
        DP[i][0] = Fraction(1)
    # Initialization of DP table is now complete

    # Compute other values with the recurrence relation
    for i in range(1, m+1):
        for j in range(1, n+1):
            r = Fraction(0)
            r += 2 * p1 * (1 - p1) * (1 - p2) * ( c1 * A(DP, i, j-3) + (1 - c1) * A(DP, i, j-1) )
            r += p1 ** 2 * (1 - p2) * ( c1 ** 2 * A(DP, i, j-6) + 2 * c1 * (1 - c1) * A(DP, i, j-4) \
                                      + (1 - c1) ** 2 * A(DP, i, j-2) )
            r += (1 - p1) ** 2 * p2 * ( c2 * A(DP, i-3, j) + (1 - c2) * A(DP, i-1, j) )
            r += p1 * (1 - p1) * p2 * ( c1 * c2 * A(DP, i-3, j-3) + c1 * (1 - c2) * A(DP, i-1, j-3) \
                                      + (1 - c1) * c2 * A(DP, i-3, j-1)
                                      + (1 - c1) * (1 - c2) * A(DP, i-1, j-1) )
            r += (1 - p1) * p1 * p2 * ( c1 * c2 * B(i-3, j) * A(DP, i-3, j-3) \
                                      + c1 * (1 - c2) * B(i-1, j) * A(DP, i-1, j-3) \
                                      + (1 - c1) * c2 * B(i-3, j) * A(DP, i-3, j-1) \
                                      + (1 - c1) * (1 - c2) * B(i-1, j) * A(DP, i-1, j-1) )
            r += p1 ** 2 * p2 * c1 * ( (1 - c2) * (1 - c1) * B(i-1, j-3) * A(DP, i-1, j-4) \
                                     + (1 - c2) * c1 * B(i-1, j-3) * A(DP, i-1, j-6) \
                                     + c2 * (1 - c1) * B(i-3, j-3) * A(DP, i-3, j-4) \
                                     + c2 * c1 * B(i-3, j-3) * A(DP, i-3, j-6) )
            r += p1 ** 2 * p2 * (1 - c1) * ( (1 - c2) * (1 - c1) * B(i-1, j-1) * A(DP, i-1, j-2) \
                                           + (1 - c2) * c1 * B(i-1, j-1) * A(DP, i-1, j-4) \
                                           + c2 * (1 - c1) * B(i-3, j-1) * A(DP, i-3, j-2) \
                                           + c2 * c1 * B(i-3, j-1) * A(DP, i-3, j-4) )
            DP[i][j] = r / (p2 + 2 * p1 - 2 * p1 * p2 - p1 ** 2 + p1 ** 2 * p2)

    return DP[m][n]

def calculate():
    """ Top level function called by the "Calculate" button. """
    if inputCheck():
        # Clear the output fields
        numEntry.delete(0, END)
        denEntry.delete(0, END)
        perEntry.delete(0, END)

        # Read input values
        hit1, hit2 = int(pHit.get()), int(eHit.get())
        dmg1, dmg2 = int(pDmg.get()), int(eDmg.get())
        crit1, crit2 = int(pCrit.get()), int(eCrit.get())
        hp1, hp2 = int(pHP.get()), int(eHP.get())

        # If the player can't hit/damage the enemy, then the enemy will win
        if hit1 == 0 or dmg1 == 0:
            numEntry.insert(0, 0)
            denEntry.insert(0, 1)
            perEntry.insert(0, 0)
            return
        # ...and likewise if the enemy can't hit/damage
        if hit2 == 0 or dmg2 == 0:
            numEntry.insert(0, 1)
            denEntry.insert(0, 1)
            perEntry.insert(0, 100)
            return

        # Having checked the cases above, we won't encounter any division by 0 errors
        m, n = int(ceil(float(hp1)/dmg2)), int(ceil(float(hp2)/dmg1))

        # Construct the other inputs to the dynamic program as fractions
        c1, c2 = Fraction(crit1, 100), Fraction(crit2, 100)
        # True hit tables needed for the hit rates
        game = RNG.get()
        if game in _1RN_games:
            p1, p2 = Fraction(_1RN[hit1], 100), Fraction(_1RN[hit2], 100)
        elif game in _2RN_games:
            p1, p2 = Fraction(_2RN[hit1], 10000), Fraction(_2RN[hit2], 10000)
        else:
            p1, p2 = Fraction(Fates[hit1], 10000), Fraction(Fates[hit2], 10000)

        # Call the appropriate dynamic program depending on which combatant, if either, can follow-up
        if followup.get() == "Neither":
            victory = DP_1_1(m, n, p1, p2, c1, c2)
            numEntry.insert(0, victory.numerator)
            denEntry.insert(0, victory.denominator)
            perEntry.insert(0, float(100 * victory))

        elif followup.get() == "Player":
            victory = DP_2_1(m, n, p1, p2, c1, c2)
            numEntry.insert(0, victory.numerator)
            denEntry.insert(0, victory.denominator)
            perEntry.insert(0, float(100 * victory))

        else:
            victory = DP_1_2(m, n, p1, p2, c1, c2)
            numEntry.insert(0, victory.numerator)
            denEntry.insert(0, victory.denominator)
            perEntry.insert(0, float(100 * victory))


###############################################################################
################################ GUI creation #################################
###############################################################################

window = Tk()
window.title("Fire Emblem Arena Probability Calculator")
window.geometry('600x340')


# Player and Enemy stat labels
pLbl = Label(window, text="Player", font=("Arial Bold", 14), fg="blue")
pLbl.grid(column=1, row=0, pady=10)

eLbl = Label(window, text="Enemy", font=("Arial Bold", 14), fg="red")
eLbl.grid(column=2, row=0)

HitLbl = Label(window, text="Hit", font=("Arial Bold", 14))
HitLbl.grid(column=0, row=1)
Hit_ttp = CreateToolTip(HitLbl, "Displayed Player/Enemy hit rate")

DmgLbl = Label(window, text="Dmg", font=("Arial Bold", 14))
DmgLbl.grid(column=0, row=2)
Dmg_ttp = CreateToolTip(DmgLbl, "Damage dealt by Player/Enemy with each strike")

CritLbl = Label(window, text="Crit", font=("Arial Bold", 14))
CritLbl.grid(column=0, row=3)
Crit_ttp = CreateToolTip(CritLbl, "Player/Enemy critical hit rate")

HPLbl = Label(window, text="HP", font=("Arial Bold", 14))
HPLbl.grid(column=0, row=4)
HP_ttp = CreateToolTip(HPLbl, "Player/Enemy HP at the start of the battle")


# Player and enemy stat entries
pHit = Entry(window, width=10)
pHit.grid(column=1, row=1, padx=10)

pDmg = Entry(window, width=10)
pDmg.grid(column=1, row=2)

pCrit = Entry(window, width=10)
pCrit.grid(column=1, row=3)

pHP = Entry(window, width=10)
pHP.grid(column=1, row=4)

eHit = Entry(window, width=10)
eHit.grid(column=2, row=1, padx=9)

eDmg = Entry(window, width=10)
eDmg.grid(column=2, row=2)

eCrit = Entry(window, width=10)
eCrit.grid(column=2, row=3)

eHP = Entry(window, width=10)
eHP.grid(column=2, row=4)


# Game selection menu
gameLbl = Label(window, text="Game", font=("Arial Bold", 14))
gameLbl.grid(column=3, row=0)
game_ttp = CreateToolTip(gameLbl, 'Displayed hit rates are only accurate in some Fire Emblem games - '
                                  'search "Fire Emblem true hit" for more information')

RNG = StringVar()
RNG.set("Choose game")
gameList = _1RN_games + _2RN_games + ["Fates"]
gameMenu = OptionMenu(window, RNG, *gameList)
gameMenu.config(width=22)
gameMenu.grid(column=3, row=1, padx=50)


# Follow-up attack radio button
followupLbl = Label(window, text="Follow-Up Attacks", font=("Arial Bold", 14))
followupLbl.grid(column=3, row=3)
followup_ttp = CreateToolTip(followupLbl, 'Select "Player" (or "Enemy") if the player (respectively, enemy) '
                                          'is fast enough to attack twice per round')

followup = StringVar()
followup.set("Neither")

nFollowup = Radiobutton(window, text="Neither", value="Neither", variable=followup)
nFollowup.grid(column=3, row=4, sticky="w", padx=75)

pFollowup = Radiobutton(window, text="Player", value="Player", variable=followup)
pFollowup.grid(column=3, row=5, sticky="w", padx=75)

eFollowup = Radiobutton(window, text="Enemy", value="Enemy", variable=followup)
eFollowup.grid(column=3, row=6, sticky="w", padx=75)


# Buttons
clear = Button(window, text="Clear All", width=10, command=clearAll)
clear.grid(column=1, row=6, columnspan=2)

calc = Button(window, text="Calculate", width=10, command=calculate)
calc.grid(column=1, row=7, columnspan=2, pady=15)


# Output labels
numLbl = Label(window, text="numerator", font=("Arial Bold", 12))
numLbl.grid(column=0, row=8, sticky="e")
num_ttp = CreateToolTip(numLbl, "Player victory probability is numerator/denominator")

denLbl = Label(window, text="denominator", font=("Arial Bold", 12))
denLbl.grid(column=0, row=9, sticky="e")
den_ttp = CreateToolTip(denLbl, "Player victory probability is numerator/denominator")

perLbl = Label(window, text="%", font=("Arial Bold", 12))
perLbl.grid(column=0, row=10, sticky="e")


# Output entries
numEntry = Entry(window, width=23)
numEntry.grid(column=1, row=8, columnspan=2)

denEntry = Entry(window, width=23)
denEntry.grid(column=1, row=9, columnspan=2)

perEntry = Entry(window, width=23)
perEntry.grid(column=1, row=10, columnspan=2)

window.mainloop()
