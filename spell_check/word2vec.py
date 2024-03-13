from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')

with open('abstracts.wiki.txt', 'r', encoding='utf-8') as file:
    corpus = file.readlines()

# 对文本进行分词处理
tokenized_corpus = [word_tokenize(sentence.lower()) for sentence in corpus]

# 训练 Word2Vec 模型
# Word2Vec 模型有两种算法：CBOW 和 Skip-gram。你可以根据具体需求选择其中之一。
# 这里我们选择 Skip-gram 算法进行训练，size 表示生成的词向量的维度，min_count 表示词频小于该值的词将被忽略
model = Word2Vec(sentences=tokenized_corpus, vector_size=100, window=5, min_count=1, sg=1)

# 保存训练好的模型
model.save('word2vec_model.bin')
print(model.wv.most_similar('daisy'))
