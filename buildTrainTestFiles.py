from nltk.corpus import conll2000, brown

f = open('dataAP/train.txt', 'w')

total = 1000
for sent in conll2000.tagged_sents():
    for word, tag in sent:
        #f.write(word + '\t' + tag + '\n')
        f.write(word + '\t' + tag + '\n')

    total -= 1
    if total == 0:
        break

print "The train.txt is generated"

f = open('dataAP/test.txt', 'w')
total = 100
for sent in conll2000.tagged_sents()[1001:1105]:
    for word, tag in sent:
        #f.write(word + '\t' + tag + '\n')
        f.write(word + '\t' + tag+'\n')

    total -= 1
    if total == 0:
        break

print "The test.txt is generated"