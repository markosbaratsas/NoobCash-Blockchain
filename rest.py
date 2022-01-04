from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import requests
import sys
import threading

from blockchain import Node, RingNode
from helper import non_bootstrap_node, bootstrap_node

this_node = None
number_nodes = None
found_nonce = threading.Event

app = Flask(__name__)
CORS(app)
# blockchain = Blockchain()


#.......................................................................................



# get all transactions in the blockchain

@app.route('/transactions/', methods=['GET'])
def get_transactions():
    """Endpoint to get last valid block's transactions.

    Returns:
        Response, int: The response with the list of transactions, along with
        the HTTP status
    """
    response = {'transactions':\
                this_node.blockchain.last_block.list_of_transactions}
    return jsonify(response), 200

@app.route('/new_transaction', methods=['POST'])
def add_transaction():
    """Endpoint to create a new transaction by a node. Checks if the node
    has enough coins to make the transaction, and if it does the function
    also broadcasts the transaction to every other node by hitting the
    /add_broadcasted_transaction endpoint,

    Returns:
        Response, int: The response, along with the HTTP status
    """
    new_transaction = request.json
    receiver = new_transaction["receiver"]
    amount = new_transaction["amount"]
    transaction = this_node.create_transaction(receiver, amount)
    if transaction == None:
        return jsonify({'error': 'Not enough coins to make transaction'}), 501
    for ring_node in this_node.ring:
        # add error checking
        requests.post(f"http://{ring_node.address}/add_broadcasted_transaction/", json={
            "transaction": transaction
        })
    return jsonify({}), 200

@app.route('/add_node/', methods=['POST'])
def add_node():
    """Endpoint to be used by bootstrap node. When new node is up, inform
    bootstrap node by hitting this endpoint.

    Returns:
        Response, int: The response, along with the HTTP status
    """
    new_node = request.json
    print("add_node", new_node)
    new_node = RingNode(new_node["index"],
                    new_node["address"],
                    new_node["public_key"],
                    [])
    this_node.register_node_to_ring(new_node)
    return jsonify({}), 200

@app.route('/add_broadcasted_transaction', methods=['POST'])
def add_broadcasted_transaction():
    """Endpoint to add a broadcasted transaction made by another node.
    Validates the transaction, using the validate_transaction function of the
    node class, and adds it to the blockchain. If the node starts mining and
    finds a nonce, before the /found_nonce endpoint is hit by another node
    the found nonce is broadcasted to the other nodes.

    Returns:
        Response, int: The response, along with the HTTP status
    """
    broadcasted_transaction = request.json["transaction"]
    validated = this_node.validate_transaction(broadcasted_transaction)
    if not validated:
        return jsonify({'error': 'Transaction not valid'}), 502

    nonce = this_node.add_transaction(broadcasted_transaction, found_nonce)
    if nonce != -1:
        for ring_node in this_node.ring:
            requests.post(f"http://{ring_node.address}/found_nonce/", json={
                "blockchain": this_node.blockchain
            })
    return jsonify({}), 200

@app.route('/found_nonce', methods=['POST'])
def found_nonce():
    """Endpoint to to be hit when a node completes mining and broadcasts its
    blockchain. Sets the found_nonce threading event's flag, to stop any
    ongoing mining done by the node at the moment. If the broadcasted
    blockchain is larger, it replaces the node's current blockchain. The
    threading event's flag is restarted.

    Returns:
        Response, int: The response, along with the HTTP status
    """
    found_nonce.set()
    blockchain = request.json["blockchain"]
    if len(this_node.blockchain.blockchain) < len(blockchain.blockchain):
        this_node.blockchain = blockchain
    found_nonce.clear()
    return jsonify({}), 200




if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=-1, type=int, help='Port to listen on')
    parser.add_argument('-i', '--index', default=-1, type=int, help='Index of node')
    parser.add_argument('-c', '--capacity', default=-1, type=int, help='Blockchain capacity')
    parser.add_argument('-d', '--difficulty', default=-1, type=int, help='Blockchain difficulty')
    parser.add_argument('-n', '--number_nodes', default=-1, type=int, help='The total number of nodes')
    args = parser.parse_args()
    port = args.port
    index = args.index
    difficulty = args.difficulty
    capacity = args.capacity
    number_nodes = args.number_nodes
    
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
    if index == 0 and number_nodes == -1:
        print("Please provide number of nodes in the bootstrap node")
        sys.exit(1)

    this_node = Node(index, difficulty, capacity)

    # non-bootstrap nodes execute this
    if this_node.index != 0:
        non_bootstrap_node(this_node, port)
    else:
        bootstrap_node(this_node, number_nodes)


    app.run(host='127.0.0.1', port=port)
