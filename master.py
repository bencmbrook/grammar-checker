import part_of_speech, cfg_check

# test values for developers
test_sentence = ["I", "saw", "the", "duck"]
cfg_test = ["Det", "N", "V", "Det", "N", "P", "Det", "N"]
from nltk.corpus import conll2000

# Build HMM
tagger = part_of_speech.PointOfSpeechTagger()
tagger.buildProbDist(conll2000)

while True:
    # Get input
    inp = raw_input("Type a sentence to be checked: ")

    # Turn sentence into part-of-speech tags
    tag_sequence = tagger.sentenceToPOS(inp)
    print "TAG SEQUENCE:", tag_sequence

    # Pass tag sequence to CFG checker
    cfg_checker = cfg_check.verifyCFG()
    print
    cfg_checker.verify(tag_sequence)
