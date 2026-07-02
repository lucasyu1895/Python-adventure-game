import random
from interface import *

# --- INTERFACE HELPER FUNCTIONS ---

def make_choice(question, choices_list):
    """
    Displays text on the UI interface and presents the buttons.
    Returns the lowercased, stripped version of the selected choice.
    """
    show_text(question)
    choice = show_choices(choices_list)
    return choice.lower().strip()

def player_status(player):
    """Displays player status using the interface layout."""
    show_text(f"❤️ Health: {player['health']} | 🎒 Inventory: {', '.join(player['inventory']) if player['inventory'] else 'Empty'}")

# --- ROOM DEFINITIONS ---

# START ROOM
def starting_room(player):
    clear_screen()
    set_location("The Center Maze")
    show_text("You are at the center of the mysterious maze.")
    show_text("Legend says two magical keys can unlock the true exit hidden deep within.")
    type_text("You stand before three heavy archways: a gray door, a red door, and a shining gold door.")

    choice = make_choice("Choose a door:", ["Gray", "Red", "Gold"])

    if choice == "gray":
        return "gray_room"
    elif choice == "red":
        return "red_room"
    elif choice == "gold":
        return "gold_room"

# ROOM 1 (GRAY ROOM)
def gray_room(player):
    clear_screen()
    set_location("The Gray Room")
    show_picture("cave.jpg")  
    show_text("You enter the cold, stone gray room.")
    
    if "gray_visited" not in player["state"]:
        show_text("A spider drops from the ceiling and bites you! -5 health.")
        player["health"] -= 5
        
        if "silver coin" not in player["inventory"]:
            show_text("You found a silver coin gleaming on the floor.")
            player["inventory"].append("silver coin")
        else:
            show_text("You see a silver coin on the floor, but you are already carrying one.")
        
        inspect = make_choice("Do you want to search the dusty spider web?", ["Yes", "No"])
        if inspect == "yes":
            if "bandage" not in player["inventory"]:
                show_text("You carefully look behind the web and find an old bandage!")
                player["inventory"].append("bandage")
            else:
                show_text("You find a bandage, but your inventory cannot hold another one.")
        else:
            show_text("You decide it is too dangerous to touch.")
        player["state"].append("gray_visited")
    else:
        show_text("The room is quiet. The spider you encountered earlier has skittered away.")

    player_status(player)
    if player["health"] <= 0:
        return "end_game"

    choice = make_choice("Choose a direction:", ["Red", "Yellow", "Tunnel", "Back"])

    if choice == "red":
        return "red_room"
    elif choice == "yellow":
        return "yellow_room"
    elif choice == "tunnel":
        return "black_room"
    elif choice == "back":
        return "starting_room"

# ROOM 2 (RED ROOM)
def red_room(player):
    clear_screen()
    set_location("The Red Room")
    show_picture("apple.webp")  
    show_text("You enter the warm red room.")
    
    if "red_visited" not in player["state"]:
        show_text("You find a fresh apple sitting on a stone pedestal! +5 health.")
        player["health"] += 5
        
        if "apple" not in player["inventory"]:
            player["inventory"].append("apple")
        else:
            show_text("There is another apple here, but you can't carry duplicates.")
        player["state"].append("red_visited")
    else:
        show_text("The pedestal where the apple once sat stands bare.")

    if "apple" in player["inventory"]:
        eat = make_choice("Do you want to eat an apple right now for an extra +10 health?", ["Yes", "No"])
        if eat == "yes":
            show_text("Delicious! You gain +10 health.")
            player["health"] += 10
            player["inventory"].remove("apple")

    player_status(player)

    choice = make_choice("Choose a path:", ["Green", "White", "Yellow", "Blue", "Iron", "Back"])

    if choice == "green":
        return "green_room"
    elif choice == "white":
        return "white_room"
    elif choice == "yellow":
        return "yellow_room"
    elif choice == "blue":
        return "blue_room"
    elif choice == "iron":
        return "armory_room"
    elif choice == "back":
        return "starting_room"

# GOLD ROOM
def gold_room(player):
    clear_screen()
    set_location("The Gold Room")
    show_picture("gold.webp")  
    show_text("You enter a brilliant, shining Gold Room.")
    
    if "gold_visited" not in player["state"]:
        show_text("A trap triggers! Spikes pop from the floor. -15 health.")
        player["health"] -= 15
        show_text("Under the loose floorboards, you discover a stash of gold coins!")
        
        if "gold coin" not in player["inventory"]:
            player["inventory"].append("gold coin")
            show_text("You picked up a shiny gold coin.")
        else:
            show_text("You see gold coins, but your bag rejects duplicates!")
            
        player["state"].append("gold_visited")
    else:
        show_text("The floor spikes are already deployed and broken. There is nothing left to loot here.")
    
    player_status(player)
    if player["health"] <= 0:
        return "end_game"
        
    choice = make_choice("Where do you go?", ["Black", "Armory", "Back"])
       
    if choice == "black":
        return "black_room"
    elif choice == "armory":
        return "armory_room"
    elif choice == "back":
        return "starting_room"

# ARMORY ROOM
def armory_room(player):
    clear_screen()
    set_location("The Armory")
    show_picture("armory.jpg")  
    show_text("You enter an ancient, dusty Armory.")
    
    if "armory_visited" not in player["state"]:
        show_text("Weapon racks line the walls, mostly rusted away.")
        choice = make_choice("Do you search the weapon crates or the armor stand?", ["Crates", "Stand"])
           
        if choice == "crates":
            if "steel sword" not in player["inventory"]:
                show_text("You find a pristine Steel Sword!")
                player["inventory"].append("steel sword")
            else:
                show_text("You find a sword, but you're already carrying one!")
        elif choice == "stand":
            show_text("You salvage an Iron Helmet! Your body feels protected. +15 health.")
            player["health"] += 15
            if "iron helmet" not in player["inventory"]:
                player["inventory"].append("iron helmet")
        player["state"].append("armory_visited")
    else:
        show_text("The crates and stands have completely been picked clean.")
        
    player_status(player)
    choice = make_choice("Where to next?", ["Blue", "Red"])
       
    if choice == "blue":
        return "blue_room"
    elif choice == "red":
        return "red_room"

# BLUE ROOM
def blue_room(player):
    clear_screen()
    set_location("The Blue Room")
    show_picture("potion.webp")  
    show_text("You enter a room bathed in a soft blue glow.")
    
    if "blue_visited" not in player["state"]:
        show_text("You find a glowing magic potion sitting quietly on a pedestal.")
        choice = make_choice("Do you drink it right now?", ["Yes", "No"])

        if choice == "yes":
            show_text("The potion heals your soul! +20 health.")
            player["health"] += 20
            if "magic potion" not in player["inventory"]:
                player["inventory"].append("magic potion")
            else:
                show_text("Your bag can't hold another potion, so it evaporates.")
        elif choice == "no":
            show_text("A strange aura drains your life force as punishment. -10 health.")
            player["health"] -= 10
        player["state"].append("blue_visited")
    else:
        show_text("The blue pedestal stands empty.")

    if "bandage" in player["inventory"] and player["health"] < 100:
        use_band = make_choice("Would you like to apply your bandage now to heal +15 HP?", ["Yes", "No"])
        if use_band == "yes":
            show_text("You wrap your wounds tightly. +15 health.")
            player["health"] += 15
            player["inventory"].remove("bandage")

    player_status(player)
    if player["health"] <= 0:
        return "end_game"

    choice = make_choice("Choose a direction:", ["Purple", "Green", "Black", "Armory"])

    if choice == "purple":
        return "purple_room"
    elif choice == "green":
        return "green_room"
    elif choice == "black":
        return "black_room"
    elif choice == "armory":
        return "armory_room"

# PURPLE ROOM (MINIBOSS BATTLE)
def purple_room(player):
    clear_screen()
    set_location("The Purple Cavern")
    show_picture("boss.webp")  
    show_text("You enter the deep purple cavern.")
    
    if "monster_dead" not in player["state"]:
        show_text("The air grows incredibly cold. A towering Abyssal Horror drops down to kill you!")
        monster_hp = 50
        
        while monster_hp > 0 and player["health"] > 0:
            show_text(f"Your Health: {player['health']} HP | Monster Health: {monster_hp} HP")
            
            actions = ["Attack", "Run"]
            if "magic potion" in player["inventory"]:
                actions.append("Potion")
                
            action = make_choice("What is your move?", actions)
           
            if action == "run":
                show_text("You turn around and scramble out of the room! The beast swipes your back.")
                show_text("You suffer -15 health but escape safely back to the Blue Room.")
                player["health"] -= 15
                if player["health"] > 0:
                    return "blue_room"
                else:
                    return "end_game"
                    
            elif action == "potion" and "magic potion" in player["inventory"]:
                show_text("You smash the magic potion over your hands! An aura of strength manifests.")
                show_text("You strike the horror for a massive 30 points of damage!")
                monster_hp -= 30
                player["inventory"].remove("magic potion")
               
            elif action == "attack":
                if "steel sword" in player["inventory"]:
                    damage = 20
                    show_text(f"You swing your Steel Sword through the darkness! You deal {damage} damage.")
                else:
                    damage = 10
                    show_text(f"You plunge forward with bare fists! You deal {damage} damage.")
                monster_hp -= damage

            if monster_hp > 0:
                monster_damage = random.randint(10, 18)
                show_text(f"The Abyssal Horror lashes out with sharp claws! You suffer -{monster_damage} health.")
                player["health"] -= monster_damage
               
        if player["health"] <= 0:
            show_text("You collapse on the floor, vanquished by the horror.")
            return "end_game"
            
        show_text("With a horrific death rattle, the monster dissolves into smoke.")
        player["state"].append("monster_dead")
       
        if "crystal key" not in player["inventory"]:
            show_text("Shining brightly amidst its ashes, you discover a crystal key!")
            player["inventory"].append("crystal key")
    else:
        show_text("The room is completely quiet. The monster's ashes still litter the floor.")
       
    player_status(player)
    choice = make_choice("Where do you go?", ["Treasure", "Blue"])
    if choice == "treasure":
        return "treasure_room"
    elif choice == "blue":
        return "blue_room"

# TREASURE ROOM
def treasure_room(player):
    clear_screen()
    set_location("The Treasure Vault")
    show_picture("treasure.webp")  
    show_text("You discover an ornate, reinforced treasure chest!")

    if "chest_opened" not in player["state"]:
        choice = make_choice("Do you open it?", ["Yes", "No"])

        if choice == "yes":
            show_text("You pry it open...")
            if "golden key" not in player["inventory"]:
                player["inventory"].append("golden key")
                show_text("You find a golden key!")
               
            if "gold coin" not in player["inventory"]:
                show_text("Hidden in the bottom velvet lining, you find a pristine gold coin!")
                player["inventory"].append("gold coin")
            else:
                show_text("You see a gold coin, but you cannot hold another one.")
               
            player["state"].append("chest_opened")
        elif choice == "no":
            show_text("You leave the treasure untouched.")
    else:
        show_text("The grand chest sits completely wide open and empty.")

    player_status(player)
    choice = make_choice("Choose an archway:", ["Secret", "Green"])
       
    if choice == "secret":
        return "secret_room"
    elif choice == "green":
        return "green_room"

# SECRET ROOM
def secret_room(player):
    clear_screen()
    set_location("The Secret Vault")
    show_picture("gate.webp")  
    show_text("You enter a grand vaulted chamber. A giant locked gate blocks the exit completely.")
    show_text("It requires both a Golden Key and a Crystal Key to unlock.")

    if "golden key" in player["inventory"] and "crystal key" in player["inventory"]:
        show_text("You place both keys into the lock mechanism. The giant iron gates slowly swing open!")
        show_text("A beautiful tunnel leads outside to eternal freedom.")
        show_text("TRUE ENDING ACHIEVED!")
        player_status(player)
        return "end_game"
    else:
        show_text("You do not have both keys to pass through this gate yet.")
        show_text("You must venture back into the maze to locate the missing parts.")
        player_status(player)
        make_choice("The only open passageway leads back into the Treasure Room.", ["Go Back"])
        return "treasure_room"


# BLACK ROOM (MERCHANT STORE HUB)
def black_room(player):
    clear_screen()
    show_picture("maze.png")  
    set_location("The Black Bazaar")
    
    # Move these outside of the loop so they only print ONCE on the screen
    show_text("You enter the quiet Black Room.")
    show_text("The strange old merchant stands beside a table illuminated by oil lamps.")
    show_text("Merchant says: 'Show me your coin and let us make a deal!'")

    shopping = True
    while shopping:
        shop_options = []
        if "silver coin" in player["inventory"]:
            shop_options.append("Trade Silver -> Shield")
        if "gold coin" in player["inventory"]:
            shop_options.append("Trade Gold -> Scroll")
        shop_options.append("Leave Shop")

        # By passing the question directly into make_choice, it updates beautifully
        trade_choice = make_choice("Select an action:", shop_options)
        
        if "silver" in trade_choice and "silver coin" in player["inventory"]:
            if "shield" not in player["inventory"]:
                clear_screen()  # Clear to prevent text pile-up
                show_text("You received a shield!")
                player["inventory"].append("shield")
                player["inventory"].remove("silver coin")
            else:
                clear_screen()
                show_text("Merchant yells: 'You already own a shield! No duplicates allowed!'")
               
        elif "gold" in trade_choice and "gold coin" in player["inventory"]:
            if "spell scroll" not in player["inventory"]:
                clear_screen()
                show_text("You bought a glowing Spell Scroll!")
                player["inventory"].append("spell scroll")
                player["inventory"].remove("gold coin")
            else:
                clear_screen()
                show_text("Merchant rolls his eyes: 'You already have a spell scroll!'")
               
        elif "leave" in trade_choice:
            shopping = False
            clear_screen()
            show_text("You back away from the merchant's stall.")
            
        # If the player runs out of money, kick them out of the shop menu automatically
        if "silver coin" not in player["inventory"] and "gold coin" not in player["inventory"]:
            shopping = False

    player_status(player)
    choice = make_choice("Where do you go?", ["Silver", "Start"])

    if choice == "silver":
        return "riddle_room"
    elif choice == "start":
        return "starting_room"

# RIDDLE ROOM
def riddle_room(player):
    clear_screen()
    show_picture("riddle.png")  

    set_location("The Chamber of Riddles")
    show_text("You enter a room filled with glowing candles.")
    
    if "riddle_solved" not in player["state"]:
        show_text("A booming voice echoes through the brick walls.")
        show_text('"I speak without a mouth and hear without ears. What am I?"')

        # Since this interface expects user text input for typing a riddle answer, we use input_text here
        answer = input_text("Your answer: ").lower().strip()

        if answer == "echo":
            show_text("Correct! The candles flare green.")
            if "fire gem" not in player["inventory"]:
                show_text("A marble pedestal rises, giving you a fire gem.")
                player["inventory"].append("fire gem")
            else:
                show_text("A pedestal rises with a fire gem, but your bag can't hold another one.")
            player["state"].append("riddle_solved")
        else:
            show_text("Wrong answer!")
            show_text("Poison gas fills the room rapidly! -20 health.")
            player["health"] -= 20
    else:
        show_text("The candles are burned out. You have already answered the riddle here.")

    player_status(player)
    if player["health"] <= 0:
        return "end_game"

    choice = make_choice("Which way?", ["Boss", "Black"])
       
    if choice == "boss":
        return "boss_room"
    elif choice == "black":
        return "black_room"

# NEW INTENSE BOSS ROOM
def boss_room(player):
    clear_screen()
    set_location("The Obsidian Amphitheater")
    show_picture("aizen.jpg")  

    show_text("You step into a colossal amphitheater of obsidian stone.")
    show_text("The shadows peel off the walls, coalescing into the massive SHADOW BEAST.")
   
    boss_hp = 150
    turn_counter = 1
    while boss_hp > 0 and player["health"] > 0:
        show_text(f"--- TURN {turn_counter} ---")
        show_text(f"PLAYER HP: {player['health']} | SHADOW BEAST HP: {boss_hp}")
       
        enraged = boss_hp <= 40
        if enraged:
            show_text("🔴 CRITICAL: The Shadow Beast has entered an ENRAGED state (+5 damage)!")

        if turn_counter % 3 == 0:
            show_text("⚠️ WARNING: The Shadow Beast is gathering void energy for an annihilating blast!")
            boss_intent = "blast"
        elif turn_counter % 3 == 2:
            show_text("🌀 WARNING: A reflective Shadow Shield is forming around the Beast!")
            boss_intent = "shield"
        else:
            show_text("The Beast bares its massive, sword-like fangs, ready to sweep.")
            boss_intent = "sweep"
           
        boss_actions = ["Strike", "Flee"]
        if "shield" in player["inventory"]:
            boss_actions.append("Defend")
        if "fire gem" in player["inventory"]:
            boss_actions.append("Detonate Gem")
        if "spell scroll" in player["inventory"]:
            boss_actions.append("Cast Scroll")
           
        action = make_choice("Execute action:", boss_actions)
        player_defending = False
        backlash_damage = 0
       
        if action == "flee":
            show_text("You panic and flee through the doorway back to safety!")
            return "riddle_room"
           
        elif action == "detonate gem":
            show_text("The Fire Gem erupts into a violent pillar of pure flame! Deal 45 damage.")
            boss_hp -= 45
            backlash_damage = 5
            player["inventory"].remove("fire gem")
           
        elif action == "cast scroll":
            show_text("A blast of localized solar light rips into the beast's flesh for 50 damage!")
            boss_hp -= 50
            backlash_damage = 10
            player["inventory"].remove("spell scroll")
           
        elif action == "defend":
            show_text("You dig your heels in and raise your sturdy shield.")
            player_defending = True
           
        elif action == "strike":
            if boss_intent == "shield":
                show_text("💥 RECOIL! You strike the shield. 0 damage and suffer -12 health recoil!")
                player["health"] -= 12
            else:
                if "steel sword" in player["inventory"]:
                    dmg = 25
                    show_text(f"You slash with your Steel Sword! You deal {dmg} damage.")
                else:
                    dmg = 12
                    show_text(f"You strike with your bare hands! You deal {dmg} damage.")
                boss_hp -= dmg

        player["health"] -= backlash_damage

        # Boss offense phase
        if boss_hp > 0 and player["health"] > 0:
            bonus = 5 if enraged else 0
           
            if boss_intent == "blast":
                if player_defending:
                    show_text(f"💥 Shield absorbs the void blast. -{15 + bonus} HP.")
                    player["health"] -= (15 + bonus)
                else:
                    show_text(f"💥 The raw void blast consumes you entirely! -{45 + bonus} HP.")
                    player["health"] -= (45 + bonus)
                   
            elif boss_intent == "sweep":
                if player_defending:
                    show_text(f"🛡️ The heavy tail sweeps across your shield. Safely slid back. -{3 + bonus} HP.")
                    player["health"] -= (3 + bonus)
                else:
                    show_text(f"❌ The claw sweep throws you violently against the wall. -{20 + bonus} HP.")
                    player["health"] -= (20 + bonus)
                   
            elif boss_intent == "shield":
                show_text("🌀 The Shadow Beast pulses with reflective void energy...")
                   
        turn_counter += 1

    if player["health"] <= 0:
        show_text("The Shadow Beast steps over your broken body. BAD ENDING")
        return "end_game"
       
    show_text("The Shadow Beast shatters into millions of fragments, dissolving completely.")
    if "shield" in player["inventory"] and "fire gem" in player["inventory"]:
        show_text("LEGENDARY ENDING UNLOCKED")
    elif "spell scroll" in player["inventory"] or "fire gem" in player["inventory"] or "steel sword" in player["inventory"]:
        show_text("MYSTICAL HERO ENDING UNLOCKED")
    else:
        show_text("SURVIVAL ENDING")
       
    player_status(player)
    return "end_game"

# GREEN ROOM
def green_room(player):
    clear_screen()
    set_location("The Gate Checkpoint")
    show_picture("green.jpg")  

    show_text("You enter a guarded checkpoint room. A heavily armored gatekeeper stands watch.")
    show_text("He asks for a payment of 1 Silver or 1 Gold coin to bypass the door.")
   
    choice = make_choice("What do you do?", ["Talk to Guard", "Turn Back"])
    if choice == "turn back":
        show_text("You leave the gatekeeper behind and head back.")
        return "red_room"
       
    if "silver coin" in player["inventory"]:
        show_text("You hand a silver coin over to the guard. GOOD ENDING")
    elif "gold coin" in player["inventory"]:
        show_text("You hand over a valuable gold coin! RICH ESCAPE ENDING")
    else:
        show_text("The guard glares: 'No money, no passage!' He shoves you backward.")
        return "red_room"

    player_status(player)
    return "end_game"

# WHITE ROOM
def white_room(player):
    clear_screen()
    set_location("Blinding Void")
    show_picture("void.jpg")  

    show_text("You walk forward into absolute, blinding white space. The door vanishes.")
    show_text("Whispers fill your ears. You are spun around!")
   
    teleport_target = random.choice(["starting_room", "gray_room", "gold_room"])
    make_choice("Space shifts beneath you...", ["Continue"])
    return teleport_target

# YELLOW ROOM
def yellow_room(player):
    clear_screen()
    set_location("Trap Corridor")
    show_picture("yellow.webp")  

    show_text("As soon as you enter, a tripwire snaps! A giant boulder rattles straight towards you!")
   
    choice = make_choice("Action:", ["Alcove", "Run"])
    if choice == "alcove":
        show_text("You press yourself flat into a slot. The boulder thunders past! Gold room cleared.")
        return "gold_room"
    else:
        show_text("You try to outrun it, but the stone is too fast! It slams directly into you. -40 health.")
        player["health"] -= 40
        player_status(player)
        if player["health"] <= 0:
            show_text("You were crushed completely by the rolling boulder.")
            return "end_game"
        else:
            show_text("The blast throws you through a drywall... you collapse in the Red Room.")
            return "red_room"


# --- ENGINE INITIALIZATION & CONFIGURATION ---

player = {
    "health": 100,
    "inventory": [],
    "state": []  
}

# Setup the Graphical UI Parameters
set_background_color("#1a1a2e")
set_text_color("#e0e0e0")
set_button_color("#16213e", "#e0e0e0")
set_font("Courier", 24)
show_title("The Mysterious Maze")

show_picture("maze.png")  
play_music("aizen_treachery.mp3") 

# Introduce Character Customization Setup
name = input_text("What is your name, traveler?")
show_text(f"The maze whispers... Welcome, {name}!")
make_choice("Begin your trial.", ["Enter Maze"])

# The System Engine State Switch Loop 
next_target = "starting_room"

while next_target != "end_game":
    if next_target == "starting_room":
        next_target = starting_room(player)
    elif next_target == "gray_room":
        next_target = gray_room(player)
    elif next_target == "red_room":
        next_target = red_room(player)
    elif next_target == "gold_room":
        next_target = gold_room(player)
    if next_target == "armory_room":
        next_target = armory_room(player)
    if next_target == "blue_room":
        next_target = blue_room(player)
    if next_target == "purple_room":
        next_target = purple_room(player)
    if next_target == "treasure_room":
        next_target = treasure_room(player)
    if next_target == "secret_room":
        next_target = secret_room(player)
    if next_target == "black_room":
        next_target = black_room(player)
    if next_target == "riddle_room":
        next_target = riddle_room(player)
    if next_target == "boss_room":
        next_target = boss_room(player)
    if next_target == "green_room":
        next_target = green_room(player)
    if next_target == "white_room":
        next_target = white_room(player)
    if next_target == "yellow_room":
        next_target = yellow_room(player)

# Game Termination Cleanups
clear_screen()
stop_music()

if player["health"] > 0:
    show_text("🎉 You successfully broke out and survived the maze!")
else:
    show_text("💀 Game Over. Better luck on your next run.")

show_choices(["Exit Game"])

