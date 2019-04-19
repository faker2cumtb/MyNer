import os
import CRFPP


def load_model(model_path):
    """
    加载模型
    :param model_path:
    :return:
    """
    # -v 3: access deep information like alpha,beta,prob
    # -nN: enable nbest output. N should be >= 2
    if os.path.exists(model_path):
        return CRFPP.Tagger('-m {0} -v 3 -n2'.format(model_path))
    return None


def get_ch_tag(tagger, text):
    """
    利用训练好的模型标记每个字
    :param tagger:
    :param text:
    :return:
    """
    for c in text:
        tagger.add(c)
        # parse and change internal stated as 'parsed'
        tagger.parse()
    print(tagger.size(), tagger.xsize())
    ch_tag = []
    for i in range(0, tagger.size()):  # tagger.size：要预测的句子的字数
        for j in range(0, tagger.xsize()):  # tagger.xsize：特征列的个数
            ch = tagger.x(i, j)
            tag = tagger.y2(i)
            ch_tag.append((ch, tag))
    return ch_tag


def infer_ner(ch_tag, ent_type_list):
    """
    识别句子中的实体
    :param ch_tag:
    :param ent_type_list:
    :return:
    """
    dict = {ent_type: [] for ent_type in ent_type_list}
    word = ""
    for ent_type in ent_type_list:
        for item in ch_tag:
            ch = item[0]
            tag = item[1]
            if tag == 'B-' + ent_type:
                word = ch
            elif tag == 'I-' + ent_type:
                word += ch
            elif tag == 'E-' + ent_type:
                word += ch
                dict[ent_type].append(word)
            elif tag == 'S-' + ent_type:
                word = ch
                dict[ent_type].append(word)
    return dict


def main(text, model_path, ent_type_list):
    """

    :param text:
    :param model_path:
    :param ent_type_list:
    :return:
    """
    tagger = load_model(model_path)
    ch_tag = get_ch_tag(tagger, text)
    return infer_ner(ch_tag, ent_type_list)
