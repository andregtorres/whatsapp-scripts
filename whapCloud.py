
#!/usr/bin/env python
#Generates a wordcloud from a exported whatsapp chat
#3/06/2018

from os import path
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image
import emoji
import re
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

#d = path.dirname(__file__)
d="./"
# Read the whole text.
text=""
#f= open(path.join(d, '../wappStats/310118.txt'))
f= open(path.join(d, 'agatka.txt'))

i=0
for line in f:
    if i ==0:
        print(line, datetime.strptime(line[0:15].rstrip(" "),'%d/%m/%y, %H:%M'), line[18:],"".join(line[18:].split(": ")[1:]).rstrip("\n"))
    try:
        date=datetime.strptime(line[0:15].rstrip(" "),'%d/%m/%y, %H:%M')
        restOfLine="".join(line[18:].split(": ")[1:]).rstrip("\n")
    except: #messages with \n (date fails)
        restOfLine=line.rstrip("\n")
    if (restOfLine != "<Media omitted>"):
        for word in restOfLine.split():
            decode= word#.decode('utf-8')
            good= True
            for c in decode:
                if c in emoji.UNICODE_EMOJI:
                    good= False
                    break
            if good:
                text+=(''.join(decode))
                text+=(" ")
                i+=1
                #print(i)
#print text


stopwords = set(STOPWORDS)
stopwords.add("ye")
stopwords.add("know")
stopwords.add("one")
stopwords.add("lot")
stopwords.add("tell")
stopwords.add("say")
stopwords.add("think")
stopwords.add("yes")
stopwords.add("will")
stopwords.add("maybe")
stopwords.add("even")
stopwords.add("still")
stopwords.add("now")
stopwords.add("really")
stopwords.add("later")
#stopwords.add("ok")
#stopwords.add("going")
stopwords.add("go")
#stopwords.add("well")
stopwords.add("nd")
#stopwords.add("yeah")
stopwords.add("got")
stopwords.add("'m'")
stopwords.add("o")
stopwords.add("ut")
stopwords.add("ou")
stopwords.add("ricardo")
stopwords.add("aby")
stopwords.add("'m'")
stopwords.add("t's")
#print stopwords



# Initializing Dictionary
dic = {}

# Count number of times each word comes up in list of words (in dictionary)
for word in text.split():
    if word.lower() not in stopwords:
        if word not in dic:
            dic[word] = 0
        dic[word] += 1
word_freq = []
for key, value in dic.items():
    word_freq.append((value, key))
word_freq.sort(reverse=True)

# read the mask image
h_mask = np.array(Image.open(path.join(d, "blue.png")))


wc = WordCloud(background_color="white", max_words=10000, mask=h_mask,
               stopwords=stopwords)
# generate word cloud

#print wc.process_text(text)
#print dic

wc.generate_from_frequencies(dic)
#wc.generate_from_frequencies(wc.process_text(text))
#wc.generate(text)

# create coloring from image
image_colors = ImageColorGenerator(h_mask)

# store to file
wc.recolor(color_func=image_colors).to_file(path.join(d, "wordcloudtest.png"))

# show
#plt.imshow(wc, interpolation='bilinear')

plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
plt.axis("off")
#plt.figure()
#plt.imshow(h_mask, cmap=plt.cm.gray, interpolation='bilinear')
#plt.axis("off")
plt.show()
