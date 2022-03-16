import threading
from time import time
from typing import List

from .block import Block
from .blockchain import Blockchain
from .wallet import Wallet
from .transaction import Transaction, TransactionOutput


class RingNode:
    """RingNode: A node class for ring list items.
    """
    def __init__(self, index: int, address: str, public_key: str,\
        utxos: List[TransactionOutput]):
        """Initialize the RingNode

        Args:
            index (int): Ring node's index
            address (int): Ring node's address
            public_key (int): Ring node's public_key
            utxos (List[TransactionOutput]): Ring node's list of unspent
                                             transactions
        """
        self.index = index
        self.address = address
        self.public_key = public_key
        self.utxos = [x for x in utxos]

    def to_dict(self) -> dict:
        """Convert object to dict

        Args:
            None

        Returns:
            dict (dict): Object's dict
        """
        return {
            "index": self.index,
            "address": self.address,
            "public_key": self.public_key,
            "utxos": [x.to_dict() for x in self.utxos]
        }

    def parser(self, dictionary: dict) -> None:
        """Convert dictionary to object

        Args:
            dictionary (dict): The dictionary to be parsed
        """
        utxos = []
        for x in dictionary["utxos"]:
            utxo = TransactionOutput(0, "", 0)
            utxo.parser(x)
            utxos.append(utxo)

        self.index = dictionary["index"]
        self.address = dictionary["address"]
        self.public_key = dictionary["public_key"]
        self.utxos = utxos

class Node:
    """Node: Node that contains node's information and a list (ring) of the
    rest of the nodes.
    """
    def __init__(self, index: int, capacity: int, difficulty: int):
        """Initialize the Node

        Args:
            index (int): Node's index
            capacity (int): Node's blockchain capacity
            difficulty (int): Node's blockchain difficulty
        """
        self.blockchain = Blockchain(capacity, difficulty)
        self.index = index
        self.wallet = self.create_wallet()
        self.ring = []
        self.mining_times = []
        self.transaction_lock = threading.Lock()

    def set_ring(self, ring_nodes: List[RingNode]):
        """Set node's ring of node.

        Args:
            ring_nodes (List[RingNode]): The list of the nodes to be added
                                         to the ring
        """
        self.ring = [x for x in ring_nodes]

    def create_wallet(self):
        """Create node's wallet.
        """
        return Wallet()

    def register_node_to_ring(self, node_ring: RingNode):
        """Register node to ring.

        Args:
            node_ring (RingNode): The node to be added to the ring
        """
        self.ring.append(node_ring)

    def create_transaction(self, receiver: str, amount: int) -> Transaction:
        """Create a new transaction made by the node.

        Args:
            receiver (str): The address of the receiver node
            amount (int): The amount to be sent

        Returns:
            transaction (Transaction): The created transaction or None if
                                       transaction could not be made.
        """
        self.transaction_lock.acquire()
        sum = 0
        i = 0
        transaction_inputs = []
        utxos = self.ring[self.index].utxos
        while i < len(utxos):
            sum += utxos[i].amount
            transaction_inputs.append(utxos[i])
            if sum >= amount:
                break
            i += 1

        if sum < amount:
            print("Not enough coins to make transaction")
            self.transaction_lock.release()
            return None
        self.ring[self.index].utxos = self.ring[self.index].utxos[i+1:]
        self.wallet.unspent_transactions = self.ring[self.index].utxos
        transaction = Transaction(self.ring[self.index].address,\
            self.wallet.public_key, receiver, amount,\
            transaction_inputs)
        transaction.sign_transaction(self.wallet.private_key)
        transaction_outputs = transaction.transaction_outputs
        self.find_node_from_address(receiver).utxos.\
            append(transaction_outputs[0])
        self.ring[self.index].utxos.append(transaction_outputs[1])
        self.transaction_lock.release()
        return transaction
    
    def find_node_from_address(self, address: str) -> RingNode:
        """Find a ring node given its address.

        Args:
            address (str): The address of the node to be found

        Returns:
            node (RingNode): The found ring node.
        """
        for node in self.ring:
            if node.address == address:
                return node
        return None

    def validate_transaction(self, transaction: Transaction) -> bool:
        """Validate transaction by:
        1. Verifying signature
        2. Enough coins to make transaction
        Also update sender's and receiver's utxos.

        Args:
            transaction (Transaction): transaction to be validated

        Returns:
            bool: True if validated else false
        """
        self.transaction_lock.acquire()
        if not transaction.verify_transaction():
            self.transaction_lock.release()
            return False
        
        sender_node = self.find_node_from_address(transaction.sender_address)
        
        if sum([x.amount for x in sender_node.utxos]) < transaction.amount:
            self.transaction_lock.release()
            return False
        
        transaction_inputs_ids = set([x.id for x in\
            transaction.transaction_inputs])

        sender = self.find_node_from_address(transaction.sender_address).index
        spent_transactions = []

        for i in range(len(self.ring[sender].utxos)):
            if (self.ring[sender].utxos[i].transaction_id in
                    transaction_inputs_ids):
                spent_transactions.remove(self.ring[sender].utxos[i])

        for i in range(len(spent_transactions)):
            self.ring[sender].utxos.remove(spent_transactions[i])

        self.find_node_from_address(transaction.receiver_address)\
            .utxos.append(transaction.transaction_outputs[0])
        self.find_node_from_address(transaction.sender_address)\
            .utxos.append(transaction.transaction_outputs[1])

        if (self.find_node_from_address(transaction.sender_address).index
                == self.index):
            self.wallet.unspent_transactions = self.ring[self.index].utxos

        self.transaction_lock.release()
        return True

    def add_transaction(self, transaction: Transaction) -> int:
        """Add transaction to blockchain transactions. If it has reached the
        blockchain capacity create new block and mine it.
        IMPORTANT NOTE: This part is considered a critical section... Before
        calling this function, lock should be acquired.

        Args:
            transaction (Transaction): Transaction to be added

        Returns:
            nonce (int): -1 if added block successfully, or nonce > 0 if new
                         block created and mined.
        """
        if len(self.blockchain.transactions) < self.blockchain.capacity:
            self.blockchain.number_of_transactions += 1
            self.blockchain.transactions.append(transaction)
            return -1

        last_block = self.blockchain.last_block
        block = Block(last_block.index+1, 0, last_block.hash)
        added_transactions = self.blockchain.\
                                transactions[:self.blockchain.capacity]
        block.add_transactions_to_block(added_transactions)
        self.blockchain.transactions = self.blockchain.\
                                transactions[self.blockchain.capacity:]
        self.blockchain.number_of_transactions += 1
        self.blockchain.transactions.append(transaction)
        nonce = self.mine_block(block)

        return nonce

    def mine_block(self, block: Block) -> int:
        """Mine new block.

        Args:
            block (Block): The new block to be mined.

        Returns:
            nonce (int): The nonce found or -1 if the event is set.
        """
        start_time = time()
        while 1:
            if self.valid_proof(block):
                self.mining_times.append(time()-start_time)
                self.blockchain.add_new_block(block)
                return block.nonce
            block.set_nonce(block.nonce+1)

        return -1

    def valid_proof(self, block) -> bool:
        return (block.hash[:self.blockchain.difficulty] ==\
                    "0" * self.blockchain.difficulty)

    def resolve_conflicts(self, blockchain: Blockchain) -> None:
        """Validate that the blockchain that we received is valid and resolve
        conflicts between transactions of the 2 blockchains.
        In this function we make sure that each unique transaction exists once.
        IMPORTANT NOTE: This part is considered a critical section... Before
        calling this function, lock should be acquired.

        Args:
            blockchain (Blockchain): The blockchain that is to replace the
                current
        """
        for hash, block in blockchain.blockchain.items():
            if not block.validate_block(hash):
                return

        transactions_set = set()
        for trans in blockchain.transactions:
            transactions_set.add(trans.transaction_id)

        for hash, block in blockchain.blockchain.items():
            for trans in block.list_of_transactions:
                transactions_set.add(trans.transaction_id)

        old_transactions = self.blockchain.transactions
        self.blockchain = blockchain
        for trans in old_transactions:
            if (trans.transaction_id not in transactions_set
                    and self.validate_transaction(trans)):
                self.add_transaction(trans)

    def delete_duplicate_transactions(self, block: Block) -> None:
        """When adding a new block that another node sent you, it is possible
        that inside the block exist some transactions that also exist in
        `Blockchain.transactions` list. We should delete those transactions
        from `Blockchain.transactions` since they will be added to the
        blockchain via the broadcasted block.

        Args:
            block (Block): The new block that was broadcasted
        """
        added_transactions = set()
        for trans in block.list_of_transactions:
            added_transactions.add(trans.transaction_id)
        
        count = len(added_transactions)

        new_transactions = []
        for trans in self.blockchain.transactions:
            if trans.transaction_id not in added_transactions:
                new_transactions.append(trans)
            else:
                count -= 1
        
        self.blockchain.number_of_transactions += count
        self.blockchain.transactions = new_transactions


    # def broadcast_transaction(self):
    #     pass

    # def broadcast_block(self):
    #     pass

    # #concencus functions
    # def valid_chain(self, chain):
    #     #check for the longer chain accroose all nodes
    #     pass
