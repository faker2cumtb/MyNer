##　BIO标注且句子以空格分开

from utils.NerTagConv.TagConv import TagSystemConvert

if __name__ == '__main__':
    data_path = "/home/luoxinyu/PycharmProjects/MyNer/data/example.train"
    store_path = "/home/luoxinyu/PycharmProjects/MyNer/data/example_BIOS.train"
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
    target_tag_list = instance.convert("BIO", "BIOS")
    print(source_tag_list[:50])
    print(target_tag_list[:50])
    with open(store_path,'w',encoding="utf8") as f:
        for i in range(len(contents)):
            if contents[i].strip():
                content = contents[i].split()[0] + " " + target_tag_list[i]
            else:
                content = ""
            f.write(content)
            f.write("\n")