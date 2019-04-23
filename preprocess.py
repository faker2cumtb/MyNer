## 对输入数据进行预处理，包括特征工程
# todo 所有实体词增加词频(默认为１就好)和词性
# todo 实体指示词增加词频，并将实体指示词保存为json文件，设计参数过滤低频指示词
# todo 指定文件存储地址

from utils.file_utils import get_column_from_file, write_json, read_json
from utils.seg_utils import segment
from utils.string_utils import strip_string
import numpy as np


def get_single_entities(char_list, tag_list, enetities_type):
    """
    得到单个实体
    :param char_list:
    :param tag_list:
    :param enetities_type:
    :return:
    """
    result = []
    word = ''
    for i in range(len(tag_list)):
        tag = tag_list[i]
        ch = char_list[i]
        if tag == 'B-' + enetities_type:
            word = ch
        elif tag == 'I-' + enetities_type:
            word += ch
        elif tag == 'E-' + enetities_type:
            word += ch
            result.append(word)
        elif tag == 'S-' + enetities_type:
            word = ch
            result.append(word)
    return result


def save_all_entities(char_lists, tag_lists, ent_type_list):
    """
    保存所有实体到文件里
    :param char_lists:
    :param tag_lists:
    :param ent_type_list:
    :return:
    """
    ent_results = set()
    for ent_type in ent_type_list:
        ent_result = set()
        for i in range(len(char_lists)):
            char_list = char_lists[i]
            tag_list = tag_lists[i]
            result = get_single_entities(char_list, tag_list, ent_type)
            ent_result |= set(result)
        ent_results |= ent_result
        with open(ent_type + '.txt', 'w', encoding="utf8") as f:
            context = "\n".join(list(ent_result))
            f.writelines(context)
    with open("all_ents.txt", "w", encoding="utf8") as f:
        contexts = "\n".join(list(ent_results))
        f.writelines(contexts)


def get_ent_pointer_words(pseg_sentences, ent_type_list):
    """
    构建命名实体指示器
    :param ent_type:
    :param pseg_sentence:
    :return:
    """
    dict = {}
    for ent_type in ent_type_list:
        result = {}
        with open(ent_type + ".txt", "r", encoding="utf8") as f:
            ents = f.readlines()
            ents = list(map(strip_string, ents))  ## 去掉后面的换行符号
        for pseg_sentence in pseg_sentences:
            for i in range(len(pseg_sentence)):
                word_p = pseg_sentence[i]
                word = word_p.split("/")[0]
                if word in ents:
                    if i - 2 >= 0:
                        temp = result.get(pseg_sentence[i - 2], 0)
                        result[pseg_sentence[i - 2]] = temp + 1
                    if i - 1 >= 0:
                        temp = result.get(pseg_sentence[i - 1], 0)
                        result[pseg_sentence[i - 1]] = temp + 1
                    if i + 1 < len(pseg_sentence):
                        temp = result.get(pseg_sentence[i + 1], 0)
                        result[pseg_sentence[i + 1]] = temp + 1
                    if i + 2 < len(pseg_sentence):
                        temp = result.get(pseg_sentence[i + 2], 0)
                        result[pseg_sentence[i + 2]] = temp + 1
        dict[ent_type] = result
    return dict


def set_ent_pot_features(pseg_sentences, ent_pot_words):
    """
    设置实体指示特征
    :param pseg_sentences:
    :param ent_pot_words:
    :return:
    """
    results = []
    for pseg_sentence in pseg_sentences:
        result = []
        for word_p in pseg_sentence:
            word = word_p.split("/")[0]
            if word_p in ent_pot_words:
                result.extend(["Y" for i in range(len(word))])
            else:
                result.extend(["N" for i in range(len(word))])
        results.append(result)
    return results


def set_poster_features(pseg_sentences):
    """
    设置词性标注特征
    :param pseg_sentences:
    :return:
    """
    results = []
    for pseg_sentence in pseg_sentences:
        result = []
        for word_p in pseg_sentence:
            word = word_p.split("/")[0]
            p = word_p.split("/")[1]
            result.extend([p] * len(word))
        results.append(result)
    return results


def set_boundary_features(pseg_sentences):
    """
    设置边界特征
    :param pseg_sentences:
    :return:
    """
    results = []
    for pseg_sentence in pseg_sentences:
        result = []
        for word_p in pseg_sentence:
            word = word_p.split('/')[0]
            boundarys = []
            if len(word) == 1:
                boundarys = ["S"]
            elif len(word) == 2:
                boundarys = ["B", "E"]
            elif len(word) > 2:
                boundarys = ["I" for i in range(len(word))]
                boundarys[0] = "B"
                boundarys[-1] = "E"
            result.extend(boundarys)
        results.append(result)
    return results


def filter_word_freq(dict, threshold):
    """
    过滤词频低的词
    :param dict:
    :param tred:
    :return:
    """
    result = []
    for key, value in dict.items():
        if value < threshold:
            pass
        else:
            result.append(key)
    return result


def main():
    data_path = "/home/luoxinyu/PycharmProjects/MyNer/data/example_BIOES.test"
    file_path = "/home/luoxinyu/PycharmProjects/MyNer/data/BIOES/segwithoutdict_pos_bound_features.test"

    ent_pointer_path = "/home/luoxinyu/PycharmProjects/MyNer/ent_pointer.json"

    # seg_dict_path = "all_ents.txt"
    seg_dict_path = None

    THRESHOLD = 20
    REGEN_ENT_WORD = False
    REGEN_POIT_WORD = False

    ent_type_list = ["LOC", "PER", "ORG"]

    char_lists = get_column_from_file(data_path, 0)
    tag_lists = get_column_from_file(data_path, -1)
    if REGEN_ENT_WORD:
        save_all_entities(char_lists, tag_lists, ent_type_list)

    sentences = ["".join(char_list) for char_list in char_lists]
    pseg_sentences = segment(sentences,seg_dict_path)

    if REGEN_POIT_WORD:
        dict = get_ent_pointer_words(pseg_sentences, ent_type_list)
        write_json(ent_pointer_path, dict)
    else:
        dict = read_json(ent_pointer_path)

    # LOC_pointer_words = filter_word_freq(dict["LOC"], THRESHOLD)
    # PER_pointer_words = filter_word_freq(dict["PER"], THRESHOLD)
    # ORG_pointer_words = filter_word_freq(dict["ORG"], THRESHOLD)

    # loc_feat = set_ent_pot_features(pseg_sentences, LOC_pointer_words)
    # per_feat = set_ent_pot_features(pseg_sentences, PER_pointer_words)
    # org_feat = set_ent_pot_features(pseg_sentences, ORG_pointer_words)
    pos_feat = set_poster_features(pseg_sentences)
    bound_feat = set_boundary_features(pseg_sentences)
    print("finished")

    # features = [char_lists, pos_feat, bound_feat, loc_feat, per_feat, org_feat, tag_lists]
    features = [char_lists, pos_feat, bound_feat, tag_lists]

    with open(file_path, "w", encoding="utf8") as f:
        for i in range(len(char_lists)):
            for j in range(len(char_lists[i])):
                per_row = []
                for h in range(len(features)):
                    per_row.append(features[h][i][j])
                row_content = " ".join(per_row)
                f.write(row_content)
                f.write("\n")
            f.write("\n")


if __name__ == '__main__':
    main()
