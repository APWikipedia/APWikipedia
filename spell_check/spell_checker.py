import re
from collections import Counter
from spellchecker import SpellChecker


def words(document):
    "Convert text to lower case and tokenize the document"
    return re.findall(r'\w+', document.lower())


# create a frequency table of all the words of the document
all_words = Counter(words(open('The_Great_Gatsby.txt', encoding='gb18030', errors='ignore').read()))


def edits_one(word):
    "Create all edits that are one edit away from `word`."
    alphabets = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [left + right[1:] for left, right in splits if right]
    inserts = [left + c + right for left, right in splits for c in alphabets]
    replaces = [left + c + right[1:] for left, right in splits if right for c in alphabets]
    transposes = [left + right[1] + right[0] + right[2:] for left, right in splits if len(right) > 1]
    return set(deletes + inserts + replaces + transposes)


def edits_two(word):
    "Create all edits that are two edits away from `word`."
    return (e2 for e1 in edits_one(word) for e2 in edits_one(e1))


def known(words):
    "The subset of `words` that appear in the `all_words`."
    return set(word for word in words if word in all_words)


def possible_corrections(word):
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits_one(word)) or known(edits_two(word)) or [word])


def prob(word, N=sum(all_words.values())):
    "Probability of `word`: Number of appearances of 'word' / total number of tokens"
    return all_words[word] / N


def rectify(word):
    "return the most probable spelling correction for `word` out of all the `possible_corrections`"
    correct_word = max(possible_corrections(word), key=prob)
    return correct_word

def test():
    spell = SpellChecker()
    misspelled = spell.unknown(['something', 'is', 'hapenning', 'here', 'speling', 'korrestcud'])
    for word in misspelled:
        print(spell.correction(word))
        print(spell.candidates(word))

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
    test()

