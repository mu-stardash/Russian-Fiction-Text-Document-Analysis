# -*- coding: utf-8 -*-

import PySimpleGUI as sg
from urllib import request
from bs4 import BeautifulSoup
from direct_speech import direct_speech
from temp import actions_character
from appearance import appearance_character
from pymystem3 import Mystem
from natasha import (
Segmenter, MorphVocab, NewsEmbedding, NewsMorphTagger, NewsSyntaxParser, NewsNERTagger, PER,
NamesExtractor, Doc
)


segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb) 
syntax_parser = NewsSyntaxParser(emb) 
ner_tagger = NewsNERTagger(emb)
names_extractor = NamesExtractor(morph_vocab)


def clear_window(window):
    window['link'].Update('Insert the link to the book ...')
    window['_output_'].Update('')

def search_names(text):
    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger) 
    doc.parse_syntax(syntax_parser)   
    doc.tag_ner(ner_tagger)   
    
    for span in doc.spans: 
        span.normalize(morph_vocab)
    
    for span in doc.spans: 
        if span.type == PER:
            span.extract_fact(names_extractor)   
    
    output = []        
    for s in {_.normal: _.fact.as_dict for _ in doc.spans if _.fact}: 
        output.append(s)
    
    nameSet = set()
        
    for n in output:
        string = ' '.join(n.split()) 
        m = Mystem()
        lemmas = m.lemmatize(string)
        phrase = []
    
    
        for l in lemmas:
            if not l[0].isalpha(): 
                continue
            phrase.append(l.title())
       
        f_name = ' '.join(phrase) 
        nameSet.add(f_name)
    
    names = []
    for x in nameSet: 
        names.append(x)
    return names

def load_link(values, window):
    # url = values['link']

    # if url.find('http://') == -1:
    #     print("Incorrect!")
    #     window['link'].Update('Insert the link to the book ...')
    #     return
    
    # response=request.urlopen(url)

    # soup = BeautifulSoup(response, 'lxml')
    # soup=soup.findAll('p',class_='tab')
    # text=''
    # for i in soup:
    #     text+=i.getText().rstrip()
    
    text ="""Красивая Маша в розовой кофте лежала на кровати и мерила температуру. Уставший Петя тоже мерил температуру, вытянув ноги на спинку, и читал газету.
– Все то же, – сказала испуганная Маша, посмотрев на градусник.
– Ну и ладно, – прошептал Иван.
– Дамы и господа, – сказала Маша.
– Ну и хорошо!
– Ты абсолютно прав."""

    names = search_names(text)
    for name in names:
        print("Name: ", name)
        direct_speech(text, name)
        appearance_character(text, name)
        actions_character(text, name)
        print("\n")
        for i in range(133):
            print("-", end = '')
        print("\n")


# ------------------- Create the window -------------------
def make_window(theme='DarkBrown2'):
    if theme:
        sg.theme(theme)
    # -----  Layout & Window Create  -----
    right_click_menu = ['&Right', ['Copy', 'Paste', 'E&xit']]
    layout = [
    [ sg.Text('Take the link to the book, for example, from this site:', font=("Helvetica", 14), right_click_menu=right_click_menu)],
    [ sg.Input('http://shmelev.lit-info.ru/shmelev/proza/solnce-mertvyh/solnce-mertvyh.htm', key = 'link', font=("Helvetica", 12), size = (67, 5)),
      sg.Button("Add", font=("Helvetica", 12), button_color=('white', 'green'), size = (5, 1)) ],
    [ sg.Output(font=("Helvetica"), key = "_output_", size=(100, 25))],
    [ sg.Exit(button_color=('white', 'green'), size = (5, 1)), sg.Button("Clear", button_color=('white', 'green'), size = (5, 1)),
      sg.Combo(sg.theme_list(), pad=((325, 0), (0, 0)), default_value ='Change theme', tooltip = "Change them",  key='_Method_', size=(20, 7)),
      sg.Button('Apply', pad=((25, 0), (0, 0)), font=("Helvetica", 12), button_color=('white', 'green'), size = (5, 1), key='_Apply_')]
     ]

    return sg.Window('Dossier', layout, location=(0, 0), size=(700, 570), grab_anywhere=True)


# ------------------- Main Program and Event Loop -------------------
def main():
    window = make_window()

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break
        if event == '_Apply_':
            # ---- Switch to your new theme! ---- IMPORTANT PART OF THE PROGRA<
            window.close()
            window = make_window(values['_Method_'])
        if event == 'Add':
            load_link(values, window)
            

    window.close()


if __name__ == '__main__':
    main()
