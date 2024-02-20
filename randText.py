# Author: Robin Shindelman
# Date Created: 2024-02-19
# Last Modified: 2024-02-19


import zmq
import markovify
from random import randint


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


if __name__ == '__main__':
    model = MarkovModel('assets/corpusOfClassics.txt')
    print(model.gen_sentence())