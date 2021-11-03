from razdel import sentenize, tokenize
from navec import Navec
from slovnet import Syntax

def actions_character(text, name):

    chunk = []
    slovar = []

    navec = Navec.load('navec_news_v1_1B_250K_300d_100q.tar')
    syntax = Syntax.load('slovnet_syntax_news_v1.tar')
    syntax.navec(navec)

    for sent in sentenize(text):
        slovar.append(sent)
        tokens = [_.text for _ in tokenize(sent.text)]
        chunk.append(tokens)
        chunk[:1]


    words, deps = [], []
    prov = 0
    print("Character actions:")
    for markup in syntax.map(chunk):
        for token in markup.tokens:
            words.append(token.text)
            source = int(token.head_id) - 1
            target = int(token.id) - 1
            if source > 0 and source != target:  # skip root, loops
                deps.append([source, target, token.rel])
    # show_markup(words, deps)
    # print(deps)
        for i in range(len(deps)):
            if words[deps[i][1]] ==name: # if this is a name
                prov = words[deps[i][0]] # we save the word from which the connection was built
                print(words[deps[i][1]], words[deps[i][0]], end = ', ') # we output the name and the word from which the connection comes
            if i+1 < len(words):
                if words[i] +" "+ words[i+1] ==name: # if we haven't found the name, look at the neighboring words and add them to the first one
                    name = words[i] +" "+ words[i+1]
                    prov = words[deps[i][0]]
                    print(name, words[deps[i][0]], end = ', ')        
            if i+2 < len(words):        
                if words[i] +" "+ words[i+1] +" "+ words[i+2] ==name: # if you did not find the name, then look at the neighboring words and add to the first and add the following full name
                    name = words[i] +" "+ words[i+1] +" "+ words[i+2]
                    prov = words[deps[i][0]]
                    print(name, words[deps[i][0]], end = ', ')
            
            
            if words[deps[i][0]] == prov and deps[i][2] == 'conj' or deps[i][2] == 'xcomp': # if the arrow is from the connecting word and the connection is 'conj' or 'xcomp'
                print(words[deps[i][1]] + "\n")
        
        words.clear()
        deps.clear()
        
    #print(otvet)

# deps stores the links between words and the name of the link
# words stores the text divided into tokens
