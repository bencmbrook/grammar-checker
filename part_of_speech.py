import nltk
import re
import sys
import AP_tagger

from nltk.corpus import conll2000, brown


class PointOfSpeechTagger(object):
    """docstring for PointOfSpeechTagger."""
    def __init__(self):
        super(PointOfSpeechTagger, self).__init__()


    def buildProbDist(self):
        # input
        inp = raw_input("Let's check a sentence: ")
        sentence = re.findall(r"[\w']+|[.,!?;]", inp)  # split including commas


        conll_tags_words = []
        brown_tags_words = []

        for sent in conll2000.tagged_sents():
            conll_tags_words.append(("BEGIN", "BEGIN"))
            conll_tags_words.extend([(tag[:3], word) for (word, tag) in sent])
            conll_tags_words.append(("STOP", "STOP"))

        for sent in brown.tagged_sents():
            brown_tags_words.append(("BEGIN", "BEGIN"))
            brown_tags_words.extend([(tag[:3], word) for (word, tag) in sent])
            brown_tags_words.append(("STOP", "STOP"))

        # Build array containing all tags of all sentences, in order
        conll_tags = [tag for (tag, word) in conll_tags_words]
        brown_tags = [tag for (tag, word) in brown_tags_words]

        Flag_C = True
        Flag_B = True

        for word in sentence:
            if word not in [w for (t, w) in conll_tags_words[1:-2]]:
                Flag_C = False
            if word not in [w for (t, w) in brown_tags_words[1:-2]]:
                Flag_B = False

        corpus_tags_words = []
        corpus_tags = []


        if Flag_B or Flag_C:
            # using the prepared corpus

            if Flag_C:
            #pass
                corpus_tags_words = conll_tags_words
                corpus_tags = conll_tags
            elif Flag_B:
            #pass
                corpus_tags_words = brown_tags_words
                corpus_tags = brown_tags


            # Build array containing all tags and words of all sentences, in order
            #for sent in corpus.tagged_sents():
            #    corpus_tags_words.append( ("BEGIN","BEGIN") )
            #    corpus_tags_words.extend( [(tag, word) for (word, tag) in sent ] )
            #    corpus_tags_words.append( ("STOP","STOP") )

            # Build a conditional frequency distribution based on all tags/words of all sentences
            fd_tagwords = nltk.ConditionalFreqDist(corpus_tags_words)
            # Build conditional probability of each tag/word based on the frequency distribution above
            self.pd_tagwords = nltk.ConditionalProbDist(fd_tagwords, nltk.MLEProbDist)


            # Build a frequency distribution based ONLY on bigrams tags
            fd_tags = nltk.ConditionalFreqDist(nltk.bigrams(corpus_tags))
            # Build conditional probability of each tag based on the frequency distribution above
            self.pd_tags = nltk.ConditionalProbDist(fd_tags, nltk.MLEProbDist)
            self.all_tags = set(corpus_tags)

            tag_sequence = self.sentenceToPOS(sentence)

        else:

            print "No such word in corpus: Conll2000 and Brown "
            print "We will use our user-defined AP tagger"
            tag_sequence = AP_tagger.AP_Tagger().tag(inp)


        return tag_sequence



    def sentenceToPOS(self, sentence):
        # Hidden Markov Model using Viterbi alg
        len_sent = len(sentence)
        #self.sentence = sentence

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

        #curr_best = max(first_viterbi.keys(), key = lambda tag: first_viterbi[ tag ])

        for wordindex in range(1, len_sent):
            temp_viterbi = { }
            temp_backpointer = { }
            pre_viterbi = viterbi[-1]

            for tag in self.all_tags:
                if tag == "BEGIN": continue
                pre_best = max(pre_viterbi.keys(), key = lambda pretag: pre_viterbi[pretag]*self.pd_tags[pretag].prob(tag)*self.pd_tagwords[tag].prob(sentence[wordindex]))

                temp_viterbi[tag] = pre_viterbi[pre_best]*self.pd_tags[pre_best].prob(tag)*self.pd_tagwords[tag].prob(sentence[wordindex])
                temp_backpointer[tag] = pre_best

            #curr_best = max(temp_viterbi.keys(), key=lambda tag: temp_viterbi[tag])

            viterbi.append(temp_viterbi)
            backpointer.append(temp_backpointer)

        pre_viterbi = viterbi[-1]
        pre_best = max(pre_viterbi.keys(), key = lambda pretag: pre_viterbi[pretag]*self.pd_tags[pretag].prob("STOP"))
        #prob_tag_seq = pre_viterbi [pre_best]*self.pd_tags[pre_best].prob("STOP")

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

"""
    def stringToPOS(self, string):
        arr = re.findall(r"[\w']+|[.,!?;]", string) # split including commas
        return self.sentenceToPOS( arr )

    def inputToPOS(self):
        inp = raw_input("Let's check a sentence: ")
        return self.stringToPOS(inp)
"""
