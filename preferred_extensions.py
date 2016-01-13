from enum import Enum

class Label(Enum):
    IN = 1
    OUT = 2
    UND = 3

class Vertex(object):
    def __init__(self, name):
        self.name = name
        self.attacks = []
        self.label = 'und'
        self.vocal = False

    def copy(self):
        ret = Vertex(self.name)
        ret.attacks = self.attacks.copy()
        ret.set_label(self.label)
        return ret

    def set_label(self, label):
        if self.vocal:
            print("Vertex", self.name, "set from", self.label, "to", label)
        self.label = label


def make_sets(graph):
    ins = [v.name for v in graph.vertices.values() if v.label=='in']
    outs = [v.name for v in graph.vertices.values() if v.label=='out']
    unds = [v.name for v in graph.vertices.values() if v.label=='und']
    return (set(ins), set(outs), set(unds))



class Graph(object):
    def __init__(self, vertex_names):
        self.vertices = {name : Vertex(name) for name in vertex_names}

    def copy(self):
        ret = Graph([])
        ret.vertices = {name : self.vertex(name).copy() for name in self.vertices}
        for v in ret.vertices.values():
            v.attacks=[]
        for v in self.vertices.values():
            for att in v.attacks:
                ret.add_attack(v.name, att.name)
        return ret

    def add_attack(self, a, b):
        self.vertices[a].attacks.append(self.vertices[b])

    def print_labels(self):
        pairs = [(v.name, v.label) for v in self.vertices.values()]
        pairs.sort()
        for name, label in pairs:
            print(name+": "+label)

    def vertex(self, name):
        return self.vertices[name]

    def attackers_of(self, name):
        return [v for v in self.vertices.values() if self.vertices[name] in v.attacks]

    def find_illegal(self):
        super_illegal = []
        illegal = []
        for v in [self.vertex(name) for name in self.vertices if self.vertex(name).label=='in']:
            if not all(att.label=='out' for att in self.attackers_of(v.name)):
                illegal.append(v)
        for v in illegal:
            if any((att.label in ['in', 'und'])and(att not in illegal) and (att not in super_illegal) for att in self.attackers_of(v.name)):
                super_illegal.append(v)
        illegal = [v for v in illegal if v not in super_illegal]
        return ([v.name for v in super_illegal], [v.name for v in illegal])

    def is_illegal_out(self, name):
        if self.vertex(name).label != 'out':
            return False
        attackers = self.attackers_of(name)
        return all(v.label!='in' for v in attackers)

    def shift(self, vertex_name):
        ver = self.vertex(vertex_name)
        ver.set_label('out')
        for v in [v for v in ver.attacks+[ver] if self.is_illegal_out(v.name)]:
            v.set_label('und')
        return self

    def find_pref(self):
        Cand = {'val':[]}
        graph = self.copy()
        for v in graph.vertices.values():
            v.label = 'in'
        def find_pref_rec(graph, level):
            print("Level", level)
            print("Doing graph",id(graph), ":")
            graph.print_labels()
            super_illegals, illegals = graph.find_illegal()
            print("Illegals:", illegals)
            print("Super illegals:", super_illegals)
            if len(super_illegals)+len(illegals) == 0:
                print ("No illegals")
                curr_ext = make_sets(graph)
                if any(ext[0]>=curr_ext[0] for ext in Cand['val']):
                    # a bigger or same extension exists already
                    print("Bigger or same extension exists, return")
                    return
                Cand['val'] = [ext for ext in Cand['val'] if not ext[0]<=curr_ext[0]]
                Cand['val'].append(curr_ext)
                print("Added to Cand, Cand is ", Cand['val'])
                return
            if len(super_illegals)>0:
                print("Choosing super illegal", super_illegals[0])
                find_pref_rec(graph.copy().shift(super_illegals[0]), level+1)
                print("Back to level", level)
            else:
                print("Going through illegals:", illegals)
                for name in illegals:
                    print("Choosing illegal", name)
                    find_pref_rec(graph.copy().shift(name), level+1)
                    print("Back to level", level)
                    if level==0:
                        print("Graph 0 id", id(graph), "is:")
                        graph.print_labels()

        find_pref_rec(graph, 0)
        return Cand



# names = ['a', 'b', 'c']
# g = Graph(names)
# g.add_attack('a','b')
# g.add_attack('b','c')
# for name in names:
#     g.vertex(name).label = 'in'
# #g.vertex('b').label = 'out'
# illegal = g.find_illegal()
# print(illegal)
# g2 = g.copy()
# print(g2.find_illegal())
# g.print_labels()
# g2.print_labels()
# print("G3")
# print([v.name for v in g.vertex('a').attacks])
# print([v.name for v in g.vertex('b').attacks])
# g.copy().shift('c').shift('b').print_labels()
names = ['a','b','c','d','e','f','g','h','i','j','k']
g = Graph(names)
g.add_attack('a', 'b')
g.add_attack('a', 'c')
g.add_attack('c', 'h')
g.add_attack('h', 'g')
g.add_attack('g', 'i')
g.add_attack('g', 'e')
g.add_attack('g', 'd')
g.add_attack('e', 'k')
g.add_attack('e', 'j')
g.add_attack('k', 'd')
g.add_attack('d', 'j')
g.add_attack('d', 'f')
g.add_attack('j', 'h')
g.add_attack('f', 'h')
g.add_attack('i', 'e')

cand = g.find_pref()
for ext in cand['val']:
    print(ext)
