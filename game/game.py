from random import shuffle
from copy import copy, deepcopy

from game.player import *
from tools.log import *



class Game():


    def __init__(self, nb_human = 1, nb_npc = 1, npc_mode = "random", stack_size = 20, min_pop = 1, max_pop = 3):

        self.stack = Stack(stack_size, min_pop, max_pop)

        self.humans = Human.creation(nb_human)
        self.npcs = NPC.creation(nb_npc, npc_mode)

        self.players = self.npcs + self.humans
        shuffle(self.players)

        self.current_player_index = 0

        self.ended = False
        self.started = False


    def copy(self):

        c = copy(self)
        c.stack = deepcopy(self.stack)

        return c


    def start(self):

        self.started = True
        Log.output("Game starts with {} players:".format(Player.count))
        Log.output("{} human player, {} computers."
                .format(Human.count, NPC.count))
        self.stack.print_init_status()
        Log.nl()


    def run(self):

        self.start()

        while not self.stack.empty():
            self.step()
            input()


    def step(self):

        while not self.current_player().play(self.stack):
            pass

        Log.output(str(self.stack))

        if self.stack.empty():
            self.end()

        else:
            self.to_next_player()
        
        return self


    def all_steps(self):

        steps = []

        for n in range(self.stack.min_pop, self.stack.max_pop + 1):
            c = self.copy()
            c.stack.pop(c.current_player(), n)
            Log.output(str(c.stack))

            if c.stack.empty():
                c.end()
            else:
                c.to_next_player()

            steps += [c]

        return steps
   
    
    def end(self):
        Log.output("The winner is {}\nCongratulations!".format(self.current_player()))
        self.ended = True


    def to_next_player(self):

        Log.nl()

        self.current_player_index += 1
        if self.current_player_index >= Player.count:
            self.current_player_index = 0


    def last_player(self):
        if self.current_player_index == 0:
            return self.players[Player.count - 1]
        else:
            return self.players[self.current_player_index - 1]


    def current_player(self):
        return self.players[self.current_player_index]


    def next_player(self):
        if self.current_player_index + 1 >= Player.count:
            return self.players[0]
        else:
            return self.players[self.current_player_index]


    def similar(self, game):

        if self.current_player() != game.current_player() or self.stack.size != game.stack.size:
                return False

        return True



class Stack():


    def __init__(self, size = 15, min_pop = 1, max_pop = 3):
        self.init_size = size
        self.size = size
        self.min_pop = min_pop
        self.max_pop = max_pop


    def __str__(self):

        if self.size == 0:
            return "Stack: empty.".format(self.size)

        elif self.size == 1:
            return "Stack: {} pill left.".format(self.size)

        else:
            return "Stack: {} pills left.".format(self.size)


    def empty(self):
        return self.size == 0


    def pop(self, player, n):

        if n <= self.max_pop and n >= self.min_pop:

            if n > self.size:
                self.size = 0
                Log.output("{} takes the last pill(s)."
                    .format(player))

            else:
                self.size -= n
                Log.output("{} takes {} pills."
                    .format(player, n))


            return True

        Log.output("You must take {} to {} pills"
            .format(self.min_pop, self.max_pop))

        return False


    def print_init_status(self):
        Log.output("The stack starts with {} pills."
                .format(self.init_size))


