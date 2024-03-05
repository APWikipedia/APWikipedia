import re
from collections import Counter
from spellchecker import SpellChecker
from gensim.models import Word2Vec

''' 不掉包用法
# def words(document):
#     "Convert text to lower case and tokenize the document"
#     return re.findall(r'\w+', document.lower())
# 
# 
# # create a frequency table of all the words of the document
# all_words = Counter(words(open('The_Great_Gatsby.txt', encoding='gb18030', errors='ignore').read()))
# 
# 
# def edits_one(word):
#     "Create all edits that are one edit away from `word`."
#     alphabets = 'abcdefghijklmnopqrstuvwxyz'
#     splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
#     deletes = [left + right[1:] for left, right in splits if right]
#     inserts = [left + c + right for left, right in splits for c in alphabets]
#     replaces = [left + c + right[1:] for left, right in splits if right for c in alphabets]
#     transposes = [left + right[1] + right[0] + right[2:] for left, right in splits if len(right) > 1]
#     return set(deletes + inserts + replaces + transposes)
# 
# 
# def edits_two(word):
#     "Create all edits that are two edits away from `word`."
#     return (e2 for e1 in edits_one(word) for e2 in edits_one(e1))
# 
# 
# def known(words):
#     "The subset of `words` that appear in the `all_words`."
#     return set(word for word in words if word in all_words)
# 
# 
# def possible_corrections(word):
#     "Generate possible spelling corrections for word."
#     return (known([word]) or known(edits_one(word)) or known(edits_two(word)) or [word])
# 
# 
# def prob(word, N=sum(all_words.values())):
#     "Probability of `word`: Number of appearances of 'word' / total number of tokens"
#     return all_words[word] / N
# 
# 
# def rectify(word):
#     "return the most probable spelling correction for `word` out of all the `possible_corrections`"
#     correct_word = max(possible_corrections(word), key=prob)
#     return correct_word
'''


def spell_check(input_query):
    spell = SpellChecker()
    word2vec_model = Word2Vec.load('word2vec_model.bin')
    # 将输入文本拆分为单词
    words = input_query.split()
    corrected_words = []
    for word in words:
        # 如果单词拼写错误，则进行纠正
        corrected_word = spell.correction(word)
        corrected_words.append(corrected_word)
    # 将纠正后的单词重新组合成字符串
    corrected_query = ' '.join(corrected_words)
    # 主题相关的查询扩展
    expanded_words = []
    for word in corrected_query.split():
        expanded_words.append(word)
        # 如果词在Word2Vec模型的词汇表中存在，则进行查询扩展
        if word in word2vec_model.wv.vocab:
            similar_words = word2vec_model.wv.most_similar(word, topn=3)
            expanded_words.extend([w for w, _ in similar_words])

    # 返回纠正过后的字符串
    return ' '.join(expanded_words)


# 创建一个main函数，用于测试
if __name__ == "__main__":
    # print(rectify("speling"))
    # print(rectify("korrectud"))
    # print(rectify("thay"))
    # print(rectify("relly"))
    # print(rectify("peotry"))
    # print(rectify("wirk"))
    # print(rectify("inconvient"))
    # print(rectify("adn"))
    # print(rectify("mispeling"))
    # print(rectify("minde"))
    # print(rectify("eror"))
    # print(rectify("documant"))
    # print(rectify("recieve"))
    # print(rectify("agian"))
    # print(rectify("seperate"))
    # print(rectify("occured"))
    # print(rectify("occuring"))
    # print(rectify("suprise"))
    # print(rectify("unpleasent"))
    # print(rectify("recieve"))
    # print(rectify("excede"))
    # print(rectify("independant"))
    input_text = "Ths is a smple sentnce with some missplled words."
    corrected_text = spell_check(input_text)
    print("Input Text:", input_text)
    print("Corrected Text:", corrected_text)
