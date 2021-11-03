# -*- coding: utf-8 -*-

from nltk import tokenize as tok 
import pymorphy2
from razdel import sentenize, tokenize 
from navec import Navec
from slovnet import Syntax 

def appearance_character(text, name):    
    # Dividing text into sentences 
    sentences = tok.sent_tokenize(text)
    
    # Creating a dictionary of sentences in which names occur 
    dictionary = dict()
    
    morph = pymorphy2.MorphAnalyzer()
    
    
    previous = ''
    for s in sentences:
        current	=	"".join(c for c	in s if c not in ('!','.',':',',','?','—','–','«','»',";","/","\\",")","(","\""))
        words = current.strip().split() 
        for word in words:
            p = morph.parse(word)[0].normal_form.title() 
            if p == name:
                name2 = p 
                list = [s]
                if name2 in dictionary: 
                    dictionary[name2].extend(list)
                else:
                    dictionary[name2] = list
            if (previous + ' ' + p) == name: 
                name2 = previous + ' ' + p 
                list = [s]
                if name2 in dictionary: 
                    dictionary[name2].extend(list)
                else:
                    dictionary[name2] = list  
    
            previous = p
    
    
    #  Finding Character Descriptions using a Syntax Analysis
    navec = Navec.load('navec_news_v1_1B_250K_300d_100q.tar')
    syntax = Syntax.load('slovnet_syntax_news_v1.tar') 
    syntax.navec(navec)
    
    def rules_for_set(phrases_list): 
        current_set = set()
        for c in phrases_list:
            if c[len(c) - 1] == ' ':
                s = c[0:len(c) - 1:1]
            if s.find(' ') == -1 and morph.parse(s)[0].tag.POS != 'ADJF': 
                continue
            flag = 0
            for f_p in c.split():
                if morph.parse(f_p)[0].tag.POS == 'VERB' or morph.parse(f_p)[0].tag.POS == 'INFN':
                    flag = 1 
            if flag == 1:
                continue 
            current_set.add(s)
        return current_set
    
    
    dict_desc = dict()
    
    
    def descriptions_to_dict(name2, description_list): 
        set_for_each_name = rules_for_set(description_list) 
        if name2 in dict_desc:
            dict_desc[name2].extend(set_for_each_name) 
        else:
            dict_desc[name2] = set_for_each_name
    
    
    all_phrases = [] 
    gl_id = 0
    for key, value in dictionary.items(): 
        phrases_for_name = []
        p = morph.parse(key)[0] 
        chunk = []
        for s in value:
            for sent in sentenize(s):
                tokens = [_.text for _ in tokenize(sent.text)] 
                chunk.append(tokens)
            chunk[:1]
        markup = next(syntax.map(chunk))
        # Convert CoNLL-style format to source, target indices 
        w, deps = [], []
        for token in markup.tokens: 
            w.append(token.text)
            source = int(token.head_id) - 1
            target = int(token.id) - 1
            if source > 0 and source != target: # skip root, loops 
                deps.append([source, target, token.rel])
    
        for i in range(len(deps)):
            if (deps[i][2] == 'nmod' or deps[i][2] == 'acl:relcl' or deps[i][2] == 'conj' or deps[i][2] == 'acl' or deps[i][2] == 'appos'):
                current_id = deps[i][1] 
                string = ''
                idc = 0
                id_s = []
                for j in range(len(deps)):
                    if (deps[j][0] == current_id and deps[j][2] != 'punct' and deps[j][2] != 'det' and deps[j][2] != 'cc'
                        and (idc == 0 or deps[j][1] == idc + 1)
                        ):
                        string += w[deps[j][1]] + ' ' 
                        idc = deps[j][1] 
                        id_s.append(idc)
                    if (deps[j][1] == current_id):
                        if not (idc == 0 or deps[j][1] == idc + 1): 
                            string = ''
                        string += w[current_id] + ' ' 
                        idc = deps[j][1] 
                        id_s.append(idc)
    
                if (len(id_s) > 0 and id_s[0] == gl_id + 1):
                    phrases_for_name[len(phrases_for_name) - 1] += string
                else:
                    phrases_for_name.append(string) 
                if (len(id_s) > 0):
    
                    gl_id = id_s[len(id_s) - 1] 
        descriptions_to_dict(p.normal_form.title(), phrases_for_name) 
        for phrase in phrases_for_name:
            all_phrases.append(phrase)
    
    
    set_phrases = rules_for_set(all_phrases)    
    
    # print('\nФразы-описания персонажей, найденные с помощью синтаксического анализатора:')
    # for ph in set_phrases: 
    #     print(ph)
    
    print('External character description:')
    for key, value in dict_desc.items(): 
        print(key, value, end = ';')
        print('\n')
