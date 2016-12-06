import Viterbi_tagger, AP_tagger, grammar

# test values for developers
test_sentence = ["I", "saw", "the", "duck"]
cfg_test = ["NNP","VBD","NNP"]
from nltk.corpus import conll2000, brown

if __name__ == '__main__':

    # print "We use the tagged corpus to analysis the input sentence"
    # print "But if one of input word can not be found in the prepared corpus,the user-defined AP tagger will be activated"
    # print "As the first step, we will test the AP tagger, and train it if necessary!"

    viterbi_tagger = Viterbi_tagger.PartOfSpeechTagger()


    # OPTIONAL: run tests on Viterbi alg using the corpora as test set
    # viterbi_tagger.testAgainstCorpus(conll2000)
    # viterbi_tagger.testAgainstCorpus(brown)

    # Build HMM
    print "Generating Hidden Markov Model..."
    viterbi_tagger = Viterbi_tagger.PartOfSpeechTagger()
    # Build probability distributions for each of the corpora we want to use
    print "Building POS tag probability distributions based on corpora...",
    print "conll2000,",
    viterbi_tagger.buildProbDist(conll2000)
    print "Brown."
    viterbi_tagger.buildProbDist(brown)

    # Train the AP Tagger weights
    print "Training Averaged Perceptron model based on corpora..."
    taggerAP = AP_tagger.AP_Tagger(False)

    # Build CFG rule set based on treebank
    print "Generating Context Free Grammar based on Treebank..."
    cfg_checker = grammar.Grammar()
    tbank_grammar = cfg_checker.buildFromTreebank()

    # Loop input to get and check sentences
    print
    while True:
        # Turn sentence into part-of-speech tags
        tag_sequence = viterbi_tagger.inputToPOS()
        print "TAG SEQUENCE:", tag_sequence

        # Pass tag sequence to CFG checker
        cfg_checker.verify(tbank_grammar, tag_sequence)
