# S   -> NP VP
# VP  -> V NP | V NP PP
# PP  -> P NP
# V   -> END
# NP  -> END | Det N | Det N PP
# Det -> END
# N   -> END
# P   -> END

class verifyCFG(object):

    def __init__(self, dev=False):
        super(verifyCFG, self).__init__()
        self.dev = dev

    def verify(self, tags):
        self.tags = tags
        self.i = 0
        print self.S()

    def S(self):
        if self.dev: print "S"
        return ( self.NP(), self.VP() ) == ( True, True ) and self.i == len(self.tags)

    def VP(self):
        if self.dev: print "VP"
        part = ( self.V(), self.NP() ) == ( True, True )
        # Even if V NP, may need to check V NP PP
        if self.i == len(self.tags):
            return part
        elif part:
            return self.PP() == True
        else:
            return False

    def PP(self):
        if self.dev: print "PP"
        return ( self.P(), self.NP() ) == ( True, True )

    def NP(self):
        if self.dev: print "NP"
        try:
            self.tags[self.i]
        except IndexError:
            return False

        if self.tags[self.i] == "NP":
            if self.dev: print "Found NP at pos", self.i
            self.i += 1
            return True
        else:
            # Overlooks the Det N PP rule as a possibility
            return ( self.Det(), self.N() ) == ( True, True )
            # part = ( Det(), N() ) == ( True, True )
            #
            # # Even if Det N, may need to check Det N PP
            # # TODO incomplete if statement. self.i could be in middle and this case still exists
            # if self.i == len(self.tags):
            #     return part
            # elif part:
            #     return PP() == True
            # else:
            #     return False

    def V(self):
        if self.dev: print "V"
        try:
            self.tags[self.i]
        except IndexError:
            return False

        if self.tags[self.i] == "V":
            if self.dev: print "Found V at pos", self.i
            self.i += 1
            return True
        else:
            return False

    def N(self):
        if self.dev: print "N"
        try:
            self.tags[self.i]
        except IndexError:
            return False

        if self.tags[self.i] == "N":
            if self.dev: print "Found N at pos", self.i
            self.i+=1
            return True
        else:
            return False

    def P(self):
        if self.dev: print "P"
        try:
            self.tags[self.i]
        except IndexError:
            return False

        if self.tags[self.i] == "P":
            if self.dev: print "Found P at pos", self.i
            self.i+=1
            return True
        else:
            return False

    def Det(self):
        if self.dev: print "Det"
        try:
            self.tags[self.i]
        except IndexError:
            return False

        if self.tags[self.i] == "Det":
            if self.dev: print "Found Det at pos", self.i
            self.i+=1
            return True
        else:
            return False
