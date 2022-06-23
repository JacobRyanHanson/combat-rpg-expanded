""" 
    This program provides a user-interface to play a simplified RPG.
    The types of items and their stats are read from a file.
    The user interactively chooses their equipment and determines how best to use their items.
    The program governs turn order, enemies, and their actions, 
    creating a complete log in the designated output file.
"""

from random import randrange

#------------------------------ Classes ------------------------------

class Character:
    """ 
        Super class designed to provide general stats 
        (name, health, attack, defence, and agility) and 
        methods for taking and receiving damage to its subclasses. 
    """
    def __init__(self, name):
        """ 
            Creates a character model with a given name and health, 
            attack, defense, and agility generated randomly within a 
            range (80-120 for health and 5-12 for the others). 
        """
        self.name = name
        self.health = randrange(80, 121)
        self.attack = randrange(5, 13)
        self.defense = randrange(5, 13)
        self.agility = randrange(5, 13)

    def damageGen(self):
        """ 
            Generates a raw damage value based on the player's or enemy's 
            attack stat (depending on the object its called on) and a random 
            modifier between 1/2 and 2. It returns the raw damage. 
        """
        return int(self.attack * (randrange(5,21) / 10))

    def takeDamage(self, value):
        """" 
            Generates the amount of damage taken by accounting for the 
            player's or enemy's defense stat (depending on the object it's called on) 
            and a random modifier between 1/2 and 2. It returns the change in health
            and the amound blocked (modifier and dfense respectively).
        """
        defense = int(self.defense // 2 * (randrange(5,21) / 10))
        modifier = value - defense
        # If the modifier is not negative, update the object's health.
        if modifier > 0: 
            self.health -= modifier
            if self.health < 0:
                self.health = 0
            return [modifier, defense]
        # Else leave the health unchanged and return the amount blocked.
        else:
            return [0, defense]

class Player(Character):
    """ 
        Inherits randomly generated states from character and adds max health, 
        weight limit, weight, and inventory as additional player-specific fields. 
        It contains methods to return the player's stats and inventory, add and 
        replace items, use health potions and run.
    """
    def __init__(self, name):
        """ 
            Creates a player object grabbing base stats from character and sets 
            the max health based on the character's original generated health. It sets 
            the weight limit to 10 though this is arbitrary and could be changed. It 
            sets the current weight to 0, and the inventory to empty as upon creation, 
            the player has no gear.
        """
        super().__init__(name)
        self.MAX_HEALTH = self.health
        # Arbitrary: can be adjusted for game balance.
        self.WEIGHT_LIMIT = 10
        self.weight = 0
        self.inventory = [[], [], []]
    
    def getStats(self):
        """ 
            Prints the player's stats to the console and logs them to the output file. 
        """
        print(self.name + "'s stats:\n")
        log(self.name + "'s stats:\n")
        print("Health: " + str(self.health) + "/" + str(self.MAX_HEALTH))
        log("Health: " + str(self.health) + "/" + str(self.MAX_HEALTH))
        print("Attack: " + str(self.attack))
        log("Attack: " + str(self.attack))
        print("Defense: " + str(self.defense))
        log("Defense: " + str(self.defense))
        print("Agility: " + str(self.agility))
        log("Agility: " + str(self.agility))
        print("Weight: " + str(self.weight) + "/" + str(self.WEIGHT_LIMIT))
        log("Weight: " + str(self.weight) + "/" + str(self.WEIGHT_LIMIT))
        print("----------------------------------------------------------------------")
        log("----------------------------------------------------------------------")
    
    def getInventory(self):
        """ 
            Prints the player's inventory to the console and logs it to the output file.
        """
        print(self.name + "'s inventory:\n")
        log(self.name + "'s inventory:\n")
        # If the player has a weapon (looking in the weapon category portion of inventory), 
        # grab the weapon and display its name, damage, and weight, respectively. 
        if len(self.inventory[0]) == 1:
            weaponIndex = self.inventory[0][0]
            print("Weapon - " + weaponIndex[1].capitalize() + ", Damage: " + weaponIndex[2] + ", Weight: " + weaponIndex[3].strip())
            log("Weapon - " + weaponIndex[1].capitalize() + ", Damage: " + weaponIndex[2] + ", Weight: " + weaponIndex[3].strip())
        else:
            print("Weapon - None")
            log("Weapon - None")
        # Same logic as above comment but for armor respectively. 
        if len(self.inventory[1]) == 1:
            armorIndex = self.inventory[1][0]
            print("Armor - " + armorIndex[1].capitalize() + ", Defense: " + armorIndex[2] + ", Weight: " + armorIndex[3].strip())
            log("Armor - " + armorIndex[1].capitalize() + ", Defense: " + armorIndex[2] + ", Weight: " + armorIndex[3].strip())
        else:
            print("Armor - None")
            log("Armor - None")
        # Same logic as above comment but for potions respectively.
        if len(self.inventory[2]) >= 1:
            potionIndex = self.inventory[2][0]
            print("Health potion(s) - Quantity: " +  str(len(self.inventory[2])) + ", Recovery: " + potionIndex[2] + ", Weight: " + potionIndex[3].strip())
            log("Health potion(s) - Quantity: " +  str(len(self.inventory[2])) + ", Recovery: " + potionIndex[2] + ", Weight: " + potionIndex[3].strip())
        else:
            print("Health potion(s) - None")
            log("Health potion(s) - None")
        print("----------------------------------------------------------------------")
        log("----------------------------------------------------------------------")
    
    def replaceItem(self, item):
        """ 
            Given an item, it adjusts weight and attack or defense, respectively, 
            depending on if the given item is a weapon or armor. The old weapon or 
            armor is removed, and the new item is added.
        """
        # If the new item is a weapon, remove attack and weight based on the current item and remove it from the inventory.
        if item[0] == 'W':
            self.attack -= int(self.inventory[0][0][2])
            self.weight -= int(self.inventory[0][0][3])
            self.inventory[0].pop(0)
        # Else the new item is armor. Remove defense and weight based on the current item and remove it from the inventory.
        else:
            self.defense -= int(self.inventory[1][0][2])
            self.weight -= int(self.inventory[1][0][3])
            self.inventory[1].pop(0)
        self.addItem(item, True) 
    
    def addItem(self, item, oldItem = False):
        """ 
            Given an item and a print status boolean (oldItem), it determines if an item 
            should be added based on the player's current item (if applicable) and the 
            weight of the new item. If successful, it modifies the attack, defense, and 
            inventory as necessary and notifies the user if successful or otherwise.
        """
        # If the item is a weapon...
        if item[0] == 'W':
            # If the player has no weapon and the new weapon does not exceed the weight limit, 
            # add it to the inventory and adjust attack and weight based on the new weapon. 
            if len(self.inventory[0]) < 1 and self.weight + int(item[3]) <= self.WEIGHT_LIMIT:
                # Boolean to avoid printing a replacement text and this aquired text when replaceItem() is called.
                if not(oldItem):
                    print("----------------------------------------------------------------------")
                    log("----------------------------------------------------------------------")
                    print(f"{self.name} aquired a(n) {item[1]}.")
                    log(f"{self.name} aquired a(n) {item[1]}.")

                self.inventory[0].append(item)
                self.attack += int(item[2])
                self.weight += int(item[3])
            # Otherwise, if the player has a weapon and the new weapon would not exceed the weight limit 
            # (accounting for the weight of the weapon that might be replaced), if the player chooses to 
            # do so, replaceItem() is called, and the player is notified of the change. 
            elif len(self.inventory[0]) > 0 and self.weight - int(self.inventory[0][0][3]) +  int(item[3]) <= self.WEIGHT_LIMIT:
                response = input(f"\nWould {self.name} like to replace their {self.inventory[0][0][1]}? (y/n): ")
                if response == 'y':
                    print("----------------------------------------------------------------------")
                    log("----------------------------------------------------------------------")
                    print(f"{self.name} replaced their {self.inventory[0][0][1]} with a(n) {item[1]}.")
                    log(f"{self.name} replaced their {self.inventory[0][0][1]} with a(n) {item[1]}.")
                    self.replaceItem(item)
                log(f"\nWould {self.name} like to replace their {self.inventory[0][0][1]}? (y/n): " + response) 
            # Else the player tried to add an item they had no way to carry and are notified.                  
            else:
                print(f"\n{self.name} is carrying too much to store a(n) {item[1]}.")
                log(f"\n{self.name} is carrying too much to store a(n) {item[1]}.")
        # Same nested logic as above begenning with "if item[0] == 'W':", only for armor respectively.
        elif item[0] == 'A':
            if len(self.inventory[1]) < 1 and self.weight + int(item[3]) <= self.WEIGHT_LIMIT:
                if not(oldItem):
                    print("----------------------------------------------------------------------")
                    log("----------------------------------------------------------------------")
                    print(f"{self.name} aquired a(n) {item[1]}.")
                    log(f"{self.name} aquired a(n) {item[1]}.")

                self.inventory[1].append(item)
                self.defense += int(item[2])
                self.weight += int(item[3])
            elif len(self.inventory[1]) > 0 and self.weight - int(self.inventory[1][0][3]) +  int(item[3]) <= self.WEIGHT_LIMIT:
                response = input(f"\nWould {self.name} like to replace their {self.inventory[1][0][1]}? (y/n): ")
                if response == 'y':
                    print("----------------------------------------------------------------------")
                    log("----------------------------------------------------------------------")
                    print(f"{self.name} replaced their {self.inventory[1][0][1]} with a(n) {item[1]}.")
                    log(f"{self.name} replaced their {self.inventory[1][0][1]} with a(n) {item[1]}.")
                    self.replaceItem(item)
                log(f"\nWould {self.name} like to replace their {self.inventory[1][0][1]}? (y/n): " + response)
            else:
                print(f"\n{self.name} is carrying too much to store a(n) {item[1]}.")
                log(f"\n{self.name} is carrying too much to store a(n) {item[1]}.")
        # Otherwise, if the item is a potion and adding it does not exceed the weight limit add the item
        # to the player's inventory.
        elif item[0] == 'P' and self.weight + int(item[3]) <= self.WEIGHT_LIMIT:
            print("----------------------------------------------------------------------")
            log("----------------------------------------------------------------------")
            print(f"{self.name} aquired a(n) {item[1]}.")
            log(f"{self.name} aquired a(n) {item[1]}.")
            self.inventory[2].append(item)
        # Otherwise, the player tried to add a potion when they could not carry anymore.
        else:
            print("----------------------------------------------------------------------")
            log("----------------------------------------------------------------------")
            print(f"{self.name} is carrying too much to store a(n) {item[1]}.")
            log(f"{self.name} is carrying too much to store a(n) {item[1]}.")
    
    def hasPotion(self):
        """
            Checks if the user has any potions and returns a boolean. 
        """
        return len(self.inventory[2]) > 0

    def useHealthPotion(self, potion):
        """
            If the player has a potion, it is consumed (removed from the inventory), 
            and health is restored up to the designated amount in Items.txt 
            (no health over MAX_HEALTH is allowed). Otherwise, the user is notified 
            they have no potions to use. 
        """
        if self.hasPotion():
            # Adds the player's current health with the value the potion heals for (grabbed from the array).
            newHealth = self.health + int(potion[2])
            # If newHealth does not exceed max health, the health is just updated.
            if newHealth <= self.MAX_HEALTH:
                self.health = newHealth
            # Else it is set to MAX_HEALTH to prevent the player from overhealing.
            else:
                self.health = self.MAX_HEALTH
            # Potion is removed.
            self.inventory[2].pop(0)
            print(self.name + " healed " + potion[2] + " points.")
            log(self.name + " healed " + potion[2] + " points.")
            print("----------------------------------------------------------------------")
            log("----------------------------------------------------------------------")
        else:
            print(self.name + " doesn't have any potions to use.")
            log(self.name + " doesn't have any potions to use.")
            print("----------------------------------------------------------------------")
            log("----------------------------------------------------------------------")

    def run(self, index, size):
        """
            If the player is not facing the last enemy, their attack and defense are 
            reduced based on the items dropped, the inventory is cleared, and their 
            weight is reset to 0 accordingly. 
        """
        # If the player is not facing the last enemy...
        if index != size - 1:
            if len(self.inventory[0]) > 0:
                self.attack -= int(self.inventory[0][0][2])
            
            if len(self.inventory[1]) > 0:
                self.defense -= int(self.inventory[1][0][2])
            
            self.inventory = [[], [], []]
            self.weight = 0

            print(self.name + " ran away, but their inventory was lost in the scuffle.")
            log(self.name + " ran away, but their inventory was lost in the scuffle.")
            print("----------------------------------------------------------------------")
            log("----------------------------------------------------------------------")
        else:
            print(self.name + " can't run from the final enemy.")
            log(self.name + " can't run from the final enemy.")
            print("----------------------------------------------------------------------")
            log("----------------------------------------------------------------------")
    
class Enemy(Character):
    """ Inherits randomly generated states from character and adds a weapon and 
        armor attribute instead of an inventory, modifying attributes accordingly. 
        It also has a method to describe the enemy and its gear."""

    def __init__(self, name, weapon, armor):
        """
            Creates an enemy object grabbing base stats from character and sets the weapon and 
            armor as designed (randomly generated by generateGear()). It then modifies attack 
            and defense accordingly.
        """
        super().__init__(name)
        self.weapon = weapon
        self.armor = armor
        # Modify stats based on the weapon and armor if present.
        if weapon is not None:
            self.attack += int(weapon[2])

        if armor is not None:
            self.defense += int(armor[2])
    
    def description(self):
        """
            Displays a description of the enemy based on their gear to indicate their relative strength to the player. 
        """
        if not(self.armor) and not(self.weapon):
            print(f"A(n) {self.name} with {self.health} health has appeared!")
            log(f"A(n) {self.name} with {self.health} health has appeared!")
        elif not(self.armor):
            print(f"A(n) {self.name} with {self.health} health and a(n) {self.weapon[1]} has appeared!")
            log(f"A(n) {self.name} with {self.health} health and a(n) {self.weapon[1]} has appeared!")
        elif not(self.weapon):
            print(f"A(n) {self.name} with {self.health} health and a(n) {self.armor[1]} has appeared!")
            log(f"A(n) {self.name} with {self.health} health and a(n) {self.armor[1]} has appeared!")
        else:
            print(f"A(n) {self.name} with {self.health} health, a(n) {self.weapon[1]}, and a(n) {self.armor[1]} has appeared!")
            log(f"A(n) {self.name} with {self.health} health, a(n) {self.weapon[1]}, and a(n) {self.armor[1]} has appeared!")
        print("----------------------------------------------------------------------")
        log("----------------------------------------------------------------------")
        
#------------------------------ Supplementary Functions ------------------------------

def readItems():
    """
        Grabs the items and parses them into a list from the input file (Items.txt). It returns the list as a nested array.
    """
    infile = open("Items.txt")
    itemList = [[], [], []]

    for line in infile:
        # Items split based on a comman and a space.
        item = line.split(", ")
        # Each item is added to one of the following categories: weapons, armor, or potions 
        # based on their identifier (the first letter).
        if item[0] == 'W':
            itemList[0].append(item)
        elif item[0] == 'A':
            itemList[1].append(item)
        else:
            itemList[2].append(item)

    infile.close()
    return itemList

def randomizeEnemyOrder(enemies):
    """
        Randomizes the enemy order by grabbing a random index from the enemy array, adding 
        it to enemy order, and then removing that index from enemies. It returns an array 
        of enemies in random order.
    """
    enemyOrder = []
    # Loop through each enemy.
    while len(enemies) > 0:
        # Grab a random enemy.
        index = randrange(0, len(enemies))
        # Add it to enemyOrder.
        enemyOrder.append(enemies[index])
        # Remove the enemy from enemies to prevent duplicates.
        enemies.pop(index)
    # Return new enemy order as an array.
    return enemyOrder


def battle(player, potion, enemies):
    """
        It randomizes enemy order using randomizeEnemyOrder(). It then loops through those enemies, 
        determining who goes first based on agility stats. So long as the player has not run and both 
        the player and the enemy are still alive (health above 0), they will continue to battle. 
        With each loop, on the player's turn, the player is given four choices, each rendered from 
        playerOptions. Checking stats or inventory does not take the player's turn but attempting to 
        attack, use a health potion, or run away will. The enemy will always use their turn to attack. 
        If the enemy dies, the player moves on to the next. If the player dies, it's game over. After 
        the enemy dies, it will drop any weapons and armor it's carrying and has a chance to drop a health 
        potion. Should the player defeat all the enemies, they win.
    """
    playerOptions = {0: "Attack", 1: "Use Health Potion", 2: "Run Away", 3: "Check Stats", 4: "Check Inventory"}
    # Randomize enemy order.
    oEnemies = randomizeEnemyOrder(enemies)
    # Loop so long as there is another enemy to face.
    for index, enemy in enumerate(oEnemies):
        enemy.description()
        # Determine turn order based on agility stats.
        if player.agility >= enemy.agility:
            playerTurn = True
        else:
            playerTurn = False

        ran = False
        # While the player and enemy are alive and the playe did not run...
        while player.health > 0 and enemy.health > 0 and not(ran):
            # On the players turn...
            if playerTurn:
                startLoop = True
                while startLoop or choice == 3 or choice == 4:
                    startLoop = False
                    print("What would " + player.name + " like to do?\n")
                    log("What would " + player.name + " like to do?\n")
                    # Display each option from playerOptions.
                    for key in playerOptions:
                        print(str(key) + " " + playerOptions.get(key))
                        log(str(key) + " " + playerOptions.get(key))
                    choice = int(input("\nEnter a number: "))
                    log("\nEnter a number: " + str(choice))
                    print("----------------------------------------------------------------------")
                    log("----------------------------------------------------------------------")
                    # If the player chooses a check option, display relevant information and allow 
                    # them to choose again since checking does not take a turn. 
                    if choice == 3:
                        player.getStats()  
                    elif choice == 4:
                        player.getInventory()                                        
                # If the player chooses to attack... 
                if choice == 0:
                    # Generate player damage.
                    damage = player.damageGen()
                    # Damage enemy.   
                    [modifier, blocked] = enemy.takeDamage(damage)
                    # Display results.
                    print(player.name + " attacked the " + enemy.name + " for " + str(damage) + " points of damage.")
                    log(player.name + " attacked the " + enemy.name + " for " + str(damage) + " points of damage.")
                    print(str(blocked) + " points of damage were blocked.")
                    log(str(blocked) + " points of damage were blocked.")
                    print("The " + enemy.name + " took " + str(modifier) + " points of damage and its health is now " + str(enemy.health) + ".")
                    log("The " + enemy.name + " took " + str(modifier) + " points of damage and its health is now " + str(enemy.health) + ".")
                    print("----------------------------------------------------------------------")
                    log("----------------------------------------------------------------------")
                # Otherwise, if the player chooses to use a health potion, allow them to attempt to do so.
                elif choice == 1:
                    player.useHealthPotion(potion)
                # Else the player chooses to run.
                else:
                    player.run(index, len(oEnemies))
                    # If the player is not facing the last enemy, allow it.
                    if index != len(oEnemies) - 1: 
                        ran = True  
            # It's the enemy's turn.
            else:
                # Same logic as player attack, but for the enemy respectively.
                damage = enemy.damageGen()
                [modifier, blocked] = player.takeDamage(damage)
                print("The " + enemy.name + " attacked " + player.name + " for " + str(damage) + " points of damage.")
                log("The " + enemy.name + " attacked " + player.name + " for " + str(damage) + " points of damage.")
                print(str(blocked) + " points of damage were blocked.")
                log(str(blocked) + " points of damage were blocked.")
                print(player.name + " took " + str(modifier) + " points of damage and their health is now " + str(player.health) + ".")
                log(player.name + " took " + str(modifier) + " points of damage and their health is now " + str(player.health) + ".")
                print("----------------------------------------------------------------------")
                log("----------------------------------------------------------------------")
            # Switch turns.
            playerTurn = not(playerTurn)
            
        if player.health <= 0:
            return "Game Over!"
        # Generate a health potion (20% chance) for the player to potentially loot from the enemy.
        healthPotion = None
        if randrange(0, 10) > 7:
            healthPotion = potion
        # If the enemy has something to loot...
        if (enemy.weapon is not None or enemy.armor is not None or healthPotion is not None) and (index != len(oEnemies) - 1 and not(ran)):
            equipment = [enemy.weapon, enemy.armor, healthPotion]
            print("The " + enemy.name + " dropped:\n")
            log("The " + enemy.name + " dropped:\n")
            
            d = {}

            selectionIndex = 0
            # Add each lootable item to the dictionary d based on their type (weapon, armor, or potion).
            for item in equipment:
                if item is not None and item[0] == 'W':
                    print(f"{selectionIndex} Weapon - {item[1].capitalize()}, Damage: {item[2]}, Weight: {item[3].strip()}")
                    log(f"{selectionIndex} Weapon - {item[1].capitalize()}, Damage: {item[2]}, Weight: {item[3].strip()}")
                    d.update({selectionIndex: item})
                    selectionIndex += 1
                elif item is not None and item[0] == 'A':
                    print(f"{selectionIndex} Armor - {item[1].capitalize()}, Defense: {item[2]}, Weight: {item[3].strip()}")
                    log(f"{selectionIndex} Armor - {item[1].capitalize()}, Defense: {item[2]}, Weight: {item[3].strip()}")
                    d.update({selectionIndex: item})
                    selectionIndex += 1
                elif item is not None:
                    print(f"{selectionIndex} Health potion - Quantity: 1, Weight: {item[3].strip()}")
                    log(f"{selectionIndex} Health potion - Quantity: 1, Weight: {item[3].strip()}")
                    d.update({selectionIndex: item})
                    selectionIndex += 1   
            itemIndex = int(input("\nEnter a number: "))
            log("\nEnter a number: " + str(itemIndex))
            # Add the player's chosen item to their inventory.
            player.addItem(d.get(itemIndex))
            print("----------------------------------------------------------------------")  
            log("----------------------------------------------------------------------")
    # At this point the player has defeated all enemies.
    return "Victory!"

def log(record):
    """
        Takes a record (string) and prints it to the out file (battle-log.txt).
    """
    print(record, file = outFile)

#------------------------------ Main ------------------------------
outFile = open("battle-log.txt", "w")

def main():
    """ 
        The main function for user interface (including nested methods) and input/output and enemy generation. 
    """
    print("----------------------------------------------------------------------")
    log("----------------------------------------------------------------------")
    name = input("Enter a name for your hero: ")
    log("Hero: " + name)
    player = Player(name)
    print("----------------------------------------------------------------------")
    log("----------------------------------------------------------------------")

    itemList = readItems()
    print("Choose a starting item:\n")
    log("Choose a starting item:\n")

    d = {}

    listIndex = 0
    # For each item in itemList add each as an option in the dictionary d.
    for index, category in enumerate(itemList):
        for item in category:
            if index == 0:
                print(f"{listIndex} {item[1].capitalize()}, Damage: {item[2]}, Weight: {item[3].strip()}")
                log(f"{listIndex} {item[1].capitalize()}, Damage: {item[2]}, Weight: {item[3].strip()}")
            elif index == 1:
                print(f"{listIndex} {item[1].capitalize()}, Defense: {item[2]}, Weight: {item[3].strip()}")
                log(f"{listIndex} {item[1].capitalize()}, Defense: {item[2]}, Weight: {item[3].strip()}")
            else:
                print(f"{listIndex} {item[1].capitalize()}, Recovery: {item[2]}, Weight: {item[3].strip()}")
                log(f"{listIndex} {item[1].capitalize()}, Recovery: {item[2]}, Weight: {item[3].strip()}")
            d.update({listIndex: item})
            listIndex += 1
    
    itemIndex = int(input("\nEnter a number: "))
    log("\nEnter a number: " + str(itemIndex))
     # Add the player's chosen item to their inventory.
    player.addItem(d.get(itemIndex))
    print("----------------------------------------------------------------------")
    log("----------------------------------------------------------------------")
    # Display stats and inventory at the begenning of the game.
    player.getStats()
    player.getInventory()

    def generateGear(gear):
        """
            Grabs a piece of equipment from gear (an array) randomly. 
        """
        index = randrange(0, len(gear))
        return gear[index]
    
    enemies = []
    # Three enemies arbitrarily. Can add more to adjust game balance.
    enemyNames = ["goblin", "skeleton", "troll"]
    # Potions grabbed and passed to battle for player use.
    potion = itemList[2][0]
    # For each enemy generate one with no items, one item (weapon or armor), or two items (weapon and armor).
    # Generate gear randomly from possible items stored in itemList.
    for enemyName in enemyNames:
        outcome = randrange(0, 4)
        if outcome == 0:
            enemies.append(Enemy(enemyName, generateGear(itemList[0]), generateGear(itemList[1])))
        elif outcome == 1:
            enemies.append(Enemy(enemyName, generateGear(itemList[0]), None))
        elif outcome == 2:
            enemies.append(Enemy(enemyName, None, generateGear(itemList[1])))
        else:
            enemies.append(Enemy(enemyName, None, None))
    
    result = battle(player, potion, enemies) 
    
    print(result)
    log(result)
    print("----------------------------------------------------------------------")
    log("----------------------------------------------------------------------")

    outFile.close()

main()