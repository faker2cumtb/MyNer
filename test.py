import jieba
import jieba.posseg as pseg
import numpy as np

def segment(sentences):
    jieba.load_userdict("all_ents.txt")
    pseg_sentences = []
    for sentence in sentences:
        pseg_sentence = [words.word + "/" + words.flag for words in pseg.cut(sentence)]
        pseg_sentences.append(pseg_sentence)
    return pseg_sentences

print (np.array([["你","是","什","么","呢"],
          ["我","怎","么","知","道","呢"]]))

if __name__ == '__main__':
    sentences = ["你是什么呢","你说我是什么弟弟","日本索尼公司","铁道部第二工程局","我是姚明"]
    print (segment(sentences))

    with open("LOC" + ".txt", "r", encoding="utf8") as f:
        ents = f.readlines()
    print (ents)