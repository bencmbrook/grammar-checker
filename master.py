import part_of_speech, cfg_check

# test values for developers
test_sentence = ["I", "saw", "the", "duck"]
cfg_test = ["Det", "N", "V", "Det", "N", "P", "Det", "N"]
from nltk.corpus import conll2000

# Build HMM
tagger = part_of_speech.PointOfSpeechTagger()
tagger.buildProbDist(conll2000)

# Get input
inp = input("Type a sentence to be checked:")

# Turn sentence into part-of-speech tags
tag_sequence = tagger.sentenceToPOS(inp)

# Pass tag sequence to CFG checker
cfg_checker = cfg_check.verifyCFG()
cfg_checker.verify(tag_sequence)
