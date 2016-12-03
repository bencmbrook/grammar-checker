import part_of_speech, cfg_check

# test values for developers
test_sentence = ["I", "saw", "the", "duck"]
cfg_test = ["NNP","VBD","NNP"]
from nltk.corpus import conll2000, brown

# Build HMM
tagger1 = part_of_speech.PointOfSpeechTagger()
tagger1.buildProbDist(conll2000)
tagger1.testAgainstCorpus(conll2000)


# tagger2 = part_of_speech.PointOfSpeechTagger()
# tagger2.buildProbDist(brown)
# tagger2.testAgainstCorpus(brown)


# while True:
#     # Turn sentence into part-of-speech tags
#     tag_sequence = tagger.inputToPOS()
#     print "TAG SEQUENCE:", tag_sequence
#
#     # Pass tag sequence to CFG checker
#     cfg_checker = cfg_check.verifyCFG()
#     cfg_checker.verify(tag_sequence)
#     print
