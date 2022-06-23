The Programming Task and its Specifications
-------------------------------------------
---------------- Overview -----------------
The program builds a user interface for playing a simplified RPG (role-playing game).
A list of items namely, weapons, armor, and potions must be provided in Items.txt.

----------------- FORMAT ------------------
Each item must only occupy one line. Each part of an item must be separated by a comma and a space.
For weapons the format is 'W' to indicate the type, a name to distinguish the weapon, damage as 
an integer for battle caluclations, and a weight as an integer for inventory caluclations. Armor is 
formatted the same as weapons; only the first entry is 'A' for armor the third entry represents defense 
instead of damage.Potions are formatted the same as weapons only; the first entry is 'P' for potions, 
and the third entry represents the amount of health healed instead of damage.

--------------- Description ---------------
The program simulates a battle with three enemies with gear randomly generated from Items.txt, 
allowing the player to name their character and choose a starting item. Turn order is determined 
based on randomly generated agility stats. On the player's turn, they are able to attack, use a 
healing potion, run from the enemy (excluding the final enemy) at the cost of their ENTIRE inventory, 
check their stats, or check their inventory. Turn order alternates, and the enemy will always attack. 
Should the player defeat an enemy, they are allowed to loot one piece of equipment it held or a health 
potion if it possessed one. Upon defeating all enemies and running as necessary, the player wins. 
Otherwise, the player dies, and the game is over. All interactions with the player through the console 
are logged and sent to the output file battle-log.txt for a full recount of the game.

---------------- Examples -----------------
Weapon Example: W, sword, 10, 3
Armor Example: A, shield, 20, 5
Potion Example: P, health potion, 50, 1

------------------ Note -------------------
*Note: At this time only health potions are supported (so do not enter more than one potion).

The Program Design
----------------------
------- Classes ------
The character class holds stats and methods shared by both the player and the enemies 
(name, health, attack, defense, and agility - all randomly generated excluding the name).
It allows players and enemies to take and recieve damage updating the appropriate object.

The player class inherits base stats from character and sets max health, weight limit,
current weight, and creates an empty inventory. It allows the player to see their stats and
inventory, add and replace items, use health potions and run.

Ther Enemy class inherits base stats from character and sets their weapon and armor if provided, 
updating their attack and defense accordingly. It also has a method to describe the enemy and its gear.

---- Supplementary Functions ----
readItems() grabs items from the Items.txt file for interpretation.

randomizeEnemyOrder() takes an array of enemies and creates a new array of randomly rearranged enemies.

battle() runs the main loop aginst the enemies, governs turn order, and allows the player to take actions
allowing the player to play the bulk of the game.

log() takes a string and sends it to the output file battle-log.txt.

-------- Main --------
main() is resobsible for user interface (including nested methods) and input/output and enemy generation. 

How to Run the Program
-----------------------
The input file Items.txt must be present in the format described above.
Import the program, the main function will get called.
>>> import RPG
Then follow the interactive prompts. The output will be written to the battle-log.txt file.