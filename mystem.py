# -*- coding: utf-8 -*-

import json
from pymystem3 import Mystem
from nltk.tokenize import sent_tokenize, word_tokenize
import time
start_time = time.time()

#m._disambiguation == True    # homonymy is enabled by default
# m.HOMONYMS_DETECTION = True # homonymy is enabled by default (the second way)

text = """
И они хотели, чтобы мама непременно мыла в классе полы. 
Мы вошли в дом втроём: я, сын, собака.
Еще видны остатки рва, который окружал крепость со стороны суши.
Какая в Москве будет погода, меня абсолютно не волнует.
Это не вранье, не небылица: Видели другие, видел я.
Неужели всевидящее око окончательно померкло для него?
Карамельки, сахар и мыло отпускали в магазине, пахло же ― керосином.
Я ехал домой.
Огни, светящиеся за окном.
Ты говоришь какую-то лабуду.
«Хуй на блюде» ― написано прямо поверх одной из картин.
А только что мне сказали: Олег, ты бледный як смерть!
Россия должна стать самой привлекательной для жизни страной.
Шо ты тут стоишь?
Так поражает молния, так поражает финский нож!
Она кривляется.
Они должны рассчитаться!
Канада, Сингапур, США, Финляндия и Англия расширяют количество онлайновых правительственных сервисов.
Я в моменте!
Завтра пойду забирать очки.
Хотя я и гопник, но перед законом чист. 
Сиреневенькая глазовыколупывательница строго посмотрела.
Но третью партию я завтра печь больше не готова.
Побойся Бога своего!
И он сказал: “Суши весла!”.
Путин подписал указ о нерабочих днях с 30 октября по 7 ноября.
Ща приду.
Смеемся над властью, над тупой местной бюрократией, над порядком вещей, которому вроде должны были служить. 
Станет речка голубей.
На площади видно стаю голубей.
"""



text = sent_tokenize(text)
m = Mystem()



for sentence in text:
    print("------------------------------------------------")
    print(sentence)
    lemmas = m.lemmatize(sentence)
    print(''.join(lemmas),"\n")
    data = m.analyze(sentence)
    for word in data:
        analysis = word.get('analysis', None)
        if analysis:
            best = analysis[0]
            gr = best['gr']
            t = best['lex']
            print(t,":", gr)
print("--- %s seconds ---" % (time.time() - start_time))

print (json.dumps(m.analyze(text), ensure_ascii = False))



# text1 = """Misha buries himself in the hay. Gone is the blue day. The hay is greenish, hazy.
# """

# text1 = sent_tokenize(text1)
# print(text1)

# for x in text1:
#     tex = word_tokenize(x)
#     print(tex)
