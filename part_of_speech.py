import nltk
import re
import sys

class PointOfSpeechTagger(object):
    """docstring for PointOfSpeechTagger."""
    def __init__(self):
        super(PointOfSpeechTagger, self).__init__()


    def buildProbDist(self, corpus):
        corpus_tags_words = []

        # Build array containing all tags and words of all sentences, in order
        for sent in corpus.tagged_sents():
            corpus_tags_words.append( ("BEGIN","BEGIN") )
            corpus_tags_words.extend( [(tag, word) for (word, tag) in sent ] )
            corpus_tags_words.append( ("STOP","STOP") )

        # Build a conditional frequency distribution based on all tags/words of all sentences
        fd_tagwords = nltk.ConditionalFreqDist(corpus_tags_words)
        # Build conditional probability of each tag/word based on the frequency distribution above
        self.pd_tagwords = nltk.ConditionalProbDist(fd_tagwords, nltk.MLEProbDist)

        # Build array containing all tags of all sentences, in order
        corpus_tags = [tag for (tag, word) in corpus_tags_words]

        # Build a frequency distribution based ONLY on bigrams tags
        fd_tags = nltk.ConditionalFreqDist(nltk.bigrams(corpus_tags))
        # Build conditional probability of each tag based on the frequency distribution above
        self.pd_tags = nltk.ConditionalProbDist(fd_tags, nltk.MLEProbDist)
        self.all_tags = set(corpus_tags)


    def sentenceToPOS(self, sentence):
        # Hidden Markov Model using Viterbi alg
        len_sent = len(sentence)
        viterbi = [ ]
        backpointer = [ ]

        first_viterbi = { }
        first_backpointer = { }

        for tag in self.all_tags:
            if tag == "BEGIN": continue
            first_viterbi[ tag ] = self.pd_tags["BEGIN"].prob(tag) * self.pd_tagwords[tag].prob( sentence[0] )
            first_backpointer[ tag ] = "BEGIN"

        viterbi.append(first_viterbi)
        backpointer.append(first_backpointer)

        curr_best = max(first_viterbi.keys(), key = lambda tag: first_viterbi[ tag ])

        for wordindex in range(1, len_sent):
            temp_viterbi = { }
            temp_backpointer = { }
            pre_viterbi = viterbi[-1]

            for tag in self.all_tags:
                if tag == "BEGIN": continue
                pre_best = max(pre_viterbi.keys(), key = lambda pretag: pre_viterbi[pretag]*self.pd_tags[pretag].prob(tag)*self.pd_tagwords[tag].prob(sentence[wordindex]))

                temp_viterbi[tag] = pre_viterbi[pre_best]*self.pd_tags[pre_best].prob(tag)*self.pd_tagwords[tag].prob(sentence[wordindex])
                temp_backpointer[tag] = pre_best

            curr_best = max(temp_viterbi.keys(), key=lambda tag: temp_viterbi[tag])

            viterbi.append(temp_viterbi)
            backpointer.append(temp_backpointer)

        pre_viterbi = viterbi[-1]
        pre_best = max(pre_viterbi.keys(), key = lambda pretag: pre_viterbi[pretag]*self.pd_tags[pretag].prob("STOP"))
        prob_tag_seq = pre_viterbi [pre_best]*self.pd_tags[pre_best].prob("STOP")

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
        arr = re.findall(r"[\w']+|[.,!?;]", string) # split including commas
        return self.sentenceToPOS( arr )

    def inputToPOS(self):
        inp = raw_input("Let's check a sentence: ")
        return self.stringToPOS(inp)

    def testAgainstCorpus(self, corpus, total_runs=1500):
        print "Testing Viterbi accuracy against corpus..."
        num_true = 0
        num_runs = 0
        for sent in corpus.tagged_sents():
            sentenceArr = [pair[0] for pair in sent]
            trueTagSeq = [pair[1] for pair in sent]
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
