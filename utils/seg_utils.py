import jieba.posseg as pseg
import jieba


def segment(sentences):
    """
    分词
    :param sentences:
    :return:
    """
    jieba.load_userdict("all_ents.txt")
    pseg_sentences = []
    for sentence in sentences:
        pseg_sentence = [words.word + "/" + words.flag for words in pseg.cut(sentence)]
        pseg_sentences.append(pseg_sentence)
    return pseg_sentences
