import nltk
from nltk.corpus import treebank
from nltk.grammar import CFG, Nonterminal, Production
from nltk import ChartParser

class Grammar(object):

    def __init__(self, dev=False):
        super(Grammar, self).__init__()
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


    def buildFromTreebank(self):
        """ Build a Context-Free-Grammar based on UPenn treebank """
        tbank_productions = set()
        for sent in treebank.parsed_sents():
            for production in sent.productions():
                if production.is_lexical():
                    new_rhs = [str(production._lhs)]
                    production = Production(production._lhs, new_rhs)
                tbank_productions.add(production)

        tbank_grammar = CFG(Nonterminal('S'), list(tbank_productions))

        return tbank_grammar

    def verify(self, grammar, tags):
        """ Verify tag sequence as grammatically correct or not """
        # rd_parser = RecursiveDescentParser(grammar)
        rd_parser = ChartParser(grammar)
        valid = False

        try:
            for tree in rd_parser.parse(tags):
                valid = True
                break
        except ValueError:
            print "This is a grammatical structure I don't understand yet."
            return

        if valid:
            print "Valid"
            return True
        else:
            print "Invalid"
            return False
