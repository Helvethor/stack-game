from code import interact
from random import random
from graph_tool.all import *


from tools.log import *


class Grapher():
    
    colors = []

    def __init__(self, game):

        self.init_game = game
        

    def one_path(self):

        game = self.init_game.copy()

        graph = Graph()
        v_map = graph.new_vertex_property("object")

        current_v = graph.add_vertex()
        v_map[current_v] = game

        while not v_map[current_v].ended:
            
            last_v = current_v
            current_v = graph.add_vertex()
            graph.add_edge(last_v, current_v)

            v_map[current_v] = v_map[last_v].copy().step()

        graph.vertex_properties["states"] = v_map

        return graph


    def all_paths(self):

        Log.mute()
        game = self.init_game.copy()
        game.start()
        age = 1

        g = Graph()
        g.vp.game = g.new_vertex_property("object")
        g.vp.age = g.new_vertex_property("int")

        v = g.add_vertex()
        g.vp.game[v] = game
        g.vp.age[v] = age

        all_ended = g.vp.game[v].ended
        current_vertices = [v]

        while not all_ended:
            all_ended = True
            age += 1

            new_vertices = []
            for v in current_vertices:

                game = g.vp.game[v]

                if game.ended:
                    continue
                all_ended = False

                new_games = game.all_steps()

                for new_game in new_games:

                    similar_v = Grapher.find_similar_game(g, new_game)
                    if similar_v:
                        g.add_edge(v, similar_v)
                        continue

                    nv = g.add_vertex()
                    g.add_edge(v, nv)
                    g.vp.game[nv] = new_game
                    g.vp.age[nv] = age
                    new_vertices += [nv]

            current_vertices = new_vertices[:]

        remove_parallel_edges(g)

        return g


    @staticmethod
    def find_similar_game(graph, game):

        for v in graph.vertices():

            vg = graph.vp.game[v]

            if game.similar(vg):
                return v

        return False


    @staticmethod
    def interactive_window(g):
 
        stack_map = g.new_vertex_property("int")
        for v in g.vertices():
            stack = g.vp.game[v].stack.size
            stack_map[v] = stack
        
        pos = radial_tree_layout(g, g.vertex(0), stack_map)
        interactive_window(g, pos=pos, async=True)

    @staticmethod
    def draw_pdf(g, file_name="graph"):

        stack_map = g.new_vertex_property("string")
        player_map = g.new_vertex_property("vector<float>")

        for v in g.vertices():

            stack = str(g.vp.game[v].stack.size)
            stack_map[v] = stack

            color = Grapher.indexed_color(g.vp.game[v].current_player_index)
            player_map[v] = color
        
        pos = radial_tree_layout(g, root=g.vertex(0))
        graph_draw(g, pos=pos, output="output/" + file_name, vertex_text=stack_map, vertex_fill_color=player_map)


    @staticmethod
    def indexed_color(i):
        while len(Grapher.colors) <= i:
            Grapher.colors += [[random(), random(), random(), 0.5]] 

        return Grapher.colors[i]
