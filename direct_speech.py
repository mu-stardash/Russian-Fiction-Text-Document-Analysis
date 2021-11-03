# -*- coding: utf-8 -*-
import re
import pymorphy2
from nltk import tokenize

def direct_speech(text, name):   

    last = []
    
    # Function for finding phrases - character descriptions
    def phrases(i, sent):
        #i = 0
        string_phrase = []
        proverka = []
        
        u = 0
        while i + u < len(sentences):
            proverka.clear()
            k = sentences[i + u]
            for j in mylist:
                if k.find(j) != -1 and j not in last:
                    string = ' ' + k
                    if string not in string_phrase:
                        string_phrase.append(string)
                        proverka.append(string)
                        last.append(j)
            if len(proverka) == 0:
                break
            else:
                # i += 1
                u += 2
        return string_phrase
       
    
    dict={}
    
    text2 = re.findall('(\–|\"|\'|\«)(.+?)(\!|\?|\,|\.{3}|\.|\"|\'|\»)', text)
    
    # Divide the text into sentences
    sentences = tokenize.sent_tokenize(text)
    
    # Creating a dictionary of sentences in which names occur
    dictionary = {}
    morph = pymorphy2.MorphAnalyzer()
    
    for s in sentences:
        current = "".join(c for c in s if c not in ('!','.',':',',','?','—','–','«','»',";","/","\\",")","(","\""))
        words = current.strip().split() 
        for word in words:
            p = morph.parse(word)[0]
            if (p.normal_form.title() == name):
                if p.normal_form.title() == name:
                    name2 = word
                list = [s]
                if name2 in dictionary:
                    dictionary[name2].extend(list)
                else:
                    dictionary[name2] = list
    
    # Если что посмотри у Кати вывод
    # print('\n')
    # for key, value in dictionary.items():
    #     print('{0}: {1}'.format(key, value), '\n')
    
    # Check that all direct speeches begin with a capital letter in 
    # the found sentences with regular expressions (not the words of the author)
    mylist = []
    for x in text2:
        kort=x[1]
        z=kort[1]
        if z.isupper():
            mylist.append(''.join(x))
    # print('\n'.join(mylist))
    
    
    all_phrases = set()
    
    
    i = 0 # this is responsible for the position of the sentence in the text. Get an index from text (tokenized text)
    for key, value in dictionary.items():
        dict[key]=[]
        for sent in value:
            i = sentences.index(sent)
            string_from_func = ' '.join(phrases(i, sent))
            # i += 1
            if string_from_func == '':
                        continue
            dict[key].append(string_from_func)
            all_phrases.add(string_from_func)
            
    # print('\n')
    # print(all_phrases)
    # print('\n')
    print("Direct speech:")
    for key, value in dict.items():
        print('{0}: {1}'.format(key, value), '\n')
