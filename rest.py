import requests
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import sys
from helper import non_bootstrap_node, bootstrap_node

from blockchain import Node, RingNode

this_node = None
number_nodes = None

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
    print(this_node.index)
    print(type(jsonify(response)))
    return jsonify(response), 200

@app.route('/add-node/', methods=['GET'])
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
        non_bootstrap_node(this_node)
        requests.get("http://127.0.0.1:5000/add-node/", json={
            "index": index,
            "address": f"127.0.0.1:{port}",
            "public_key": f"127.0.0.1:{port}"
        })
    else:
        bootstrap_node(this_node)


    app.run(host='127.0.0.1', port=port)
