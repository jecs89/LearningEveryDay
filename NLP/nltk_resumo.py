## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
## %% Utilizando processamento de linguagem natural para criar um sumarização automática de textos
## %% Source: https://medium.com/@viniljf/utilizando-processamento-de-linguagem-natural-para-criar-um-sumariza%C3%A7%C3%A3o-autom%C3%A1tica-de-textos-775cb428c84e
## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
## %% Modified by jecs89
## %% website: https://www.researchgate.net/profile/Josimar_Chire/
## %% github: https:##github.com/jecs89/EA
## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
## %% DON'T FORGET THE CREDITS OF THE CODE
## %% IF YOU ARE INTERESTED TO PERFORM EXPERIMENTS
## %% WRITE ME AND WE CAN DISCUSS
## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

## You must install nltk
## beautifulsoup4
## and download some packages, go to the link.

from urllib.request import Request, urlopen

link = Request('http:##ultimosegundo.ig.com.br/brasil/2017-11-24/eua-vice-consul-baleada-rj.html',
               headers={'User-Agent': 'Mozilla/5.0'})
pagina = urlopen(link).read().decode('utf-8', 'ignore')

from bs4 import BeautifulSoup

soup = BeautifulSoup(pagina, "lxml")
texto = soup.find(id="noticia").text

from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize

sentencas = sent_tokenize(texto)
print(sentencas)
palavras = word_tokenize(texto.lower())
print(palavras)

from nltk.corpus import stopwords
from string import punctuation

stopwords = set(stopwords.words('portuguese') + list(punctuation))
palavras_sem_stopwords = [palavra for palavra in palavras if palavra not in stopwords]
print(palavras_sem_stopwords)

from nltk.probability import FreqDist

frequencia = FreqDist(palavras_sem_stopwords)
for fr in frequencia:
	print(fr)

print('------------------------------\n')
print(frequencia.most_common(50))

from collections import defaultdict

sentencas_importantes = defaultdict(int)

for i, sentenca in enumerate(sentencas):
    for palavra in word_tokenize(sentenca.lower()):
        if palavra in frequencia:
            sentencas_importantes[i] += frequencia[palavra]

from heapq import nlargest

idx_sentencas_importantes = nlargest(4, sentencas_importantes, sentencas_importantes.get)

for i in sorted(idx_sentencas_importantes):
    print(sentencas[i])




