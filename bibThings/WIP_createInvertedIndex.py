
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "bibThings.settings")
# Setup django project
django.setup()

from django.conf import settings


import codecs
from collections import defaultdict



"""
inv_indx = {i:[] for i in corpus_dict}
for word in corpus_dict:
    for i in range(len(docs)):
        if word in docs[i]:
            inv_indx[word].append(i)

inv_indx = defaultdict(list)
for idx, text in enumerate(docs):
    for word in text:
        inv_indx[word].append(idx)

"""

def get_first_items(L):
    first_items = []
    for member in L:
        first_items.append(member[0])
    return first_items



def intersection (L1,L2):
    result = []
    for lst in L1:
        if lst in L2:
            result.append(lst)
    return result


inv_index = defaultdict(list)

def createInvertedIndices():

    for book_name in settings.BOOK_ABBR_LIST:

        f_path = '/Users/hosoolee/Desktop/bibleBot/BibleText/KSV_woSectionTitle/' + book_name + '.txt'

        i=1 # may not need
        with codecs.open(f_path, 'r', encoding='euc-kr') as f:
            line = f.readline()

            while line:
                print("Line {}: {}".format(i, line.strip()))
                words_list = line.split(" ")
                for idx, word in enumerate(words_list):
                    #for key_word in text:
                    #    inv_index[key_word].append(i * 1000 + idx)  # 879 verses in John


                    #print(inv_index[word])
                    inv_index[word].append([words_list[0], idx])  # or [i, idx]
                    print("inv_index({}) : {}".format(word, inv_index[word]))

                line = f.readline()
                i += 1
        f.close()



    return (sorted(inv_index.items()))

invertedIndices = createInvertedIndices()
for key, value in invertedIndices:
    print("key ({}): indices:{}".format(key, value))


result=[]
for key, listOfItems in invertedIndices:
    result.append([key, get_first_items(listOfItems)])

print('RESULT', result)


print('사람으로 ', inv_index.get('사람으로'))
print('증거를 ', inv_index.get('증거를'))
print('정하신 ', inv_index.get('정하신'))

a = inv_index.get('사람으로')
b = inv_index.get('증거를')
c = inv_index.get('정하신')



r = intersection(a, b)
print(r)
rr = intersection(r, c)
print(rr)

