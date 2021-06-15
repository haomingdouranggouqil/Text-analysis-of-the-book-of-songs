import json
import pkuseg
import matplotlib.pyplot as plt
from wordcloud import WordCloud
def clean(path):
    #传入诗歌文本json路径，返回纯文本（无作者题目）字符串
    cleantxt = ''
    f = open(path, 'r', encoding='UTF-8',errors = 'ignore')
    content = f.read()
    context = json.loads(content)
    for poem in context:
        for sentence in poem['content']:
            cleantxt += sentence
    f.close()
    return cleantxt


def remove_punctuation(contextstr):
    #传入纯文本字符串，返回单字为元素且无标点的文字列表
    punctuation = "，。！？、 （）【】<>《》=：+-*—“”…\n"
    character_clean = []
    for character in contextstr:
        if character in punctuation:
            pass
        else:
            character_clean.append(character)
    return character_clean

def character_number(remove_list):
    #传入文字列表，输出字数
    return len(remove_list)

def single_number(remove_list):
    #传入文字列表，输出不同字数
    character_set = set(remove_list)
    return len(character_set)

def character_sort(character_list):
    #传入文字列表，输出对应排序字典
    character_dict = {}
    for character in character_list:
        if character not in character_dict:
            character_dict[character] = 1
        else:
            character_dict[character] += 1

    sorted_character = sorted(character_dict.items(), key=lambda x:x[1],  reverse=True)
    return sorted_character

def sort_txt(path):
    #整合函数，输入路径，输出排序字典
    sj_cleantxt = clean(path)
    sj_remove = remove_punctuation(sj_cleantxt)
    sj_sorted_character = character_sort(sj_remove)
    return sj_sorted_character

def show_outcome(outcome_list, n):
    #传入字频结果列表，输出前n个结果
    for i in range(n):
        sort_show = outcome_list[i][0] + "    " + str(outcome_list[i][1])
        print(sort_show)

def character_main(path):
    #关于字数总函数
    sorted_character_outcome = sort_txt(path)
    sj_cleantxt = clean(path)
    sj_remove = remove_punctuation(sj_cleantxt)
    print('诗经总字数')
    print(character_number(sj_remove))
    print('诗经不同字数')
    print(single_number(sj_remove))
    print('诗经前20字频')
    show_outcome(sorted_character_outcome, 20)


#字数函数功能结束，以下词频功能函数

def seg_word(path):
    #因需求输入不同，故从头开始提取数据，放入列表，由pku分词
    cleantxt = []
    f = open(path, 'r', encoding='UTF-8',errors = 'ignore')
    content = f.read()
    context = json.loads(content)
    for poem in context:
        for sentence in poem['content']:
            cleantxt.append(sentence)
    f.close()
    #初始化pku分词
    word_list = []
    seg = pkuseg.pkuseg()
    for sentence in cleantxt:
        word = seg.cut(sentence)
        word_list += word
    return word_list

def sort_word(path):
    #传入路径，输出词频
    word_list = seg_word(path)
    clean_word_list = []
    for word in word_list:
        if len(word) == 1:
            pass
        else:
            clean_word_list.append(word)
    sorted_list = character_sort(clean_word_list)
    return sorted_list

#词云自动分词，不能生成字云
def word_cloud(pku_word):
    #传入pku分词结果，生成字云
    sj_word = ' '.join(pku_word)
    pku_cloud = WordCloud(scale=64, font_path = "青鸟华光简隶变.ttf").generate(sj_word)
    plt.imshow(pku_cloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig('wordcloud.png', dpi = 4000)
    plt.show()


def word_main(path):
    sj_word_list = sort_word(path)
    print('诗经前20非单字词频')
    show_outcome(sj_word_list, 20)
    sj_pku_seg = seg_word('shijing.json')
    word_cloud(sj_pku_seg)

#提取高频字
def get_freq(p):
    sj_cleantxt = clean('shijing.json')
    sj_remove = remove_punctuation(sj_cleantxt)
    raw_num = character_number(sj_remove)
    target_num = raw_num * p
    sj_sorted_character = character_sort(sj_remove)
    frequent_list = []
    character_times = 0
    for character in sj_sorted_character:
        frequent_list.append(character[0])
        character_times += character[1]
        if character_times >= target_num:
            break
    return frequent_list

def draw_curve():
    x = []
    y = []
    for i in range(1, 21):
        x.append(i / 20)
        y.append(len(get_freq(i / 20)))
    plt.ylabel('character number')
    plt.xlabel('frequency')
    plt.plot(x,y)
    plt.show()

if __name__ == '__main__':
    #character_main('shijing.json')
    word_main('shijing.json')
    #draw_curve()
