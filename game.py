import random

# =========================
# DATA CLASSES
# =========================

class Item:
    def __init__(self, id, name, category, price, damage=0):
        self.id=id
        self.name=name
        self.category=category
        self.price=price
        self.damage=damage


class Player:
    def __init__(self,name):
        self.name=name
        self.money=1000
        self.hp=100
        self.inventory=[]
        self.weapon=None
        self.x=0
        self.y=0
        self.hotbar=[None]*5

    def buy(self,item):
        if self.money>=item.price:
            self.money-=item.price
            self.inventory.append(item)
            self.update_hotbar()
            print("Bought",item.name)
        else:
            print("Not enough money")

    def update_hotbar(self):
        weapons=[i for i in self.inventory if i.damage>0]
        for i in range(5):
            self.hotbar[i]=weapons[i] if i<len(weapons) else None

    def equip_hotbar(self,slot):
        if self.hotbar[slot]:
            self.weapon=self.hotbar[slot]
            print("Equipped",self.weapon.name)
        else:
            print("Empty slot")


# =========================
# WEAPONS
# =========================

guns=[

Item(1,"Derringer .22","Pistol",150,10),
Item(2,"Beretta M9","Pistol",350,18),
Item(3,"Glock 17","Pistol",500,25),
Item(4,"Desert Eagle","Pistol",900,45),

Item(10,"MP5","SMG",1200,40),
Item(11,"Vector","SMG",2000,55),
Item(12,"P90","SMG",2500,60),

Item(20,"AK-47","Rifle",1200,45),
Item(21,"M4A1","Rifle",1500,48),
Item(22,"SCAR-H","Rifle",2200,60),

Item(30,"Remington 870","Shotgun",600,50),
Item(31,"SPAS-12","Shotgun",1400,80),

Item(40,"Mosin Nagant","Sniper",400,70),
Item(41,"Dragunov","Sniper",1800,110),
Item(42,"Barrett M82","Sniper",5000,200),

Item(999,"Infinity Cannon","God",0,10**18)
]

# =========================
# KNIVES
# =========================

knives=[]
for i in range(1,21):
    knives.append(Item(200+i,f"Knife #{i}","Knife",100+i*10,5+i))


# =========================
# VEHICLES
# =========================

vehicles=[
Item(300,"F16 Fighter","Aircraft",1500000),
Item(301,"UH1 Huey","Helicopter",500000),
Item(302,"Jeep","Ground",15000),
Item(303,"Abrams Tank","Tank",5500000)
]


# =========================
# UTILITIES
# =========================

utilities=[
Item(400,"Frag Grenade","Utility",300),
Item(401,"Flashbang","Utility",250),
Item(402,"Medkit","Healing",1200),
Item(403,"Armor Plate","Defense",500)
]


# =========================
# ENEMIES
# =========================

class Enemy:
    def __init__(self,name,hp,reward):
        self.name=name
        self.hp=hp
        self.reward=reward


def spawn_enemy():

    r=random.random()

    if r<0.75:
        return Enemy("Robot",120,40)

    elif r<0.95:
        return Enemy("Zombie",220,120)

    else:
        return Enemy("Skeleton Boss",700,900)


# =========================
# WORLD
# =========================

WORLD_SIZE=20
world={}

for x in range(-WORLD_SIZE,WORLD_SIZE):
    for y in range(-WORLD_SIZE,WORLD_SIZE):

        r=random.random()

        if r<0.05:
            world[(x,y)]="Shop"

        elif r<0.10:
            world[(x,y)]="Hospital"

        elif r<0.15:
            world[(x,y)]="Treasure"

        else:
            world[(x,y)]="Wild"


# =========================
# SHOP
# =========================

def show_shop(items):

    for item in items:

        if item.damage:
            print(item.id,item.name,"$",item.price,"DMG",item.damage)
        else:
            print(item.id,item.name,"$",item.price)


def find_item(items,id):

    for item in items:
        if item.id==id:
            return item


# =========================
# MOVEMENT
# =========================

def move_player(player):

    print("WASD move | X exit | 1-5 equip")

    while True:

        print("Position:",player.x,player.y)

        loc=world.get((player.x,player.y),"Wild")
        print("Location:",loc)

        m=input("> ").lower()

        if m=="w": player.y+=1
        elif m=="s": player.y-=1
        elif m=="a": player.x-=1
        elif m=="d": player.x+=1
        elif m=="x": break

        elif m in ["1","2","3","4","5"]:
            player.equip_hotbar(int(m)-1)
            continue

        if loc=="Treasure":
            money=random.randint(50,200)
            player.money+=money
            print("You found treasure +$",money)

        if loc=="Hospital":
            player.hp=100
            print("Healed!")

        if random.random()<0.35:
            fight(player)


# =========================
# COMBAT
# =========================

def fight(player):

    enemy=spawn_enemy()

    print("Enemy:",enemy.name,"HP",enemy.hp)

    while enemy.hp>0 and player.hp>0:

        print("1 Attack")
        print("2 Run")

        c=input("> ")

        if c=="1":

            if player.weapon:
                dmg=player.weapon.damage+random.randint(-5,5)
            else:
                dmg=random.randint(1,5)

            enemy.hp-=dmg

            print("Damage:",dmg)

            if enemy.hp<=0:
                print("Enemy defeated")
                player.money+=enemy.reward
                return

            edmg=random.randint(8,18)
            player.hp-=edmg

            print("Enemy hit:",edmg)

        elif c=="2":
            return

    if player.hp<=0:
        print("GAME OVER")
        exit()


# =========================
# SECRET CODES
# =========================

def enter_code(player):

    code=input("Enter code > ")

    if code=="rich":
        player.money+=100000

    elif code=="heal":
        player.hp=999

    elif code=="arsenal":
        player.inventory.extend(guns)
        player.update_hotbar()

    elif code=="god":
        for g in guns:
            if g.id==999:
                player.weapon=g
                player.inventory.append(g)


# =========================
# GAME LOOP
# =========================

def game():

    name=input("Player name: ")
    player=Player(name)

    while True:

        print("\n1 Explore")
        print("2 Weapon Shop")
        print("3 Utility Shop")
        print("4 Vehicle Shop")
        print("5 Inventory")
        print("6 Stats")
        print("7 Enter Code")
        print("8 Quit")

        c=input("> ")

        if c=="1":
            move_player(player)

        elif c=="2":
            show_shop(guns)
            b=input("ID or x ")
            if b!="x":
                item=find_item(guns,int(b))
                if item: player.buy(item)

        elif c=="3":
            show_shop(utilities)
            b=input("ID or x ")
            if b!="x":
                item=find_item(utilities,int(b))
                if item: player.buy(item)

        elif c=="4":
            show_shop(vehicles)
            b=input("ID or x ")
            if b!="x":
                item=find_item(vehicles,int(b))
                if item: player.buy(item)

        elif c=="5":
            for i in player.inventory:
                print("-",i.name)

        elif c=="6":
            print("HP:",player.hp)
            print("Money:",player.money)
            print("Weapon:",player.weapon.name if player.weapon else "None")

        elif c=="7":
            enter_code(player)

        elif c=="8":
            break


game()