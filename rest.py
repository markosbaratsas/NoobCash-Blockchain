import requests
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import sys

from blockchain import Node

this_node = None

### JUST A BASIC EXAMPLE OF A REST API WITH FLASK



app = Flask(__name__)
CORS(app)
# blockchain = Blockchain()


#.......................................................................................



# get all transactions in the blockchain

@app.route('/transactions/', methods=['GET'])
def get_transactions():
    # transactions = blockchain.transactions

    response = {'transactions': "transactions"}
    return jsonify(response), 200

@app.route('/new_transaction', methods=['POST'])
def add_transaction():
    # data = request.form.data
    response = request.json
    print(response)
    return jsonify(response), 200
    
    


# run it once fore every node

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=-1, type=int, help='Port to listen on')
    parser.add_argument('-i', '--index', default=-1, type=int, help='Index of node')
    parser.add_argument('-c', '--capacity', default=-1, type=int, help='Blockchain capacity')
    parser.add_argument('-d', '--difficulty', default=-1, type=int, help='Blockchain difficulty')
    args = parser.parse_args()
    port = args.port
    index = args.index
    difficulty = args.difficulty
    capacity = args.capacity
    
    if port == -1:
        print("Please provide port number")
        sys.exit(1)
    if index == -1:
        print("Please provide index")
        sys.exit(1)
    if capacity == -1:
        print("Please provide capacity")
        sys.exit(1)
    if difficulty == -1:
        print("Please provide difficulty")
        sys.exit(1)

    this_node = Node(index, difficulty, capacity)

    app.run(host='127.0.0.1', port=port)
