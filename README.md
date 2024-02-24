# Random Text Generator
--------------------------

A random text generator based off Markov chaining. Designed for use in conjunction with Michael Hunter's CS361 project, a text encryption service. However, this file can easily be used as a script on its own to generate interesting words and short sentences. 

### Markov Chaining

This modeling technique relies on probability to try to predict the future state of an object, purely based on what state it's presently in. Within the context of text generation, this more or less means that the Markov Process is able to identify the *next* word in a sentence, based on the *current* word. By analyzing a large document, we can assign probabilities to the relationships between words. That is, given a specific word, what word is most likely to follow it?

For this project, the author used a Python library called Markovify. This library is incredibly lightweight and easy to learn. In accordance with a classic modeling rule of thumb, ~70% of the author's time was spent cleaning and curating data for the model to learn on, while only ~30% of development time was spent building the model itself. Even so, since the quality of the model's output is so dependent on the quality of the corpus, more time could have been spent carefully preparing the data. 
**Markovify:** https://github.com/jsvine/markovify


### Service Communication
----------------------

#### Random-Text-Generator File Structure:

Random-Text-Generator (root)
|
|---assets
|   	|---CLEANED_corpus.txt
|	    |---RAW_corpus.txt
|	    |---TOKENIZED_corpus.txt
|
|---randTextVenv
|---.gitignore
|---randText.py
|---test_client.py
|---textCleaner.py

### Requesting Communication

randText.py uses ZeroMQ to request and receive communication. To programmatically request a sentence or word from randText.py, the following set up is recommended.

In the client program, initialize a ZMQ context and REQ socket.
```python
import zmq

context = zmq.Context()

# Connect to same host as randText.py
print('Connecting to host 4000')
socket = context.socket(zmq.REQ)  # Becomes a request socket
socket.connect('tcp://localhost:4000')

# To request a word:
socket.send_string('word')
word = socket.recv()

# To request a sentence:
socket.send_string('sentence')
sentence = socket.recv()

# To kill randText.py:
socket.send_string('stop')
print('Stopping randText.py')
```
These strings can be sent as often or as quickly as necessary. Please note that the strings, **`'word'`**, **`'sentence'`**, and **`'stop'`**.  are the only messages that randText.py will respond to. 
Send `word` to have randText.py generate a single word.
Send `sentence` to have randText.py generate a short sentence between 50 and 150 characters.

### Receiving Communication

In randText.py, the following code is set up to run the program indefinitely until killed by the client. randText.py contains only one socket, a REP socket, and so is keyed to respond to the client.
```python
import zmq

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
		socket.send_string('Invalid communication. Please use "word",                               "sentence", or "stop".')
```

Please note again that there are three valid communication options: **`'word'`** , **`'sentence'`**, **`'stop'`**.  Prior to this communication loop opening, a Markov model is instantiated via the MarkovModel class. This occurs as soon as the program is booted up, allowing for very fast text generation.


The file **test_client.py** contains a simple ZeroMQ "app" that anyone can use to see this communication pipeline in action.

### UML Sequence Diagram
**Note**: The below diagram is built specifically with the aforementioned Encryption Service program in mind.
<img width="468" alt="image" src="https://github.com/shindelr/Random-Text-Generator/assets/129821483/8960f41d-e077-482b-bd60-cf5064e7bd40">


