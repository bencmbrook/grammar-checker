import viterbi_tagger, perceptron_tagger
from nltk.corpus import conll2000, brown

if __name__ == '__main__':

    # verify the if AP tagger is ready to function
    taggerAP = perceptron_tagger.AP_Tagger(False)
    print "If the averaged perceptron tagger is not trained, train it and cache the results."
    try:
        taggerAP.APTaggerTesting()
    except IOError:
        taggerAP.APTaggerTraining()
        taggerAP.APTaggerTesting()


    viterbi_tagger = viterbi_tagger.PartOfSpeechTagger()
    print "The tests will take a while."
    print "Test of accuracy: conll2000 corpus (1/2)."
    viterbi_tagger.buildProbDist(conll2000)

    viterbi_tagger.testAgainstCorpus(conll2000)

    print "Test of accuracy: Brown corpus (2/2)"
    viterbi_tagger.buildProbDist(brown)
    viterbi_tagger.testAgainstCorpus(brown)
