import jieba.posseg as pseg
import jieba


def segment(sentences,seg_dict_path = None):
    """
    分词
    :param sentences:
    :return:
    """
    if seg_dict_path is not None:
        jieba.load_userdict(seg_dict_path)
    pseg_sentences = []
    for sentence in sentences:
        pseg_sentence = [words.word + "/" + words.flag for words in pseg.cut(sentence)]
        pseg_sentences.append(pseg_sentence)
    return pseg_sentences
