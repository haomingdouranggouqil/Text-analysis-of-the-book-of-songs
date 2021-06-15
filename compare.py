import thulac
import pkuseg
import jieba
import re
test = ["关关雎鸠，在河之洲。窈窕淑女，君子好逑。","参差荇菜，左右流之。窈窕淑女，寤寐求之。","求之不得，寤寐思服。悠哉悠哉，辗转反侧。","参差荇菜，左右采之。窈窕淑女，琴瑟友之。","参差荇菜，左右芼之。窈窕淑女，钟鼓乐之。"]

word_list = []
seg = pkuseg.pkuseg()
for sentence in test:
    word = seg.cut(sentence)
    word_list += word
print(word_list)

textall = []
thu1 = thulac.thulac(seg_only=True)
for sentence in test:
    text = thu1.cut(sentence, text=True)
    textlist = re.split('。|，|！| |？',text)
    textall += textlist
print(textall)

text = []
for sentence in test:
    word = jieba.cut(sentence)
    text += word
print(text)
