# -*- coding: utf-8 -*-

import pymorphy2
morph = pymorphy2.MorphAnalyzer()
from nltk.tokenize import sent_tokenize, word_tokenize
import time

start_time = time.time()

text = """
Myron tells it without bragging or rancor.
"""

text = sent_tokenize(text) 
    
for sent in text:
    print(sent)
    words = word_tokenize(sent)
    for word in words:
        p = morph.parse(word)[0]
        for k in morph.parse(word):
            print(p.normal_form, k.tag)
            break
    print("-----------------------------------------------------------------")
    
print("--- %s seconds ---" % (time.time() - start_time))
