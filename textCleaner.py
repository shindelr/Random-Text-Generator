# Author: Robin Shindelman
# Date Created: 2024-02-20
# Last Modified: 2024-02-20
# Some of the code in this cleaning script is based off an article from 
# Towards Data Science. The inspiration to use spaCy and several of the Regex
# commands come from that article.
# Citation for the code:
# https://towardsdatascience.com/text-generation-with-markov-chains-an-introduction-to-using-markovify-742e6680dc33


from re import sub
import spacy


# Initialize documents
input_path = 'assets/RAW_corpus.txt'
output_path = 'assets/CLEANED_corpus.txt'

# Initial cleaning with regex's
with open(input_path, 'r') as input:
    with open(output_path, 'w') as output:
        for line in input:
            line = sub(r'--', ' ', line)  # Replace all double dashes with space
            line = sub('[\[].*?[\]]', '', line)  # Delete all [ ]
            line = sub(r'(\b|\s+\-?|^\-?)(\d+|\d*\.\d+)\b','', line)  # Delete all numerical operators
            line = sub(r'Chapter \d+', '', line)  # Delete chapter headings
            line = sub(r'CHAPTER \d+', '', line)
            # line = ' '.join(line.split())  # Remove extra white spaces

            output.write(line)


# Load the spaCy NLP model:
tokenized_path = 'assets/TOKENIZED_corpus.txt'
nlp = spacy.load('en_core_web_sm')

# Grab the newly preprocessed text doc.
with open (output_path, 'r') as file:
    preproc_corpus = file.read()

# Turns out, nlp requires 1gb of memory per 100,000 characters. Since my corpus
# is greater than 4 million characters in length, I need to batch it out.
n = len(preproc_corpus) 
block = 100000 
# Take slices of the corpus from i to the end of a block. Do this from 0 to the
# the end of the corpus and step by blocks.
batches = [preproc_corpus[i : i + block] for i in range(0, n, block)]

token_batches = []
# Tokenize and annotate text with information that will help our markov model.
for batch in batches:
    token_batches.append(nlp(batch))

# space_corpus = spacy.tokens.DocBin(docs=token_batches)
# space_corpus.to_disk(tokenized_path)
corpus_str = ''
with open(tokenized_path, 'w') as output:
    for batch in token_batches:
        for doc in batch:
            corpus_str += doc.text + ''
    output.write(corpus_str)
    
    

