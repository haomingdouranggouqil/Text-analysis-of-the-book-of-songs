# coding=utf-8
from snownlp import SnowNLP
import re
test = ["关关雎鸠，在河之洲。窈窕淑女，君子好逑。","参差荇菜，左右流之。窈窕淑女，寤寐求之。","求之不得，寤寐思服。悠哉悠哉，辗转反侧。","参差荇菜，左右采之。窈窕淑女，琴瑟友之。","参差荇菜，左右芼之。窈窕淑女，钟鼓乐之。"]
def cal_emo(test):
    poemstr = ''
    poem_sentence_list = []
    for i in test:
        poemstr += i
    poem_sentence_list = re.split(r'[，。！？]', poemstr)
    del(poem_sentence_list[-1])
    print(poem_sentence_list)
    emotion = 0
    lens = 0
    for sentence in poem_sentence_list:
        if len(sentence) > 1:
            s = SnowNLP(sentence)
            print(s.sentiments)
            emotion += s.sentiments
            lens += 1
    emotion = emotion / lens
    print(emotion)

def mean_emo(poem):
    all_emo = 0
    for i in poem:
        all_emo += cal_emo
    all_emo = all_emo / len(poem)
    return all_emo

t = "疫情期间的大学就像婚姻——里面的人想出来，外面的人想进去。在学校，我们能享受到国王一般的待遇。风能进，雨能进，学生不能进；游客能出，快递能出，学生不能出。区别是，在家你可以随时申请返校，在学校你却不能申请回家。（我们一般称这种返校政策为“请君入瓮”）学校会议上要讨论两个话题，一个是十一假期的防疫工作，一个是学校闭环管理的审批策略。因为学生一律不得出门，所以直接散会。在2019年，游客试图装作学生混进校园。在2020年，学生需要装作游客返校上课。一名学生到了学校门前，却无法进入，百般无奈之下向辅导员求助。”返校后，学生抱怨宿舍生老鼠。今年，当大家都在吐槽只有学生不能进学校时，他决定把学生关在学校里不让出去"

print(len(t))
cal_emo(t)
s = SnowNLP(t).sentiments
print(s)
