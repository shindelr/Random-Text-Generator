import zmq
import time

context = zmq.Context()

#  Socket to talk to server
print("Connecting to host 4000")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:4000")

while True:
    # Request words or sentences
    socket.send_string(input('Please enter either "word" or "sentence": '))

    response = socket.recv()
    print(f'\n{response} \n')
    