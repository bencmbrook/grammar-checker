import nltk, re, sys, AP_tagger
from nltk.corpus import conll2000, brown

class PartOfSpeechTagger(object):
    def __init__(self):
        super(PartOfSpeechTagger, self).__init__()
        # List containing tuples: ( pd_tagwords, pd_tags, all_tags, flag )
        self.corpora_prob_dists = []
        # this input only prepares for AP tagger
        self.AP_sent = []


    def buildProbDist(self, corpus):
        """ Build tag probability distribution for Viterbi algorithm """

        corpus_tags_words = []

        # Build array containing all tags and words of all sentences, in order
        for sent in corpus.tagged_sents():
            corpus_tags_words.append( ("BEGIN","BEGIN") )
            corpus_tags_words.extend( [(tag, word) for (word, tag) in sent ] )
            corpus_tags_words.append( ("STOP","STOP") )

        # Build a conditional frequency distribution based on all tags/words of all sentences
        fd_tagwords = nltk.ConditionalFreqDist(corpus_tags_words)
        # Build conditional probability of each tag/word based on the frequency distribution above
        pd_tagwords = nltk.ConditionalProbDist(fd_tagwords, nltk.MLEProbDist)

        # Build array containing all tags of all sentences, in order
        corpus_tags = [tag for (tag, word) in corpus_tags_words]

        # Build a frequency distribution based ONLY on bigrams tags
        fd_tags = nltk.ConditionalFreqDist(nltk.bigrams(corpus_tags))
        # Build conditional probability of each tag based on the frequency distribution above
        pd_tags = nltk.ConditionalProbDist(fd_tags, nltk.MLEProbDist)
        all_tags = set(corpus_tags)

        self.corpora_prob_dists.append( (pd_tagwords, pd_tags, all_tags, corpus_tags_words) )


    def sentenceToPOS(self, sentence):
        """ Choose and call method (Viterbi Brown, Viterbi conll2000, Averaged Perceptron) """
        i = 0
        # Choose corpus (Are all words in input sentence in one of the corpora?)
        # Finds the ith corpus that contains all words in input. Flag is false if no corpora contains all words.
        for (_, _, _, corpus_tags_words) in self.corpora_prob_dists:
            flag = True
            for word in sentence:
                if word not in [w for (t, w) in corpus_tags_words[1:-2]]:
                    flag = False
                    break
            if flag: break
            else: i+= 1

        # Choose and call method
        if flag:
            # All words in a corpora. Choose Viterbi with ith corpora.
            print "Using Viterbi: corpora", i+1
            c = self.corpora_prob_dists[i]
            tag_sequence = self._getViterbiPath(sentence, c[0], c[1], c[2])
            #print tag_sequence
        else:
            # Missing word from corpora. Choose Averaged Perceptron.
            print "Your input contains a never-before-seen word! Using an Average Perceptron"
            tag_sequence = AP_tagger.AP_Tagger().tag( self.AP_sent )

        return tag_sequence


    def _getViterbiPath(self, sentence, pd_tagwords, pd_tags, all_tags):
        """ Hidden Markov Model using Viterbi alg """

        len_sent = len(sentence)
        viterbi = [ ]
        backpointer = [ ]

        first_viterbi = { }
        first_backpointer = { }

        for tag in all_tags:
            if tag == "BEGIN": continue
            first_viterbi[ tag ] = pd_tags["BEGIN"].prob(tag) * pd_tagwords[tag].prob( sentence[0] )
            first_backpointer[ tag ] = "BEGIN"

        viterbi.append(first_viterbi)
        backpointer.append(first_backpointer)

        curr_best = max(first_viterbi.keys(), key = lambda tag: first_viterbi[ tag ])

        for wordindex in range(1, len_sent):
            temp_viterbi = { }
            temp_backpointer = { }
            pre_viterbi = viterbi[-1]

            for tag in all_tags:
                if tag == "BEGIN": continue
                pre_best = max(pre_viterbi.keys(), key = lambda pretag: pre_viterbi[pretag]*pd_tags[pretag].prob(tag)*pd_tagwords[tag].prob(sentence[wordindex]))

                temp_viterbi[tag] = pre_viterbi[pre_best]*pd_tags[pre_best].prob(tag)*pd_tagwords[tag].prob(sentence[wordindex])
                temp_backpointer[tag] = pre_best

            curr_best = max(temp_viterbi.keys(), key=lambda tag: temp_viterbi[tag])

            viterbi.append(temp_viterbi)
            backpointer.append(temp_backpointer)

        pre_viterbi = viterbi[-1]
        pre_best = max(pre_viterbi.keys(), key = lambda pretag: pre_viterbi[pretag]*pd_tags[pretag].prob("STOP"))
        prob_tag_seq = pre_viterbi [pre_best]*pd_tags[pre_best].prob("STOP")

        best_tag_seq = ["STOP", pre_best]
        backpointer.reverse()


        curr_best_tag = pre_best
        for b in backpointer:
            best_tag_seq.append(b[curr_best_tag])
            curr_best_tag = b[curr_best_tag]

        best_tag_seq.reverse()

        # Remove BEGIN/END tags
        best_tag_seq.pop()
        best_tag_seq.pop(0)

        return best_tag_seq


    def stringToPOS(self, string):
        """ Convert string to array and get tag sequence """
        self.AP_sent = string
        arr = re.findall(r"[\w']+|[.,!?;]", string) # split including commas
        return self.sentenceToPOS( arr )


    def inputToPOS(self):
        """ Get input from command line and get tag sequence  """

        inp = raw_input("Let's check a sentence: ")
        return self.stringToPOS(inp)


    def testAgainstCorpus(self, corpus, total_runs=100):
        """ Test method for Viterbi method accuracy against a corpus """

        print "Testing Viterbi accuracy against corpus..."
        num_true = 0
        num_runs = 0
        for sent in corpus.tagged_sents():

            sentenceArr = []
            trueTagSeq = []
            for (word, tag) in sent:
                sentenceArr.append( word )
                trueTagSeq.append( tag )
            predTagSeq = self.sentenceToPOS(sentenceArr)

            if trueTagSeq == predTagSeq:
                num_true += 1
            num_runs += 1

            # Update percent complete output
            sys.stdout.write('\r')
            sys.stdout.write("%.2f%% " % (float(num_runs) / total_runs * 100))
            sys.stdout.flush()

            if num_runs >= total_runs:
                break

        print "ACCURACY: %.2f%%" % (num_true / float(num_runs) * 100)
        return
