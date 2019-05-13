## ***************************************************
## Shivesh Malhotra 
## Python Project: TextWorldAdventure
## ***************************************************


class Thing:
    '''Fields: id (Nat),
               name (Str),
               description (Str)
    '''
    
    def __init__(self, id):
        self.id = id
        self.name = '???'
        self.description = ''
        
    def __repr__(self):
        return '<thing #{0}: {1}>'.format(self.id, self.name)
        
    def look(self):
        print(self.name)
        print(self.description)
        
class Player:
    '''Fields: id (Nat),
               name (Str), 
               description (Str),
               location (Room),
               inventory ((listof Thing))
    '''
    
    def __init__(self, id):
        self.id = id
        self.name = '???'
        self.description = ''
        self.location = None
        self.inventory = []
        
    def __repr__(self):
        return '<player #{0}: {1}>'.format(self.id, self.name)
        
    def look(self):
        print(self.name)
        print(self.description)
        if len(self.inventory) != 0:
            print('Carrying: {0}.'.format(
                ', '.join(map(lambda x: x.name,self.inventory))))
 
class Room:
    '''Fields: id (Nat),
               name (Str), 
               description (Str),
               contents ((listof Thing)),
               exits ((listof Exit))
    '''    
    
    def __init__(self, id):
        self.id = id
        self.name = '???'
        self.description = ''
        self.contents = []
        self.exits = []
        
    def __repr__(self):
        return '<room {0}: {1}>'.format(self.id, self.name)
        
    def look(self):
        print(self.name)
        print(self.description)
        if len(self.contents) != 0:
            print('Contents: {0}.'.format(
                ', '.join(map(lambda x: x.name, self.contents))))
        if len(self.exits) != 0:
            print('Exits: {0}.'.format(
                ', '.join(map(lambda x: x.name, self.exits)))) 
 
class Exit:
    '''Fields: name (Str), 
               destination (Room)
               key (Thing)
               message (Str)
    '''       
    
    def __init__(self,name,dest):
        self.name = name
        self.destination = dest
        self.key = None
        self.message = ""
        
    def __repr__(self):
        return '<exit {0}>'.format(self.name)


class World:
    '''Fields: rooms ((listof Room)), 
               player (Player)
    '''       
    
    msg_look_fail = "You don't see that here."
    msg_no_inventory = "You aren't carrying anything."
    msg_take_succ = "Taken."
    msg_take_fail = "You can't take that."
    msg_drop_succ = "Dropped."
    msg_drop_fail = "You aren't carrying that."
    msg_go_fail = "You can't go that way."
        
    msg_quit = "Goodbye."
    msg_verb_fail = "I don't understand that."    
    
    def __init__(self, rooms, player):
        self.rooms = rooms
        self.player = player

    def look(self, noun):
        '''
        returns none and accepts noun argument which the user wants to 
        look at and prints the name and the description of the passed-in noun.
        Looks at the player or location if noun is "me" or "here" correspondingly.
        Effects: prints name and description of the passed-in noun. 
        
        look: World Str -> None
        '''
        if noun == "me":
            self.player.look()
        elif noun == "here":
            self.player.location.look()
        elif noun in list(map(lambda z: z.name ,self.player.inventory)):
            for item in self.player.inventory:
                if item.name == noun:
                    item.look()
        elif noun in list(map(lambda z: z.name, self.player.location.contents)):
            for item in self.player.location.contents:
                if item.name == noun:
                    item.look()
        else:
            print(self.msg_look_fail)
            
            
    def inventory(self):
        '''
        returns none and takes in no argument other than self. Prints the 
        formatted list of the names of the things that the player is carrying, 
        otherwise prints "You aren’t carrying anything."
        Effects: prints the formatted list of the names of the things that the 
                 player is carrying.
                 Prints "You aren’t carrying anything." otherwise
        
        inventory: World -> None
        '''
        if self.player.inventory != []:
            count = 0
            print("Inventory: ", end = "")
            while count <= len(self.player.inventory) - 1:
                if count == len(self.player.inventory) - 1:
                    print(self.player.inventory[count].name)
                    count += 1
                else:
                    print(self.player.inventory[count].name, end = ", ")
                    count += 1
        else:
            print(self.msg_no_inventory)
            
    def take(self, noun):
        '''
        returns none and takes in noun(name of thing) argument. Prints "Taken" 
        if the thing is present in the player's current location and mutates 
        the World, otherwise prints "You can’t take that.".
        Effects: prints "Taken" if thing is present and mutates the World 
                 prints "You can’t take that." otherwise
        
        take: World Str -> None
        '''
        if noun in list(map(lambda z: z.name, self.player.location.contents)):
            for item in self.player.location.contents:
                if noun == item.name:
                    self.player.location.contents.remove(item)
                    self.player.inventory.append(item)
                    print(self.msg_take_succ) 
        else:
            print(self.msg_take_fail)
            
            
    def drop(self, noun):
        '''
        returns none and takes in noun(name of thing) argument. Prints "Dropped" 
        if the thing is present in the player's inventory and mutates 
        the player's inventory, otherwise prints "You aren’t carrying that.".
        Effects: prints "dropped" if thing is present and mutates the player's inventory 
                 prints "You aren’t carrying that." otherwise
        
        drop: World Str -> None
        '''
        if noun in list(map(lambda z: z.name, self.player.inventory)):
            for item in self.player.inventory:
                if noun == item.name:
                    self.player.inventory.remove(item)
                    self.player.location.contents.append(item)
                    print(self.msg_drop_succ)
        else:
            print(self.msg_drop_fail)
            
        
    def go(self, noun):
        '''
        returns none and takes in noun argument(name of the exit). If noun 
        corresponds to the one of the room's exit and doesn't have a key then 
        function mutates the player's location, otherwise prints "You can’t go 
        that way." If exit has the key then player must have it to exit, otherwise
        print exit's message.
        Effects: mutates the World if player is successful to exit
                 prints "You can’t go that way." if noun doesn't correspond to room's
                 exit
                 prints exit's message if exit has the key and player doesn't
        
        go: World Str -> None 
        '''
        if noun in list(map(lambda x: x.name, self.player.location.exits)):
            for items in self.player.location.exits:
                if items.key == None:
                    if noun == items.name:
                        self.player.location = items.destination
                        items.destination.look() 
                else:
                    if noun == items.name:
                        if items.key in self.player.inventory:
                            self.player.location = items.destination
                            items.destination.look()
                        else:
                            print(items.message)              
        else:
            print(self.msg_go_fail)
                
      
       
    def play(self):
        player = self.player
        
        player.location.look()
        
        while True:
            line = input( "- " )
            
            wds = line.split()
            verb = wds[0]
            noun = ' '.join( wds[1:] )
            
            if verb == 'quit':
                print( self.msg_quit )
                return
            elif verb == 'look':
                if len(noun) > 0:
                    self.look(noun)  
                else:
                    self.look('here')
            elif verb == 'inventory':
                self.inventory()     
            elif verb == 'take':
                self.take(noun)    
            elif verb == 'drop':
                self.drop(noun)
            elif verb == 'go':
                self.go(noun)   
            else:
                print(self.msg_verb_fail)
                
                
    def save(self, fname):
        '''
        returns none and takes in fname(Str) other than self as an argument. 
        Function writes the complete current state of the World in the textfile fname.
        Effects: current state of the World is written in the 
                 text file fname
        
        save: World Str -> None
        '''
        f = open(fname, "w")
        for items in self.player.inventory:
            f.write("thing #{0} {1}\n".format(items.id, items.name))
            f.write("{0}\n".format(items.description))
        for items in self.rooms:
            for t in items.contents:
                f.write("thing #{0} {1}\n".format(t.id, t.name))
                f.write("{0}\n".format(t.description))        
        for items in self.rooms:
            f.write("room #{0} {1}\n".format(items.id, items.name))
            f.write("{0}\n".format(items.description))
            a = list(map(lambda x: "#" + str(x.id), items.contents))
            b = " ".join(a)
            f.write("contents" + " {0}\n".format(b))
        f.write("player #{0} {1}\n".format(self.player.id, self.player.name))
        f.write("{0}\n".format(self.player.description))
        c = list(map(lambda x: "#" + str(x.id), self.player.inventory))
        d = " ".join(c)
        f.write("inventory" + " {0}\n".format(d))
        f.write("location #{0}\n".format(self.player.location.id))
        for items in self.rooms:
            for ex in items.exits:
                if ex.key == None:    
                    f.write("exit #{0} #{1} {2}\n".format(items.id, ex.destination.id, ex.name))
                else:
                    f.write("keyexit #{0} #{1} {2}\n".format(items.id, ex.destination.id, ex.name))
                    f.write("#{0} {1}\n".format(ex.key.id, ex.message))       
        f.close()  
            

def load(fname):
    '''
    returns a complete new World after reading information from the textfile fname
    (Str).
    load: Str -> World
    
    '''
    ww = open(fname, "r")
    next_line_str = ww.readline()
    ret = {}
    rooms_list = []
    player = Player(id)
    while next_line_str != '':
        split_list = next_line_str.split()
        if "thing" in split_list[0]:
            method = Thing(int(split_list[1][1:]))
            method.name = " ".join(split_list[2:])
            method.description = ww.readline().strip()
            ret[method.id] = method 
        elif 'room' in split_list[0]:
            method = Room(int(split_list[1][1:]))
            method.name = " ".join(split_list[2:])
            method.description = ww.readline().strip()
            next_line_str = ww.readline()
            content_list = next_line_str.split()
            if len(content_list) >= 2:
                i = 1 
                while i < len(content_list):
                    intnum = int(content_list[i][1:])
                    for item in ret:
                        if item == intnum:
                            method.contents.append(ret[item])
                    i += 1
            ret[method.id] = method 
            rooms_list.append(method)
        elif 'player' in split_list[0]:
            method = Player(int(split_list[1][1:]))
            method.name = " ".join(split_list[2:])
            method.description = ww.readline().strip()
            next_line_str = ww.readline()
            inventory_list = next_line_str.split()
            if len(inventory_list) >= 2:
                i = 1 
                while i < len(inventory_list):
                    intnum = int(inventory_list[i][1:])
                    for item in ret:
                        if item == intnum:
                            method.inventory.append(ret[item])
                    i += 1
            next_line_str = ww.readline()
            location_list = next_line_str.split()
            for item in ret:
                if int(location_list[1][1:]) == item:
                    method.location = (ret[item])
            ret[method.id] = method 
            player = method
        elif 'keyexit' == split_list[0]:
                    exit_list = next_line_str.split()
                    next_line_str = ww.readline()
                    exit_list2 = next_line_str.split()
                    method = Exit(' '.join(exit_list[3:]),ret[int(exit_list[2][1:])]) 
                    method.key = ret[int(exit_list2[0][1:])]
                    method.message = " ".join(exit_list2[1:])
                    for item in list(ret.keys()):
                        if int(exit_list[1][1:]) == item:
                            ret[item].exits.append(method)          
        elif 'exit' in split_list[0]:
            exit_list = next_line_str.split()
            method = Exit(' '.join(exit_list[3:]),ret[int(exit_list[2][1:])])
            for item in list(ret.keys()):
                if int(exit_list[1][1:]) == item:
                    ret[item].exits.append(method)
        next_line_str = ww.readline()
    new_World = World(rooms_list,player)
    return new_World 
    
                
def makeTestWorld(usekey):
    wallet = Thing(1)
    wallet.name = 'wallet'
    wallet.description = 'A black leather wallet containing a WatCard.'
    
    keys = Thing(2)
    keys.name = 'keys'
    keys.description = 'A metal keyring holding a number of office and home keys.'
    
    phone = Thing(3)
    phone.name = 'phone'
    phone.description = 'A late-model smartphone in a Hello Kitty protective case.'
    
    coffee = Thing(4)
    coffee.name = 'cup of coffee'
    coffee.description = 'A steaming cup of black coffee.'
    
    hallway = Room(5)
    hallway.name = 'Hallway'
    hallway.description = 'You are in the hallway of a university building. \
Students are coming and going every which way.'
    
    c_and_d = Room(6)
    c_and_d.name = 'Coffee Shop'
    c_and_d.description = 'You are in the student-run coffee shop. Your mouth \
waters as you scan the room, seeing many fine foodstuffs available for purchase.'
    
    classroom = Room(7)
    classroom.name = 'Classroom'
    classroom.description = 'You are in a nondescript university classroom. \
Students sit in rows at tables, pointedly ignoring the professor, who\'s \
shouting and waving his arms about at the front of the room.'
    
    player = Player(8)
    player.name = 'Stu Dent'
    player.description = 'Stu Dent is an undergraduate Math student at the \
University of Waterloo, who is excelling at this studies despite the fact that \
his name is a terrible pun.'
    
    c_and_d.contents.append(coffee)
    player.inventory.extend([wallet,keys,phone])
    player.location = hallway
    
    hallway.exits.append(Exit('shop', c_and_d))
    ex = Exit('west', classroom)
    if usekey:
        ex.key = coffee
        ex.message = 'On second thought, it might be better to grab a \
cup of coffee before heading to class.'
    hallway.exits.append(ex)
    c_and_d.exits.append(Exit('hall', hallway))
    classroom.exits.append(Exit('hall', hallway))
    
    return World([hallway,c_and_d,classroom], player)

testWorld = makeTestWorld(False)
testWorld_key = makeTestWorld(True)
                

    


   





