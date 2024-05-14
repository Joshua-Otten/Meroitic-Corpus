from gensim.models import KeyedVectors

# Load the pre-trained Word2Vec model from file
#model_path = "egyptian_super_clean_100.txt"
model_path = "meroitic_super_clean_100.txt"
word_vectors = KeyedVectors.load_word2vec_format(model_path, binary=False)

# Function to find nearest neighbors for a given word
def find_nearest_neighbors(word, topn=10):
    try:
        neighbors = word_vectors.most_similar(positive=[word], topn=topn)
        print(f"Nearest neighbors for '{word}':")
        for neighbor, similarity in neighbors:
            print(f"{neighbor}: {similarity}")
        print()
    except KeyError:
        print(f"'{word}' not found in the vocabulary.")

def word_analogy(word_a, word_b, word_c, topn=10):
    try:
        # Perform the analogy calculation
        result = word_vectors.most_similar(positive=[word_b, word_c], negative=[word_a], topn=topn)
        if topn == 1:
            print(f"{word_a} is to {word_b} as {word_c} is to {result[0][0]}")
        else:
            print(f"{word_a} is to {word_b} as {word_c} is to:")
            for word, similarity in result:
                print(f"{word}: {similarity}")
    except KeyError as e:
        missing_word = str(e).strip("'")
        print(f"'{missing_word}' not found in the vocabulary.")


    


#word_analogy('rmṯ', 'ḥm.t', 'nswt')
#word_analogy('nswt','wr','ms')
#word_analogy('qEr','pqr','abr') # expect 'as' for child
word_analogy('qEr', 'lx', 'as')
#while True:
#    word1 = input("word1: ")
#    word2 = input("word2: ")
#    similarity = word_vectors.similarity(word1, word2)
#    print(similarity)
    #find_nearest_neighbors(word)
