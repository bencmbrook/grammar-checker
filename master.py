import viterbi_tagger, perceptron_tagger, cfg

# test values for developers
test_sentence = ["I", "saw", "the", "duck"]
cfg_test = ["NNP","VBD","NNP"]
from nltk.corpus import conll2000, brown

if __name__ == '__main__':

    print "We use the tagged corpus to analysis the input sentence"
    print "But if one of input word can not be found in the prepared corpus,the user-defined AP tagger will be activated"

    # Build HMM
    print "Generating Hidden Markov Model..."
    viterbi_tagger = Viterbi_tagger.PartOfSpeechTagger()
    # Build probability distributions for each of the corpora we want to use
    print "Building POS tag probability distributions based on..."
    print "Corpora 1: Conll2000,"
    viterbi_tagger.buildProbDist(conll2000)
    print "Corpora 2: Brown."
    viterbi_tagger.buildProbDist(brown)
    #
    #Train the AP Tagger weights
    print "Prepare Averaged Perceptron tagger based on tagged corpora"
    taggerAP = AP_tagger.AP_Tagger(False)
    #
    # Build CFG rule set based on treebank
    print "Generating Context Free Grammar based on Treebank..."
    cfg_checker = grammar.Grammar()
    tbank_grammar = cfg_checker.buildFromTreebank()
    #
    # Loop input to get and check sentences
    # print
    while True:
         # Turn sentence into part-of-speech tags
         tag_sequence = viterbi_tagger.inputToPOS()
         print "TAG SEQUENCE:", tag_sequence

         # Pass tag sequence to CFG checker
         cfg_checker.verify(tbank_grammar, tag_sequence)
