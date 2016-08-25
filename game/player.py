from random import randint, choice

from tools.log import *

class Player():

    count = 0

    def __init__(self, name):

        self.name = name
        Player.count += 1
        self.index = Player.count

    def play(self, stack):

        Log.output("{} plays.".format(self))

        n = self.choose_number(stack)
        return stack.pop(self, n)

    def __str__(self):
        return "({}) {}".format(self.index, self.name)


class Human(Player):
    
    count = 0

    def __init__(self, name):
        super().__init__(name)
        Human.count += 1

    @staticmethod
    def creation(n):

        if n > 0:
            Log.output("Human players creation:")
            Log.tab()
            humans = [Human.create_from_input() for i in range(n)]
            Log.untab()
            Log.nl()

        else:
            humans = []

        return humans


    @staticmethod
    def create_from_input():
        name = Log.input("({}) ".format(Player.count + 1))

        return Human(name)

    def choose_number(self, stack):

        # Sanitize player's input
        n = Log.input("How many pills to take [{from}-{to}]: "
            .format(**{ "from": stack.min_pop,
                        "to": stack.max_pop}))

        return int(n)


class NPC(Player):

    count = 0
    modes = ["random"]

    def __init__(self, name, mode):
        super().__init__(name)
        NPC.count += 1

        if mode not in NPC.modes:
            raise ValueError("NPC mode not recognized (\"{}\")".format(mode))
        self.mode = mode

    def __str__(self):
        return "{}.{}".format(super().__str__(), self.mode)

    @staticmethod
    def creation(n, mode):

        npcs = []

        if n > 0:

            with open("resources/dwarf-names.txt", "r") as f:
                names = f.read().splitlines()

            Log.output("NPC players creation:")
            Log.tab()

            for i in range(n):

                npc = NPC(choice(names), mode)
                npcs += [npc]
                Log.output(str(npc))

            Log.untab()
            Log.nl()

        return npcs

    def choose_number(self, stack):

        if self.mode == "random":
            n = self.random_choice(stack)

        return n

    def random_choice(self, stack):

        n = randint(stack.min_pop, stack.max_pop)
        return n

