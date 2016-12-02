import part_of_speech, cfg_check

# test values for developers
test_sentence = ["I", "saw", "the", "duck"]
cfg_test = ["NNP","VBD","NNP"]
from nltk.corpus import conll2000

# Build HMM
tagger = part_of_speech.PointOfSpeechTagger()
tagger.buildProbDist(conll2000)

while True:
    # Turn sentence into part-of-speech tags
    tag_sequence = tagger.inputToPOS()
    print "TAG SEQUENCE:", tag_sequence

    # Pass tag sequence to CFG checker
    cfg_checker = cfg_check.verifyCFG()
    print
    cfg_checker.verify(tag_sequence)
