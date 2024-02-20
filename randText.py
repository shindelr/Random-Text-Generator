# Author: Robin Shindelman
# Date Created: 2024-02-19
# Last Modified: 2024-02-19


import zmq
import markovify
from random import randint
from re import sub
from language_tool_python import LanguageTool


class MarkovModel:
    """Instantiate a Markov model."""

    def __init__(self, corpus_path) -> None:
        self.text = self.read_corpus(corpus_path)
        self.model = self.initialize_markov_model(self.text)


    def read_corpus(self, corpus_path):
        """Opens the corpus document."""
        with open(corpus_path) as file:
            corpus = file.read()
        return corpus

    def initialize_markov_model(self, opened_corpus):
        """Builds the model using the corpus."""
        return markovify.Text(opened_corpus)
    

    def gen_sentence(self):
        """
        Generate a sentence of a length between 50 and 250 characters.
        Returns the sentence as a string.
        """
        n = randint(50, 250) 
        return self.model.make_short_sentence(n)


class GrammerChecker:
    """
    Instantiate an instance of the Python Language Tool wrapper. Not currently
    used since it adds a significant performance cost.
    """

    def __init__(self) -> None:
        self.tool = LanguageTool('en-US')

    
    def refine(self, sentence: str) -> str:
        """Refine the grammer and spelling of a sentence."""
        return self.tool.correct(sentence)


    def close(self):
        """Close the Language Tool gracefully."""
        self.tool.close()



def preprocess_corpus(input, output):
    """
    Remove all special characters from a .txt file. Specify the file path
    of the text file to be modified as the input. Specify the file path of the
    file you would like the cleaned version to go to as output.
    Returns nothing.
    """
    with open(input, 'r') as input_file:
        with open(output, 'w') as output_file:
            for line in input_file:
                cleaned_line = sub(r'[^\w\s.,?!"]', '', line)  # Remove all special chars but quotations
                output_file.write(cleaned_line)


if __name__ == '__main__':
    # input = 'assets/corpusOfClassics.txt'
    # output = 'assets/corpusOfClassicsClean.txt'
    # preprocess_corpus(input, output)


    clean_corpus = 'assets/corpusOfClassicsClean.txt'
    dirty_corpus = 'assets/corpusOfClassics.txt'
    model = MarkovModel(clean_corpus)

    for _ in range(10):
        raw_sentence = model.gen_sentence()
        print(raw_sentence)
    
