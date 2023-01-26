import math
import re
from collections import defaultdict
import stop_list as stop_l
import numpy as np
from nltk.stem import PorterStemmer
the_stem = PorterStemmer()
valus = defaultdict(lambda: defaultdict(float))

def final_calc (q_tfidf, ab_tfidf):
    bwean_val_i =0
    ab_tot = 0
    words_in_q = []
    q_t_i = []
    ab_val = []
    valus = defaultdict(lambda: defaultdict(float))
    for i in q_tfidf.keys():
        q_t_i = list(q_tfidf[i].values())
        words_in_q = list(q_tfidf[i].keys())
        for ab in ab_tfidf.keys():
            for s in range(len(q_t_i)):
                bwean_val_i += q_t_i[s]**2 #1

            word_options = list(q_tfidf[i].keys())

            for word in range(len(word_options)):
                ab_idf_keys = list(ab_tfidf[ab].keys())
                if word_options[word] in ab_idf_keys:
                    ab_as = ab_tfidf[ab][word_options[word]]
                    ab_val.append(ab_as)
                else:
                    ab_val.append(0)

            for m in range(len(ab_val)):
                ab_tot += ab_val[m]**2


            final_score = 0
            sim_exists = False
            if np.sqrt(bwean_val_i * ab_tot) != 0:
                sim_exists = True
            if (sim_exists):
                final_score = np.dot(q_t_i, ab_val) / np.sqrt(bwean_val_i * ab_tot)

            ab_val = []

            valus[i][ab] = final_score

    for i in valus.keys():
        valus[i] = {bro: go for bro, go in sorted(valus[i].items(), key=lambda item: item[1], reverse=True)}

    return valus




#     Some more example of stemming for root word "like" include:
#
# -> "likes"
# -> "liked"
# -> "likely"
# -> "liking"

ytr = 0
dic = {}
with open('cran.qry', 'r') as file_obj:

    for rdl in file_obj:
        if ('.I' in rdl):

            ytr+=1

            if '.W' not in rdl:
                if ytr not in dic:
                    dic[ytr]  = list(filter(None, re.split('\W|\d', rdl.strip()))) # strip removes leading and trailing whitespace


                else:
                    dic[ytr] += list(filter(None, re.split('\W|\d', rdl.strip()))) # split will use non words as separators and basically leave you with all the words_in_q
            flag = True


        if flag==True and '.W' not in rdl:
            if ytr in dic:
                dic[ytr] += list(filter(None, re.split('\W|\d', rdl.strip())))

            else:
                dic[ytr]  = list(filter(None, re.split('\W|\d', rdl.strip())))



in_bwean = dic
for hey in dic:
    val = []
    col = dic[hey]
    length = len(col)
    for index in range(length):
        tyr = col[index]
        bwean = the_stem.stem(tyr) # HM
        if tyr in stop_l.closed_class_stop_words: # getting rid of the stop words
            print("in here")
            continue
        else:
            val.append(bwean) #.stem will give you the root word eg: ps.stem(programs) = program
    dic[hey] = val # so now dic will contain the relevant text without stop words in the form of a list where each element is a word

file_obj.close() # dic is a dict where hey is the id number and value is the relevant part of the text (thinking just abstract)
print ("function terminates here dic post mod is ", dic)
print ("pre mod is ", in_bwean)
q =  dic




ytr = 0
dic = {}
with open('cran.all.1400', 'r') as file_obj:

    for rdl in file_obj:
        if ('.I' in rdl):

            ytr+=1

            if '.W' not in rdl:
                if ytr not in dic:
                    dic[ytr]  = list(filter(None, re.split('\W|\d', rdl.strip()))) # strip removes leading and trailing whitespace


                else:
                    dic[ytr] += list(filter(None, re.split('\W|\d', rdl.strip()))) # split will use non words as separators and basically leave you with all the words_in_q
            flag = True


        if flag==True and '.W' not in rdl:
            if ytr in dic:
                dic[ytr] += list(filter(None, re.split('\W|\d', rdl.strip())))

            else:
                dic[ytr]  = list(filter(None, re.split('\W|\d', rdl.strip())))



in_bwean = dic
for hey in dic:
    val = []
    col = dic[hey]
    length = len(col)
    for index in range(length):
        tyr = col[index]
        bwean = the_stem.stem(tyr) # HM
        if tyr in stop_l.closed_class_stop_words:
            print("in here")
            continue
        else:
            val.append(bwean)
    dic[hey] = val

file_obj.close()
print ("function terminates here dic post mod is ", dic)
print ("pre mod is ", in_bwean)
ab = dic



print ("Q is ",q)
#calculating tfidf scores by iterating through each word in each sentence
dic = q
lenth = 225
all_sentence = list(dic.values())
gg = {}
tfidf = defaultdict(lambda: defaultdict(float))
i = 1
for sentence in all_sentence:
    flag = True # entered here
    for word in sentence:
        if not (word in gg.keys()): #1
            check = 0
            for quote in all_sentence:
                if word in quote:
                    check += 1
            gg[word] = math.log(lenth / check)
        num = sentence.count(word)
        dum = len(sentence)
        tf = num/dum #2
        in_b = tf * gg[word]
        tfidf[i][word] = in_b

    if (flag==True):
        i += 1 # 3
q_tfidf = tfidf


dic = ab
lenth = 1400

all_sentence = list(dic.values())
gg = {}
tfidf = defaultdict(lambda: defaultdict(float))
i = 1
for sentence in all_sentence:
    flag = True # entered here
    for word in sentence:
        if not (word in gg.keys()): #1
            check = 0
            for quote in all_sentence:
                if word in quote:
                    check += 1
            gg[word] = math.log(lenth / check)
        num = sentence.count(word)
        dum = len(sentence)
        tf = num/dum #2
        in_b = tf * gg[word]
        tfidf[i][word] = in_b

    if (flag==True):
        i += 1 # 3
ab_tfidf = tfidf

scores = final_calc(q_tfidf,ab_tfidf)

with open('output.txt', 'w') as f:
    for q in scores.keys():
        for ab in scores[q].keys():
            f.write('{0}'' ''{1}'' ''{2}\n'.format(str(q), str(ab), str('{:f}'.format(scores[q][ab]))))
f.close()
