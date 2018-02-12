from defrdsub import *

class f:
    def __init__(self, arg):
        self.name = None
        self.arg = arg

    def __repr__(self):
        return "(%s %s)" % (self.name, " ".join(list(map(str, self.arg))))

    def interp(self, **kwargs):
        raise NotImplementedError

    def subst(self, sym, val):
        raise NotImplementedError


class f_num(f):
    def __init__(self, arg):
        super(f_num, self).__init__(arg)
        self.name = "num"

    def interp(self, **kwargs):
        return self.arg[0]

    def subst(self, sym, val):
        return self


class f_add(f):
    def __init__(self, arg):
        super(f_add, self).__init__(arg)
        self.name = "add"

    def interp(self, **kwargs):
        return self.arg[0].interp(**kwargs)\
               + self.arg[1].interp(**kwargs)

    def subst(self, sym, val):
        return f_add([self.arg[0].subst(sym, val),
                      self.arg[1].subst(sym, val)])


class f_sub(f):
    def __init__(self, arg):
        super(f_sub, self).__init__(arg)
        self.name = "sub"

    def interp(self, **kwargs):
        return self.arg[0].interp(**kwargs)\
               - self.arg[1].interp(**kwargs)

    def subst(self, sym, val):
        return f_sub([self.arg[0].subst(sym, val),
                      self.arg[1].subst(sym, val)])


class f_with(f):
    def __init__(self, arg):
        super(f_with, self).__init__(arg)
        self.name = "with"

    def interp(self, **kwargs):
        # Method using subst
        # return self.arg[2].subst(self.arg[0],
        #                          self.arg[1].interp(**kwargs)).interp(**kwargs)

        # Method using DefrdSub
        newSub = {}
        for k, v in kwargs.items(): newSub[k] = v
        newSub['defrdSub'] = ASub([self.arg[0], self.arg[1].interp(**kwargs), kwargs['defrdSub']])
        return self.arg[2].interp(**newSub)

    def subst(self, sym, val):
        if sym == self.arg[0]:
            return f_with([self.arg[0],
                           self.arg[1].subst(sym, val),
                           self.arg[2]])
        else:
            return f_with([self.arg[0],
                           self.arg[1].subst(sym, val),
                           self.arg[2].subst(sym, val)])


class f_id(f):
    def __init__(self, arg):
        super(f_id, self).__init__(arg)
        self.name = "id"

    def interp(self, **kwargs):
        lookup_result = kwargs['defrdSub'].lookup(self.arg[0])
        if lookup_result is None:
            raise RuntimeError("error: free identifier " + self.arg[0])
        else:
            return lookup_result

    def subst(self, sym, val):
        if sym == self.arg[0]:
            return f_num([val])
        else:
            return self


class f_app(f):
    def __init__(self, arg):
        super(f_app, self).__init__(arg)
        self.name = "app"

    def interp(self, **kwargs):
        for fd in kwargs.get('fds', []):
            if fd.arg[0] == self.arg[0]:
                newSub = {}
                for k, v in kwargs.items(): newSub[k] = v
                newSub['defrdSub'] = ASub([fd.arg[1],
                                           self.arg[1].interp(**kwargs),
                                           MtSub([])])
                return fd.arg[2].interp(**newSub)

        raise RuntimeError("cannot find function")

    def subst(self, sym, val):
        return f_app([self.arg[0], self.arg[1].subst(sym, val)])
