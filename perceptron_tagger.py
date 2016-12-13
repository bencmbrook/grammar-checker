'''An averaged perceptron, inspired by the nltk project and the website below:
  http://honnibal.wordpress.com/2013/09/11/a-good-part-of-speechpos-tagger-in-about-200-lines-of-python/
    '''

from __future__ import division
from __future__ import absolute_import
from collections import defaultdict

import os
import pickle
import random

PICKLE = "dataAP/user_defined_tagger.pickle"

class APerceptron(object):

    def __init__(self):
        # Each feature gets its own weight vector, so weights is a dict-of-dicts
        self.weights = {}
        self.classes = set()
        # The accumulated values, for the averaging. These will be keyed by
        # feature/clas tuples
        self._totals = defaultdict(int)
        # The last time the feature was changed, for the averaging. Also
        # keyed by feature/clas tuples
        # (tstamps is short for timestamps)
        self._tstamps = defaultdict(int)
        # Number of instances seen
        self.i = 0

    def predict(self, features):
        '''Dot-product the features and current weights and return the best label.'''
        scores = defaultdict(float)
        for feat, value in features.items():
            if feat not in self.weights or value == 0:
                continue
            weights = self.weights[feat]
            for label, weight in weights.items():
                scores[label] += value * weight
        # Do a secondary alphabetic sort, for stability
        return max(self.classes, key=lambda label: (scores[label], label))

    def update(self, truth, guess, features):
        '''Update the feature weights.'''
        def upd_feat(c, f, w, v):
            param = (f, c)
            self._totals[param] += (self.i - self._tstamps[param]) * w
            self._tstamps[param] = self.i
            self.weights[f][c] = w + v

        self.i += 1
        if truth == guess:
            return None
        for feat in features:
            weights = self.weights.setdefault(feat, {})
            upd_feat(truth, feat, weights.get(truth, 0.0), 1.0)
            upd_feat(guess, feat, weights.get(guess, 0.0), -1.0)
        return None

    def average_weights(self):
        '''Average weights from all iterations.'''
        for feat, weights in self.weights.items():
            new_feat_weights = {}
            for clas, weight in weights.items():
                param = (feat, clas)
                total = self._totals[param]
                total += (self.i - self._tstamps[param]) * weight
                averaged = round(total / float(self.i), 3)
                if averaged:
                    new_feat_weights[clas] = averaged
            self.weights[feat] = new_feat_weights
        return None


#######################################################################################

class AP_Tagger():
    '''Greedy Averaged Perceptron tagger
      :param load: Load the pickled model upon instantiation.
    '''

    BEGIN = ['-BEGIN-', '-BEGIN2-']
    STOP = ['-STOP-', '-STOP2-']
    AP_MODEL_LOC = os.path.join(os.path.dirname(__file__), PICKLE)

    def __init__(self, load=True):
        self.model = APerceptron()
        self.tagdict = {}
        self.classes = set()
        if load:
            self.load(self.AP_MODEL_LOC)

    def tag(self, sentence):
        '''Tags a sentence.'''
        # format untokenized corpus has \n between sentences and ' ' between words

        s_split = lambda t: t.split('\n')
        w_split = lambda s: s.split()

        def split_sents(sentence):
            for s in s_split(sentence):
                yield w_split(s)
        ########################################

        prev, prev2 = self.BEGIN
        tokens = []

        for words in split_sents(sentence):
            context = self.BEGIN + [self._normalize(w) for w in words] + self.STOP
            for i, word in enumerate(words):
                tag = self.tagdict.get(word)
                if not tag:
                    features = self._get_features(i, word, context, prev, prev2)
                    tag = self.model.predict(features)
                tokens.append((word, tag[:-1]))
                prev2 = prev
                prev = tag
        return tokens

    def train(self, sentences, save_loc=None, nr_iter=10):
        '''Train a model from sentences, and save it at ``save_loc``. ``nr_iter``
        controls the number of Perceptron training iterations.
        :param sentences: A list of (words, tags) tuples.
        :param save_loc: If not ``None``, saves a pickled model in this location.
        :param nr_iter: Number of training iterations.
        '''
        self._make_tagdict(sentences)
        self.model.classes = self.classes
        for iter_ in range(nr_iter):
            c = 0
            n = 0
            for words, tags in sentences:
                prev, prev2 = self.BEGIN
                context = self.BEGIN + [self._normalize(w) for w in words] \
                          + self.STOP
                for i, word in enumerate(words):
                    guess = self.tagdict.get(word)
                    if not guess:
                        feats = self._get_features(i, word, context, prev, prev2)
                        guess = self.model.predict(feats)
                        self.model.update(tags[i], guess, feats)
                    prev2 = prev
                    prev = guess
                    c += guess == tags[i]
                    n += 1
            random.shuffle(sentences)
            print "Iteration {0}: {1}/{2}={3}".format(iter_, c, n, (c / n) * 100)

        self.model.average_weights()
        # Pickle as a binary file
        if save_loc is not None:
            pickle.dump((self.model.weights, self.tagdict, self.classes),
                        open(save_loc, 'wb'), -1)
        return None

    def load(self, loc):
        '''Load a pickled model.'''
        try:
            weight_tagdict_class = pickle.load(open(loc, 'rb'))
        except IOError:
            msg = ("Missing user-define pickle file.")
            raise IOError(msg)
        self.model.weights, self.tagdict, self.classes = weight_tagdict_class
        self.model.classes = self.classes
        return None

    def _normalize(self, word):
        '''Normalization used in pre-processing.
        - All words are lower cased
        - Digits in the range 1800-2100 are represented as !YEAR;
        - Other digits are represented as !DIGITS
        :rtype: str
        '''
        if '-' in word and word[0] != '-':
            return '!HYPHEN'
        elif word.isdigit() and len(word) == 4:
            return '!YEAR'
        elif word[0].isdigit():
            return '!DIGITS'
        else:
            return word.lower()

    def _get_features(self, i, word, context, prev, prev2):
        '''Map tokens into a feature representation, implemented as a
        {hashable: float} dict. If the features change, a new model must be
        trained.
        '''

        def add(name, *args):
            features[' '.join((name,) + tuple(args))] += 1

        i += len(self.BEGIN)
        features = defaultdict(int)
        # It's useful to have a constant feature, which acts sort of like a prior
        add('bias')
        add('i suffix', word[-3:])
        add('i pref1', word[0])
        add('i-1 tag', prev)
        add('i-2 tag', prev2)
        add('i tag+i-2 tag', prev, prev2)
        add('i word', context[i])
        add('i-1 tag+i word', prev, context[i])
        add('i-1 word', context[i - 1])
        add('i-1 suffix', context[i - 1][-3:])
        add('i-2 word', context[i - 2])
        add('i+1 word', context[i + 1])
        add('i+1 suffix', context[i + 1][-3:])
        add('i+2 word', context[i + 2])
        return features

    def _make_tagdict(self, sentences):
        '''Make a tag dictionary for single-tag words.'''
        counts = defaultdict(lambda: defaultdict(int))
        for words, tags in sentences:
            for word, tag in zip(words, tags):
                counts[word][tag] += 1
                self.classes.add(tag)
        freq_thresh = 20
        ambiguity_thresh = 0.97
        for word, tag_freqs in counts.items():
            tag, mode = max(tag_freqs.items(), key=lambda item: item[1])
            n = sum(tag_freqs.values())
            # Don't add rare words to the tag dictionary
            # Only add quite unambiguous words
            if n >= freq_thresh and (float(mode) / n) >= ambiguity_thresh:
                self.tagdict[word] = tag

    def APTaggerTraining(self):
        AP_tagger = AP_Tagger(False)
        # to train the averaged perceptron tagger
        print 'Loading corpus...'
        training_data = []
        training_sentence = ([], [])

        # put every line into training data
        for sent in open('dataAP/train.txt'):
            w_list = sent.split('\t')
            training_sentence[0].append(w_list[0])
            training_sentence[1].append(w_list[1])
            if w_list[0] == '.':
                training_data.append(training_sentence)
                training_sentence = ([], [])
        print 'training corpus size : %d', len(training_data)
        print 'Start training...'
        AP_tagger.train(training_data, save_loc=PICKLE)

    def APTaggerTesting(self):
        AP_tagger = AP_Tagger(False)
        AP_tagger.load(PICKLE)
        print 'Testing Averaged Perceptron with a simple sentence : "I saw the cat?" '
        print "AP TAG SEQUENCE", AP_tagger.tag("I saw the cat ?")

        right = 0.0
        total = 0.0
        test_sentence = ([], [])
        for line in open('dataAP/test.txt'):
            params = line.split()
            if len(params) != 2: continue
            test_sentence[0].append(params[0])
            test_sentence[1].append(params[1])
            if params[0] == '.':
                text = ''
                words = test_sentence[0]
                tags = test_sentence[1]
                for i, word in enumerate(words):
                    text += word
                    if i < len(words): text += ' '
                outputs = AP_tagger.tag(text)
                assert len(tags) == len(outputs)
                total += len(tags)
                for o, t in zip(outputs, tags):
                    if o[1].strip() == t: right += 1
                test_sentence = ([], [])
        print "ACCURACY: %.2f%%" % (100 * right / total)
