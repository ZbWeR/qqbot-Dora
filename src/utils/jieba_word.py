import jieba.analyse
import jieba

jieba.load_userdict('jiebaSrc/userdict.txt')
jieba.analyse.set_idf_path("jiebaSrc/userIdf.text")
jieba.analyse.set_stop_words("jiebaSrc/stopwords.txt")

def get_keywords(rawmsg):
    """
    对输入的文本进行关键词提取，并返回关键词组成的字符串

    Args:
        rawmsg: str,待处理的文本
    Returns:
        str,关键词组成的字符串
    """
    words  = jieba.analyse.extract_tags(rawmsg,topK=5,withWeight=False)
    words.sort()
    return rawmsg if len(words) == 0 else " ".join(words)