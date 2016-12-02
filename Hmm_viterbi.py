import nltk
from nltk.corpus import conll2000

class PointOfSpeechTagger(object):
    """docstring for PointOfSpeechTagger."""
    def __init__(self, arg):
        super(PointOfSpeechTagger, self).__init__()
        self.arg = arg
        

    def buildProbDist(self, corpus):
        conll_tags_words = [ ]

        for sent in conll2000.tagged_sents():
            conll_tags_words.append(("BEGIN","BEGIN"))
            conll_tags_words.extend([(tag[:3], word) for (word, tag) in sent ])
            conll_tags_words.append(("STOP","STOP"))

        fd_tagwords = nltk.ConditionalFreqDist(conll_tags_words)
        self.pd_tagwords = nltk.ConditionalProbDist(fd_tagwords, nltk.MLEProbDist)

        conll_tags = [tag for (tag, word) in conll_tags_words ]

        fd_tags = nltk.ConditionalFreqDist(nltk.bigrams(conll_tags))
        self.pd_tags = nltk.ConditionalProbDist(fd_tags, nltk.MLEProbDist)
        self.all_tags = set(conll_tags)


    def sentenceToPOS(self, sentence):
        #Viterbi
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


sentence = ["I", "saw", "look", "duck"]


###################################
print "The sentence was: "
for s in sentence:
    print s

print "The best tag sequence is:"
for t in best_tag_seq:
    print t

print "The probability of the best tag sequence is:", prob_tag_seq
