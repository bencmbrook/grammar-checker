import part_of_speech, cfg_check, AP_tagger

# test values for developers
test_sentence = ["I", "saw", "the", "duck"]
cfg_test = ["NNP","VBD","NNP"]
from nltk.corpus import conll2000, brown



if __name__ == '__main__':

    print "We use the tagged corpus to analysis the input sentence"
    print "But if one of input word can not be found in the prepared corpus,the user-defined AP tagger will be activated"
    print "As the first step, we will test the AP tagger, and train it if necessary!"


    # Train the AP Tagger
    taggerAP = AP_tagger.AP_Tagger()
    try:
        taggerAP.APTaggerTesting()

    except IOError:
        taggerAP.APTaggerTraining()


# tagger1.testAgainstCorpus(conll2000)


# tagger2 = part_of_speech.PointOfSpeechTagger()
# tagger2.buildProbDist(brown)
# tagger2.testAgainstCorpus(brown)


    while True:
        # Build HMM
        tagger1 = part_of_speech.PointOfSpeechTagger()
        tag_sequence = tagger1.buildProbDist()
        # Turn sentence into part-of-speech tags
        #tag_sequence = tagger1.inputToPOS()

        print "TAG SEQUENCE:", tag_sequence

        # Pass tag sequence to CFG checker
        cfg_checker = cfg_check.verifyCFG()
        cfg_checker.verify(tag_sequence)

