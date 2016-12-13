import Viterbi_tagger, AP_tagger
from nltk.corpus import conll2000, brown

if __name__ == '__main__':

    # verify the if AP tagger is ready to function
    taggerAP = AP_tagger.AP_Tagger(False)
    print "verify if the AP tagger is trained"
    print "if not, train the AP tagger"
    try:
        taggerAP.APTaggerTesting()
    except IOError:
        taggerAP.APTaggerTraining()
        taggerAP.APTaggerTesting()


    viterbi_tagger = Viterbi_tagger.PartOfSpeechTagger()
    print "Test of accuracy: Brown corpus."
    print "The test will use a long time, please be patient."
    viterbi_tagger.buildProbDist(conll2000)

    viterbi_tagger.testAgainstCorpus(conll2000)

    print "Test of accuracy: Brown corpus"
    print "The test will use a long time, please be patient."
    viterbi_tagger.buildProbDist(brown)
    viterbi_tagger.testAgainstCorpus(brown)

