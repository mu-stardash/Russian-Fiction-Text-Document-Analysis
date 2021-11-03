# Russian-Fiction-Text-Document-Analysis
NLP project at the university of Oulu, autumn 2021

The project was carried out by two students Daria Efimova, Polina Chainikova

To run the program, you need to put some files in one folder and install the libraries.
The following libraries were used in these programs (to install them, enter the pip install command in the command line. For example: pip install pymorphy2): 
- pymorphy2
- pymystem3
- nltk
- time
- bs4
- urlib
- numpy
- re
- PySimpleGUI
- natasha
- string

The main file is interface_NLP.py, which must be run. For this, such environments as Anaconda (Spyder), Visual Studio Code can be used.
interface_NLP.py creates a program interface and handles push buttons. You can try to insert, for example, works from this site: http://shmelev.lit-info.ru/shmelev/proza/solnce-mertvyh/solnce-mertvyh.htm
After adding the link, click Add and the program will start its work (you should wait about 3-5 minutes! Don't worry if the app says "Not responding"). 

Along with the main file, the following files should be present in the folder:
- appearance.py is an algorithm for finding the appearance of characters
- direct_speech.py - an algorithm for finding direct speech
- temp.py - an algorithm for looking for actions.

Since temp.py and appearance.py use two dictionaries Navec and Slovnet for parsing, you must download and add the archives of these dictionaries to the same folder.
- To download Navec: https://github.com/natasha/navec (download navec_news_v1_1B_250K_300d_100q.tar, it is located in the Readme section)
- To download Slovnet: https://github.com/natasha/slovnet (download slovnet_ner_news_v1.tar, it is located in the Readme section)

In the files names_rules.py, names_Natasha.py, algorithms for finding names are implemented. For the first file, this is a search using independently compiled rules, for the second, using the Natasha library. You can use them to compare how algorithms work on different texts. Also, in these files, graphs of the occurrence of names are built using the FreqDist module from nltk.probability.

In the files pymorphy_2.py, mystem.py, morphological parsing of sentences and lemmatization of words are implemented. The first file uses the Pymorphy2 analyzer, the second uses the Pymystem3. You can use them to compare how algorithms work on different texts.

You can read the detailed work of the algorithms in the report.
