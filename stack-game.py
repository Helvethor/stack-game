#!/usr/bin/python3


import sys


from game.game import Game
from graph.graph import Grapher


class Main():


    def __init__(self, argv):
        self.argv = argv
        self.name = argv[0]


    def run(self):

        if len(self.argv) == 1:
            self.help()
            return

        command = self.argv[1]

        if command == "play":
            self.game = Game(0, 10, "random", 20)
            self.game.run()

        elif command == "graph":
            nb_npc = int(self.argv[2])
            stack_size = int(self.argv[3])
            min_pop = int(self.argv[4])
            max_pop = int(self.argv[5])

            self.game = Game(0, nb_npc, "random", stack_size, min_pop, max_pop)
            self.grapher = Grapher(self.game)
            self.graph = self.grapher.all_paths()

            file_name = str(nb_npc) + "." + str(stack_size) + "." + str(min_pop) + "." + str(max_pop) + ".pdf"
            Grapher.draw_pdf(self.graph, file_name)


    def help(self):
        print(  "Stack Game\n"
                "Two-players game where you have to remove a number (within a range) of pills from a stack."
                "\nThe player who empties the stack wins.\n"
                "\n"
                "Usage:\n"
                "\t{name} play (--random|--ia)\n"
                "\t{name} graph <stack_size>\n"
                "\n"
                "Options:\n"
                "\t-r, --random\tRandom decisions are made\n"
                "\t-i, --ia\t\tStatistical IA takes decisions\n"
                "\n"
                "Author:\n"
                "\tName:\tVincent Pasquier\n"
                "\tEmail:\tvincentpasquier@posteo.net\n"
                "\tGitHub:\tHelvethor\n"
                .format(**{"name": self.name}))



if __name__ == "__main__":

    main = Main(sys.argv)
    main.run()
