## 模型训练
import os


def train_model(crf_learn_path, template_file_path, train_file_path, model_file_path):
    report = os.popen(" ".join([crf_learn_path, template_file_path, train_file_path, model_file_path]))
    return report

if __name__ == '__main__':
    crf_learn_path = "/home/luoxinyu/CRF++-0.58/crf_learn"
    template_file_path = "/home/luoxinyu/CRF++-0.58/my_data/model_3/template1"
    train_file_path = "/home/luoxinyu/CRF++-0.58/my_data/model_3/file.train"
    model_file_path = "/home/luoxinyu/CRF++-0.58/my_data/model_3/model"
    train_model(crf_learn_path, template_file_path, train_file_path, model_file_path)
