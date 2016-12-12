import nltk
from nltk.corpus import treebank
from nltk.grammar import CFG, Nonterminal, Production
from nltk import RecursiveDescentParser

# tbank_productions = set(production for sent in treebank.parsed_sents()
#                         for production in sent.productions())

""" Turn lexical leaf nodes into tags themselves
e.g. NN -> 'director' becomes NN -> 'NN'
"""
tbank_productions = set()
for sent in treebank.parsed_sents():
    for production in sent.productions():
        if production.is_lexical():
            new_rhs = [str(production._lhs)]
            production = Production(production._lhs, new_rhs)
        tbank_productions.add(production)

tbank_grammar = CFG(Nonterminal('S'), list(tbank_productions))

rd_parser = RecursiveDescentParser(tbank_grammar)
tags = ["DT", "NN", "VB", "NN"]

try:
    for tree in rd_parser.parse(tags):
        print "Good"
except ValueError:
    print "This is a grammatical structure I don't understand yet."
