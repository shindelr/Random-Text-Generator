# Author: Robin Shindelman
# Date Created: 2024-02-19
# Last Modified: 2024-02-20


import zmq
import markovify
from random import randint
from re import sub
import spacy
nlp = spacy.load("en_core_web_sm")


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
        model = markovify.Text(opened_corpus, state_size=3)
        return model
    

    def gen_sentence(self):
        """
        Generate a sentence of a length between 50 and 150 characters.
        Returns the sentence as a string.
        """
        n = randint(50, 150) 
        sentence = None
        while sentence is None:
            sentence = self.model.make_short_sentence(max_chars=n, 
                                                      #test_ouput=False
                                                      max_overlap_ratio = 80)
        
        # These two commands split and join the generated sentences using
        # some kind of nlp magic to try to make them make more sense.
        split_sentence = self.model.word_split(sentence) 
        joined_sentence = self.model.word_join(split_sentence) 
        return joined_sentence


    def gen_word(self):
        """
        Generate a random word by taking a slice at random out of the corpus
        between the characters of 100 and 3000. I slimmed this range down so 
        low because all the possible word extraction techniques I found were
        O(n) running time, and that's pretty slow. Returns a single word from
        that slice.
        """
        slice_a, slice_b = randint(100, 2000), randint(2001, 3000)
        start, end = min(slice_a, slice_b), max(slice_a, slice_b)
        rand_slice = self.text[start:end]

        word_list = rand_slice.split()  # Split long slice into a list of words
        for i, word in enumerate(word_list): 
            word = sub(r'[^a-zA-Z0-9\s]', '', word)  # Clean punctuation out
            word_list[i] = word
        word_int = randint(0, 3000) % len(word_list)  # Modulo for a random selection

        return word_list[word_int]
        

if __name__ == '__main__':
    # MODEL SETUP
    c_corp = 'assets/CLEANED_corpus.txt'
    r_corp = 'assets/RAW_corpus.txt'
    model = MarkovModel(c_corp)

    # COMMUNICATION SETUP
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:4000")
    print("Waiting on host 4000")

    while True:
        valid_comm = [b'word', b'sentence', b'stop']
        request = socket.recv()
        print(f'Received request: {request}')
        # Requests can either be 'word' or 'sentence'
        if request == b'word':
            response = model.gen_word()
            socket.send_string(f'Random Word: {response}')

        if request == b'sentence':
            response = model.gen_sentence()
            socket.send_string(f'Random Sentence: {response}')
        
        if request == b'stop':
            print('Stopping service.')
            socket.send_string('Stopping')
            break
        
        if request not in valid_comm:
            socket.send_string('Invalid communication. Please use "word", "sentence", or "stop".')
