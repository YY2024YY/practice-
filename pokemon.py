import random

class Skill:
    def __init__(self, name, effect, value, usage_point):
        self.name = name
        self.effect = effect
        self.value = value
        self.usage_point = usage_point

    def __str__(self):
        return f"{self.name} ({self.effect} {self.value} {self.usage_point})"

class Creature:
    def __init__(self, name, level, rarity, base_attack, base_defense, skills):
        self.name = name
        self.level = level
        self.rarity = rarity
        self.base_attack = base_attack
        self.base_defense = base_defense
        self.skills = skills
        self.HP = self.level * 10
        self.current_health = self.HP
        self.current_attack = self.base_attack
        self.current_defense = self.base_defense
        
    def __str__(self):
        return f"{self.name} (Level {self.level}) Rarity: {self.rarity} HP: {self.HP} Attack: {self.base_attack} Defense: {self.base_defense}"
        
    def use_skill(self, target, is_player=True):
        if is_player:
            while True:
            # Player's creature chooses a skill
                print(f"{self.name}'s turn. Choose a skill:")
                for i, skill in enumerate(self.skills, 1):
                    print(f"{i}, {skill.name}, {skill.effect}:, {skill.value}, Usage point: {skill.usage_point}")  
                choice = int(input("Enter the number of the skill: ")) - 1
                if choice < 0 or choice >= len(self.skills):
                    print("Invalid choice. Please choose again.")
                else:
                    skill = self.skills[choice]
                    break
        else:
            # Enemy creature randomly chooses a skill
            skill = random.choice(self.skills)

        if skill.usage_point <= 0:
            print(f"{self.name} has no usage point for {skill.name}!")
            return
        
        skill.usage_point -= 1
        match skill.effect:
            case "damage":
                # Calculate damage and apply it to the target
                damage = skill.value + self.current_attack - target.current_defense
                damage = max(damage, 1)  # Ensure damage is non-negative
                print(f"{self.name} used {skill.name} on {target.name} for {damage} damage!")
                target.take_damage(damage)
            case "heal":
                # Heal the creature
                heal_amount = skill.value
                self.heal(heal_amount)
                print(f"{self.name} used {skill.name} and healed for {heal_amount} HP! Current health: {self.current_health}")
            case "attack_boost":
                # Boost attack
                boost_value = skill.value
                self.boost_attack(boost_value)
                print(f"{self.name} used {skill.name} and boosted attack by {boost_value}! Current attack: {self.current_attack}")
            case "defense_boost":
                # Boost defense
                boost_value = skill.value
                self.boost_defense(boost_value)
                print(f"{self.name} used {skill.name} and boosted defense by {boost_value}! Current defense: {self.current_defense}")

    def take_damage(self, damage):
        self.current_health -= damage
        if self.current_health < 0:
            self.current_health = 0
        print(f"{self.name} took {damage} damage. {self.name}'s health: {self.current_health}")

    def heal(self, heal_amount):
        self.current_health += heal_amount
        if self.current_health > self.HP:
            self.current_health = self.HP

    def boost_attack(self, boost_value):
        self.current_attack += boost_value
        
    def boost_defense(self, boost_value):
        self.current_defense += boost_value

class PlayerOwnedCreature(Creature):
    def __init__(self, name, level, rarity, base_attack, base_defense, skills):
        super().__init__(name, level, rarity, base_attack, base_defense, skills)
        self.current_EXP = 0
        self.require_EXP = self.level * 50

    def __str__(self):
        return f"{self.name} (Level {self.level}) Rarity: {self.rarity} HP: {self.HP} Attack: {self.base_attack} Defense: {self.base_defense} EXP: {self.current_EXP}/{self.require_EXP}"

    def check_level(self):
        if self.current_EXP>= self.require_EXP:
            self.level += 1
            self.current_EXP= self.current_EXP - self.require_EXP
            self.require_EXP*= 2
            self.recalculate_stat()
            print(f"{self.name} leveled up to level {self.level}!")
            print(f"{self.name} (Level {self.level}) Rarity: {self.rarity} HP: {self.HP} Attack: {self.base_attack} Defense: {self.base_defense} EXP: {self.current_EXP}/{self.require_EXP}")

    def recalculate_stat(self):
        match self.rarity:
            case "normal":
                self.base_attack += 5
                self.base_defense += 5
                self.HP += 10
            case "rare":
                self.base_attack += 10
                self.base_defense += 10
                self.HP += 20
            case "epic":
                self.base_attack += 15
                self.base_defense += 15
                self.HP += 30
            case "legendary":
                self.base_attack += 20
                self.base_defense += 20
                self.HP += 40

class Player:
    def __init__(self, name):
        self.name = name
        self.own_creatures = []

    def add_creature(self, creature):
        self.own_creatures.append(creature)

    def display_creatures(self):
        print("Player's Creatures:")
        for creature in self.own_creatures:
            print(creature)
            
class Map:
    def __init__(self, name, level_range, creature_data):
        self.name = name
        self.level_range = level_range
        self.creature_data = creature_data

    def generate_creature(self, starter=False):
        creature_probabilities = self.calculate_probabilities()
        selected_species = random.choices(list(creature_probabilities.keys()), weights=list(creature_probabilities.values()))[0]
        creature_stats = self.creature_data[selected_species]
        
        rarity = creature_stats["rarity"]
        base_attack = random.randint(creature_stats["base_attack"] - 5, creature_stats["base_attack"] + 5)
        base_defense = random.randint(creature_stats["base_defense"] - 5, creature_stats["base_defense"] + 5)
        
        if starter:
            level = 5
        else:
            level = random.randint(self.level_range[0], self.level_range[1])
        
        if level > 5:
            level_difference = level - 5
            match rarity:
                case "normal":
                    base_attack += level_difference * 5
                    base_defense += level_difference * 5
                case "rare":
                    base_attack += level_difference * 10
                    base_defense += level_difference * 10
                case "epic":
                    base_attack += level_difference * 15
                    base_defense += level_difference * 15
                case "legendary":
                    base_attack += level_difference * 20
                    base_defense += level_difference * 20

        selected_skills = random.sample(creature_stats["skills"], 4)
        
        return Creature(selected_species, level, rarity, base_attack, base_defense, selected_skills)

    def calculate_probabilities(self):
        rarities = {"normal": 60, "rare": 30, "epic": 8, "legendary": 2}
        creature_probabilities = {}
        total_rarity = sum(rarities.values())
        for species, data in self.creature_data.items():
            rarity = rarities[data["rarity"]]
            creature_probabilities[species] = rarity / total_rarity
        return creature_probabilities

# Define creature data including base stats and potential skills
grass_type_skills = [
    Skill("Vine Whip", "damage", 25, 20),
    Skill("Razor Leaf", "damage", 30, 15),
    Skill("Absorb", "heal", 15, 25),
    Skill("Seed Bomb", "damage", 35, 12),
    Skill("Bullet Seed", "damage", 20, 25),
    Skill("Mega Drain", "heal", 25, 20),
    Skill("Leaf Blade", "damage", 40, 10),
    Skill("Energy Ball", "damage", 35, 12),
    Skill("Solar Beam", "damage", 50, 8),
    Skill("Grass Knot", "attack_boost", 30, 15),
    Skill("Giga Drain", "heal", 40, 10),
    Skill("Synthesis", "heal", 20, 25),
    Skill("Leaf Storm", "damage", 60, 5),
    Skill("Power Whip", "damage", 45, 10),
    Skill("Defense Curl", "defense_boost", 15, 25),
    Skill("Swords Dance", "attack_boost", 25, 20),
]

water_type_skills = [
    Skill("Water Gun", "damage", 20, 25),
    Skill("Bubble", "damage", 15, 30    ),
    Skill("Aqua Jet", "damage", 25, 20),
    Skill("Bubble Beam", "damage", 30, 15),
    Skill("Hydro Pump", "damage", 40, 10),
    Skill("Surf", "damage", 35, 12),
    Skill("Water Pulse", "damage", 25, 20),
    Skill("Aqua Tail", "damage", 30, 15),
    Skill("Healing Wave", "heal", 20, 25),
    Skill("Heal Pulse", "heal", 30, 20),
    Skill("Rain Dance", "attack_boost", 20, 25),
    Skill("Mist", "defense_boost", 15, 30),
]

fire_type_skills = [
    Skill("Ember", "damage", 20, 25),
    Skill("Flamethrower", "damage", 35, 12),
    Skill("Fire Blast", "damage", 40, 10),
    Skill("Fire Spin", "damage", 30, 15),
    Skill("Inferno", "damage", 45, 8),
    Skill("Flare Blitz", "damage", 50, 5),
    Skill("Fire Punch", "damage", 30, 20),
    Skill("Heat Wave", "damage", 35, 12),
    Skill("Reburn", "heal", 25, 20),
    Skill("Sunny Day", "attack_boost", 20, 25),
    Skill("Flame Wheel", "damage", 35, 12),
    Skill("Recover", "heal", 40, 10),
    Skill("Flame Charge", "attack_boost", 30, 15),
    Skill("Fire Shield", "defense_boost", 25, 20),
]

electric_type_skills = [
    Skill("Thunder Shock", "damage", 20, 25),
    Skill("Thunderbolt", "damage", 35, 12),
    Skill("Thunder", "damage", 40, 10),
    Skill("Spark", "damage", 25, 20),
    Skill("Volt Tackle", "damage", 50, 5),
    Skill("Charge Beam", "damage", 30, 15),
    Skill("Discharge", "damage", 35, 12),
    Skill("Wild Charge", "damage", 40, 10),
    Skill("Zap Cannon", "damage", 45, 8),
    Skill("Charge", "attack_boost", 25, 20),
    Skill("Thunder Wave", "heal", 25, 20),
    Skill("Recover", "heal", 40, 10),
    Skill("Light Screen", "defense_boost", 20, 25),
    Skill("Electric Field", "defense_boost", 30, 15)
]

# Define creature data for each map
town_trainning_ground_creature_data = {
    "Bulbasaur": {"base_attack": 18, "base_defense": 20, "rarity": "normal", "skills": grass_type_skills},
    "Chikorita": {"base_attack": 15, "base_defense": 20, "rarity": "normal", "skills": grass_type_skills},
    "Charmander": {"base_attack": 25, "base_defense": 10, "rarity": "normal", "skills": fire_type_skills},
    "Cyndaquil": {"base_attack": 22, "base_defense": 12, "rarity": "normal", "skills": fire_type_skills},
    "Squirtle": {"base_attack": 22, "base_defense": 18, "rarity": "rare", "skills": water_type_skills},
}

shadowed_woodland_creature_data = {
    "Pikachu": {"base_attack": 25, "base_defense": 20, "rarity": "rare", "skills": electric_type_skills},
    "Bulbasaur": {"base_attack": 18, "base_defense": 20, "rarity": "normal", "skills": grass_type_skills},
    "Oddish": {"base_attack": 16, "base_defense": 18, "rarity": "normal", "skills": grass_type_skills},
    "Bellsprout": {"base_attack": 19, "base_defense": 15, "rarity": "normal", "skills": grass_type_skills},
    "Tangela": {"base_attack": 20, "base_defense": 35, "rarity": "epic", "skills": grass_type_skills},
    "Chikorita": {"base_attack": 15, "base_defense": 20, "rarity": "normal", "skills": grass_type_skills},
    "Sunkern": {"base_attack": 18, "base_defense": 20, "rarity": "normal", "skills": grass_type_skills},
    "Treecko": {"base_attack": 18, "base_defense": 16, "rarity": "normal", "skills": grass_type_skills},
    "Seedot": {"base_attack": 18, "base_defense": 15, "rarity": "normal", "skills": grass_type_skills},
    "Turtwig": {"base_attack": 27, "base_defense": 21, "rarity": "rare", "skills": grass_type_skills},
}

misty_lake_creature_data = {
    "Squirtle": {"base_attack": 22, "base_defense": 18, "rarity": "rare", "skills": water_type_skills},
    "Magikarp": {"base_attack": 10, "base_defense": 10, "rarity": "normal", "skills": water_type_skills},
    "Vaporeon": {"base_attack": 24, "base_defense": 20, "rarity": "rare", "skills": water_type_skills},
    "Totodile": {"base_attack": 23, "base_defense": 17, "rarity": "rare", "skills": water_type_skills},
    "Mudkip": {"base_attack": 21, "base_defense": 19, "rarity": "rare", "skills": water_type_skills},
    "Lapras": {"base_attack": 25, "base_defense": 22, "rarity": "rare", "skills": water_type_skills},
    "Sobble": {"base_attack": 20, "base_defense": 16, "rarity": "normal", "skills": water_type_skills},
    "Gyarados": {"base_attack": 28, "base_defense": 22, "rarity": "epic", "skills": water_type_skills},
    "Blastoise": {"base_attack": 27, "base_defense": 23, "rarity": "epic", "skills": water_type_skills},
    "Lugia": {"base_attack": 33, "base_defense": 35, "rarity": "legendary", "skills": water_type_skills}
}

drystep_creature_data = {
    "Charmander": {"base_attack": 25, "base_defense": 10, "rarity": "normal", "skills": fire_type_skills},
    "Vulpix": {"base_attack": 20, "base_defense": 15, "rarity": "normal", "skills": fire_type_skills},
    "Cyndaquil": {"base_attack": 22, "base_defense": 12, "rarity": "normal", "skills": fire_type_skills},
    "Torchic": {"base_attack": 21, "base_defense": 11, "rarity": "normal", "skills": fire_type_skills},
    "Chimchar": {"base_attack": 23, "base_defense": 13, "rarity": "normal", "skills": fire_type_skills},
    "Litten": {"base_attack": 24, "base_defense": 14, "rarity": "normal", "skills": fire_type_skills},
    "Scorbunny": {"base_attack": 22, "base_defense": 12, "rarity": "normal", "skills": fire_type_skills},
    "Charizard": {"base_attack": 30, "base_defense": 25, "rarity": "epic", "skills": fire_type_skills},
    "Entei": {"base_attack": 35, "base_defense": 25, "rarity": "legendary", "skills": fire_type_skills},
    "Ho-Oh": {"base_attack": 32, "base_defense": 28, "rarity": "legendary", "skills": fire_type_skills}
}


# Create a Map instance with creature data
town_trainning_ground = Map("Town Training Ground", (1, 5), town_trainning_ground_creature_data)
shadowed_woodland = Map("Shadowed Woodland", (5, 10), shadowed_woodland_creature_data)
misty_lake = Map("Misty Lake", (10, 15), misty_lake_creature_data)
drystep = Map("Dry Step", (15, 20), drystep_creature_data)

def display_menu(options):
    print("Please use number to make a selection: ")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    print()

def main_game_loop():
    running = True
    while running:
        display_menu(["Start", "Quit"])
        choice = input("Choose an option: ")
        if choice.isdigit():
            choice = int(choice)
            if choice == 1:
                start_game()
            elif choice == 2:
                running = False
            else:
                print("Invalid choice. Please choose again.")
        else:
            print("Invalid input. Please enter a number.")

def start_game():
    print("Starting Pokemon YY version 0.1...")
    print("Welcome to the test adventure game refered to Pokemon! Are you ready to start your adventure to become the best creature trainer in the world? Let's find out")
    player_name = input("Enter your name: ")
    player = Player(player_name)
    print("Please choose your starter creature.")
    choose_starter(player)
    print(f"Hello, {player_name}! Let's begin the adventure.")
    main_game_menu(player)

def choose_starter(player):
    starters = [shadowed_woodland.generate_creature(starter=True) for _ in range(3)]
    display_menu(starters)
    choice = input("Please choose your starter  creature: ")
    if choice.isdigit():
        choice = int(choice)
        if 1 <= choice <= len(starters):
            player_starter = PlayerOwnedCreature(starters[choice - 1].name, 5, starters[choice - 1].rarity, starters[choice - 1].base_attack, starters[choice - 1].base_defense, starters[choice - 1].skills)
            print(f"You chose {starters[choice - 1].name}!")
            player.add_creature(player_starter)
        else:
            print("Invalid choice. Please choose again.")
    else:
        print("Invalid input. Please enter a number.")


def main_game_menu(player):
    while True:
        display_menu(["Explore", "Team of Creatures", "Pokemon Center", "Quit"])
        choice = input("Choose an option: ")
        if choice.isdigit():
            choice = int(choice)
            if choice == 1:
                explore(player)
            elif choice == 2:
                view_team(player)
            elif choice == 3:
                print("Welcome to the Pokemon Center!")
                heal_creatures(player)
            elif choice == 4:
                return  # Return to the previous menu
            else:
                print("Invalid choice. Please choose again.")
        else:
            print("Invalid input. Please enter a number.")

def explore(player):
    display_menu(["Town Traning Ground", "Shadowed Woodland", "Misty Lake", "Dry Step", "Back"])
    choice = input("Choose a location to explore: ")
    if choice.isdigit():
        choice = int(choice)
        if choice == 1:
            print("The Town Training Ground serves as a specialized arena for creature battles, offering a safe environment for leveling up before embarking on perilous wilderness explorations.")
            explore_location(town_trainning_ground, player)
        elif choice == 2:
            print("Shadowed Woodland is a verdant settlement nestled amidst ancient trees, known as the dwelling place of a diverse array of grass-type creatures.")
            explore_location(shadowed_woodland, player)
        elif choice == 3:
            print("Misty Lake is a serene water body teeming with aquatic life, serving as a haven for water-type creatures to thrive and flourish.Rumors whisper of legendary encounters within Misty Lake, with tales of the majestic Lugia occasionally gracing its tranquil waters. Though sightings are rare, the chance to encounter such a mythical creature adds an aura of mystery and excitement to the already enchanting atmosphere of the lake.")
            explore_location(misty_lake, player)
        elif choice == 4:
            print("Drystep, a fiery landscape forged from the aftermath of an epic clash between two legendary titans of fire, Entei and Ho-Oh. The remnants of their battle linger, as both creatures lie dormant, their slumber disrupted only by the faintest echoes of their past conflict. Rumors speak of their potential awakening, warning travelers of the unpredictable nature of these powerful entities and the imminent possibility of their return to consciousness. In the heart of Drystep, the legacy of their battle continues to shape the land, drawing adventurers seeking both danger and the allure of encountering these legendary guardians of fire.")
            explore_location(drystep, player)
        elif choice == 5:
            return  
        else:
            print("Invalid choice. Please choose again.")
    else:
        print("Invalid input. Please enter a number.")

def explore_location(location, player):
    print(f"Exploring {location.name}...")
    wild_creature = location.generate_creature()
    print(f"A wild {wild_creature.name} appeared! Level: {wild_creature.level}")
    player_creature = player.own_creatures[0]
    battle(player_creature, wild_creature)

def view_team(player):
    print("Viewing team of creatures...")
    player.display_creatures()
    
def battle(player_creature, enemy_creature):
    while player_creature.current_health > 0 and enemy_creature.current_health > 0:
        # Player's turn
        player_creature.use_skill(enemy_creature)
        if enemy_creature.current_health <= 0:
            print(f"You defeat a wild {enemy_creature.name}!")
            player_creature.current_EXP += enemy_creature.level * 50
            print(f"{player_creature.name} gained {enemy_creature.level * 50} EXP!")
            player_creature.check_level()
            break
        
        # Enemy's turn
        enemy_creature.use_skill(player_creature, is_player=False)
        if player_creature.current_health <= 0:
            print("You were defeated!")
            break

    player_creature.current_attack = player_creature.base_attack
    player_creature.current_defense = player_creature.base_defense

def heal_creatures(player):
    for creature in player.own_creatures:
        creature.current_health = creature.HP
        for skill in creature.skills:
            skill.usage_point = 10
    print("All creatures have been healed!")

# Main game loop
if __name__ == "__main__":
    main_game_loop()
    