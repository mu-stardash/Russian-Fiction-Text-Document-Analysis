# -*- coding: utf-8 -*-

from natasha import (
    Segmenter,
    MorphVocab,

    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,

    PER,
    NamesExtractor,

    Doc
)

from pymystem3 import Mystem

import nltk
import numpy as np
from urllib import request
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize,word_tokenize
from textblob import TextBlob
from nltk.probability import FreqDist
import matplotlib.pyplot as plt

import pymorphy2
morph = pymorphy2.MorphAnalyzer()

# you can use another link on text
url="http://shmelev.lit-info.ru/shmelev/proza/rasskaz/lihoradka.htm"
response=request.urlopen(url)

soup = BeautifulSoup(response, 'lxml')
soup=soup.findAll('p',class_='tab')

text=''
for i in soup:
    text+=i.getText().rstrip()

toc = word_tokenize(text)

m = Mystem()
segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)
names_extractor = NamesExtractor(morph_vocab)

output = []
names = []

doc = Doc(text)
doc.segment(segmenter)
doc.tag_morph(morph_tagger)
doc.parse_syntax(syntax_parser)
doc.tag_ner(ner_tagger)

matches = names_extractor(text)

for span in doc.spans:
    span.normalize(morph_vocab)

for span in doc.spans:
  if span.type == PER:
    span.extract_fact(names_extractor)
    output.append(span.text)
 
   
list = []
with open('output.txt', 'w', encoding='utf-8') as out:
    for line in output: 
        # lemmas = morph.parse(line)[0] #fast
        # lemmas = lemmas.normal_form
        lemmas = m.lemmatize(line) # longer
        names.append(''.join(lemmas))
        if ''.join(lemmas) not in list:
            list.append(''.join(lemmas))
    out.write(''.join(list).title())

print(list, "\n")    
   
# graphic
fd = FreqDist(names)
print(fd.most_common(50))

fd.plot(50)
