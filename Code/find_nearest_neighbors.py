from gensim.models import KeyedVectors

# Load the pre-trained Word2Vec model from file
model_path = "meroitic_no_separator.txt"
word_vectors = KeyedVectors.load_word2vec_format(model_path, binary=False)

# Function to find nearest neighbors for a given word
def find_nearest_neighbors(word, topn=10):
    try:
        neighbors = word_vectors.most_similar(positive=[word], topn=topn)
        print(f"Nearest neighbors for '{word}':")
        for neighbor, similarity in neighbors:
            print(f"{neighbor}: {similarity}")
    except KeyError:
        print(f"'{word}' not found in the vocabulary.")

while True:
    word = input("Nearest Neighbors for: ")
    find_nearest_neighbors(word)
    print('\n')

