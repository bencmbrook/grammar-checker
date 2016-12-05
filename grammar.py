import nltk
from nltk.corpus import treebank
from nltk.grammar import CFG, Nonterminal, Production
from nltk import RecursiveDescentParser

class Grammar(object):

    def __init__(self, dev=False):
        super(verifyCFG, self).__init__()
        self.dev = dev

    grammar1 = CFG.fromstring("""
        S  -> NP VP
        NP -> "DT" Nom | "NNP" | "PRP"
        Nom -> "JJ" Nom | N
        VP -> V "JJ" | V NP | V S | V NP PP | V "RB"
        V -> "VBD" | "VB" | "VBG" | "VBN" | "VBP" | "VBZ"
        N -> "NN" | "NNP" | "NNS" | "NNPS"
        PP -> "IN" NP
    """)

    grammar2 = CFG.fromstring("""
        S  -> NP VP
        NP -> "DT" Nom | "NNP" | "PRP"
        Nom -> "JJ" Nom | N | Nom N
        VP -> V "JJ" | V NP | V S | V NP PP | V "RB" | V PP | V
        V -> "VBD" | "VB" | "VBG" | "VBN" | "VBP" | "VBZ"
        N -> "NN" | "NNP" | "NNS" | "NNPS"
        PP -> "IN" NP | "TO" NP
    """)


    def buildFromTreebank(self, treebank):
        # Build a Context-Free-Grammar based on a treebank
        tbank_productions = set()
        for sent in treebank.parsed_sents():
            for production in sent.productions():
                if production.is_lexical():
                    new_rhs = [str(production._lhs)]
                    production = Production(production._lhs, new_rhs)
                tbank_productions.add(production)

        tbank_grammar = CFG(Nonterminal('S'), list(tbank_productions))

        return tbank_grammar


    def verifySentence(self, grammar, tags):
        rd_parser = RecursiveDescentParser(grammar)
        valid = False

        if any(x in tags for x in ["WP", "WDT", "WP$", "WRB"]):
            print "I haven't learned about question words yet"
            return

        try:
            for tree in rd_parser.parse(tags):
                valid = True
                break
        except ValueError:
            print "This is a grammatical structure I don't understand yet."
            return

        if valid:
            print "Valid"
        else:
            print "Invalid"