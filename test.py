#!/usr/bin/env python3 # -*- coding: utf-8 -*-

## 模型测试
import os


def test_model(crf_test_path, model_file_path, test_file_path, result_file_path):
    report = os.popen(" ".join([crf_test_path, "-m", model_file_path, test_file_path, '>', result_file_path]))
    return report


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
        print(correct_loc_tag)
        print(pred_loc_tag)
        loc_P = 1.0 * correct_loc_tag / pred_loc_tag
        loc_R = 1.0 * correct_loc_tag / loc_tag
        print('loc_P:{0}, loc_R:{1}, loc_F1:{2}'.format(loc_P, loc_R, (2 * loc_P * loc_R) / (loc_P + loc_R)))


if __name__ == '__main__':
    crf_test_path = "/home/luoxinyu/CRF++-0.58/crf_test"
    model_file_path = "/home/luoxinyu/CRF++-0.58/my_data/model_3/model"
    test_file_path = "/home/luoxinyu/CRF++-0.58/my_data/model_3/segwithoutdict_pos_bound_features.test"
    result_file_path = "/home/luoxinyu/CRF++-0.58/my_data/model_3/result.rst"

    # test_model(crf_test_path, model_file_path, test_file_path, result_file_path)

    f1(result_file_path)
