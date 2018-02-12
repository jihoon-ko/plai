class FunDef:
    def __init__(self, arg):
        self.name = "deffun"
        self.arg = arg

    def __repr__(self):
        return "(%s %s)" % (self.name, " ".join(list(map(str, self.arg))))