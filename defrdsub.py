class DefrdSub:
    def __init__(self, arg):
        self.name = None
        self.arg = arg

    def __repr__(self):
        return "(%s %s)" % (self.name, " ".join(list(map(str, self.arg))))

    def lookup(self, sym):
        raise NotImplementedError


class MtSub(DefrdSub):
    def __init__(self, arg):
        super(MtSub, self).__init__(arg)
        self.name = "mtSub"

    def __repr__(self):
        return "(mtSub)"

    def lookup(self, sym):
        return None


class ASub(DefrdSub):
    def __init__(self, arg):
        super(ASub, self).__init__(arg)
        self.name = "aSub"

    def lookup(self, sym):
        if self.arg[0] == sym:
            return self.arg[1]
        else:
            return self.arg[2].lookup(sym)