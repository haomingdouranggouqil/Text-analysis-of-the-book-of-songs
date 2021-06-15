import json
import re
import numpy as np
from snownlp import SnowNLP
import pkuseg
import matplotlib.pyplot as plt
from jieba.analyse import *
#分割出风雅颂
f = open('shijing.json', 'r', encoding='UTF-8',errors = 'ignore')
content = f.read()
context = json.loads(content)
feng = []
ya = []
song = []
for i in range(305):
    if i < 160:
        feng.append(context[i]['content'])
    elif i < 265:
        ya.append(context[i]['content'])
    else:
        song.append(context[i]['content'])
f.close()

#引入停用词
path = 'cn_stopwords.txt'
f = open(path, 'r', encoding='UTF-8',errors = 'ignore')
stop = f.read()
stopword = re.split(r'[\n]', stop)

def poem_character_number(poemlist):
    #传入列表，输出zong字数
    poemstr = ''
    for i in poemlist:
        poemstr += i
    punctuation = "，。！？、 （）【】<>《》=：+-*—“”…\n"
    character_clean = []
    for character in poemstr:
        if character in punctuation:
            pass
        else:
            character_clean.append(character)
    return len(character_clean)

def compare_character():
    #比较平均长度
    feng_average = 0
    ya_average = 0
    song_average = 0
    print('风部分篇目平均长度')
    for poem in feng:
        feng_average += poem_character_number(poem) / 160
    print(feng_average)
    print('雅部分篇目平均长度')
    for poem in ya:
        ya_average += poem_character_number(poem) / 105
    print(ya_average)
    print('颂部分篇目平均长度')
    for poem in song:
        song_average += poem_character_number(poem) / 40
    print(song_average)

def variance(poemlist):
    poemstr = ''
    poem_sentence_list = []
    poem_sentence_number = []
    for i in poemlist:
        poemstr += i
    poem_sentence_list = re.split(r'[，。！？]', poemstr)
    #del(poem_sentence_list[-1])
    for i in poem_sentence_list:
        poem_sentence_number.append(len(i))
    return np.var(poem_sentence_number)

def compare_variance():
    feng_variance = 0
    ya_variance = 0
    song_variance = 0
    print('风部分篇目平均方差')
    for poem in feng:
        feng_variance += variance(poem) / 160
    print(feng_variance)
    print('雅部分篇目平均方差')
    for poem in ya:
        ya_variance += variance(poem) / 105
    print(ya_variance)
    print('颂部分篇目平均方差')
    for poem in song:
        song_variance += variance(poem) / 40
    print(song_variance)

def remove_stop(poem_list):
    word_list = []
    clean_list = []
    seg = pkuseg.pkuseg()
    for sentence in poem_list:
        word = seg.cut(sentence)
        word_list += word
    for word in word_list:
        if word in stopword:
            pass
        else:
            clean_list.append(word)

def cal_emo(test):
    poemstr = ''
    poem_sentence_list = []
    for i in test:
        poemstr += i
    poem_sentence_list = re.split(r'[，。！？]', poemstr)
    del(poem_sentence_list[-1])
    emotion = 0
    for sentence in poem_sentence_list:
        s = SnowNLP(sentence)
        emotion += s.sentiments
    emotion = emotion / len(poem_sentence_list)
    return emotion

def mean_emo(poem):
    all_emo = 0
    for i in poem:
        all_emo += cal_emo(i)
    all_emo = all_emo / len(poem)
    return all_emo

def draw_emotion(poem):
    x = range(len(poem))
    y = []
    for i in poem:
        y.append(cal_emo(i))
    plt.ylabel('number')
    plt.xlabel('emotion value')
    plt.plot(x,y)
    plt.show()

def topic(poem):
    seg = pkuseg.pkuseg()
    word_list = []
    for i in poem:
        for j in i:
            word = seg.cut(j)
            word_list += word
    poemstr = ' '.join(word_list)
    keyword = []
    for i in extract_tags(poemstr, topK=64, withWeight=True):
        keyword.append(i[0])
    return keyword

if __name__ == '__main__':
    #compare_character()
    #compare_variance()
    sj = feng + ya + song
    print(mean_emo(sj))
    #draw_emotion(ya)
    #sj_key = topic(sj)
    #print(sj_key)
