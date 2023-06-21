import jieba.analyse
import jieba

jieba.load_userdict('jiebaSrc/userdict.txt')
jieba.analyse.set_idf_path("jiebaSrc/userIdf.text")
jieba.analyse.set_stop_words("jiebaSrc/stopwords.txt")

def getKeywords(rawmsg):
    words  = jieba.analyse.extract_tags(rawmsg,topK=5,withWeight=False)# allowPOS=['n']
    words.sort()
    if len(words) == 0:
        return rawmsg
    return " ".join(words)