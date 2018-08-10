# Fire-Emblem-Arena-Probabilities

The exact probability of winning a Fire Emblem arena battle can be computed efficiently using dynamic programming. This project implements the DP algorithm in a simple GUI (created using Tkinter). Several versions of the app are available:

1. arena.py

This is the project source code. At 22 kB, this script is significantly smaller than the standalone executables. It can be run as is, works with Python 2.7 or 3+, and should work on all major platforms (tested so far on Linux, Windows 7, and Windows 10). Running this file requires you to have Python. The alternative is to use one of the executable files.

2. arena

This is the standalone Linux executable, created from arena.py using PyInstaller.

3. arena.exe

This is the standalone Windows executable, created from arena.py using PyInstaller on a Windows 7 system. Before creating this executable, I increased the default window size in arena.py slightly (from 600x340 to 600x350); originally, a few pixels from the bottom of the GUI were cut off when run on Windows. Also, it seems to take a few seconds after execution to display the GUI. I don't know why this happens or if there's a good way around it.


Some noteworthy points about the app and algorithm are as follows:

1. The math behind the algorithm assumes a truly random and independent RNG, whereas it is only pseudo-random in reality. Practically speaking, this distinction is unimportant (barring RNG manipulation).

2. Due to a presumed programming error, it is apparently possible for an attack with 100 hit to miss in FE6 (Binding Blade). The probability of this happening is reportedly about 1 in 3,000,000. I don't know the exact numbers involved here, so for now, I've just programmed the app to treat FE6 the same as the other 2RN true hit games.

3. Research suggests that the true hit in Fates is a hybrid of the 1RN and 2RN true hits: hit rates below 50 are accurate, while hit rates 50 and higher use an unevenly weighted 2RN average.

4. This app is rather rudimentary in that it does not take into account Fates dual strikes, offensive/defensive skills, or special weapons (e.g. brave weapons, Nosferatu). Some of these features may be implemented someday. However, the math behind the algorithm was already very messy, and it becomes exponentially worse as more sources of uncertainty are thrown into the mix. In particular, the possibility of a combatant healing him/herself (through Nosferatu, Sol, or Aether) seems like it would be very troublesome. Correctly accounting for some skills may also require more information than is displayed on screen - for example, the overall effect of Luna depends on the target's defense/resistance.

5. HP and Dmg are required fields for both the player and enemy. Blank Hit and Crit fields will result in a warning, but the app will fill these blank fields in with their default values (100 for hit, 0 for crit) and successfully run.
