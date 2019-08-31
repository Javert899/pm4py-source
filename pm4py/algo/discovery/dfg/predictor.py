import math

class DFGPredictor(object):
    def __init__(self, dfg):
        self.dfg = dfg
        self.activities = set(x[0] for x in dfg).union(x[1] for x in dfg)
        self.AA = {}
        self.A = {}
        self.DD = {}
        self.D = {}

        self.initialize_A()
        self.initialize_AA()
        self.initialize_D()
        self.initialize_DD()

        self.current_relations = self.evaluate_all_relations()
        self.other_relations = self.possible_other_relations()
        self.normalize()

    def initialize_A(self):
        for a in self.activities:
            self.A[a] = set(x[0] for x in self.dfg if x[1] == a)

    def initialize_AA(self):
        for a in self.activities:
            self.AA[a] = set(y[0] for x in self.dfg if x[1] == a for y in self.dfg if y[1] == x[0])

    def initialize_D(self):
        for a in self.activities:
            self.D[a] = set(x[1] for x in self.dfg if x[0] == a)

    def initialize_DD(self):
        for a in self.activities:
            self.DD[a] = set(y[1] for x in self.dfg if x[0] == a for y in self.dfg if y[0] == x[1])

    def calculate_similarity(self, x,  y):
        if (x, y) in self.dfg:
            return 1.0
        elif x not in self.activities or y not in self.activities:
            return 0.0
        return self.calculate_similarity_0(x, y)

    def calculate_similarity_0(self, x, y, k=1.0/math.sqrt(3.0), defv=1.0/6.0):
        val1 = self.sim_A(x, y, k=k, defv=defv)
        val2 = self.sim_AA(x, y, k=k, defv=defv)
        val3 = self.sim_D(x, y, k=k, defv=defv)
        val4 = self.sim_DD(x, y, k=k, defv=defv)

        return (val1 + val2 + val3 + val4)/4.0

    def sim_A(self, x, y, k=1.0/math.sqrt(3.0), defv=1.0/6.0):
        if self.A[x]:
            num = self.A[x].intersection(self.A[y])
            v1 = len(num)/len(self.A[x])
            v2 = 1.0/(k * len(self.A[x]))
            return max(0.0, v1 - v2)
        return defv

    def sim_AA(self, x, y, k=1.0/math.sqrt(3.0), defv=1.0/6.0):
        if self.A[x] and self.AA[y]:
            num = self.A[x].intersection(self.AA[y])
            v1 = len(num)/len(self.A[x])
            v2 = 1.0/(k * len(self.A[x]))
            return max(0.0, v1 - v2)
        return defv

    def sim_D(self, x, y, k=1.0/math.sqrt(3.0), defv=1.0/6.0):
        if self.D[x]:
            num = self.D[x].intersection(self.D[y])
            v1 = len(num)/len(self.D[x])
            v2 = 1.0/(k * len(self.D[x]))
            return max(0.0, v1 - v2)
        return defv

    def sim_DD(self, x, y, k=math.sqrt(3), defv=1.0/6.0):
        if self.D[y] and self.DD[x]:
            num = self.D[y].intersection(self.DD[x])
            v1 = len(num)/len(self.DD[x])
            v2 = 1.0/(k * len(self.DD[x]))
            return max(0.0, v1 - v2)
        return defv

    def evaluate_all_relations(self):
        relations = []
        for (x, y) in self.dfg:
            relations.append([x, y, self.calculate_similarity_0(x, y)])
        relations = sorted(relations, key=lambda x: x[2])
        return relations

    def possible_other_relations(self):
        relations = []
        for x in self.activities:
            for y in self.activities:
                if (x, y) not in self.dfg and not x == y:
                    z = self.calculate_similarity_0(x, y)
                    if z > 0:
                        relations.append([x, y, z])
        red_relations = {(x, y) for (x, y, z) in relations}
        red_relations = {(x, y) for (x, y) in red_relations if (y, x) not in red_relations}
        relations = [[x, y, z] for [x, y, z] in relations if (x, y) in red_relations]
        relations = sorted(relations, key=lambda x: x[2], reverse=True)
        return relations

    def normalize(self):
        max_value = max(x[2] for x in self.current_relations)
        if max_value > 0:
            for i in range(len(self.current_relations)):
                self.current_relations[i][2] = self.current_relations[i][2] / max_value
            for i in range(len(self.other_relations)):
                self.other_relations[i][2] = self.other_relations[i][2] / max_value
