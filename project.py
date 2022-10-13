
import random

class Character:
  def __init__(self):
    self.name = ""
    self.health = 1
    self.health_max = 1
  def do_damage(self, monster):
    damage = min(
        max(random.randint(0, self.health) - random.randint(0, monster.health), 0),
        monster.health)
    monster.health = monster.health - damage
    if damage == 0:
		print "%s evades %s's attack." % (monster.name, self.name)
    else:
		print "%s hurts %s!" % (self.name, monster.name)
    return monster.health <= 0

class Monster(Character):
  def __init__(self, player):
    Character.__init__(self)
    self.name = 'a dragon'
    self.health = random.randint(1, player.health)

class Player(Character):
  def __init__(self):
    Character.__init__(self)
    self.state = 'normal'
    self.health = 10
    self.health_max = 10
  def quit(self):
    print "%s can't find the way back home, and dies of starvation.\nR.I.P." % self.name
    self.health = 0
  def help(self):
	  print Commands.keys()
  def status(self):
	  print "%s's health: %d/%d" % (self.name, self.health, self.health_max)
  def tired(self):
    print "%s is exhausted." % self.name
    self.health = max(1, self.health - 1)
  def rest(self):
    if self.state != 'normal':
		print "%s can't rest now!" % self.name; self.monster_fights()
    else:
      print "%s rests." % self.name
      if random.randint(0, 1):
        self.monster = Monster(self)
        print "%s is rudely awakened by %s!" % (self.name, self.monster.name)
        self.state = 'fight'
        self.monster_fights()
      else:
        if self.health < self.health_max:
          self.health = self.health + 1
        else:
			print "%s overslept." % self.name; self.health = self.health - 1
  def explore(self):
    if self.state != 'normal':
      print "%s is too busy right now!" % self.name
      self.monster_fights()
    else:
      print "%s explores an ominous cave." % self.name
      if random.randint(0, 1):
        self.monster = Monster(self)
        print "%s comes across %s!" % (self.name, self.monster.name)
        self.state = 'fight'
      else:
        if random.randint(0, 1): self.tired()
  def flee(self):
    if self.state != 'fight':
		print "%s runs around in circles for a while." % self.name; self.tired()
    else:
      if random.randint(1, self.health + 5) > random.randint(1, self.monster.health):
        print "%s runs away from %s." % (self.name, self.monster.name)
        self.monster = None
        self.state = 'normal'
      else: print "%s couldn't escape from %s!" % (self.name, self.monster.name); self.monster_fights()
  def fight(self):
    if self.state != 'fight':
		print "%s swats the air, with no notable results." % self.name; self.tired()
    else:
      if self.do_damage(self.monster):
        print "%s slays %s!" % (self.name, self.monster.name)
        self.monster = None
        self.state = 'normal'
        if random.randint(0, self.health) < 10:
          self.health = self.health + 1
          self.health_max = self.health_max + 1
          print "%s feels invincible!" % self.name
      else:
		  self.monster_fights()
  def monster_fights(self):
    if self.monster.do_damage(self):
		print "%s was devoured by %s!!!\nR.I.P." %(self.name, self.monster.name)

Commands = {
  'quit': Player.quit,
  'help': Player.help,
  'status': Player.status,
  'rest': Player.rest,
  'explore': Player.explore,
  'flee': Player.flee,
  'attack': Player.fight,
  }

def main():
	p = Player()
	p.name = raw_input("What is your character's name? ")
	print "(type help to get a list of actions)\n"
	print "%s enters a dark cave, searching for adventure." % p.name

	while(p.health > 0):
		line = raw_input("> ")
		args = line.split()
		if len(args) > 0:
			commandFound = False
		for c in Commands.keys():
			if args[0] == c[:len(args[0])]:
				Commands[c](p)
				commandFound = True
				break
		if not commandFound:
			print "%s try a different command." % p.name

if __name__ == "__main__":
	main()
