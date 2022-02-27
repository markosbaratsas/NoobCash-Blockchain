import requests
import sys

from .node_script import addresses
from blockchain import Node, RingNode, Block, Transaction, TransactionOutput


def do_variable_checks(args):
    """Does a variety of checks based on user input on the CLI

    Args:
        port (int): Port
        index (int): Node index
        difficulty (int): Blockchain difficulty
        capacity (int): Capacity of transactions ineach block of the blockchain
        number_nodes (int): Number of nodes in the blockchain

    Returns:
        None, or exits the program if there is error
    """
    if args.which == "node":
        if args.index != 0 and args.port == -1:
            print("Please provide port number")
            sys.exit(1)
        if args.index == -1:
            print("Please provide index")
            sys.exit(1)
        if args.capacity == -1:
            print("Please provide capacity")
            sys.exit(1)
        if args.difficulty == -1:
            print("Please provide difficulty")
            sys.exit(1)
        if args.index == 0 and args.number_nodes == -1:
            print("Please provide number of nodes in the bootstrap node")
            sys.exit(1)
    elif args.which == "transaction":
        if args.recipient == -1:
            print("Please provide recipient node")
            sys.exit(1)
        if args.sender == -1:
            print("Please provide sender node")
            sys.exit(1)
        if args.amount == -1:
            print("Please provide transaction amount")
            sys.exit(1)
    elif args.which == "view":
        if args.node == -1:
            print("Please provide node, from which to view transaction")
            sys.exit(1)
    elif args.which == "balance":
        if args.node == -1:
            print("Please provide node, for which to print balance")
            sys.exit(1)


def non_bootstrap_node(node: Node, port: str):
    """Initialization of a non bootstrap node. Sends the node's information
    to the bootstrap node.

    Args:
        node (Node): The node to be initialized
        port (str): The port of the node
    """
    requests.post(f"http://{addresses[0]}/add_node", json={
        "index": node.index,
        "address": addresses[node.index],
        "public_key": addresses[node.index]
    })

def bootstrap_node(node: Node, number_of_nodes: str):
    """Initialization of the bootstrap node. Creates the genesis block that
    contains the initial transaction of the 100*n coins, and adds it to the
    blockchain.

    Args:
        node (Node): The bootstrap node to be initialized
        number_of_nodes (int): The number of the nodes of the system
    """
    new_node = RingNode(0, addresses[0], addresses[0], [])
    node.register_node_to_ring(new_node)
    node.blockchain.last_block = Block(0, 0, 1)
    transaction = Transaction(0, 0, addresses[0], 100*number_of_nodes,\
        [], "00")
    node.ring[0].utxos.append(transaction.transaction_outputs[0])
    node.wallet.unspent_transactions = node.ring[0].utxos
    node.blockchain.last_block.add_transactions_to_block([transaction])
    new_block = Block(node.blockchain.last_block.index+1, 0,\
        node.blockchain.last_block.hash)
    node.blockchain.add_new_block(new_block)
    pass
