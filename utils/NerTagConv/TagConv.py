class TaggingSystem:
    """
    NER标注系统
    """
    def __init__(self):
        pass

    def isEmptyTag(self, tag):
        if tag.strip():
            return False
        return True

    def isBeginTag(self, tag):
        if not self.isEmptyTag(tag):
            if tag.split("_")[0] == "B":
                return True
        return False

    def isInterTag(self, tag):
        if tag.strip():
            if tag.split("_")[0] == "I":
                return True

    def isOutTag(self, tag):
        if not self.isEmptyTag(tag):
            if tag.strip() == "O":
                return True
        return False

    def isSingleTag(self, tag):
        if not self.isEmptyTag(tag):
            if tag.split("_")[0] == "S":
                return True
        return False

    def isEndTag(self, tag):
        if not self.isEmptyTag(tag):
            if tag.split("_")[0] == "E":
                return True
        return False


class TagSystemConvert:
    """

    """
    def __init__(self, source_tag_list):
        self.source_tag_list = source_tag_list
        self.len_tag_list = len(source_tag_list)
        self.target_tag_list = source_tag_list.copy()

        self.Tag_Sys = TaggingSystem()

    def get_convert_method(self, source_system, target_system):
        """

        :param source_system: 源标注体系名
        :param target_system: 目标标注体系名
        :return: 转换方法
        """
        convert_method = None
        if source_system == "BIO" and target_system == "BIOE":
            convert_method = self.BIO2BIOE
        if source_system == "BIO" and target_system == "BIOS":
            convert_method = self.BIO2BIOS
        if source_system == "BIO" and target_system == "BIOES":
            convert_method = self.BIO2BIOES
        if source_system == "BIOE" and target_system == "BIO":
            convert_method = self.BIOE2BIO
        if source_system == "BIOE" and target_system == "BIOS":
            convert_method = self.BIOE2BIOS
        if source_system == "BIOE" and target_system == "BIOES":
            convert_method = self.BIOE2BIOES
        if source_system == "BIOS" and target_system == "BIO":
            convert_method = self.BIOS2BIO
        if source_system == "BIOS" and target_system == "BIOE":
            convert_method = self.BIOS2BIOE
        if source_system == "BIOS" and target_system == "BIOES":
            convert_method = self.BIOS2BIOES
        if source_system == "BIOES" and target_system == "BIO":
            convert_method = self.BIOES2BIO
        if source_system == "BIOES" and target_system == "BIOE":
            convert_method = self.BIOES2BIOE
        if source_system == "BIOES" and target_system == "BIOS":
            convert_method = self.BIOES2BIOS
        return convert_method

    def convert(self, source_system, target_system):
        """

        :param source_system:
        :param target_system:
        :return: 转换完的标签列表
        """
        convert_method = self.get_convert_method(source_system, target_system)
        for i in range(self.len_tag_list - 1):
            tag = self.source_tag_list[i]
            next_tag = self.source_tag_list[i + 1]
            convert_method(tag, next_tag, i)
        convert_method(self.source_tag_list[-1], None, -1)
        return self.target_tag_list

    def addTagE(self, tag, next_tag, index):
        """
        增加标签”Ｅ“
        :param tag:
        :param next_tag:
        :param index:
        :return:
        """
        if next_tag is not None:
            if self.Tag_Sys.isInterTag(tag) and \
                    (not self.Tag_Sys.isInterTag(next_tag)):
                self.target_tag_list[index] = "E_" + tag.split("_")[1]
        else:
            if self.Tag_Sys.isInterTag(tag):
                self.target_tag_list[index] = "E_" + tag.split("_")[1]

    def addTagS(self, tag, next_tag, index):
        """
        增加标签”S“
        :param tag:
        :param next_tag:
        :param index:
        :return:
        """
        if next_tag is not None:
            if self.Tag_Sys.isBeginTag(tag) and \
                    (not (self.Tag_Sys.isInterTag(next_tag) or self.Tag_Sys.isEndTag(next_tag))):
                self.target_tag_list[index] = "S_" + tag.split("_")[1]
        else:
            if self.Tag_Sys.isBeginTag(tag):
                self.target_tag_list[index] = "S_" + tag.split("_")[1]

    def delTagS(self, tag, next_tag, index):
        """
        删除标签”S“
        :param tag:
        :param next_tag:
        :param index:
        :return:
        """
        if self.Tag_Sys.isSingleTag(tag):
            self.target_tag_list[index] = "B_" + tag.split("_")[1]

    def delTagE(self, tag, next_tag, index):
        """
        删除标签”S“
        :param tag:
        :param next_tag:
        :param index:
        :return:
        """
        if self.Tag_Sys.isEndTag(tag):
            self.target_tag_list[index] = "I_" + tag.split("_")[1]

    def BIO2BIOE(self, tag, next_tag, index):
        self.addTagE(tag, next_tag, index)

    def BIO2BIOS(self, tag, next_tag, index):
        self.addTagS(tag, next_tag, index)

    def BIO2BIOES(self, tag, next_tag, index):
        self.addTagE(tag, next_tag, index)
        self.addTagS(tag, next_tag, index)

    def BIOE2BIO(self, tag, next_tag, index):
        self.delTagE(tag, next_tag, index)

    def BIOE2BIOS(self, tag, next_tag, index):
        self.delTagE(tag, next_tag, index)
        self.addTagS(tag, next_tag, index)

    def BIOE2BIOES(self, tag, next_tag, index):
        self.addTagS(tag, next_tag, index)

    def BIOS2BIO(self, tag, next_tag, index):
        self.delTagS(tag, next_tag, index)

    def BIOS2BIOE(self, tag, next_tag, index):
        self.delTagS(tag, next_tag, index)
        self.addTagE(tag, next_tag, index)

    def BIOS2BIOES(self, tag, next_tag, index):
        self.addTagE(tag, next_tag, index)

    def BIOES2BIO(self, tag, next_tag, index):
        self.delTagS(tag, next_tag, index)
        self.delTagE(tag, next_tag, index)

    def BIOES2BIOE(self, tag, next_tag, index):
        self.delTagS(tag, next_tag, index)

    def BIOES2BIOS(self, tag, next_tag, index):
        self.delTagE(tag, next_tag, index)


if __name__ == '__main__':
    ## BIO
    BIO_source_tag_list = ['O', 'B_PERSON', 'I_PERSON', 'I_PERSON', 'O', 'O', 'B_PERSON', 'B_PERSON', ' ', 'B_PERSON', 'B_PERSON']
    ## BIOE
    BIOE_source_tag_list = ['O', 'B_PERSON', 'I_PERSON', 'E_PERSON', 'O', 'O', 'B_PERSON', 'B_PERSON', ' ', 'B_PERSON', 'B_PERSON']
    ## BIOS
    BIOS_source_tag_list = ['O', 'B_PERSON', 'I_PERSON', 'I_PERSON', 'O', 'O', 'S_PERSON', 'S_PERSON', ' ', 'S_PERSON', 'S_PERSON']
    ## BIOES
    BIOES_source_tag_list = ['O', 'B_PERSON', 'I_PERSON', 'E_PERSON', 'O', 'O', 'S_PERSON', 'S_PERSON', ' ', 'S_PERSON', 'S_PERSON']
    conv_instance = TagSystemConvert(BIO_source_tag_list)
    target_tag_list = conv_instance.convert("BIO", "BIOES")
    print(target_tag_list)