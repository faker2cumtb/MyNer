import json


def get_column_from_file(data_path, column_index, sep=None):
    """

    :param data_path:
    :param column_index:
    :param sep:
    :return:
    """
    with open(data_path, 'r', encoding="utf8") as f:
        contents = f.readlines()
    data = []
    sep_data = []
    for content in contents:
        content = content.strip()
        if content:
            if sep is not None:
                content = content.split(sep)[column_index]
            else:
                content = content.split()[column_index]
            data.append(content)
        else:
            if data:
                sep_data.append(data)
            data = []
    return sep_data


def write_json(file_path, dict):
    with open(file_path, "w", encoding="utf8") as f:
        json.dump(dict, f, ensure_ascii=False)


def read_json(file_path):
    with open(file_path, "r", encoding="utf8") as f:
        return json.load(f)


if __name__ == '__main__':
    ent_pointer_path = "/home/luoxinyu/PycharmProjects/MyNer/ent_pointer.json"
    dict = {"名字": "你是猪吗"}
    write_json(ent_pointer_path, dict)
    print(read_json(ent_pointer_path))
