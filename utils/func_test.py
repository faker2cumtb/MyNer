##　BIO标注且句子以空格分开

from utils.NerTagConv.TagConv import TagSystemConvert

data_path = "/home/luoxinyu/PycharmProjects/MyNer/data/example.test"


def get_char_from_file(data_path,index):
    with open(data_path, 'r', encoding="utf8") as f:
        contents = f.readlines()
    char_list = []
    chars_list = []
    for content in contents:
        content = content.strip()
        if content:
            content = content.split()[index]
            char_list.append(content)
        else:
            if char_list:
                chars_list.append(char_list)
            char_list = []
    return chars_list


if __name__ == '__main__':
    data_path = "/home/luoxinyu/PycharmProjects/MyNer/data/example.test"
    store_path = "/home/luoxinyu/PycharmProjects/MyNer/data/example_BIOES.test"
    with open(data_path, 'r', encoding="utf8") as f:
        contents = f.readlines()
    source_tag_list = []
    for content in contents:
        if content.strip():
            content = content.split()[-1].replace("-", "_")
            source_tag_list.append(content)
        else:
            source_tag_list.append("")
    print(len(contents), len(source_tag_list))
    # source_tag_list = ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'B-LOC', 'I-LOC', 'O', 'B-LOC', 'I-LOC', 'O', 'O']
    instance = TagSystemConvert(source_tag_list)
    target_tag_list = instance.convert("BIO", "BIOES")
    print(source_tag_list[:50])
    print(target_tag_list[:50])
    with open(store_path,'w',encoding="utf8") as f:
        for i in range(len(contents)):
            if contents[i].strip():
                content = contents[i].split()[0] + " " + target_tag_list[i]
                content = content.replace("_", "-")
            else:
                content = "\n"
            f.write(content)
            f.write("\n")
    import CRFPP