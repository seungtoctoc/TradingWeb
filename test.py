from room import Room, Item
from item import Item, Weapon, LightSource, Gold, Container
from player import Player, Monster, Merchant
from os import system, name

#Item list
ten_gold = Gold(
    -1,
    "a smattering of 10 gold pieces lies on the cobblestone tile next to the rusty sword.",
    10
)

thousand_gold = Gold(
    -1,
    "a pile of 1000 gold pieces is piled high in a treasure chest near something.",
    10
)

torch = LightSource(
    0,
    "torch",
    "a crude stick with an oil soaked rag at its tip",
    "a torch lies on the floor next to the chest, hastily discarded.",
    0,
    0,
    4
)

chest = Container(
    1,
    "chest",
    "its lock was clearly broken, but there appears to be something inside.",
    "a battered wooden chest sits in the corner",
    [ten_gold]
)

rusty_sword = Weapon(
    2,
    "rusty_sword",
    "rusting, it could probably do better if it were sharpened",
    "a rusty sword lies nearby under a drip somewhere on the cavern's ceiling",
    2,
    4
)

golden_sword = Weapon(
    3,
    "golden_sword",
    "This brilliant blade has clearly been well taken care of",
    "a golden sword lies buried to the hilt in a large stone just before the mouth of the chasm",
    2000,
    200
)

items = [ten_gold.name, torch.name, chest.name, rusty_sword.name, golden_sword.name]

#Monster list
small_spider = Monster(
    0,
    "spider",
    """
    A harmless looking but very large spider skitters along the floor.
    This must be what you heard outside.
    """,
    5,
    1,
    1
)

skeleton = Monster(
    1,
    "skeleton",
    """
    a skeleton's jangly bones quiver at the sight of you
    it appears to be afraid.
    """,
    10,
    3,
    5
)

boulder = Monster(
    2,
    "boulder",
    """
    a menacing-looking, but badly cracked boulder (yes, cracked
    boulders can look menacing) looks in your direction (yes, cracked
    boulders can look in your direction.)

    """,
    20,
    10,
    15
)

dragon = Monster(
    3,
    "dragon",
    """
        A golden dragon guards the far end of the room.
        Orange-hot fire shoots from its snout occasionally.
        It appears to be sleeping...
    """,
    200,
    88,
    1000
)

monsters = [small_spider.name, skeleton.name, dragon.name, boulder.name]

# Declare all the rooms
rooms = {

    'outside': Room(
        "Outside Cave Entrance",
        """
        You are standing to the South of the mouth of what
        appears to be a large cavern. It's dark inside of the
        cavern, but you think you make out the shadow of what
        appears to be a foyer with connected rooms...
        There also appears to be something skittering on the floor.
        """,
        [chest, torch],
        []
    ),

    'foyer': Room(
        "Foyer",
        """
        Dim light filters in from the south. Dusty
        passages run north and east.
        """,
        [chest, rusty_sword],
        [small_spider]
    ),

    'something': Room(
        "Something",
        """
        Something coming soon
        """,
        [chest, thousand_gold],
        [boulder]
    ),

    'overlook': Room(
        "Grand Overlook",
        """
        A steep cliff appears before you, falling
        into the darkness. Ahead to the north, a light flickers in
        the distance, but there is no way across the chasm.
        """,
        [golden_sword],
        [skeleton]),
        
    'narrow':   Room(
        "Narrow Passage",
        """
        The narrow passage bends here from west
        to north. The smell of gold permeates the air.
        """,
        [],
        []
    ),

    'treasure': Room(
        "Treasure Chamber",
        """
        You've found the long-lost treasure
        chamber! Sadly, it has already been completely emptied by
        earlier adventurers. A dragon stubbornly guards the far end
        of the room. The only exit is to the south.
        """,
        [],
        [dragon]
    ),
}

# Link rooms together

rooms['outside'].n_to = rooms['foyer']
rooms['foyer'].s_to = rooms['outside']
rooms['foyer'].n_to = rooms['overlook']
rooms['foyer'].e_to = rooms['narrow']
rooms['foyer'].w_to = rooms['something']
rooms['something'].e_to = rooms['foyer']
rooms['overlook'].s_to = rooms['foyer']
rooms['narrow'].w_to = rooms['foyer']
rooms['narrow'].n_to = rooms['treasure']
rooms['treasure'].s_to = rooms['narrow']
#initial room
room = rooms['outside']


# Main
#

# Print important messages
def sys_print(s):
    print(f"\n***{s}***")

def clear():
    if name == "nt":
        system("cls")
    else:
        system("clear")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # ----------
# Make a new player object that is currently in the 'outside' room.
clear()
merchant = Merchant(rooms['outside'], "there's a merchant here. Try trade merchant.")
rooms['outside'].monsters.append(merchant)
monsters.append(merchant)

i = input("Welcome to Cavern of Marvelous Adventures! Please enter your name:\n")
player = Player(i, room, 100, 0, 0)


sys_print(f"Welcome to your doom, {player.name}")

def help():
    return """
            A friendly digitized voice that seems out of place in this dank, harsh environment says to you:

            * [L] to look around
            * [N,S,E,W] [North, South, East, West] [Up, Down, Right, Left] to travel
            * [Inspect] [item] to inspect an item 
                (ex: `inspect rock` to inspect an item named rock)
            * [Take] [item] to take an item 
                (ex: `take rock` to take a rock)
            * [Drop] [item] to drop an item 
                (ex: `drop rock` to drop a rock)
            * [Equip] [Item] to equip an item in your inventory 
                (ex: `equip sword` to equip a sword you already have)
            * [Q|q] to quit

            Written on the wall nearby you see a message, hastily scrawled:
            The rock is a lie
        """

def available_directions():
    availableDirs = directions()

    if availableDirs.__contains__("n"):
        availableDirs.extend(["north", "up", "forward", "forwards"])

    if availableDirs.__contains__("s"):
        availableDirs.extend(["south", "down", "backward", "backwards"])
        

    if availableDirs.__contains__("e"):
        availableDirs.extend(["east", "right"])

    if availableDirs.__contains__("w"):
        availableDirs.extend(["west", "left"])

    return availableDirs

def directions():
    directions = []

    if hasattr(player.current_room, "n_to"):
        directions.append("n")
    if hasattr(player.current_room, "s_to"):
        directions.append("s")
    if hasattr(player.current_room, "e_to"):
        directions.append("e")
    if hasattr(player.current_room, "w_to"):
        directions.append("w")

    return directions

def travel(input):   

    input = input.lower()
    if input in available_directions():
        if input == "n" or input == "north" or input == "up" or input == "forward" or input == "forwards":
            player.current_room = player.current_room.n_to
        elif input == "s" or input == "south" or input == "down" or input == "backward" or input == "backwards":
            player.current_room = player.current_room.s_to
        elif input == "e" or input == "east" or input == "right":
            player.current_room = player.current_room.e_to
        elif input == "w" or input == "west" or input == "left":
            player.current_room = player.current_room.w_to
    else:
        sys_print("There's nothing in that direction. Try again.")

def look():
    if player.has_light() or player.current_room == rooms['outside']:
        sys_print("You look around the room and see:")

        item_instructions = "try \"take rock\" to take a rock, or \"inspect rock\" to inspect it"
        monster_instructions = "try \"fight spider\" to fight a spider"    

        #empty line
        print()

        if len(player.current_room.items) == 0:
            print(f"There are no items here. If there were, you could {item_instructions}")
            item_instructions = ""

        if len(player.current_room.monsters) == 0:
            print(f"There are no monsters here. If there were, you could {monster_instructions}")
            monster_instructions = ""

        #print the room_description(s)
        item_descs = [x.room_description for x in player.current_room.items]
        for i, _ in enumerate(item_descs):
            print(f"{player.current_room.items[i].name}: {item_descs[i]}")
        #empty line
        print()
        #print monsters in the room:
        for i in player.current_room.monsters:
            print(i.room_description)
        instructions = item_instructions + "\n" + monster_instructions
        sys_print(f"\n{instructions}\n")
    else:
        sys_print(f"Maybe if you had some light, you could see what the heck was happening!")

def inspect(item):    
    if isinstance(item, Item):
        sys_print(f"You are inspecting a(n) {item.name}")
        print(item.description)
    if isinstance(item, Container):
        #empty line
        print()
        item.list_inventory(player)  
        return

def prompt(s):
    # print a quicklist of commands
    commands = f"(L to look around | {' | '.join(directions())} to travel | Q to quit | [Help|?] for common commands): "
    prompt = f"\nWhat would you like to do, {player.name}?\n{commands}"

    return input(s + prompt)

def parse(inpt):    
    available_commands = [
        "travel", "walk", "go", "run",
        "take", "t", "steal",
        "pull", "remove", "arthur",
        "inspect", "look",
        "equip", "wear",
        "drop",
        "fight", "attack", "kick", "slap", "hug",
        "finger",
        "rock"
    ]
    available_commands.extend(available_directions())

    #add objects available in current room to command list    
    available_commands.extend([item.name for item in player.current_room.items])
    available_commands.extend([monster.name for monster in player.current_room.monsters])

    #add all available objects and monsters
    #available_commands.extend(items)
    #available_commands.extend(monsters)

    #add player's items
    available_commands.extend([item.name for item in player.inventory])
    available_commands.append(player.leftHandItem.name)
    available_commands.append(player.rightHandItem.name)

    inpt = inpt.lower()
    clear()
    # list of commands separated by space
    inputList = inpt.split()

    # only allow available commands to be parsed
    commands = []
    for cmd in inputList:            
        if cmd in available_commands or cmd in items or cmd in monsters:
            commands.append(cmd)

    if len(commands) >= 1:
        cmd1 = commands[0]

    if len(commands) > 1:
        cmd2 = commands[1]
        if len(commands) >2:
            sys_print("warning, a maximum of 2 commands (words separated by a space) will be used")
        #win and exit
        if cmd1 == "take" and cmd2 == "rock":
            if player.current_room != rooms['treasure']:
                sys_print("The rock is a lie!!!")
            else:
                print("""
                You somehow missed it earlier when you scanned the room,
                but right in front of the dragon's snout lies a plain looking rock.
                
                "This must be what all the fuss is about," you think to yourself.

                You approach the dragon stealthily, like a thief in the night...
                As you get closer, you can feel the heat from the occasional lick of flame
                coming from the sleeping dragon's snout. You time it just right. You reach in...
                """)

                quest = input("You think you noticed the dragon stirring. Continue? ")
                if quest == "y" or quest == "yes" or quest == "continue":                    
                    sys_print("You win! ... ... a rock? Thanks for playing!")
                else:
                    print("""
                    You back away as quietly as you came, scared for your life.
                    You stumble, making a small, but noticable noise. The dragon opens one eye...

                    Without even seeming to think about it, he opens his mouth, breathes
                    orange-hot flame and incinerates you in place. The dragon, satisfied
                    closes his eyes and goes back to sleep.

                    Dragons are so inconsiderate
                    """)                    
                #empty line
                print()
                exit(0)

        # parse verb commands
        if cmd1 == "travel" or cmd1 == "go" or cmd1 == "run" or cmd1 == "walk":
            travel(cmd2)
            return

        if cmd1 == "take" or cmd1 == "t" or cmd1 == "steal":
            player.take(cmd2)
            return

        elif cmd1 == "pull" or cmd1 == "remove" or cmd1 == "arthur":
            if cmd1 == "arthur":
                sys_print(f"{player.name} has summoned the power of King Arthur!")
                player.arthur = True

            player.pull(cmd2)
            return

        elif cmd1 == "inspect" or cmd1 == "look":            
            item = player.find(cmd2)
            inspect(item)
            return

        elif cmd1 == "equip" or cmd1 == "wear":
            item = player.get_from_inventory(cmd2)
            player.equipItem(item)
            return

        elif cmd1 == "drop":
            player.dropItem(cmd2)
            return

        elif cmd1 == "fight" or cmd1 == "attack" or cmd1 == "kick" or cmd1 == "slap" or cmd1 == "hug":
            player_items = [item.name for item in player.inventory]
            room_items = [item.name for item in player.current_room.items]
            room_monsters = [monster.name for monster in player.current_room.monsters]
            if cmd2 in player_items or cmd2 in room_monsters or cmd2 in room_items or cmd2 == player.leftHandItem.name or cmd2 == player.rightHandItem.name:
                if cmd1 == "hug":
                    sys_print(f"you try to hug a {cmd2} but it doesn't like that")
                elif cmd1 == "slap":
                    sys_print(f"you slap a {cmd2} - en guarde!")
                elif cmd1 == "kick":
                    sys_print(f"you kick a {cmd2} in the teeth - ouch your toe!")
            else:
                sys_print(f"{cmd2} isn't in this room!")

            player.fight(cmd2)
            return
    #single commands
    else:    
        dirs = ["n", "north", "up", "e", "east", "right", "s", "south", "down", "w", "west", "left"]
        
        if inpt == "q":
            exit(0)
        elif inpt == "help" or inpt == "?" or inpt == "h":
            print(help())
            return
        elif inpt in dirs:
            travel(inpt)
            return
        elif inpt == "l":
            look()
            return
        elif inpt == "arthur":
            sys_print(f"{player.name} has summoned the power of King Arthur!")
            player.arthur = True
            return
        elif inpt == "inventory" or inpt == "i":
            player.list_inventory()
            return
        elif inpt == "trade":
            if player.current_room.monsters.contains(merchant):
                merchant.list_inventory()
    sys_print("invalid command")

# Write a loop that:
#
# * Prints the current room name
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.
#
# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.



while True:
    # check if the player can see
    if player.has_light() == True or player.current_room == rooms['outside']:
        sys_print(f"{player.current_room.name}")
        p = prompt(f"\n{player.current_room.description}\n")
    else:
        dark_text = "It's dark. Maybe you should find some light"
        
        if player.current_room == rooms['overlook']:
            sys_print(f"You don't have a light!")
            print("""
You stumble forward, hands in front of you - feeling
for something to familiarize yourself with.

You hear an echo and see a light in the distance.
You continue forward...""")
            sys_print("You have fallen to your death!")
            # empty line
            print()
            exit(0)
        else:
            p = prompt(f"\n{dark_text}\n")
    parse(p)