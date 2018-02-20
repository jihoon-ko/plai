class Value:
    def __init__(self, arg):
        self.name = None
        self.arg = arg
    
    def __repr__(self):
        return "(%s %s)" % (self.name, " ".join(list(map(str, self.arg))))


class numV(Value):
    def __init__(self, arg):
        super(numV, self).__init__(arg)
        self.name = "numV"

    def __add__(self, other):
        return numV([self.arg[0] + other.arg[0]])

    def __sub__(self, other):
        return numV([self.arg[0] - other.arg[0]])


class closureV(Value):
    def __init__(self, arg):
        super(closureV, self).__init__(arg)
        self.name = "closureV"

