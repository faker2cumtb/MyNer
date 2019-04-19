#!/usr/bin/env python3 # -*- coding: utf-8 -*-
def f1(path):
    with open(path) as f:
        all_tag = 0  # 记录所有的标记数
        loc_tag = 0  # 记录真实的地理位置标记数
        pred_loc_tag = 0  # 记录预测的地理位置标记数
        correct_tag = 0  # 记录正确的标记数
        correct_loc_tag = 0  # 记录正确的地理位置标记数
        # 地理命名实体标记
        states = ['O']
        for line in f:  # i=i+1
            line = line.strip()
            if line == '':
                continue
            r = line.split()[-2].strip()  # print(_, r, p)
            p = line.split()[-1].strip()
            all_tag += 1
            if r == p:
                correct_tag += 1
                if r not in states:
                    correct_loc_tag += 1
            if r not in states:
                loc_tag += 1
            if p not in states:
                pred_loc_tag += 1
        loc_P = 1.0 * correct_loc_tag / pred_loc_tag
        loc_R = 1.0 * correct_loc_tag / loc_tag
        print('loc_P:{0}, loc_R:{1}, loc_F1:{2}'.format(loc_P, loc_R, (2 * loc_P * loc_R) / (loc_P + loc_R)))


def load_model(path):
    import os, CRFPP
    # -v 3: access deep information like alpha,beta,prob
    # -nN: enable nbest output. N should be >= 2
    if os.path.exists(path):
        return CRFPP.Tagger('-m {0} -v 3 -n2'.format(path))
    return None


def locationNER(text):
    tagger = load_model('/home/luoxinyu/CRF++-0.58/my_data/model')
    # 利用训练好的模型标记每个字
    for c in text:
        tagger.add(c)
        # parse and change internal stated as 'parsed'
        tagger.parse()
    result = []
    word = ''
    print(tagger.size(), tagger.xsize())
    for i in range(0, tagger.size()):  # tagger.size：要预测的句子的字数
        for j in range(0, tagger.xsize()):  # tagger.xsize：特征列的个数
            ch = tagger.x(i, j)
            tag = tagger.y2(i)
            print(ch, tag)
            if tag == 'B-LOC':
                word = ch
            elif tag == 'I-LOC':
                word += ch
            elif tag == 'E-LOC':
                word += ch
                result.append(word)
            elif tag == 'S-LOC':
                word = ch
                result.append(word)
    return result


if __name__ == '__main__':
    f1('/home/luoxinyu/PycharmProjects/MyNer/data/result.rst')
    # # 测试
    # text = '我中午要去北京饭店，下午去中山公园，晚上回亚运村。'
    # print(text, locationNER(text), sep='==> ')
    # text = '我去回龙观，不去南锣鼓巷'
    # print(text, locationNER(text), sep='==> ')
    # text = '打的去北京南站地铁站'
    # print(text, locationNER(text), sep='==> ')
