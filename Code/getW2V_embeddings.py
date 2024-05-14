# written with the help of ChatGPT
from gensim.models import Word2Vec
from gensim.utils import simple_preprocess
from gensim.models import KeyedVectors
import multiprocessing

# Path to your corpus file
corpus_file_path = 'ProcessedData/meroitic_clean2.txt'
#corpus_file_path = 'ProcessedData/egyptian_clean.txt'

# Function to read the corpus file
def read_corpus(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Tokenize line, considering it's a low-resource and undeciphered language
            tokens = [token.strip() for token in line.split()]
            yield tokens

# Initialize and train the Word2Vec model
corpus = list(read_corpus(corpus_file_path))
# You can adjust the parameters based on your requirements
model = Word2Vec(corpus, vector_size=100, window=5, min_count=1, workers=multiprocessing.cpu_count())

# Save the model
#model.save("word2vec_meroitic")
#model.wv.save_word2vec_format("word2vec_meroitic_no_sep_aug.bin",binary=True)
#model.save("egyptian.vec")
model.wv.save_word2vec_format("meroitic_clean_100.txt",binary=False)

# Load the model later
# model = Word2Vec.load("word2vec_model.vec")

# Get embeddings for specific words
word = "t"
embedding = model.wv[word]
print(f"Embedding for '{word}': {embedding}")
