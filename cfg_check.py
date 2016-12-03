# S   -> NP VP
# VP  -> VB NP | VB NP PP
# PP  -> IN NP
# VB   -> END
# NP  -> END | DT NN | DT NN PP
# DT -> END
# NN   -> END
# IN   -> END
from nltk import CFG
from nltk import RecursiveDescentParser

class verifyCFG(object):

    def __init__(self, dev=False):
        super(verifyCFG, self).__init__()
        self.dev = dev

    # grammar1 = CFG.fromstring("""
    #     S -> NP VP
    #     VP -> VB NP | VB NP PP
    #     PP -> IN NP
    #     VB -> "saw" | "ate" | "walked"
    #     NP -> "John" | "Mary" | "Bob" | DT NN | DT NN PP
    #     DT -> "a" | "an" | "the" | "my"
    #     NN -> "man" | "dog" | "cat" | "telescope" | "park"
    #     IN -> "in" | "on" | "by" | "with"
    # """)

    grammar2 = CFG.fromstring("""
        S  -> NP VP
        NP -> "DT" Nom | "NNP" | "PRP"
        Nom -> "JJ" Nom | N
        VP -> V "JJ" | V NP | V S | V NP PP | V "RB"
        V -> "VBD" | "VB" | "VBG" | "VBN" | "VBP" | "VBZ"
        N -> "NN" | "NNP" | "NNS" | "NNPS"
        PP -> "IN" NP
    """)

    grammar3 = CFG.fromstring("""
        S  -> NP VP
        NP -> "DT" Nom | "NNP" | "PRP"
        Nom -> "JJ" Nom | N | Nom N
        VP -> V "JJ" | V NP | V S | V NP PP | V "RB" | V PP | V
        V -> "VBD" | "VB" | "VBG" | "VBN" | "VBP" | "VBZ"
        N -> "NN" | "NNP" | "NNS" | "NNPS"
        PP -> "IN" NP | "TO" NP
    """)
        # NNP -> 'Buster' | 'Chatterer' | 'Joe'
        # DT -> 'the' | 'a'
        # NN -> 'bear' | 'squirrel' | 'tree' | 'fish' | 'log'
        # JJ  -> 'angry' | 'frightened' |  'little' | 'tall'
        # VB ->  'chased'  | 'saw' | 'said' | 'thought' | 'was' | 'put'
        # IN -> 'on'

    def verify(self, tags):
        rd_parser = RecursiveDescentParser(self.grammar2)
        valid = False

        if any(x in tags for x in ["WP", "WDT", "WP$", "WRB"]):
            print "I haven't learned about question words yet"
            return

        try:
            for tree in rd_parser.parse(tags):
                valid = True
        except ValueError:
            print "This is a grammatical structure I don't understand yet."
            return

        # If all tags VBG (default when error), explain error
        if tags[1:] == tags[:-1] and tags[0] == "VBG":
            print "I've never seen one of those words before."
            return

        if valid:
            print "Valid"
        else:
            print "Invalid"

    # def verify(self, tags):
    #     self.tags = tags
    #     self.i = 0
    #     print self.S()
    #
    # def S(self):
    #     if self.dev: print "S"
    #     return ( self.NP(), self.VP() ) == ( True, True ) and self.i == len(self.tags)
    #
    # def VP(self):
    #     if self.dev: print "VP"
    #     part = ( self.VB(), self.NP() ) == ( True, True )
    #     # Even if VB NP, may need to check VB NP PP
    #     if self.i == len(self.tags):
    #         return part
    #     elif part:
    #         return self.PP() == True
    #     else:
    #         return False
    #
    # def PP(self):
    #     if self.dev: print "PP"
    #     return ( self.IN(), self.NP() ) == ( True, True )
    #
    # def NP(self):
    #     if self.dev: print "NP"
    #     try:
    #         self.tags[self.i]
    #     except IndexError:
    #         return False
    #
    #     if self.tags[self.i] == "NP":
    #         if self.dev: print "Found NP at pos", self.i
    #         self.i += 1
    #         return True
    #     else:
    #         # Overlooks the DT NN PP rule as a possibility
    #         return ( self.DT(), self.NN() ) == ( True, True )
    #         # part = ( DT(), NN() ) == ( True, True )
    #         #
    #         # # Even if DT NN, may need to check DT NN PP
    #         # # TODO incomplete if statement. self.i could be in middle and this case still exists
    #         # if self.i == len(self.tags):
    #         #     return part
    #         # elif part:
    #         #     return PP() == True
    #         # else:
    #         #     return False
    #
    # def VB(self):
    #     if self.dev: print "VB"
    #     try:
    #         self.tags[self.i]
    #     except IndexError:
    #         return False
    #
    #     if self.tags[self.i] == "VB":
    #         if self.dev: print "Found VB at pos", self.i
    #         self.i += 1
    #         return True
    #     else:
    #         return False
    #
    # def NN(self):
    #     if self.dev: print "NN"
    #     try:
    #         self.tags[self.i]
    #     except IndexError:
    #         return False
    #
    #     if self.tags[self.i] == "NN":
    #         if self.dev: print "Found NN at pos", self.i
    #         self.i+=1
    #         return True
    #     else:
    #         return False
    #
    # def IN(self):
    #     if self.dev: print "IN"
    #     try:
    #         self.tags[self.i]
    #     except IndexError:
    #         return False
    #
    #     if self.tags[self.i] == "IN":
    #         if self.dev: print "Found IN at pos", self.i
    #         self.i+=1
    #         return True
    #     else:
    #         return False
    #
    # def DT(self):
    #     if self.dev: print "DT"
    #     try:
    #         self.tags[self.i]
    #     except IndexError:
    #         return False
    #
    #     if self.tags[self.i] == "DT":
    #         if self.dev: print "Found DT at pos", self.i
    #         self.i+=1
    #         return True
    #     else:
    #         return False
