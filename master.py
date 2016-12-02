import point_of_speech, cfg_check
from nltk.corpus import conll2000

# Build HMM
sentence = ["I", "saw", "look", "duck"]
tagger = point_of_speech.PointOfSpeechTagger()

tagger.buildProbDist(conll2000)
print tagger.sentenceToPOS(sentence)


cfg_checker = cfg_check.verifyCFG()
test = ["Det", "N", "V", "Det", "N", "P", "Det", "N"]
cfg_checker.verify(test)
