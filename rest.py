import argparse
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import requests
import sys
import threading
from time import sleep

from blockchain import Node, RingNode, Blockchain, Transaction
from helper import non_bootstrap_node, bootstrap_node, do_variable_checks
from cli_parser_args import add_arguments


this_node = None
number_nodes = None
found_nonce_thread = threading.Event()

app = Flask(__name__)
CORS(app)


@app.route('/get_statistics', methods=['GET'])
def get_statistics():
    """Endpoint that provides statistics regarding this node and its
    blockchain (e.g. number of transactions in the blockchain, time needed to
    mine a block)

    Returns:
        Response, int: The response, along with the HTTP status
    """
    return jsonify({
        "number_of_transactions": this_node.blockchain.number_of_transactions,
        "mining_times": this_node.mining_times,
        "number_of_blocks": len(this_node.blockchain.blockchain.keys())
        }), 200

@app.route('/transactions', methods=['GET'])
def get_transactions():
    """Endpoint to get last valid block's transactions.

    Returns:
        Response, int: The response with the list of transactions, along with
        the HTTP status
    """
    response = {'transactions':\
                    [x.to_dict() for x in\
                    this_node.blockchain.last_block.list_of_transactions]
                }
    return jsonify(response), 200

@app.route('/new_transaction', methods=['POST'])
def add_transaction():
    """Endpoint to create a new transaction by a node. Checks if the node
    has enough coins to make the transaction, and if it does the function
    also broadcasts the transaction to every other node by hitting the
    /add_broadcasted_transaction endpoint.

    Returns:
        Response, int: The response, along with the HTTP status
    """
    new_transaction = request.json
    receiver = new_transaction["receiver"]
    amount = new_transaction["amount"]
    transaction = this_node.create_transaction(receiver, amount)
    if transaction == None:
        return jsonify({'error': 'Not enough coins to make transaction'}), 501

    for node in this_node.ring:
        if node.index != this_node.index:
            r = requests.post(f"http://{node.address}" +
                "/add_broadcasted_transaction",\
                json={
                    "transaction": transaction.to_dict()
                })
            if r.status_code != 200:
                return jsonify({'error': 'Transaction not validated'}), 503

    nonce = this_node.add_transaction(transaction, found_nonce_thread)
    if nonce != -1:
        for ring_node in this_node.ring:
            if ring_node.index != this_node.index:
                requests.post(f"http://{ring_node.address}/found_nonce",\
                    json={
                        "blockchain": this_node.blockchain.to_dict()
                    })
    return jsonify({}), 200

@app.route('/add_node', methods=['POST'])
def add_node():
    """Endpoint to be used by bootstrap node. When new node is up, inform
    bootstrap node by hitting this endpoint. Everytime a new node is
    registered, bootstrap send it 100 coins by creating and broadcasting a
    new transaction.

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
    transaction = this_node.create_transaction(new_node.address, 100)
    this_node.add_transaction(transaction, found_nonce_thread)

    return jsonify({}), 200

@app.route('/receive_blockchain_and_ring', methods=['POST'])
def receive_blockchain_and_ring():
    """Endpoint to add broadcasted by the bootstrap node blockchain and ring,
    when all of the nodes are inserted to the system.

    Returns:
        Response, int: The response, along with the HTTP status
    """
    blockchain = Blockchain(0, 0)
    blockchain.parser(request.json["blockchain"])
    ring = []
    for node in request.json["ring"]:
        ring_node = RingNode(0, "", "", [])
        ring_node.parser(node)
        ring.append(ring_node)
    this_node.blockchain = blockchain
    this_node.ring = ring
    this_node.wallet.unspent_transactions =\
        this_node.ring[this_node.index].utxos
    return jsonify({}), 200


@app.route('/broadcast_nodes', methods=['GET'])
def broadcast_nodes():
    """Endpoint to be used by bootstrap node. If all nodes are registered,
    bootstrap node broadcasts its blockchain and ring.

    Returns:
        Response, int: The response, along with the HTTP status
    """
    if len(this_node.ring) == number_nodes:
        for node in this_node.ring:
            if node.index != this_node.index:
                requests.post(f"http://{node.address}" +
                    "/receive_blockchain_and_ring",
                    json={
                        "blockchain": this_node.blockchain.to_dict(),
                        "ring": [x.to_dict() for x in this_node.ring]
                    })

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
    broadcasted_transaction = Transaction("", "", "", 0, [], "s")
    broadcasted_transaction.parser(request.json["transaction"])
    validated = this_node.validate_transaction(broadcasted_transaction)
    if not validated:
        return jsonify({'error': 'Transaction not valid'}), 502

    nonce = this_node.add_transaction(broadcasted_transaction,\
                                    found_nonce_thread)
    if nonce != -1:
        for ring_node in this_node.ring:
            if ring_node.index != this_node.index:
                requests.post(f"http://{ring_node.address}/found_nonce",\
                    json={
                        "blockchain": this_node.blockchain.to_dict()
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
    found_nonce_thread.set()
    blockchain = Blockchain(0, 0)
    blockchain.parser(request.json["blockchain"])
    if len(this_node.blockchain.blockchain) < len(blockchain.blockchain):
        this_node.blockchain = blockchain
    found_nonce_thread.clear()
    return jsonify({}), 200

@app.route('/get_balance', methods=['GET'])
def get_balance():
    """Return Balance of current node

    Returns:
        Response, int: The response, along with the HTTP status
    """
    return jsonify({"balance": this_node.wallet.balance()}), 200



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='CLI tool to manage\
                                    Blockchain from different nodes')

    add_arguments(parser)
    args = parser.parse_args()
    do_variable_checks(args)

    if args.which == "node":
        port = args.port
        index = args.index
        difficulty = args.difficulty
        capacity = args.capacity
        number_nodes = args.number_nodes

        this_node = Node(index, capacity, difficulty)

        # non-bootstrap nodes execute this
        if this_node.index != 0:
            non_bootstrap_node(this_node, port)
        else:
            bootstrap_node(this_node, number_nodes)
            port = 5000

        app.run(host='0.0.0.0', port=port, threaded=True)

    elif args.which == "transaction":
        r = requests.post(f"http://{args.sender}/new_transaction", json={
            "receiver": args.recipient,
            "amount": args.amount
        })
        print(r.content)

    elif args.which == "view":
        r = requests.get(f"http://{args.node}/transactions")
        print(r.content)

    elif args.which == "balance":
        r = requests.get(f"http://{args.node}/get_balance")
        print(r.content)

    elif args.which == "broadcast_nodes":
        r = requests.get(f"http://127.0.0.1:5000/broadcast_nodes")
        print(r.content)
