from nltk.corpus import conll2000

f = open('train.txt', 'w')

total = 1000
for sent in conll2000.tagged_sents():
    for word, tag in sent:
        f.write(word + '\t' + tag + '\n')

    total -= 1
    if total == 0:
        break

f = open('test.txt', 'w')
total = 100
for sent in conll2000.tagged_sents()[1001:1105]:
    for word, tag in sent:
        f.write(word + '\t' + tag + '\n')

    total -= 1
    if total == 0:
        break
