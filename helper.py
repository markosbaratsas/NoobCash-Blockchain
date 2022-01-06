import requests

from blockchain import Node, RingNode, Block, Transaction, TransactionOutput


def non_bootstrap_node(node: Node, port: str):
    """Initialization of a non bootstrap node. Sends the node's information
    to the bootstrap node.

    Args:
        node (Node): The node to be initialized
        port (str): The port of the node
    """
    requests.post("http://127.0.0.1:5000/add_node/", json={
        "index": node.index,
        "address": f"127.0.0.1:{port}",
        "public_key": f"127.0.0.1:{port}"
    })

def bootstrap_node(node: Node, number_of_nodes: str):
    """Initialization of the bootstrap node. Creates the genesis block that
    contains the initial transaction of the 100*n coins, and adds it to the
    blockchain.

    Args:
        node (Node): The bootstrap node to be initialized
        number_of_nodes (int): The number of the nodes of the system
    """
    new_node = RingNode(0, "127.0.0.1:5000", "127.0.0.1:5000", [])
    node.register_node_to_ring(new_node)
    node.blockchain.last_block = Block(0, 0, 1)
    transaction = Transaction(0, 0, node.wallet.address, 100*number_of_nodes,\
        [], "00")
    node.blockchain.last_block.add_transactions_to_block([transaction])
    new_block = Block(node.blockchain.last_block.index+1, 0,\
        node.blockchain.last_block.hash)
    node.blockchain.add_new_block(new_block)
    pass
