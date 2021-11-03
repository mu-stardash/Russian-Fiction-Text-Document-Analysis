# -*- coding: utf-8 -*-

from os import name

import pymorphy2
import string
import nltk
from urllib import request
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.probability import FreqDist


nltk.download('stopwords') 
from nltk.corpus import stopwords
stop = set(stopwords.words("russian")) 
 
nltk.download('punkt')
prob_thresh = 0.30
morph = pymorphy2.MorphAnalyzer()
 

url="http://shmelev.lit-info.ru/shmelev/proza/rasskaz/lihoradka.htm"
# url = "http://tolstoy-lit.ru/tolstoy/vospominaniya/shmelev-kak-ya-hodil-k-tolstomu.htm"
response=request.urlopen(url)

soup = BeautifulSoup(response, 'lxml')
soup=soup.findAll('p',class_='tab')
text=''
for i in soup:
    text+=i.getText().rstrip()

names = []
marks = str.maketrans(dict.fromkeys(string.punctuation)) # убирает знаки препинания 
without_marks = text.translate(marks)
text1 = without_marks.split()
 
processed_text = [x for x in text1 if not x in stop] # убирает стоп слова
output = set()
i = 0
while i < len(processed_text):
  for p in morph.parse(processed_text[i]): 
    if i+1 < len(processed_text) and processed_text[i].istitle() == True  and ('Name' in p.tag or 'Surn' in p.tag or 'Patr' in p.tag ) and 'NOUN' in p.tag and 'anim' in p.tag and p.score >= prob_thresh: 
      first = morph.parse(processed_text[i])[0]
      first = first.normal_form
      for p in morph.parse(processed_text[i + 1]):
          if i+1 < len(processed_text):
              if processed_text[i+1].istitle() == True  and ('Name' in p.tag or 'Surn' in p.tag or 'Patr' in p.tag ) and 'NOUN' in p.tag and 'anim' in p.tag and p.score >= prob_thresh: 
                  second = morph.parse(processed_text[i+1])[0]
                  second = second.normal_form
                  for p in morph.parse(processed_text[i + 2]):
                      if i+2 < len(processed_text):
                          if processed_text[i+2].istitle() == True  and ('Name' in p.tag or 'Surn' in p.tag or 'Patr' in p.tag ) and 'NOUN' in p.tag and 'anim' in p.tag and p.score >= prob_thresh: 
                              third = morph.parse(processed_text[i+2])[0] 
                              third = third.normal_form
                              output.add(first + " " + second + " " + third)
                              names.append(first + " " + second + " " + third)
                              i += 3
                              break
                          else: 
                              output.add(first + " " + second)
                              names.append(first + " " + second)
                              i += 2
                              break
              else:
                  output.add(first)
                  names.append(first)
                  break
    i += 1
 
list = []


fd = FreqDist(names)
print(fd.most_common(50))
for line in output: 
    if line not in list:
        list.append(line)
with open('output.txt', 'w', encoding='utf-8') as out:
    out.write('\n'.join(list).title())
print(output)
print(names)

fd.plot(50)
