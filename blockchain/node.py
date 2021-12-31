import threading

from .block import Block
from .blockchain import Blockchain
from .wallet import Wallet
from .transaction import Transaction, TransactionOutput


class RingNode:
    def __init__(self, index, address, public_key, utxos):
        self.index = index
        self.address = address
        self.public_key = public_key
        self.utxos = [x for x in utxos]

class Node:
    def __init__(self, index, capacity, difficulty):
        self.blockchain = Blockchain(capacity, difficulty)
        self.index = index
        self.wallet = self.create_wallet()
        self.ring = []

    def set_ring(self, ring_nodes):
        self.ring = [x for x in ring_nodes]

    def create_new_block(self):
        pass

    def create_wallet(self):
        #create a wallet for this node, with a public key and a private key
        return Wallet()

    def register_node_to_ring(self, node_ring):
        #add this node to the ring, only the bootstrap node can add a node to the ring after checking his wallet and ip:port address
        #bottstrap node informs all other nodes and gives the request node an id and 100 NBCs
        self.ring.append(node_ring)

    def create_transaction(self, receiver, amount):
        sum = 0
        transaction_inputs = []
        utxos = self.ring[self.index].utxos
        for i in range(len(utxos)):
            sum += utxos[i].amount
            transaction_inputs.append(utxos[i])
            if sum >= amount:
                break

        if sum < amount:
            print("Not enough coins to make transaction")
            return None

        self.ring[self.index].utxos = self.ring[self.index].utxos[i+1:]
        transaction = Transaction(self.wallet.address, self.wallet.private_key, receiver, amount, transaction_inputs)
        return transaction
    
    def find_node_from_address(self, address):
        for node in self.ring:
            if node.address == address:
                return node
        return None
        

    def validate_transaction(self, transaction: Transaction) -> bool:
        """Validate transaction by:
        1. Verifying signature
        2. Enough coins to make transaction

        Args:
            transaction (Transaction): transaction to be validated

        Returns:
            bool: True if validated else false
        """
        if not transaction.verify_transaction():
            return False
        
        sender_node = self.find_node_from_address(transaction.sender_address)
        
        if sum([x.amount for x in sender_node.utxos]) < transaction.amount:
            return False
        
        return True

    def add_transaction(self, transaction: Transaction,\
            found_nonce: threading.Event) -> int:
        """Add transaction to blockchain transactions. If it has reached the
        blockchain capacity create new block and mine it.

        Args:
            transaction (Transaction): Transaction to be added
            found_nonce (threading.Event): If a nonce if found from other node
                this variable will be updated

        Returns:
            int: -1 if added block successfully, or nonce > 0 if new block
                created and mined.
        """
        if len(self.blockchain.transactions) <= self.blockchain.capacity:
            self.blockchain.transactions.append(transaction)
            return -1

        last_block = self.blockchain.last_block
        block = Block(last_block.index+1, 0, last_block.hash)
        added_transactions = self.blockchain.\
                                transactions[:self.blockchain.capacity]
        block.add_transactions_to_block(added_transactions)
        self.blockchain.transactions = self.blockchain.\
                                transactions[self.blockchain.capacity:]
        nonce = self.mine_block(block, found_nonce)
        
        return nonce

    def mine_block(self, block: Block, found_nonce: threading.Event) -> int:
        while not found_nonce.isSet():
            if int(block.hash[:self.blockchain.difficulty]) == 0:
                return block.nonce
            block.set_nonce(block.nonce+1)

        return -1

    # def valid_proof(self, difficulty=MINING_DIFFICULTY):
    #     pass

    # def broadcast_transaction(self):
    #     pass

    # def broadcast_block(self):
    #     pass

    # #concencus functions
    # def valid_chain(self, chain):
    #     #check for the longer chain accroose all nodes
    #     pass

    # def resolve_conflicts(self):
    #     #resolve correct chain
    #     pass
